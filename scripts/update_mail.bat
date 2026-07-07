@echo off
REM ============================================================
REM update_mail.bat
REM 実行タイミング: 毎朝 6:30（Windowsタスクスケジューラ）
REM 処理内容:
REM   - ニュース収集（dashboard_app.py 5001 + news_app.py 5002）
REM   - Economist メール要約（Outlook 接続）
REM   - サイト HTML 再生成 + GitHub Pages プッシュ
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

echo [%date% %time%] ホームページ全更新（ニュース + Economist）開始...
"%PYTHON%" "%BASE%\update_home.py" --with-economist
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] update_home.py --with-economist が失敗しました（ERRORLEVEL=%ERRORLEVEL%）。
)

echo [%date% %time%] 完了。
exit /b 0
