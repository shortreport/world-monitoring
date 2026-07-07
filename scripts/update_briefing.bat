@echo off
REM ============================================================
REM update_briefing.bat
REM 実行タイミング: 毎朝 8:00（Windowsタスクスケジューラ）
REM 処理内容: Claude API でブリーフィング生成 → PDF → summary.html → git push
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

if not exist "%BASE%\logs" mkdir "%BASE%\logs"

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i
if "%TODAY%"=="" set TODAY=00000000
set LOGFILE=%BASE%\logs\briefing_%TODAY%.log

echo. >> "%LOGFILE%"
echo ====================================================== >> "%LOGFILE%"
echo [%DATE% %TIME%] update_briefing.bat START >> "%LOGFILE%"

if not exist "%PYTHON%" (
    echo [ERROR] Python not found: %PYTHON% >> "%LOGFILE%"
    exit /b 1
)

"%PYTHON%" "%BASE%\make_briefing_auto.py" >> "%LOGFILE%" 2>&1
set ERR=%ERRORLEVEL%
echo [%DATE% %TIME%] make_briefing_auto.py END (ERRORLEVEL=%ERR%) >> "%LOGFILE%"
echo [%DATE% %TIME%] update_briefing.bat DONE >> "%LOGFILE%"
exit /b %ERR%
