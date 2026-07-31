[CmdletBinding()]
param([string]$AppDir = "")

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Common.ps1")

$Paths = Get-DemoProxyPaths -AppDir $AppDir
Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null
$settings = Test-DemoConfig -ConfigPath $Paths.Config -AppDir $Paths.Root
$DefaultPacUrl = "http://127.0.0.1:8765/demo-proxy.pac"

$PacUrl = if ($env:DEMO_PROXY_PAC_URL) {
    $env:DEMO_PROXY_PAC_URL
} elseif ($settings.PacPort -eq 8765) {
    $DefaultPacUrl
} else {
    "http://127.0.0.1:$($settings.PacPort)/demo-proxy.pac"
}
$StartUrl = if ($env:DEMO_PROXY_START_URL) {
    $env:DEMO_PROXY_START_URL
} else {
    "https://nexus-cloud-web-stg.bsc.bscal.com/"
}

if (-not $env:LOCALAPPDATA) {
    throw "LOCALAPPDATA is required to create the dedicated Chrome profile."
}
$ProfileDir = if ($env:DEMO_PROXY_CHROME_PROFILE) {
    $env:DEMO_PROXY_CHROME_PROFILE
} else {
    $Paths.ChromeProfile
}

$Candidates = [System.Collections.Generic.List[string]]::new()
if ($env:DEMO_PROXY_CHROME_PATH) {
    $Candidates.Add($env:DEMO_PROXY_CHROME_PATH)
}
if ($env:ProgramFiles) {
    $Candidates.Add((Join-Path $env:ProgramFiles "Google\Chrome\Application\chrome.exe"))
}
if (${env:ProgramFiles(x86)}) {
    $Candidates.Add((Join-Path ${env:ProgramFiles(x86)} "Google\Chrome\Application\chrome.exe"))
}
$Candidates.Add((Join-Path $env:LOCALAPPDATA "Google\Chrome\Application\chrome.exe"))

$ChromePath = $Candidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
if (-not $ChromePath) {
    throw "Google Chrome was not found. Set DEMO_PROXY_CHROME_PATH."
}

try {
    Invoke-WebRequest -Uri $PacUrl -UseBasicParsing -TimeoutSec 3 | Out-Null
} catch {
    throw "DemoProxy PAC endpoint is unavailable: $PacUrl"
}

New-Item -ItemType Directory -Path $ProfileDir -Force | Out-Null

$existing = Test-DemoTrackedProcess -StatePath $Paths.ChromeState -ExpectedKind "chrome"
if ($existing.IsOwned) {
    Write-Host "Dedicated DemoProxy Chrome is already running (PID $($existing.Process.ProcessId))."
    exit 0
}
if ($existing.IsRunning) {
    throw "Chrome state points to another process. Run disable.ps1 -Force to clear stale state."
}
Remove-Item -LiteralPath $Paths.ChromeState -Force -ErrorAction SilentlyContinue

$ChromeArguments = @(
    "--user-data-dir=`"$ProfileDir`""
    "--proxy-pac-url=$PacUrl"
    "--no-first-run"
    "--no-default-browser-check"
    $StartUrl
)

$ChromePath = [System.IO.Path]::GetFullPath($ChromePath)
$process = Start-Process -FilePath $ChromePath -ArgumentList $ChromeArguments -PassThru
Write-DemoJsonState -Path $Paths.ChromeState -Value ([ordered]@{
    kind = "chrome"
    pid = $process.Id
    executable = $ChromePath
    commandLineMarkers = @($ProfileDir, $PacUrl)
    startedAtUtc = [DateTime]::UtcNow.ToString("o")
})

Write-Host "Dedicated DemoProxy Chrome launched (PID $($process.Id))."
