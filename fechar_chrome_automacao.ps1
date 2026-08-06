$ErrorActionPreference = "SilentlyContinue"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$profile = Join-Path $root "chrome_profile"

Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -eq "chromedriver.exe" -or
        ($_.CommandLine -and $_.CommandLine.Contains($profile))
    } |
    ForEach-Object {
        Stop-Process -Id $_.ProcessId -Force
    }

Start-Sleep -Seconds 1

$lock = Join-Path $profile "lockfile"
if (Test-Path -LiteralPath $lock) {
    Remove-Item -LiteralPath $lock -Force
}

Write-Host "Chrome da automacao fechado e trava limpa."
