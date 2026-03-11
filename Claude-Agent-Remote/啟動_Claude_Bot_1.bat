@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 🤖 正在啟動 Claude_Bot_1...
echo.
python Claude_Bot_1.py
if errorlevel 1 (
    echo.
    echo ❌ 啟動失敗！
    echo.
    echo 📋 檢查清單：
    echo 1. Python 是否已安裝？
    echo    運行：python --version
    echo.
    echo 2. telegram_credentials.txt 是否已建立？
    echo    複製 telegram_credentials_example.txt
    echo    填入你的 CHAT_ID 和其他設定
    echo.
    echo 3. Claude_Bot_1.py 是否已建立？
    echo    複製 Claude_Bot_Template.py 為 Claude_Bot_1.py
    echo    並在檔案中填入正確的路徑
    echo.
    pause
)
