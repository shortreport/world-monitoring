$BASE   = "C:\Users\shondo\Desktop\agent_project"
$PYTHON = "$BASE\venv\Scripts\python.exe"
$env:PYTHONUTF8 = "1"

$TODAY   = Get-Date -Format "yyyyMMdd"
$LOGFILE = "$BASE\logs\home_full_$TODAY.log"
if (-not (Test-Path "$BASE\logs")) { New-Item -ItemType Directory "$BASE\logs" | Out-Null }

"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] START: News + Economist" | Out-File $LOGFILE -Append -Encoding UTF8
try {
    & $PYTHON "$BASE\update_home.py" --with-economist 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] DONE" | Out-File $LOGFILE -Append -Encoding UTF8
} catch {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] FAILED: $_" | Out-File $LOGFILE -Append -Encoding UTF8
}
