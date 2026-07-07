@echo off
REM update_home_full.bat
REM Schedule: 06:30 daily (Task Scheduler)
REM Action: News + Economist + generate HTML + push
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHON=%BASE%\venv\Scripts\python.exe
set PYTHONUTF8=1

if not exist "%BASE%\logs" mkdir "%BASE%\logs"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i
if "%TODAY%"=="" set TODAY=00000000
set LOGFILE=%BASE%\logs\home_full_%TODAY%.log

echo [%date% %time%] START: News + Economist >> "%LOGFILE%"
"%PYTHON%" "%BASE%\update_home.py" --with-economist >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] FAILED ERRORLEVEL=%ERRORLEVEL% >> "%LOGFILE%"
) else (
    echo [%date% %time%] DONE >> "%LOGFILE%"
)
exit /b 0