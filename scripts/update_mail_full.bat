@echo off
REM ============================================================
REM update_mail_full.bat
REM 実行タイミング: 毎朝 7:00（Windowsタスクスケジューラ）
REM 処理内容:
REM   1. Outlook 未読メール処理 → PDF 生成（outlook_to_pdf.py）
REM   2. PDF を送信者別にグループ化・Claude 要約・Web 反映
REM      （mail_slides.py）
REM   3. Type B intelligence.html 生成・push（make_en_intelligence.py）
REM   4. Type C intelligence.html 生成・push（update_type_c.py --only intelligence）
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

if not exist "%BASE%\logs" mkdir "%BASE%\logs"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i
if "%TODAY%"=="" set TODAY=00000000
set LOGFILE=%BASE%\logs\mail_full_%TODAY%.log

echo [%date% %time%] メール処理開始（outlook_to_pdf.py）... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\outlook_to_pdf.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] outlook_to_pdf.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"
)

echo [%date% %time%] スライド生成・Web反映（mail_slides.py）... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\mail_slides.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] mail_slides.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"
)

echo [%date% %time%] Type B intelligence.html 生成・push（make_en_intelligence.py）... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\make_en_intelligence.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] make_en_intelligence.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"
)

echo [%date% %time%] Type C intelligence.html 生成中... >> "%LOGFILE%"
"%PYTHON%" "%BASE%\update_type_c.py" --only intelligence --no-push >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] update_type_c.py FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"
)

echo [%date% %time%] Type C git push 中... >> "%LOGFILE%"
cd /d "%BASE%"
git add docs/jp/intelligence.html >> "%LOGFILE%" 2>&1
git diff --staged --quiet
if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] 変更なし。スキップします。 >> "%LOGFILE%"
) else (
    git commit -m "Intelligence update (JP): %date% %time%" >> "%LOGFILE%" 2>&1
    git push >> "%LOGFILE%" 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [%date% %time%] push 失敗。merge でリトライ中... >> "%LOGFILE%"
        git fetch origin main >> "%LOGFILE%" 2>&1
        git merge -X ours origin/main --no-edit >> "%LOGFILE%" 2>&1
        git push >> "%LOGFILE%" 2>&1
    )
    echo [%date% %time%] Push 完了 >> "%LOGFILE%"

    echo [%date% %time%] GitHub Pages デプロイトリガー... >> "%LOGFILE%"
    powershell -NoProfile -ExecutionPolicy Bypass -File "%BASE%\scripts\trigger_deploy.ps1" >> "%LOGFILE%" 2>&1
)

echo [%date% %time%] DONE >> "%LOGFILE%"
exit /b 0
