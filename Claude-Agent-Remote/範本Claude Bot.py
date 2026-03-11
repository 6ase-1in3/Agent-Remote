"""
Claude Code Remote Bot — 由 Bot_Generator.py 自動產生，請勿手動編輯
如需修改，請編輯「範本Claude Bot.py」後重新執行「產生Bot腳本.bat」
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

# ── 產生器注入的設定 ──────────────────────────────────
BOT_NAME    = "<BOT_NAME>"
TG_TOKEN    = "<TG_TOKEN>"
TG_CHAT_ID  = "<TG_CHAT_ID>"
SKILLS_PATH = r"<SKILLS_PATH>"
SKILLS_INDEX = r"<SKILLS_INDEX>"
MODELS = <MODELS_LIST>
PREVIEW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "__Remote_Previews")

POLL_INTERVAL = 1.5

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

def tg_send_photo(path, caption=""):
    with open(path, "rb") as f:
        data = f.read()
    fname = os.path.basename(path)
    tg_request("sendPhoto", {"chat_id": TG_CHAT_ID, "caption": caption},
               files={"photo": (fname, data, "image/png")})

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

# ── IDE 注入（VS Code / Antigravity）───────────────────
user32 = ctypes.windll.user32

_PS_FOCUS = r"""
Add-Type -TypeDefinition @'
using System.Runtime.InteropServices;
public class WinFocus {
    [DllImport("user32.dll")] public static extern bool ShowWindow(System.IntPtr h, int n);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(System.IntPtr h);
}
'@ -ErrorAction SilentlyContinue

# 修改此處為你的 IDE 程序名稱，如 "Code" (VS Code) 或 "Antigravity"
$proc = Get-Process -Name 'Code' -ErrorAction SilentlyContinue |
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

def focus_ide():
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
    ok = focus_ide()
    print(f"[Focus] hwnd found: {ok}")

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

# ── Skills 載入 ───────────────────────────────────────
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

# ── 主迴圈 ────────────────────────────────────────────
def main():
    print(f"[{BOT_NAME}] Claude Code Remote Bot 啟動")
    tg_send(f"✅ <b>{BOT_NAME}</b> 已上線\n\n/help 查看指令列表")

    os.makedirs(PREVIEW_DIR, exist_ok=True)
    offset = 0
    skills_cache = []
    pending = {}   # 互動狀態: {"type": "model"} 或 {"type": "skill"}

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

            text     = msg.get("text", "").strip()
            photo    = msg.get("photo")
            document = msg.get("document")

            # ── 圖片 / 檔案 ──
            if photo or document:
                pending.clear()
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                if photo:
                    file_id   = photo[-1]["file_id"]
                    save_path = os.path.join(PREVIEW_DIR, f"photo_{ts}.jpg")
                else:
                    file_id = document["file_id"]
                    ext     = os.path.splitext(document.get("file_name", ".bin"))[1] or ".bin"
                    save_path = os.path.join(PREVIEW_DIR, f"file_{ts}{ext}")

                tg_send("📥 下載中...")
                if tg_download_file(file_id, save_path):
                    caption    = msg.get("caption", "")
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

            # ── 互動狀態回覆（編號選擇）──
            if pending and text.isdigit():
                idx = int(text) - 1

                if pending.get("type") == "model":
                    if 0 <= idx < len(MODELS):
                        key, name = MODELS[idx]
                        inject_to_claude(f"/model {key}")
                        tg_send(f"✅ 已切換至：<b>{name}</b>")
                    else:
                        tg_send(f"❌ 請輸入 1–{len(MODELS)} 之間的編號")
                    pending.clear()
                    continue

                elif pending.get("type") == "skill":
                    if 0 <= idx < len(skills_cache):
                        skill_name = skills_cache[idx]
                        skill_path = os.path.join(SKILLS_PATH, skill_name, "SKILL.md")
                        inject_to_claude(f"請使用 {skill_path}")
                        tg_send(f"✅ 已注入 skill：<code>{skill_name}</code>")
                    else:
                        tg_send(f"❌ 請輸入 1–{len(skills_cache)} 之間的編號")
                    pending.clear()
                    continue

            # 收到非數字 → 取消等待狀態
            if pending and not text.startswith("/"):
                pending.clear()

            # ── 指令 ──
            if text in ("/start", "/help"):
                tg_send(
                    f"🤖 <b>{BOT_NAME}</b> 指令列表：\n\n"
                    "<b>📚 Skill 相關：</b>\n"
                    "/skills — 列出所有 skill（互動式選擇）\n\n"
                    "<b>⚙️ Claude Code 指令：</b>\n"
                    "/model — 切換模型（互動式選擇）\n"
                    "/cost — 查詢對話成本\n"
                    "/stats — 查看使用統計\n"
                    "/clear — 清除對話\n"
                    "/diff — 查看檔案變更\n\n"
                    "<b>🔧 其他：</b>\n"
                    "/status — Bot 狀態\n\n"
                    "其他文字 → 直接注入 Claude Code"
                )

            elif text == "/status":
                tg_send(f"✅ <b>{BOT_NAME}</b> 運行中")

            elif text == "/model":
                lines = ["🤖 <b>選擇模型</b>（回傳編號）："]
                for i, (key, name) in enumerate(MODELS, 1):
                    lines.append(f"{i}. {name}  <code>{key}</code>")
                tg_send("\n".join(lines))
                pending["type"] = "model"

            elif text == "/skills":
                skills_cache = load_skills()
                if not skills_cache:
                    tg_send("找不到任何 skill。")
                else:
                    lines = ["📚 <b>Skills 清單</b>（回傳編號）："]
                    for i, s in enumerate(skills_cache, 1):
                        lines.append(f"{i}. {s}")
                    tg_send("\n".join(lines))
                    pending["type"] = "skill"

            elif text == "/cost":
                inject_to_claude("/cost")
                tg_send("💰 已注入 /cost")

            elif text == "/clear":
                inject_to_claude("/clear")
                tg_send("🗑️ 已注入 /clear")

            elif text == "/stats":
                inject_to_claude("/stats")
                tg_send("📊 已注入 /stats")

            elif text == "/diff":
                inject_to_claude("/diff")
                tg_send("📝 已注入 /diff")

            else:
                pending.clear()
                inject_to_claude(text)
                tg_send("✅ 已注入")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
