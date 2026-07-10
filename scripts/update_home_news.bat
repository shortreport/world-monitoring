@echo off
REM ============================================================
REM update_home_news.bat
REM 実行タイミング: 12:30 / 18:30 / 0:30（Windowsタスクスケジューラ）
REM 処理内容: ニュースのみ + Type B/C home 生成 + push + Pages デプロイ
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

if not exist "%BASE%\logs" mkdir "%BASE%\logs"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i
if "%TODAY%"=="" set TODAY=00000000
set LOGFILE=%BASE%\logs\home_news_%TODAY%.log

echo [%date% %time%] START: News only >> "%LOGFILE%"
"%PYTHON%" "%BASE%\update_home.py" --no-generate >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] update_home.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"
) else (
    echo [%date% %time%] update_home.py DONE >> "%LOGFILE%"
)

echo [%date% %time%] Type B home 生成中... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\generate_en_home.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 echo [%date% %time%] generate_en_home.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"

echo [%date% %time%] Type C home 生成中... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\update_type_c.py" --only home --no-push >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 echo [%date% %time%] update_type_c.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"

echo [%date% %time%] Git push 中... >> "%LOGFILE%"
cd /d "%BASE%"
git add docs/ >> "%LOGFILE%" 2>&1
git diff --staged --quiet
if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] 変更なし。スキップします。 >> "%LOGFILE%"
) else (
    git commit -m "Home update (news): %date% %time%" >> "%LOGFILE%" 2>&1
    git push >> "%LOGFILE%" 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [%date% %time%] push 失敗。merge でリトライ中... >> "%LOGFILE%"
        git fetch origin main >> "%LOGFILE%" 2>&1
        git merge -X ours origin/main --no-edit >> "%LOGFILE%" 2>&1
        git push >> "%LOGFILE%" 2>&1
    )
    echo [%date% %time%] Push 完了 >> "%LOGFILE%"
)

echo [%date% %time%] GitHub Pages デプロイトリガー... >> "%LOGFILE%"
powershell -NoProfile -ExecutionPolicy Bypass -File "%BASE%\scripts\trigger_deploy.ps1" >> "%LOGFILE%" 2>&1

echo [%date% %time%] DONE >> "%LOGFILE%"
exit /b 0
