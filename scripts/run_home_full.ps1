$BASE   = "C:\Users\shondo\Desktop\agent_project"
$PYTHON = "$BASE\venv\Scripts\python.exe"
$env:PYTHONUTF8 = "1"

$TODAY   = Get-Date -Format "yyyyMMdd"
$LOGFILE = "$BASE\logs\home_full_$TODAY.log"
if (-not (Test-Path "$BASE\logs")) { New-Item -ItemType Directory "$BASE\logs" | Out-Null }

"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] START: News + Economist" | Out-File $LOGFILE -Append -Encoding UTF8

# --- Type A: ニュース + Economist 収集 + home/trump/theme/mail HTML 生成 + push ---
try {
    & $PYTHON "$BASE\update_home.py" --with-economist 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
} catch {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] update_home.py FAILED: $_" | Out-File $LOGFILE -Append -Encoding UTF8
}

# --- Type B (EN): home.html 生成 ---
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] Type B home 生成中..." | Out-File $LOGFILE -Append -Encoding UTF8
try {
    & $PYTHON "$BASE\generate_en_home.py" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
} catch {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] generate_en_home.py FAILED: $_" | Out-File $LOGFILE -Append -Encoding UTF8
}

# --- Type C (JP): home.html 生成 ---
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] Type C home 生成中..." | Out-File $LOGFILE -Append -Encoding UTF8
try {
    & $PYTHON "$BASE\update_type_c.py" --only home --no-push 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
} catch {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] update_type_c.py FAILED: $_" | Out-File $LOGFILE -Append -Encoding UTF8
}

# --- B/C ファイルを push ---
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] B/C Git push 中..." | Out-File $LOGFILE -Append -Encoding UTF8
Set-Location $BASE
& git add docs/en/index.html docs/jp/index.html 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
$diff = & git diff --staged --quiet 2>&1; $changed = ($LASTEXITCODE -ne 0)
if (-not $changed) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] B/C 変更なし。スキップします。" | Out-File $LOGFILE -Append -Encoding UTF8
} else {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm JST"
    & git commit -m "Home update (B/C): $ts" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
    & git push 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
    if ($LASTEXITCODE -ne 0) {
        "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] push 失敗。merge でリトライ..." | Out-File $LOGFILE -Append -Encoding UTF8
        & git fetch origin main 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
        & git merge -X ours origin/main --no-edit 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
        & git push 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
    }
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] B/C Push 完了" | Out-File $LOGFILE -Append -Encoding UTF8

    # --- GitHub Pages デプロイ ---
    & powershell -NonInteractive -ExecutionPolicy Bypass -File "$BASE\scripts\trigger_deploy.ps1" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
}

"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] DONE" | Out-File $LOGFILE -Append -Encoding UTF8
