[CmdletBinding()]
param([string]$AppDir = "")

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Common.ps1")

$Paths = Get-DemoProxyPaths -AppDir $AppDir
Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null
& (Join-Path $PSScriptRoot "verify.ps1") -AppDir $Paths.Root -ConfigurationOnly
Test-DemoHardening -AppDir $Paths.Root

$certificatePath = Join-Path $Paths.MitmConf "mitmproxy-ca-cert.cer"
if (-not (Test-Path -LiteralPath $certificatePath -PathType Leaf)) {
    & (Join-Path $PSScriptRoot "start.ps1") -AppDir $Paths.Root
    $deadline = [DateTime]::UtcNow.AddSeconds(15)
    while (
        -not (Test-Path -LiteralPath $certificatePath -PathType Leaf) -and
        [DateTime]::UtcNow -lt $deadline
    ) {
        Start-Sleep -Milliseconds 250
    }
    if (-not (Test-Path -LiteralPath $certificatePath -PathType Leaf)) {
        throw "mitmproxy did not generate its local CA certificate."
    }
}

$wasTrusted = Test-DemoCertificateTrust -CertificateStatePath $Paths.CertificateState
& (Join-Path $PSScriptRoot "install-ca.ps1") -AppDir $Paths.Root

$running = Test-DemoTrackedProcess -StatePath $Paths.ProxyState -ExpectedKind "proxy"
if ($running.IsOwned -and -not $wasTrusted) {
    & (Join-Path $PSScriptRoot "stop.ps1") -AppDir $Paths.Root
}
& (Join-Path $PSScriptRoot "start.ps1") -AppDir $Paths.Root
& (Join-Path $PSScriptRoot "verify.ps1") -AppDir $Paths.Root
& (Join-Path $PSScriptRoot "launch-chrome.ps1") -AppDir $Paths.Root
& (Join-Path $PSScriptRoot "verify.ps1") -AppDir $Paths.Root

$settings = Test-DemoConfig -ConfigPath $Paths.Config -AppDir $Paths.Root
Write-Host "DemoProxy enabled. Operator status: http://127.0.0.1:$($settings.HealthPort)/status"
