$BASE   = "C:\Users\shondo\Desktop\agent_project"
$PYTHON = "$BASE\venv\Scripts\python.exe"
$env:PYTHONUTF8 = "1"

$TODAY   = Get-Date -Format "yyyyMMdd"
$LOGFILE = "$BASE\logs\mail_full_$TODAY.log"
if (-not (Test-Path "$BASE\logs")) { New-Item -ItemType Directory "$BASE\logs" | Out-Null }

"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] START mail_full" | Out-File $LOGFILE -Encoding UTF8

# 1. Outlook 未読メール -> PDF 変換
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] outlook_to_pdf.py 実行中..." | Out-File $LOGFILE -Append -Encoding UTF8
& $PYTHON "$BASE\outlook_to_pdf.py" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
if ($LASTEXITCODE -ne 0) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] outlook_to_pdf.py FAILED ($LASTEXITCODE)" | Out-File $LOGFILE -Append -Encoding UTF8
}

# 2. PDF -> スライド生成・Web反映
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] mail_slides.py 実行中..." | Out-File $LOGFILE -Append -Encoding UTF8
& $PYTHON "$BASE\mail_slides.py" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
if ($LASTEXITCODE -ne 0) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] mail_slides.py FAILED ($LASTEXITCODE)" | Out-File $LOGFILE -Append -Encoding UTF8
}

# 3. Type B intelligence.html 生成
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] make_en_intelligence.py 実行中..." | Out-File $LOGFILE -Append -Encoding UTF8
& $PYTHON "$BASE\make_en_intelligence.py" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
if ($LASTEXITCODE -ne 0) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] make_en_intelligence.py FAILED ($LASTEXITCODE)" | Out-File $LOGFILE -Append -Encoding UTF8
}

# 4. Type C intelligence.html 生成
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] update_type_c.py --only intelligence 実行中..." | Out-File $LOGFILE -Append -Encoding UTF8
& $PYTHON "$BASE\update_type_c.py" --only intelligence --no-push 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8

# 5. Type C git push
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] Git push 中..." | Out-File $LOGFILE -Append -Encoding UTF8
Set-Location $BASE
& git add docs/jp/intelligence.html 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
$diff = & git diff --staged --quiet 2>&1; $changed = ($LASTEXITCODE -ne 0)
if (-not $changed) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] JP intelligence 変更なし。スキップします。" | Out-File $LOGFILE -Append -Encoding UTF8
} else {
    $ts = Get-Date -Format 'yyyy-MM-dd HH:mm JST'
    $msg = "Intelligence update (JP): $ts"
    & git commit -m $msg 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
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