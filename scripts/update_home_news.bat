@echo off
REM ============================================================
REM update_home_news.bat
REM 実行タイミング: 12:30 / 18:30 / 0:30（Windowsタスクスケジューラ）
REM 処理内容: ニュース収集のみ（Economist はスキップ）
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

if not exist "%BASE%\logs" mkdir "%BASE%\logs"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i
if "%TODAY%"=="" set TODAY=00000000
set LOGFILE=%BASE%\logs\home_news_%TODAY%.log

echo [%date% %time%] START: News only >> "%LOGFILE%"
"%PYTHON%" "%BASE%\update_home.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"
) else (
    echo [%date% %time%] DONE >> "%LOGFILE%"
)
exit /b 0
