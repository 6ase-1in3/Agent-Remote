"""
Claude Code Telegram Bot - 公開範本版本
複製此檔案為 Claude_Bot_1.py，並在 telegram_credentials.txt 中設定你的憑證
"""
import subprocess
import time
import os
import re
import ctypes
import urllib.request
import urllib.parse
import json
from datetime import datetime

# ── 讀取共用憑證 ──────────────────────────────────
CRED_FILE = r"{CREDENTIALS_PATH}\telegram_credentials.txt"

def load_credentials():
    """從共用檔案讀取憑證"""
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read(CRED_FILE, encoding="utf-8")

    if "GLOBAL" not in cfg:
        raise ValueError(f"找不到 [GLOBAL] 區段在 {CRED_FILE}")

    g = cfg["GLOBAL"]
    return {
        "chat_id": g.get("CHAT_ID", ""),
        "skills_path": g.get("SKILLS_PATH", "").replace("\\\\", "\\"),
        "skills_index": g.get("SKILLS_INDEX_PATH", "").replace("\\\\", "\\"),
        "models": g.get("MODELS", "opus:Opus 4.6|sonnet:Sonnet 4.6|haiku:Haiku 4.5"),
    }

# 載入憑證
try:
    creds = load_credentials()
    BOT_NAME      = "Claude_Bot_1"
    TG_TOKEN      = "{TG_TOKEN_PLACEHOLDER}"
    TG_CHAT_ID    = creds["chat_id"]
    SKILLS_PATH   = creds["skills_path"]
    SKILLS_INDEX  = creds["skills_index"]
    MODELS_STR    = creds["models"]
    PREVIEW_DIR   = r"{PREVIEW_DIR_PLACEHOLDER}"
except Exception as e:
    print(f"❌ 讀取憑證失敗：{e}")
    print(f"請確認 {CRED_FILE} 存在且格式正確")
    exit(1)

POLL_INTERVAL = 1.5   # Telegram polling 間隔秒數

# ── 解析 Models ────────────────────────────────────
def parse_models(models_str):
    """解析 MODELS 字串"""
    models = []
    for pair in models_str.split("|"):
        if ":" in pair:
            code, name = pair.split(":", 1)
            models.append({"code": code.strip(), "name": name.strip()})
    return models

AVAILABLE_MODELS = parse_models(MODELS_STR)

