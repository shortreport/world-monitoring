@echo off
REM このタスクは run_theme_bc (ps1) に置き換え済み。何もしない。
exit /b 0
REM ============================================================
REM update_theme_bc.bat (stub)
REM 実行タイミング: 毎朝 8:00（Windowsタスクスケジューラ）
REM 処理内容:
REM   1. 監視テーマデータ収集（theme_monitor.py）
REM   2. Type B theme.html 生成（make_en_theme.py）
REM   3. Type C theme.html 生成（update_type_c.py --only theme）
REM   4. GitHub Pages プッシュ + デプロイトリガー
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

if not exist "%BASE%\logs" mkdir "%BASE%\logs"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i
if "%TODAY%"=="" set TODAY=00000000
set LOGFILE=%BASE%\logs\theme_bc_%TODAY%.log

echo [%date% %time%] テーマモニター収集開始... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\theme_monitor.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] theme_monitor.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"
    exit /b 1
)

echo [%date% %time%] Type B theme.html 生成中... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\make_en_theme.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 echo [%date% %time%] make_en_theme.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"

echo [%date% %time%] Type C theme.html 生成中... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\update_type_c.py" --only theme --no-push >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 echo [%date% %time%] update_type_c.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"

echo [%date% %time%] Git push 中... >> "%LOGFILE%"
cd /d "%BASE%"
git add docs/ >> "%LOGFILE%" 2>&1
git diff --staged --quiet
if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] 変更なし。スキップします。 >> "%LOGFILE%"
) else (
    git commit -m "Theme update (B+C): %date% %time%" >> "%LOGFILE%" 2>&1
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
