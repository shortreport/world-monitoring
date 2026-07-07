@echo off
REM ============================================================
REM update_mail_full.bat
REM 実行タイミング: 毎朝 7:00（Windowsタスクスケジューラ）
REM 処理内容:
REM   1. Outlook 未読メール処理 → PDF 生成（outlook_to_pdf.py）
REM   2. PDF を送信者別にグループ化・Claude 要約・Web 反映
REM      （mail_slides.py）
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

echo [%date% %time%] メール処理開始（outlook_to_pdf.py）...
"%PYTHON%" "%BASE%\outlook_to_pdf.py"
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] outlook_to_pdf.py が失敗しました（ERRORLEVEL=%ERRORLEVEL%）。
)

echo [%date% %time%] スライド生成・Web反映（mail_slides.py）...
"%PYTHON%" "%BASE%\mail_slides.py"
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] mail_slides.py が失敗しました（ERRORLEVEL=%ERRORLEVEL%）。
)

echo [%date% %time%] 完了。
exit /b 0
