import os
import re

def main():
    print("==================================================")
    print("🤖 Agent Tools Snippet 產生器")
    print("==================================================\n")
    
    # 動態取得當前腳本所在目錄，拼湊出同目錄下的範本檔案路徑
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "範本Agent snippet.txt")
    
    if not os.path.exists(template_path):
        print(f"❌ 找不到模板檔案：{template_path}")
        print("請確保此腳本與原始的 範本Agent snippet.txt 放在同一個專案或修改路徑。")
        input("按 Enter 鍵離開...")
        return

    # 1. 詢問 TG_CHAT_ID (User ID)
    chat_id = input("1. 請輸入您的 Telegram User ID (預設: 8377743279): ").strip()
    if not chat_id:
        chat_id = "8377743279"

    # 2. 詢問 BOT_NAME (機器人名字)
    bot_name = input("2. 請輸入您的機器人代號/名稱 (例如: BotX): ").strip()
    if not bot_name:
        print("❌ 機器人名稱不能為空！")
        return

    # 3. 詢問 TG_TOKEN (API Token)
    bot_token = input("3. 請輸入您的 Telegram Bot API Token: ").strip()
    if not bot_token:
        print("❌ Bot Token 不能為空！")
        return

    print("\n⏳ 正在產生客製化腳本...")

    # 讀取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 取代參數
    text = re.sub(r'const BOT_NAME = ".*?";', f'const BOT_NAME = "{bot_name}";', text)
    text = re.sub(r'const TG_TOKEN = ".*?";', f'const TG_TOKEN = "{bot_token}";', text)
    text = re.sub(r'const TG_CHAT_ID = ".*?";', f'const TG_CHAT_ID = "{chat_id}";', text)

    # 存檔
    output_filename = f"{bot_name}_Agent_Tools.txt"
    output_path = os.path.join(os.path.dirname(template_path), output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print("==================================================")
    print(f"✅ 成功！已建立專屬腳本：{output_filename}")
    print("==================================================")
    input("按 Enter 鍵離開...")

if __name__ == "__main__":
    main()
