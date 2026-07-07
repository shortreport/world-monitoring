@echo off
REM ============================================================
REM collect_trump.bat
REM 実行タイミング: 毎朝 5:30（Windowsタスクスケジューラ）
REM 処理内容:
REM   - トランプモニターデータ収集・JSON生成のみ
REM   - サイト更新・pushはしない（6:30のupdate_home_full.batが行う）
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

cd /d "%BASE%"

if not exist "%BASE%\logs" mkdir "%BASE%\logs"
set LOGFILE=%BASE%\logs\trump.log

echo [%date% %time%] Trump Monitor 収集開始... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\trump_monitor.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] trump_monitor.py 失敗 (ERRORLEVEL=%ERRORLEVEL%) >> "%LOGFILE%"
) else (
    echo [%date% %time%] trump_monitor.py 完了 >> "%LOGFILE%"
)
exit /b 0
