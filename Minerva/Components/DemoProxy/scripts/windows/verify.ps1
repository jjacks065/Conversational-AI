[CmdletBinding()]
param(
    [string]$AppDir = "",
    [switch]$ConfigurationOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Common.ps1")

$Paths = Get-DemoProxyPaths -AppDir $AppDir
Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null
$settings = Test-DemoConfig -ConfigPath $Paths.Config -AppDir $Paths.Root
Write-Host "Configuration: valid and loopback-only."

if ($ConfigurationOnly) {
    exit 0
}

$process = Test-DemoTrackedProcess -StatePath $Paths.ProxyState -ExpectedKind "proxy"
if (-not $process.IsOwned) {
    throw "Proxy process verification failed: $($process.Reason)."
}
if (-not (Test-DemoPortOpen -HostName "127.0.0.1" -Port $settings.ListenPort)) {
    throw "Proxy port is not listening on 127.0.0.1:$($settings.ListenPort)."
}

$healthResponse = Wait-DemoUri -Uri "http://127.0.0.1:$($settings.HealthPort)/health" -TimeoutSeconds 5
$health = $healthResponse.Content | ConvertFrom-Json
if (
    $health.status -ne "ok" -or
    -not $health.proxyListening -or
    -not $health.pacServerListening -or
    -not $health.configurationLoaded -or
    -not $health.certificateTrusted
) {
    throw "Health endpoint reports an incomplete proxy startup."
}

$pacResponse = Wait-DemoUri -Uri "http://127.0.0.1:$($settings.PacPort)/demo-proxy.pac" -TimeoutSeconds 5
if ($pacResponse.Content -notmatch 'FindProxyForURL') {
    throw "PAC endpoint did not return a PAC function."
}
if (-not (Test-DemoCertificateTrust -CertificateStatePath $Paths.CertificateState)) {
    throw "The recorded DemoProxy CA is not trusted in Cert:\CurrentUser\Root."
}

Write-Host "Verification passed: process, proxy port, health, PAC, and certificate trust."
