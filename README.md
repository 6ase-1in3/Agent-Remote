# Antigravity Telegram 遠端多控系統
這是一個專為 Antigravity AI (VSCode 架構的擴充套件) 打造的前端增強管理模組。
本套件為您帶來以下 **三大核心功能**，大幅解決長時間運作與跨裝置操作的痛點：

1. **📱 Telegram 全域遠端遙控**
   讓您跨越空間，用手機 Telegram 免持操作家裡的 AI 開發視窗。
   - **[接收成果]**：對話與執行摘要傳至 Telegram，圖片成品則自動存入 OneDrive 雲端預覽，供您隨時用手機 App 驗收。
   - **[發送素材]**：完全支援在 Telegram 上傳送圖片給 AI，系統會自動載回電腦裡的本機工作區進行視覺解析。
2. **▶ 智慧防呆點擊器 (Auto-Clicker)**
   防止掛機。當 AI 因系統安全跳出「確認執行」或「展開」等需要人手點擊的防禦視窗時，腳本會從底層自動幫您同意，讓您就算不在電腦前也能全自動推進。
3. **⚡ Master Skills 快捷選單**
   將本機的技能庫 (`.agent_global_skills`) 化作超方便的 UI 選單。點擊一下，即可將複雜的技能呼叫指令自動填入到對話框中。

*(💡 快捷操作：若想臨時關閉並移除整個 Snippet 插件介面，只要對著畫面上的**紫色懸浮按鈕點下「滑鼠右鍵」**，就能瞬間完全卸載。)*

## � 建議資料夾架構
為了將本模組完美無縫地融合到您的環境中，建議將檔案配置如下：
```text
C:\Your_Workspace\
 ├── .agent_global_skills\
 │    └── 00_remote-mode\           <-- 將這包技能放置於您的全域技能庫中
 │         └── SKILL.md
 ├── __Remote_Previews\             <-- 建立一個空資料夾，如果可以請能與您的手機雲端同步 (OneDrive/Google Drive)
 └── Agent_Remote_Project\          <-- 此專案包存放區
      ├── README.md
      ├── Bot_Generator.py          <-- 產生專屬腳本  
      ├── telegram_credentials.txt  <-- 記錄要產生的腳本資料
      └── 範本Agent snippet.txt     <-- 產生專屬腳本的母版
```

## ⚠️ 首次使用必讀：設定檔 `telegram_credentials.txt`
本專案為了能夠開源發布，並支援一鍵同步更新。請先將 `telegram_credentials_example.txt` 重新命名為 `telegram_credentials.txt` (此檔已被 gitignore 忽略以保護隱私)。

接著開啟 `telegram_credentials.txt`，裡面採用標準的 INI 格式，請依照您的本機環境修改：

```ini
[GLOBAL]
# 你的 Telegram User ID (必填)
CHAT_ID=8377743279
# 此為截圖上傳的 OneDrive 資料夾 (用雙斜線轉義 \\ 或是單斜線 \ 皆可腳本會自動處理)
PREVIEW_DIR_PATH=D:\OneDrive\Python_File\插件_Antigravity\__Remote_Previews
# 此為 Master Skills 腳本資料夾路徑
SKILLS_PATH=D:\OneDrive\Python_File\.agent_global_skills
# 此為自定義技能索引的絕對路徑 (用於動態產生腳本內的右下角 UI 選單)
SKILLS_INDEX_PATH=D:\OneDrive\Python_File\.agent_global_skills\_自定義_Skills_目錄索引.md

[Remote_Bot_1]
TOKEN=YOUR_BOT_TOKEN_1
USERNAME=@eason_Remote_1_bot

# 若有更多機器人分身，可以直接往下新增 [Remote_Bot_2] 等等
```

> **💡 動態技能選單（Dynamic Skills Indexing）**
> 腳本現在會「**自動去讀取**」您填寫在 `SKILLS_INDEX_PATH` 中的 Markdown 索引檔！也就是說，當您的自定義技能庫新增或減少技能時，您不需要手動去更改程式碼。使用者也可根據自己現有的清單格式（只要包含 `00_xxxxx` 這種命名規則的純文字或 Markdown 皆可），腳本會自動正規化提取出來，並於每次執行產生器時一鍵刷新所有 UI 選單！

- **📍 `Bot_Generator.py` (批次產生器)** 
  （🌟強烈推薦一鍵更新神器！）這支腳本是全自動的。只要您設定好 `telegram_credentials.txt`，直接雙擊執行它。它就會瞬間產出 **所有分身機器人的獨立腳本**（例如 `Remote_Bot_1_Agent_Tools.txt`）。如果您未來搬移了資料夾、修改了路徑、或是技能清單有更新，只要改完設定檔，再執行一次這個 Python 檔案，就可以直接「**一鍵覆蓋/熱更新**」所有的輸出腳本！


