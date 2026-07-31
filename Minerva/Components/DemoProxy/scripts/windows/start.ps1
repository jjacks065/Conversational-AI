[CmdletBinding()]
param([string]$AppDir = "")

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Common.ps1")

$Paths = Get-DemoProxyPaths -AppDir $AppDir
Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null
New-DemoDirectories -Paths $Paths
$settings = Test-DemoConfig -ConfigPath $Paths.Config -AppDir $Paths.Root

$existing = Test-DemoTrackedProcess -StatePath $Paths.ProxyState -ExpectedKind "proxy"
if ($existing.IsOwned) {
    Write-Host "DemoProxy is already running (PID $($existing.Process.ProcessId))."
    exit 0
}
if ($existing.IsRunning) {
    throw "The proxy state points to another process. Run disable.ps1 -Force to clear stale state."
}
Remove-Item -LiteralPath $Paths.ProxyState -Force -ErrorAction SilentlyContinue

$runtime = Get-DemoRuntimeExecutable -AppDir $Paths.Root
$addonPath = [System.IO.Path]::GetFullPath((Join-Path $Paths.Root "proxy\addon.py"))
if (-not (Test-Path -LiteralPath $addonPath -PathType Leaf)) {
    throw "Proxy addon not found: $addonPath"
}

$configOption = "demo_proxy_config=$($Paths.Config)"
$arguments = @(
    "--listen-host"
    "127.0.0.1"
    "--listen-port"
    [string]$settings.ListenPort
    "--set"
    "confdir=$($Paths.MitmConf)"
    "--set"
    "flow_detail=0"
    "--set"
    $configOption
    "--scripts"
    $addonPath
)

$priorPlatform = [Environment]::GetEnvironmentVariable("DEMO_PROXY_PLATFORM", "Process")
$priorCertificateTrust = [Environment]::GetEnvironmentVariable(
    "DEMO_PROXY_CERTIFICATE_TRUSTED",
    "Process"
)
try {
    $env:DEMO_PROXY_PLATFORM = "windows"
    $env:DEMO_PROXY_CERTIFICATE_TRUSTED = if (
        Test-DemoCertificateTrust -CertificateStatePath $Paths.CertificateState
    ) { "true" } else { "false" }
    $process = Start-Process `
        -FilePath $runtime `
        -ArgumentList $arguments `
        -WorkingDirectory $Paths.Root `
        -RedirectStandardOutput $Paths.ProxyStdout `
        -RedirectStandardError $Paths.ProxyStderr `
        -WindowStyle Hidden `
        -PassThru
} finally {
    [Environment]::SetEnvironmentVariable("DEMO_PROXY_PLATFORM", $priorPlatform, "Process")
    [Environment]::SetEnvironmentVariable(
        "DEMO_PROXY_CERTIFICATE_TRUSTED",
        $priorCertificateTrust,
        "Process"
    )
}

$state = [ordered]@{
    kind = "proxy"
    pid = $process.Id
    executable = $runtime
    commandLineMarkers = @($addonPath, $configOption)
    startedAtUtc = [DateTime]::UtcNow.ToString("o")
}
Write-DemoJsonState -Path $Paths.ProxyState -Value $state

try {
    Wait-DemoUri -Uri "http://127.0.0.1:$($settings.HealthPort)/health" -TimeoutSeconds 20 | Out-Null
    Wait-DemoUri -Uri "http://127.0.0.1:$($settings.PacPort)/demo-proxy.pac" -TimeoutSeconds 10 | Out-Null
} catch {
    try {
        Stop-DemoTrackedProcess -StatePath $Paths.ProxyState -ExpectedKind "proxy" -Force | Out-Null
    } catch {
        Write-Warning "Proxy startup cleanup could not verify the launched process."
    }
    throw
}

Write-Host "DemoProxy started on 127.0.0.1:$($settings.ListenPort) (PID $($process.Id))."
