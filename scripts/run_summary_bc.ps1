$BASE   = "C:\Users\shondo\Desktop\agent_project"
$PYTHON = "$BASE\venv\Scripts\python.exe"
$env:PYTHONUTF8 = "1"

# ログを最初に開く（どこで止まるかわかるように）
$TODAY   = Get-Date -Format "yyyyMMdd"
$LOGFILE = "$BASE\logs\summary_bc_$TODAY.log"
if (-not (Test-Path "$BASE\logs")) { New-Item -ItemType Directory "$BASE\logs" | Out-Null }
"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] START summary_bc" | Out-File $LOGFILE -Encoding UTF8

# GH_TOKEN: レジストリ優先 → git credential fill フォールバック
if (-not $env:GH_TOKEN) {
    try {
        $reg = Get-ItemProperty -Path "HKCU:\Environment" -Name "GH_TOKEN" -ErrorAction Stop
        $env:GH_TOKEN = $reg.GH_TOKEN
        "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] GH_TOKEN: レジストリから取得" | Out-File $LOGFILE -Append -Encoding UTF8
    } catch {
        "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] GH_TOKEN: レジストリになし。git credential fill を試みる..." | Out-File $LOGFILE -Append -Encoding UTF8
        try {
            $lines = ("protocol=https`nhost=github.com`n" | git credential fill 2>$null) -split "`n"
            $pw = ($lines | Where-Object { $_ -match "^password=" } | Select-Object -First 1) -replace "^password=",""
            if ($pw) {
                $env:GH_TOKEN = $pw.Trim()
                "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] GH_TOKEN: git credential fill から取得" | Out-File $LOGFILE -Append -Encoding UTF8
            }
        } catch {}
    }
}

"[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] make_en_exec_summary.py 実行中..." | Out-File $LOGFILE -Append -Encoding UTF8

& $PYTHON "$BASE\make_en_exec_summary.py" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8

if ($LASTEXITCODE -ne 0) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] make_en_exec_summary.py FAILED ($LASTEXITCODE)" | Out-File $LOGFILE -Append -Encoding UTF8
} else {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] DONE" | Out-File $LOGFILE -Append -Encoding UTF8
}

# Toyota Watch: 当日PDFがまだなければ実行（PC未起動日の補完）
$WATCH_PDF = "$BASE\docs\toyota_watch\toyota_watch_$TODAY.pdf"
if (Test-Path $WATCH_PDF) {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] Toyota Watch: 本日分PDF済み → スキップ ($WATCH_PDF)" | Out-File $LOGFILE -Append -Encoding UTF8
} else {
    "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] Toyota Watch: 本日分PDFなし → 実行" | Out-File $LOGFILE -Append -Encoding UTF8
    $env:SMTP_HOST     = "smtp.gmail.com"
    $env:SMTP_PORT     = "587"
    $env:SMTP_USER     = "1min.shortreport@gmail.com"
    $env:SMTP_PASS     = "omjx hrgl shrf pfuv"
    $env:WATCH_MAIL_TO = "shondo@iies.co.jp"
    & $PYTHON "$BASE\make_toyota_watch.py" 2>&1 | Out-File $LOGFILE -Append -Encoding UTF8
    if ($LASTEXITCODE -ne 0) {
        "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] Toyota Watch FAILED ($LASTEXITCODE)" | Out-File $LOGFILE -Append -Encoding UTF8
    } else {
        "[$((Get-Date -Format 'yyyy/MM/dd HH:mm:ss'))] Toyota Watch 完了" | Out-File $LOGFILE -Append -Encoding UTF8
    }
}
