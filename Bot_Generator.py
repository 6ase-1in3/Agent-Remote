import os
import re
import configparser

def parse_skills_from_md(index_path):
    skills = []
    try:
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 尋找類似 [00_xxxxx] 這樣的字眼
                matches = re.findall(r'\[(00_[a-zA-Z0-9_\-]+)\]', content)
                skills.extend(matches)
                
                # 有時候如果是直接寫 00_xxxxx 的清單，不是用 [] 框起來的，可以抓更寬鬆的條件
                matches2 = re.findall(r'`?(00_[a-zA-Z0-9_\-]+)`?', content)
                skills.extend(matches2)
    except Exception as e:
        print(f"⚠️ 解析技能索引發生錯誤: {e}")
        
    # 去除重複並排序
    skills = sorted(list(set(skills)))
    return skills

def main():
    print("==================================================")
    print("🤖 Agent Tools Snippet 批次產生器")
    print("==================================================\n")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "範本Agent snippet.txt")
    config_path = os.path.join(script_dir, "telegram_credentials.txt")
    
    if not os.path.exists(template_path):
        print(f"❌ 找不到模板檔案：{template_path}")
        print("請確保檔案 範本Agent snippet.txt 存在於相同目錄。")
        input("按 Enter 鍵離開...")
        return

    if not os.path.exists(config_path):
        print(f"❌ 找不到設定檔案：{config_path}")
        print("請確認 telegram_credentials.txt 是否與本程式放在同一個目錄。")
        input("按 Enter 鍵離開...")
        return
        
    print(f"📄 讀取配置檔: {config_path}")
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_path, encoding='utf-8')
    
    if 'GLOBAL' not in config:
        print("❌ 設定檔缺少 [GLOBAL] 區塊！")
        return
        
    chat_id = config['GLOBAL'].get('CHAT_ID', '8377743279').strip()
    preview_dir = config['GLOBAL'].get('PREVIEW_DIR_PATH', r'D:\OneDrive\Python_File\__Remote_Previews').strip()
    skills_path = config['GLOBAL'].get('SKILLS_PATH', r'D:\OneDrive\Python_File\.agent_global_skills').strip()
    skills_index_path = config['GLOBAL'].get('SKILLS_INDEX_PATH', '').strip()

    # 從 Markdown 索引中抓取最新的技能清單
    master_skills = []
    if skills_index_path:
        print(f"🔍 正在解析自定義技能庫清單: {skills_index_path}")
        master_skills = parse_skills_from_md(skills_index_path)
        
    # 如果抓不到，預設提供幾個基本的 fallback
    if not master_skills:
        master_skills = [
            "00_remote-mode",
            "00_skill-creator",
            "00_project-manager",
            "00_visual-director"
        ]
        
    print(f"📦 總共抓取到 {len(master_skills)} 個自定義技能")
    
    # 將 Python 的 list 轉成 JavaScript 陣列字串
    js_array_str = "[\n    " + ",\n    ".join(f'"{s}"' for s in master_skills) + "\n  ];"

    # 處理 Windows 路徑跳脫斜線
    preview_dir_js = preview_dir.replace('\\', '\\\\')
    skills_path_js = skills_path.replace('\\', '\\\\')

    # 讀取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template_text = f.read()

    # 取代母板內的全域路徑參數
    template_text = template_text.replace('<YOUR_PREVIEW_DIR_PATH>', preview_dir_js)
    template_text = template_text.replace('<YOUR_SKILLS_PATH>', skills_path_js)

    print("\n⏳ 正在批次產生客製化腳本...\n")
    count = 0
    for section in config.sections():
        if section == 'GLOBAL':
            continue
            
        bot_name = section
        bot_token = config[section].get('TOKEN', '').strip()
        
        if not bot_token:
            print(f"⚠️ 跳過 {bot_name}: 缺少 TOKEN")
            continue
            
        # 取代參數
        text = template_text
        text = re.sub(r'const BOT_NAME = ".*?";', f'const BOT_NAME = "{bot_name}";', text)
        text = re.sub(r'const TG_TOKEN = ".*?";', f'const TG_TOKEN = "{bot_token}";', text)
        text = re.sub(r'const TG_CHAT_ID = ".*?";', f'const TG_CHAT_ID = "{chat_id}";', text)

        # 動態替換 masterSkills 陣列
        # 尋找: const masterSkills = [ ...任意內容... ];
        text = re.sub(r'const masterSkills = \[[ \r\n\t\S]*?\];', f'const masterSkills = {js_array_str}', text)

        # 存檔
        output_filename = f"{bot_name}_Agent_Tools.txt"
        output_path = os.path.join(script_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
            
        print(f"✅ 成功產出：{output_filename}")
        count += 1

    print("\n==================================================")
    print(f"🎉 全部完成！共產生了 {count} 份專屬 Agent Tools 腳本 (成功同步最新技能)。")
    print("==================================================")

if __name__ == "__main__":
    main()
