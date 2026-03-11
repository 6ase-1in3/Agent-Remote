# Claude Code Remote Bot

讓你用手機 Telegram 遠端控制 Claude Code，自動注入指令、切換模型、選擇 Skill。

## 📋 功能

- ✅ **文字訊息** → 直接注入 Claude Code chat
- ✅ **圖片/檔案** → 自動下載並請 Claude 分析
- ✅ **互動式 Skill 選擇** → `/skills` 顯示清單，回覆編號即套用
- ✅ **互動式模型切換** → `/model` 顯示清單，回覆編號即切換
- ✅ **一鍵產生多 Bot** → 填好設定檔，一次產出所有 Bot 腳本

---

## 🚀 快速開始

### 1. 準備 Telegram Bot Token

在 Telegram 找 `@BotFather`，輸入 `/newbot`，取得你的 Bot Token。

### 2. 複製並填寫設定檔

```bash
copy telegram_credentials_example.txt telegram_credentials.txt
```

編輯 `telegram_credentials.txt`：

```ini
[GLOBAL]
CHAT_ID=你的_Telegram_User_ID
SKILLS_PATH=C:\你的路徑\.agent_global_skills
SKILLS_INDEX_PATH=C:\你的路徑\.agent_global_skills\_自定義_Skills_目錄索引.md
MODELS=opus:Opus 4.6|sonnet:Sonnet 4.6|haiku:Haiku 4.5

[Claude_Bot_1]
TOKEN=你的_Bot_Token
```

取得 CHAT_ID：Telegram 搜尋 `@userinfobot`，發 `/start`，複製 User ID。

### 3. 執行產生器

雙擊 **`產生Bot腳本.bat`**，自動產出 `Claude_Bot_1.py` 和 `啟動_Claude_Bot_1.bat`。

### 4. 啟動 Bot

雙擊 **`啟動_Claude_Bot_1.bat`**，Bot 上線後 Telegram 會收到通知。

---

## 📁 檔案結構

```
Claude-Agent-Remote/
├── 範本Claude Bot.py               ← Bot 程式範本（請勿手動修改）
├── Bot_Generator.py                ← 產生器（讀設定檔 → 輸出 Bot 腳本）
├── 產生Bot腳本.bat                  ← 執行產生器
├── telegram_credentials_example.txt← 設定檔範本
│
│   ── 執行產生器後自動出現 ──
├── telegram_credentials.txt        ← 你的設定（gitignore，不會上傳）
├── Claude_Bot_1.py                 ← 產出的 Bot（gitignore，不會上傳）
├── 啟動_Claude_Bot_1.bat           ← 產出的啟動器（gitignore，不會上傳）
└── __Remote_Previews/              ← 圖片下載暫存（自動建立）
```

---

## 📖 指令說明

| 指令 | 說明 |
|------|------|
| `/help` | 顯示所有指令 |
| `/status` | 檢查 Bot 狀態 |
| `/model` | 互動式切換模型 |
| `/skills` | 互動式選擇 Skill |
| `/cost` | 查詢對話成本 |
| `/clear` | 清除對話記錄 |
| `/stats` | 查看使用統計 |
| `/diff` | 查看檔案變更 |
| 任何文字 | 直接注入到 Claude Code |

### 互動式操作範例

**切換模型：**
```
你：/model
Bot：🤖 選擇模型
     1. Opus 4.6   opus
     2. Sonnet 4.6 sonnet
     3. Haiku 4.5  haiku
你：2
Bot：✅ 已切換至：Sonnet 4.6
```

**套用 Skill：**
```
你：/skills
Bot：📚 Skills 清單
     1. 00_project-manager
     2. 00_web-ui-design
     ...
你：1
Bot：✅ 已注入 skill：00_project-manager
```

---

## ⚙️ 多 Bot 設定

在 `telegram_credentials.txt` 中新增多個 section，一次產出多組腳本：

```ini
[Claude_Bot_1]
TOKEN=TOKEN_1

[Claude_Bot_2]
TOKEN=TOKEN_2
```

執行 `產生Bot腳本.bat` 後會產出 `Claude_Bot_1.py`、`Claude_Bot_2.py` 等。

---

## 🔧 自訂 IDE 程序名稱

`範本Claude Bot.py` 中的 PowerShell 腳本預設尋找 `Code`（VS Code）程序。
若使用其他 IDE，請修改 `_PS_FOCUS` 中這行後重新執行產生器：

```powershell
$proc = Get-Process -Name 'Code' -ErrorAction SilentlyContinue |
```

---

## 🔐 安全須知

- `telegram_credentials.txt` 已列入 `.gitignore`，不會上傳到 GitHub
- 永遠不要公開分享你的 Bot Token 和 Chat ID

---

## 🐛 常見問題

**Q: 訊息沒有注入到 Claude Code？**
A: 確認 Claude Code 視窗已開啟，且 `_PS_FOCUS` 中的程序名稱正確。

**Q: 找不到 Skills？**
A: 檢查 `SKILLS_PATH` 和 `SKILLS_INDEX_PATH` 是否填寫正確。

**Q: 模型清單顯示不正常？**
A: 檢查 `MODELS` 格式：`代碼:名稱|代碼:名稱`，冒號和管道符不能有空格。

---

## 📐 架構說明

```
Telegram 訊息
    ↓
Bot polling 接收
    ↓
判斷訊息類型
├─ /model, /skills → 互動式選單（state machine）
├─ 圖片/檔案 → 下載到 __Remote_Previews/ → 注入分析請求
└─ 普通文字 → 直接注入
    ↓
PowerShell 找 IDE 視窗 → SetForegroundWindow
    ↓
Set-Clipboard → Ctrl+V → Enter
    ↓
Claude Code 接收並回應
```

---

這是由個人工作環境撰寫的，使用前請依你的本機環境調整路徑與程序名稱。
