@echo off
REM ============================================================
REM update_toyota_watch.bat
REM Schedule: Daily 08:10 (Windows Task Scheduler)
REM Action:   Extract Toyota/auto industry news -> PDF -> email
REM ============================================================
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

if not exist "%BASE%\logs" mkdir "%BASE%\logs"

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i
if "%TODAY%"=="" set TODAY=00000000
set LOGFILE=%BASE%\logs\toyota_watch_%TODAY%.log

echo. >> "%LOGFILE%"
echo ====================================================== >> "%LOGFILE%"
echo [%DATE% %TIME%] update_toyota_watch.bat START >> "%LOGFILE%"

if not exist "%PYTHON%" (
    echo [ERROR] Python not found: %PYTHON% >> "%LOGFILE%"
    exit /b 1
)

REM Mail settings (Gmail)
set SMTP_HOST=smtp.gmail.com
set SMTP_PORT=587
set SMTP_USER=1min.shortreport@gmail.com
set SMTP_PASS=omjx hrgl shrf pfuv
set WATCH_MAIL_TO=shondo@iies.co.jp

"%PYTHON%" "%BASE%\make_toyota_watch.py" >> "%LOGFILE%" 2>&1
set ERR=%ERRORLEVEL%
echo [%DATE% %TIME%] make_toyota_watch.py END (ERRORLEVEL=%ERR%) >> "%LOGFILE%"
echo [%DATE% %TIME%] update_toyota_watch.bat DONE >> "%LOGFILE%"
exit /b %ERR%