# ── Telegram API ──────────────────────────────────────
def tg_request(method, data=None, files=None):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/{method}"
    if files:
        boundary = "----FormBoundary7MA4YWxkTrZu0gW"
        body = b""
        for k, v in (data or {}).items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        for k, (fname, fdata, ctype) in files.items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fname}\"\r\nContent-Type: {ctype}\r\n\r\n".encode()
            body += fdata + f"\r\n".encode()
        body += f"--{boundary}--\r\n".encode()
        req = urllib.request.Request(url, data=body,
              headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    else:
        payload = json.dumps(data or {}).encode()
        req = urllib.request.Request(url, data=payload,
              headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"[TG Error] {e}")
        return {}

def tg_send(text):
    tg_request("sendMessage", {"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "HTML"})

def tg_get_updates(offset):
    r = tg_request("getUpdates", {"offset": offset, "timeout": 30, "limit": 5})
    return r.get("result", [])

def tg_download_file(file_id, save_path):
    r = tg_request("getFile", {"file_id": file_id})
    fp = r.get("result", {}).get("file_path")
    if not fp:
        return False
    url = f"https://api.telegram.org/file/bot{TG_TOKEN}/{fp}"
    urllib.request.urlretrieve(url, save_path)
    return True

# ── VS Code 注入 ──────────────────────────────────────
user32 = ctypes.windll.user32

_PS_FOCUS = r"""
Add-Type -TypeDefinition @'
using System.Runtime.InteropServices;
public class WinFocus {
    [DllImport("user32.dll")] public static extern bool ShowWindow(System.IntPtr h, int n);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(System.IntPtr h);
}
'@ -ErrorAction SilentlyContinue

$proc = Get-Process -Name 'Antigravity' -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowHandle -ne [IntPtr]::Zero } |
        Select-Object -First 1

if ($proc) {
    $hwnd = $proc.MainWindowHandle
    [WinFocus]::ShowWindow($hwnd, 9)
    [WinFocus]::SetForegroundWindow($hwnd)
    Write-Output "OK:$($proc.Name):$hwnd"
} else {
    Write-Output "NOTFOUND"
}
"""

def focus_vscode():
    """用 PowerShell 找 VS Code 視窗並帶到前景"""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as f:
        f.write(_PS_FOCUS)
        tmp = f.name
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-File", tmp],
            capture_output=True, text=True
        )
        out = r.stdout.strip()
    finally:
        os.unlink(tmp)
    print(f"[Focus] {out}")
    time.sleep(0.4)
    return out.startswith("OK:")

def inject_to_claude(text, auto_send=True):
    """將文字注入 Claude Code 輸入框並送出"""
    ok = focus_vscode()
    print(f"[Focus] VS Code hwnd found: {ok}")

    escaped = text.replace("'", "''")
    subprocess.run(
        ["powershell", "-Command", f"Set-Clipboard -Value @'\n{escaped}\n'@"],
        capture_output=True
    )
    time.sleep(0.25)

    VK_CTRL, VK_V = 0x11, 0x56
    user32.keybd_event(VK_CTRL, 0, 0, 0)
    user32.keybd_event(VK_V,    0, 0, 0)
    user32.keybd_event(VK_V,    0, 2, 0)
    user32.keybd_event(VK_CTRL, 0, 2, 0)

    if auto_send:
        time.sleep(0.2)
        VK_ENTER = 0x0D
        user32.keybd_event(VK_ENTER, 0, 0, 0)
        user32.keybd_event(VK_ENTER, 0, 2, 0)

# ── Skills 選單 ───────────────────────────────────────
def load_skills():
    skills = []
    if os.path.exists(SKILLS_INDEX):
        with open(SKILLS_INDEX, encoding="utf-8") as f:
            for line in f:
                m = re.search(r"(00_[\w\-]+)", line)
                if m:
                    skills.append(m.group(1))
    if not skills and os.path.exists(SKILLS_PATH):
        for name in sorted(os.listdir(SKILLS_PATH)):
            if name.startswith("00_") and os.path.isdir(os.path.join(SKILLS_PATH, name)):
                skills.append(name)
    return list(dict.fromkeys(skills))

def send_skills_menu(skills):
    if not skills:
        tg_send("找不到任何 skill。")
        return
    lines = ["📚 <b>Skills 清單</b>（回覆編號選擇）："]
    for i, s in enumerate(skills, 1):
        lines.append(f"{i}. {s}")
    lines.append("\n回覆編號以套用對應 skill")
    tg_send("\n".join(lines))

# ── State 管理 ────────────────────────────────────────
pending_state = {}

# ── 主迴圈 ────────────────────────────────────────────
def main():
    print(f"[{BOT_NAME}] Claude Code Remote Bot 啟動")
    tg_send(f"✅ <b>{BOT_NAME}</b> 已上線，等待指令...\n\n/help 查看指令列表")

    os.makedirs(PREVIEW_DIR, exist_ok=True)
    offset = 0
    skills_cache = []

    while True:
        try:
            updates = tg_get_updates(offset)
        except Exception as e:
            print(f"[Poll Error] {e}")
            time.sleep(5)
            continue

        for upd in updates:
            offset = upd["update_id"] + 1
            msg = upd.get("message", {})

            if str(msg.get("chat", {}).get("id", "")) != str(TG_CHAT_ID):
                continue

            user_id = msg.get("from", {}).get("id")
            text = msg.get("text", "").strip()
            photo = msg.get("photo")
            document = msg.get("document")

            # ── 圖片 / 檔案 ──
            if photo or document:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                if photo:
                    file_id = photo[-1]["file_id"]
                    save_path = os.path.join(PREVIEW_DIR, f"photo_{ts}.jpg")
                else:
                    file_id = document["file_id"]
                    ext = os.path.splitext(document.get("file_name", ".bin"))[1] or ".bin"
                    save_path = os.path.join(PREVIEW_DIR, f"file_{ts}{ext}")

                tg_send("📥 下載中...")
                if tg_download_file(file_id, save_path):
                    caption = msg.get("caption", "")
                    inject_msg = f"請分析這個檔案：{save_path}"
                    if caption:
                        inject_msg += f"\n{caption}"
                    inject_to_claude(inject_msg)
                    tg_send(f"✅ 已注入：<code>{os.path.basename(save_path)}</code>")
                else:
                    tg_send("❌ 下載失敗")
                continue

            if not text:
                continue

            # ── 檢查待機狀態 ──
            if user_id in pending_state:
                state = pending_state[user_id]
                if state["type"] == "skill_select" and text.isdigit():
                    idx = int(text) - 1
                    if 0 <= idx < len(state["skills"]):
                        skill_name = state["skills"][idx]
                        skill_path = os.path.join(SKILLS_PATH, skill_name, "SKILL.md")
                        inject_to_claude(f"請使用 {skill_path}")
                        tg_send(f"✅ 已注入 skill：<code>{skill_name}</code>")
                        del pending_state[user_id]
                    else:
                        tg_send("❌ 編號無效，請重新選擇")
                    continue
                elif state["type"] == "model_select" and text.isdigit():
                    idx = int(text) - 1
                    if 0 <= idx < len(AVAILABLE_MODELS):
                        model = AVAILABLE_MODELS[idx]
                        inject_to_claude(f"/model {model['code']}")
                        tg_send(f"✅ 已切換到：{model['name']}")
                        del pending_state[user_id]
                    else:
                        tg_send("❌ 編號無效，請重新選擇")
                    continue

            # ── 指令 ──
            if text in ("/start", "/help"):
                tg_send(
                    f"🤖 <b>{BOT_NAME}</b> 指令列表：\n\n"
                    "<b>📚 Skill 相關：</b>\n"
                    "/skills — 列出所有 skill（回覆編號選擇）\n\n"
                    "<b>⚙️ 模型切換：</b>\n"
                    "/model — 顯示模型列表（回覆編號切換）\n\n"
                    "<b>🔧 其他：</b>\n"
                    "/status — Bot 狀態\n\n"
                    "其他文字 → 直接注入到 Claude Code"
                )

            elif text == "/status":
                tg_send(f"✅ <b>{BOT_NAME}</b> 運行中\nPreview: <code>{PREVIEW_DIR}</code>")

            elif text == "/skills":
                skills_cache = load_skills()
                if skills_cache:
                    send_skills_menu(skills_cache)
                    pending_state[user_id] = {"type": "skill_select", "skills": skills_cache}
                else:
                    tg_send("找不到任何 skill。")

            elif text == "/model":
                if AVAILABLE_MODELS:
                    lines = ["🤖 <b>選擇模型</b>（回覆編號）："]
                    for i, m in enumerate(AVAILABLE_MODELS, 1):
                        lines.append(f"{i}. {m['name']}")
                    tg_send("\n".join(lines))
                    pending_state[user_id] = {"type": "model_select"}
                else:
                    tg_send("❌ 無可用模型")

            else:
                # 一般訊息 → 注入
                inject_to_claude(text)
                tg_send("✅ 已注入")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
