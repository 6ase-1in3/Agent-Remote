"""
Claude Bot 批次產生器
讀取 telegram_credentials.txt + 範本Claude Bot.py
自動產出 Claude_Bot_X.py 和 啟動_Claude_Bot_X.bat
"""
import os
import re
import configparser

def parse_models(models_str):
    """將 'opus:Opus 4.6|sonnet:Sonnet 4.6|haiku:Haiku 4.5'
       轉成 Python list literal: [("opus", "Opus 4.6"), ...]"""
    pairs = []
    for item in models_str.split("|"):
        item = item.strip()
        if ":" in item:
            key, name = item.split(":", 1)
            pairs.append((key.strip(), name.strip()))
    # 輸出成 Python list of tuples literal
    items_str = ", ".join(f'("{k}", "{n}")' for k, n in pairs)
    return f"[{items_str}]"

def main():
    print("=" * 50)
    print("Claude Bot 批次產生器")
    print("=" * 50)
    print()

    script_dir    = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "範本Claude Bot.py")
    config_path   = os.path.join(script_dir, "telegram_credentials.txt")

    # 檢查必要檔案
    if not os.path.exists(template_path):
        print(f"找不到範本檔案：{template_path}")
        input("按 Enter 離開...")
        return

    if not os.path.exists(config_path):
        print(f"找不到憑證檔案：{config_path}")
        input("按 Enter 離開...")
        return

    # 讀取設定
    print(f"讀取配置：{config_path}")
    cfg = configparser.ConfigParser()
    cfg.optionxform = str
    cfg.read(config_path, encoding="utf-8")

    if "GLOBAL" not in cfg:
        print("設定檔缺少 [GLOBAL] 區塊！")
        return

    g = cfg["GLOBAL"]
    chat_id      = g.get("CHAT_ID", "").strip()
    skills_path  = g.get("SKILLS_PATH", "").strip()
    skills_index = g.get("SKILLS_INDEX_PATH", "").strip()
    models_str   = g.get("MODELS", "opus:Opus 4.6|sonnet:Sonnet 4.6|haiku:Haiku 4.5").strip()
    models_list  = parse_models(models_str)

    print(f"MODELS: {models_list}")
    print()

    # 讀取範本
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    count = 0
    for section in cfg.sections():
        if section == "GLOBAL":
            continue

        bot_name  = section
        bot_token = cfg[section].get("TOKEN", "").strip()

        if not bot_token:
            print(f"跳過 {bot_name}：缺少 TOKEN")
            continue

        # 替換佔位符（保留 Windows 路徑原樣，因為 Python raw string 會正確處理）
        text = template
        text = text.replace("<BOT_NAME>",    bot_name)
        text = text.replace("<TG_TOKEN>",    bot_token)
        text = text.replace("<TG_CHAT_ID>",  chat_id)
        text = text.replace("<SKILLS_PATH>", skills_path)
        text = text.replace("<SKILLS_INDEX>", skills_index)
        text = text.replace("<MODELS_LIST>", models_list)

        # 輸出 Python 腳本
        py_filename = f"Claude_Bot_{bot_name.split('_')[-1]}.py"
        py_path     = os.path.join(script_dir, py_filename)
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"產出：{py_filename}")

        # 輸出啟動 bat
        bat_filename = f"啟動_Claude_Bot_{bot_name.split('_')[-1]}.bat"
        bat_path     = os.path.join(script_dir, bat_filename)
        bat_content  = f"""@echo off
chcp 65001 >nul
echo [{bot_name}] Starting...
python "{py_path}"
if errorlevel 1 (
    echo.
    echo [ERROR] 啟動失敗，請確認 Python 是否已安裝
    echo.
    pause
)
"""
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(bat_content)
        print(f"產出：{bat_filename}")
        count += 1

    print()
    print("=" * 50)
    print(f"完成！共產生了 {count} 組 Bot 腳本")
    print("=" * 50)

if __name__ == "__main__":
    main()
    input("\n按 Enter 離開...")
