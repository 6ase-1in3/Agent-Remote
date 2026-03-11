# Claude Code Telegram Bot

讓 Claude Code 接收 Telegram 訊息，自動注入到 chat 輸入框。

## 📋 功能

✅ **文字訊息** → 直接注入 Claude Code chat
✅ **圖片/檔案** → 自動下載並分析
✅ **互動式操作** → Telegram 選擇 skill/model，自動切換
✅ **模型配置** → 從設定檔動態讀取可用模型

## 🚀 快速開始

### 1️⃣ 準備工作

**複製並重命名檔案：**
```bash
# 複製 Claude_Bot_Template.py 為 Claude_Bot_1.py
copy Claude_Bot_Template.py Claude_Bot_1.py

# 複製憑證範本
copy telegram_credentials_example.txt telegram_credentials.txt
```

### 2️⃣ 設定憑證

編輯 `telegram_credentials.txt`：

```ini
[GLOBAL]
CHAT_ID=8377743279               # 你的 Telegram Chat ID
SKILLS_PATH=...                  # Claude Code skills 路徑
SKILLS_INDEX_PATH=...            # Skills 索引檔案
MODELS=opus:Opus 4.6|sonnet:...  # 可用模型列表
```

**取得 CHAT_ID：**
1. 在 Telegram 找 @userinfobot
2. 發送 `/start`
3. 複製顯示的 User ID

### 3️⃣ 啟動 Bot

**方法 A：雙擊批次檔**
```
啟動_Claude_Bot_1.bat
```

**方法 B：終端機**
```bash
python Claude_Bot_1.py
```

### 4️⃣ 在 Telegram 發訊息

在 Telegram 發送訊息給 bot，自動注入到 Claude Code。

---

## 📖 使用方式

### 基本指令

| 指令 | 說明 |
|------|------|
| `/help` | 顯示所有指令 |
| `/status` | 檢查 bot 狀態 |
| 任何文字 | 直接注入到 Claude Code |

### 互動式操作

#### 選擇 Skill
```
發送：/skills
Bot 顯示：
📚 Skills 清單
1. chromium
2. web-ui-design
3. autonomous-dev
...

回覆：2
Bot 自動注入：請使用 .../web-ui-design/SKILL.md
```

#### 切換模型
```
發送：/model
Bot 顯示：
🤖 選擇模型
1. Opus 4.6
2. Sonnet 4.6
3. Haiku 4.5

回覆：3
Bot 自動注入：/model haiku
Claude Code 切換到 Haiku 模型
```

### 檔案上傳

在 Telegram 直接發送圖片或檔案，bot 會：
1. 自動下載到 `__Remote_Previews/` 資料夾
2. 注入「請分析這個檔案：路徑」到 Claude Code
3. Claude 自動分析

---

## 📁 檔案結構

```
Claude-Agent-Remote/
├── Claude_Bot_Template.py           ← 複製為 Claude_Bot_1.py
├── Claude_Bot_1.py                  ← 實際運行的 bot（複製後建立）
├── telegram_credentials_example.txt ← 複製為 telegram_credentials.txt
├── telegram_credentials.txt         ← 你的憑證（複製後建立）
├── 啟動_Claude_Bot_1.bat             ← 快速啟動器
├── __Remote_Previews/               ← 檔案下載快取（自動建立）
└── README.md                        ← 本檔案
```

---

## ⚙️ 高級設定

### 自訂模型列表

在 `telegram_credentials.txt` 中編輯 `MODELS`：

```ini
MODELS=opus:Opus 4.6|sonnet:Sonnet 4.6|haiku:Haiku 4.5
```

格式：`代碼:顯示名稱|代碼:顯示名稱|...`

Bot 會自動解析，用戶在 Telegram 中就可以用編號快速切換。

---

## 🔐 安全提示

⚠️ **永遠不要**公開分享以下內容：
- Telegram Bot Token（在 `telegram_credentials.txt` 中）
- Chat ID
- 任何個人路徑

此範本檔案中的 Token 已用佔位符，確保安全。

---

## 🐛 常見問題

**Q: 訊息沒有注入到 Claude Code？**
A: 檢查：
- Claude Code 視窗是否開啟並在前景
- Telegram 憑證是否正確設定
- 終端機是否有錯誤訊息

**Q: 找不到 Skills？**
A: 檢查 `SKILLS_PATH` 是否指向正確的資料夾

**Q: 模型列表顯示不正常？**
A: 檢查 `MODELS` 格式是否正確（冒號和管道符）

---

## 📝 架構說明

```
Telegram 訊息
    ↓
Bot 接收（polling）
    ↓
檢查訊息類型
├─ 指令（/skills, /model, /help）→ 互動式操作
├─ 圖片/檔案 → 下載並注入分析請求
└─ 普通文字 → 直接注入
    ↓
VS Code 焦點切換
    ↓
Ctrl+V 貼上訊息
    ↓
Enter 送出
    ↓
Claude Code 接收並回應
```

---

## 🎯 典型使用場景

**場景 1：遠端快速提問**
```
使用者在手機發：「解釋閉包的概念」
→ Bot 注入到 Claude Code
→ Claude 立即回覆
→ Bot 確認訊息
```

**場景 2：發送圖片分析**
```
使用者在手機發送截圖 + caption「檢查這個錯誤」
→ Bot 下載圖片
→ 注入分析請求
→ Claude 分析圖片並解釋
```

**場景 3：快速切換模型**
```
使用者發：/model
→ Bot 顯示可用模型
→ 使用者回覆：3
→ Bot 自動切換到 Haiku
→ 節省成本同時保持速度
```

---

## 📞 支援

有問題或建議？請提交 issue 或 PR。

祝使用愉快！🚀
