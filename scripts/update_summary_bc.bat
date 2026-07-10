@echo off
REM ============================================================
REM update_summary_bc.bat
REM 実行タイミング: 毎朝 8:30（Windowsタスクスケジューラ）
REM 処理内容:
REM   1. 当日のエグゼクティブサマリーを生成
REM      - Type B 英語 HTML（docs/en/summary.html）
REM      - JP PDF（docs/briefing_latest.pdf + アーカイブ）
REM      - Type C 日本語 HTML（docs/jp/summary.html）アーカイブ更新
REM   2. push + GitHub Pages デプロイ
REM ※ 1日1回のみ実行。次の実行は翌朝 8:30。
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

if not exist "%BASE%\logs" mkdir "%BASE%\logs"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i
if "%TODAY%"=="" set TODAY=00000000
set LOGFILE=%BASE%\logs\summary_bc_%TODAY%.log

echo [%date% %time%] START: Executive Summary (B+C) >> "%LOGFILE%"
"%PYTHON%" "%BASE%\make_en_exec_summary.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] make_en_exec_summary.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"
) else (
    echo [%date% %time%] DONE >> "%LOGFILE%"
)
exit /b 0
