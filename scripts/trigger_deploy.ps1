# trigger_deploy.ps1
# GitHub Pages デプロイトリガー（update.yml workflow_dispatch）
# git credential store からトークンを取得して API を呼び出す

function Get-GhToken {
    try {
        $input_str = "protocol=https`nhost=github.com`n"
        $lines = ($input_str | git credential fill 2>$null) -split "`n"
        $pw = $lines | Where-Object { $_ -match "^password=" } | Select-Object -First 1
        if ($pw) { return ($pw -replace "^password=","").Trim() }
    } catch {}
    return $null
}

$token = $env:GH_TOKEN
if (-not $token) { $token = Get-GhToken }
if (-not $token) {
    Write-Host "[Deploy] WARN: GH_TOKEN 取得失敗。デプロイをスキップします。"
    exit 0
}

$headers = @{
    "Authorization"        = "Bearer $token"
    "Accept"               = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}
try {
    Invoke-RestMethod `
        -Uri "https://api.github.com/repos/shortreport/world-monitoring/actions/workflows/update.yml/dispatches" `
        -Method Post `
        -Headers $headers `
        -Body '{"ref":"main"}' `
        -ContentType "application/json" | Out-Null
    Write-Host "[Deploy] OK: GitHub Actions デプロイトリガー完了"
} catch {
    Write-Host "[Deploy] WARN: トリガー失敗 - $_"
}