---

## 🚀 工作流程 (如何同時開多個 AI 工作區)

假設您想要開三個專案並讓 AI 同時平行工作：

1. **申請分身**：在 Telegram 找 `@BotFather`，新增三個不同的機器人拿到三個 Token。
2. **產生腳本**：雙擊或用終端機執行 `python Bot_Generator.py`。依序貼上這三個 Token，並給它們取名字 (如 Bot1, Bot2...)，系統會幫您自動產出三份 `Agent Tools.txt`。
3. **建立 Snippet 注入編輯器**：開啟三個不同的 Antigravity 視窗（各自對應不同的開發專案）。按下 `Ctrl+Shift+P` 叫出 `Developer: Toggle Developer Tools` 開啟開發者工具。接著導覽至 **Sources** 面板 > 點開左側的 **Snippets** 頁籤 > 點擊 **New snippet**，並將產出的專屬腳本（例如 `Remote_Bot_1_Agent_Tools.txt` 的內容）貼上後執行。每開一個新視窗/機器人，就重複此步驟一次。
4. **全面遠端**：現在您可以出門了。打開 Telegram，分別密這三個機器人，下達指令。它們的程式不會互相干擾，且下載的照片、產生出的預覽畫面也會加上機器人代號 (例如 `Screenshot_Bot1.png`) 安全存放在共通的 OneDrive 預覽資料夾中。

---

## 🔧 目前支援的前端跨越技術 (技術細節)
這個 Snippet 套件成功跨越了 Chromium 嚴苛的沙盒限制：
- **Lexical React 繞道**：自動模擬底層 `ClipboardEvent(Paste)` 強制寫入 React State，避免純文字修改無效。
- **純本地照片截停**：偵測到 Telegram 照片時，不再試圖餵給瀏覽器，而是轉換成背景 `PowerShell` 指令強制 AI 本機下載以繞過 File Sandbox，將檔案儲存至 `__Remote_Previews` 資料夾後，再透過指令引導 AI 分析該圖片。

---

## 🛠️ 強大附加功能：本機擴充選單
腳本除了提供 Telegram 遠端連線外，在將其貼入 Console 後，VSCode/Antigravity 左下角會出現一個**紫色懸浮按鈕**。點擊展開後可以使用以下本機輔助功能：

1. **▶ 開始 Auto Click (防呆點擊器)** 
   這是一個智慧擴充點擊器（每 0.3 秒偵測一次）。當 AI 運作到一半被系統詢問「確認要執行嗎？」、「是否展開檔案？」時，它會自動從底層派送 MouseEvent 點擊同意，讓您就算人不在電腦前，AI 也不會因為卡在等待確認視窗而停置。它具備防誤殺機制，**絕不會**失控去按到終止或取消任務。
   
2. **⚡ Master Skills (專業技能庫)** 
   選單內建了一整排強大的自定義技能清單（如 `project-manager`、`visual-director` 等）。當您用滑鼠點擊任意技能時，腳本會透過底層傳輸直接把 `請使用 D:\...\SKILL.md` 指令強制灌入對話框。
   *（註：技能清單會預設讀取您放置於 `<YOUR_SKILLS_PATH>` 的檔案結構，需配合 `.agent_global_skills` 目錄使用）*

---

## 🖼️ 雲端預覽與 OneDrive 應用 (Remote Previews)
由於在 Telegram 遠端模式下，您無法直接查看 Antigravity 的預覽畫面，因此系統引入了以下設計：

1. **專屬匯出資料夾**：
   所有的圖片傳輸、網頁截圖，都會被鎖定輸出至指定的預覽資料夾內（建議如 `D:\OneDrive\__Remote_Previews`）。若該資料夾未設定雲端同步，您在遠端手機上將無法查看 AI 傳回的截圖，但依然能正常透過 Telegram 傳送圖片供系統接收解析。
   
2. **多重機器人隔離**：
   為了避免名稱衝突，此資料夾內的檔案會嚴格採用 `[檔案類型]_[機器人代號]_[時間戳記].[副檔名]` 格式命名（例如 `Screenshot_Bot1_2026-03-04.png`）。

3. **OneDrive 手機應用程式聯動**：
   因為該路徑恰好位於您的 OneDrive 同步範圍內，所以只要 AI 傳送了：「我已經建立預覽圖並存放在 `__Remote_Previews`」，您就可以直接在手機上打開 OneDrive App，秒速查看最新的設計或執行結果！


最後: 這是由我自己的工作環境撰寫的, 要使用的話請自行或是由AI Agent幫忙處理檔案結構命名等落地前的調整。