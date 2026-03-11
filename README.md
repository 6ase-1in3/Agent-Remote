# Agent Remote - 多 AI 平台遠端控制套件

統一的 Telegram Bot 框架，讓你可以遠端控制 **Antigravity（自訂 VS Code）** 和 **Claude Code**。

## 📦 專案結構

```
Agent-Remote/
├── Antigravity-Agent-Remote/   ← Antigravity chat 遠端控制
├── Claude-Agent-Remote/        ← Claude Code 遠端控制
└── README.md                   ← 本檔案
```

---

## 🎯 快速導航

### Antigravity Agent Remote
**用途**：遠端控制 Antigravity（客製化 VS Code），支援自動點擊、Telegram 接收等

📖 [完整文檔](./Antigravity-Agent-Remote/README.md)

**核心功能**：
- ✅ Telegram 直接控制 Antigravity
- ✅ 自動點擊確認按鈕
- ✅ Skills 整合
- ✅ Agent Tools snippet

**快速開始**：
```bash
cd Antigravity-Agent-Remote
python Bot_Generator.py
# 或雙擊：產生Bot腳本.bat
```

---

### Claude Agent Remote
**用途**：遠端控制 Claude Code，支援模型切換、Skills、Telegram 互動

📖 [完整文檔](./Claude-Agent-Remote/README.md)

**核心功能**：
- ✅ Telegram 文字訊息自動注入
- ✅ 圖片/檔案上傳分析
- ✅ 互動式 Skills 選擇
- ✅ 互動式模型切換
- ✅ 動態配置模型列表

**快速開始**：
```bash
cd Claude-Agent-Remote
# 複製檔案
copy Claude_Bot_Template.py Claude_Bot_1.py
copy telegram_credentials_example.txt telegram_credentials.txt

# 編輯 telegram_credentials.txt，填入你的設定
# 編輯 Claude_Bot_1.py，填入路徑

# 啟動
python Claude_Bot_1.py
# 或雙擊：啟動_Claude_Bot_1.bat
```

---

## 🔧 共用設定

兩個 Bot 都使用同一份 Telegram 憑證：

```
telegram_credentials.txt
├── CHAT_ID              # 你的 Telegram Chat ID
├── SKILLS_PATH          # Claude Code skills 路徑
├── SKILLS_INDEX_PATH    # Skills 索引檔案
└── MODELS               # Claude Code 可用模型列表
```

### 取得 CHAT_ID

1. Telegram 搜尋 `@userinfobot`
2. 發送 `/start`
3. 複製顯示的 User ID

---

## 📝 功能對比

| 功能 | Antigravity | Claude Code |
|------|------------|------------|
| Telegram 訊息注入 | ✅ | ✅ |
| 自動點擊 | ✅ | ❌ |
| Skills 整合 | ✅ | ✅ |
| 互動式操作 | ❌ | ✅ |
| 模型切換 | ❌ | ✅ |
| Agent Tools | ✅ | ❌ |

---

## 🚀 使用案例

### 案例 1：遠端工作流
```
工作中（手機 Telegram）
  → 發：「幫我寫一個 React component」
  → Bot 注入到 Claude Code
  → Claude 生成程式碼
  → 複製到編輯器
```

### 案例 2：快速模型切換省錢
```
進行昂貴分析（用 Opus）
  → 分析完成，改簡單任務
  → Telegram: /model
  → 選 3（Haiku）
  → 自動切換，省 80% 成本
```

### 案例 3：圖片分析
```
在手機截圖一個 bug
  → Telegram 發送圖片 + caption
  → Bot 下載圖片
  → 注入分析請求
  → Claude 詳細解釋
```

---

## 🔐 安全須知

⚠️ **永遠不要公開分享：**
- Telegram Bot Token
- Chat ID
- 個人路徑

此 repo 中的所有檔案都使用**佔位符和範本**，確保複製使用時是安全的。

---

## 📚 詳細文檔

- [Antigravity Agent Remote 文檔](./Antigravity-Agent-Remote/README.md)
- [Claude Agent Remote 文檔](./Claude-Agent-Remote/README.md)

---

## 🐛 除錯

**通用檢查清單：**
1. Python 已安裝？ → `python --version`
2. Telegram 憑證正確？ → 檢查 `telegram_credentials.txt`
3. AI 平台視窗開啟？ → 確保 VS Code 或 Antigravity 在前景
4. 有 error 訊息？ → 查看終端機輸出

---

## 🎓 架構設計

```
┌─────────────────┐
│   Telegram      │
│   訊息/指令     │
└────────┬────────┘
         │
    ┌────▼────┐
    │   Bot   │
    │ (Python)│
    └────┬────┘
         │
    ┌────┴──────────────────────┐
    │                           │
┌───▼─────────┐      ┌────────▼───┐
│ Antigravity │      │ Claude Code │
│  (VS Code)  │      │ (Web App)   │
└─────────────┘      └─────────────┘
```

---

## 📞 貢獻

發現 bug 或有改進建議？歡迎提交 issue 或 PR！

---

## 📄 授權

MIT License - 自由使用和修改

---

**祝使用愉快！** 🚀

有問題？先看各自的 README，一般都有解答。
