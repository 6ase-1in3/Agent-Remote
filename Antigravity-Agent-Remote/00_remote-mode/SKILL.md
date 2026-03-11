---
name: 00_remote-mode
description: Instructs the agent on how to behave when receiving commands remotely via Telegram, focusing on saving visual outputs directly to OneDrive since the user cannot see the screen.
---

# 📱 Remote Mode (Telegram Control)

You are currently being operated **REMOTELY** by the user via a Telegram Bot integration on their phone. The user **CANNOT SEE the VSCode editor, the Chrome browser, or any graphical UI.**

## 🚨 CRITICAL RULES FOR REMOTE MODE

1. **NO UI PINGS**: Do not ask the user to "look at the screen", "check the preview", or "click this link". They cannot see it.
2. **ACTIVE WORKSPACE FOR CODE**: If you write code files (`.html`, `.py`, `.js`), create directories, or build project structures, you MUST explicitly write them to the user's **current active workspace path** (e.g., `<YOUR_CURRENT_WORKSPACE>`). Do **NOT** lump project code into the `__Remote_Previews` folder.
3. **SCREENSHOT PROOF DEDICATED FOLDER**: The `<YOUR_PREVIEW_DIR_PATH>` directory is strictly reserved for visual artifacts bridging to Telegram. If you create a web preview, use a browser automation tool to screenshot it. Save the file exactly as `Screenshot_<BOT_NAME>_<Timestamp>.png` (e.g., `Screenshot_Bot1_2026-03-04_12-30.png`). Use the `BOT_NAME` identifier supplied in your prompt.
4. **TELEGRAM LIMITATIONS**: Keep your textual summaries highly concise. Long, markdown-heavy tables are hard to read on a mobile Telegram client.
5. **AGENTIC BIAS**: Bias heavily towards action. If there is an error, fix it autonomously instead of prompting the user, as the user is AFK and cannot easily debug code on their phone.

## 📡 Telegram Broadcast Protocol (CRITICAL)
Since the user cannot see your standard chat responses, you MUST wrap any final summary or question you want the user to see in their Telegram App within these exact tags:
`[TG_BROADCAST_START]`
(Write your concise summary, status update, or question here. Maximum 3-4 sentences.)
`[TG_BROADCAST_END]`

The system will intercept this block and push it to their phone. If you don't include these tags, they will only see "Task Completed" without knowing what you actually did.

## 📸 Workflow for Delivering UI to Phone
If the user asks "Show me the UI" or "Build a landing page":
1. Write the code (`.html` or `.jsx`).
2. Start the local server if needed.
3. Automatically run a screenshot utility.
4. Output: 
`[TG_BROADCAST_START]`
I have built the UI and captured a screenshot. You can view the live design on your phone at: `__Remote_Previews/Screenshot_<BOT_NAME>_<Timestamp>.png` in your OneDrive.
`[TG_BROADCAST_END]`
