@echo off
chcp 65001 >nul
echo 正在啟動 Claude Bot 批次產生器...
python "%~dp0Bot_Generator.py"
