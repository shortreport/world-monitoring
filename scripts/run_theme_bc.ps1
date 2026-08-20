$BASE   = "C:\Users\shondo\Desktop\agent_project"
$PYTHON = "$BASE\venv\Scripts\python.exe"
$env:PYTHONUTF8 = "1"

$TODAY   = Get-Date -Format "yyyyMMdd"
$LOGFILE = "$BASE\logs\theme_bc_$TODAY.log"
if (-not (Test-Path "$BASE\logs")) { New-Item -ItemType Directory "$BASE\logs" | Out-Null }

"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] START theme_bc" | Out-File $LOGFILE -Encoding UTF8

# 1. テーマデータ収集
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] theme_monitor.py 実行中..." | Out-File $LOGFILE -Append -Encoding UTF8
& $PYTHON "$BASE\theme_monitor.py" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
if ($LASTEXITCODE -ne 0) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] theme_monitor.py FAILED ($LASTEXITCODE) - 終了" | Out-File $LOGFILE -Append -Encoding UTF8
    exit 1
}

# 2. Type B theme.html 生成
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] make_en_theme.py 実行中..." | Out-File $LOGFILE -Append -Encoding UTF8
& $PYTHON "$BASE\make_en_theme.py" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
if ($LASTEXITCODE -ne 0) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] make_en_theme.py FAILED ($LASTEXITCODE)" | Out-File $LOGFILE -Append -Encoding UTF8
}

# 3. Type C theme.html 生成
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] update_type_c.py --only theme 実行中..." | Out-File $LOGFILE -Append -Encoding UTF8
& $PYTHON "$BASE\update_type_c.py" --only theme --no-push 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8

# 4. Git push
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] Git push 中..." | Out-File $LOGFILE -Append -Encoding UTF8
Set-Location $BASE
& git add docs/en/theme.html docs/jp/theme.html docs/data/theme_latest.json 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
$diff = & git diff --staged --quiet 2>&1; $changed = ($LASTEXITCODE -ne 0)
if (-not $changed) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] 変更なし。スキップします。" | Out-File $LOGFILE -Append -Encoding UTF8
} else {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm JST"
    & git commit -m "Auto update Theme: $ts" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
    & git push 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
    if ($LASTEXITCODE -ne 0) {
        "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] push 失敗。merge でリトライ..." | Out-File $LOGFILE -Append -Encoding UTF8
        & git fetch origin main 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
        & git merge -X ours origin/main --no-edit 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
        & git push 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
    }
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] Push 完了" | Out-File $LOGFILE -Append -Encoding UTF8
    & pwsh -NonInteractive -ExecutionPolicy Bypass -File "$BASE\scripts\trigger_deploy.ps1" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
}

"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] DONE" | Out-File $LOGFILE -Append -Encoding UTF8
