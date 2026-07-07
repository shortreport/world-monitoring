@echo off
REM ============================================================
REM update_trump.bat
REM 実行タイミング: 毎朝 7:30（Windowsタスクスケジューラ）
REM 処理内容:
REM   1. トランプモニターデータ収集・要約（trump_monitor.py）
REM   2. サイト HTML 再生成（generate_site.py）
REM   3. GitHub Pages プッシュ
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

echo [%date% %time%] トランプモニター収集開始（trump_monitor.py）...
"%PYTHON%" "%BASE%\trump_monitor.py"
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] trump_monitor.py が失敗しました（ERRORLEVEL=%ERRORLEVEL%）。
    exit /b 1
)

echo [%date% %time%] サイト HTML 再生成（generate_site.py）...
"%PYTHON%" "%BASE%\generate_site.py"
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] generate_site.py が失敗しました（ERRORLEVEL=%ERRORLEVEL%）。
    exit /b 1
)

echo [%date% %time%] GitHub Pages にプッシュ...
cd /d "%BASE%"
git add docs/
git diff --staged --quiet
if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] 変更なし。スキップします。
) else (
    git commit -m "Auto update Trump Monitor: %date% %time%"
    git push
    echo [%date% %time%] プッシュ完了。
)

echo [%date% %time%] 完了。
exit /b 0
