@echo off
set BASE=C:\Users\shondo\Desktop\agent_project
set PYTHONUTF8=1

if not exist "%BASE%\logs" mkdir "%BASE%\logs"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i
if "%TODAY%"=="" set TODAY=00000000
set LOGFILE=%BASE%\logs\home_full_%TODAY%.log

echo [%date% %time%] TEST: ログ作成テスト >> "%LOGFILE%"
echo LOGFILE=%LOGFILE%
echo TODAY=%TODAY%
