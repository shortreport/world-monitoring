@echo off
cd /d "C:\Users\shondo\Desktop\agent_project"
call venv\Scripts\activate.bat
set PYTHONUTF8=1
echo === update_home.py --with-economist ===
python update_home.py --with-economist > debug_run.log 2>&1
echo EXIT CODE: %ERRORLEVEL% >> debug_run.log
echo === DONE, exit=%ERRORLEVEL% ===
