$BASE   = "C:\Users\shondo\Desktop\agent_project"
$PYTHON = "$BASE\venv\Scripts\python.exe"
$env:PYTHONUTF8 = "1"

$TODAY   = Get-Date -Format "yyyyMMdd"
$LOGFILE = "$BASE\logs\summary_bc_$TODAY.log"
if (-not (Test-Path "$BASE\logs")) { New-Item -ItemType Directory "$BASE\logs" | Out-Null }

"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] START summary_bc" | Out-File $LOGFILE -Encoding UTF8
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] make_en_exec_summary.py 実行中..." | Out-File $LOGFILE -Append -Encoding UTF8

& $PYTHON "$BASE\make_en_exec_summary.py" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8

if ($LASTEXITCODE -ne 0) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] make_en_exec_summary.py FAILED ($LASTEXITCODE)" | Out-File $LOGFILE -Append -Encoding UTF8
} else {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] DONE" | Out-File $LOGFILE -Append -Encoding UTF8
}
