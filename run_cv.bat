@echo off
chcp 65001 > nul
cd /d "C:\Users\shondo\Desktop\agent_project"
call web_app\.venv\Scripts\activate.bat

:: GEMINI_API_KEY をここに貼り付け
set GEMINI_API_KEY=%1

set PYTHONUTF8=1
python run_cv.py %2 %3 %4
