[CmdletBinding()]
param(
    [string]$AppDir = "",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Common.ps1")

$Paths = Get-DemoProxyPaths -AppDir $AppDir
Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null

try {
    Stop-DemoTrackedProcess `
        -StatePath $Paths.ChromeState `
        -ExpectedKind "chrome" `
        -Force:$Force | Out-Null
} catch {
    if (-not $Force) {
        throw
    }
    Write-Warning $_.Exception.Message
    Remove-Item -LiteralPath $Paths.ChromeState -Force -ErrorAction SilentlyContinue
}

try {
    & (Join-Path $PSScriptRoot "stop.ps1") -AppDir $Paths.Root -Force:$Force
} catch {
    if (-not $Force) {
        throw
    }
    Write-Warning $_.Exception.Message
    Remove-Item -LiteralPath $Paths.ProxyState -Force -ErrorAction SilentlyContinue
}

if (Test-Path -LiteralPath $Paths.Config -PathType Leaf) {
    $settings = Test-DemoConfig -ConfigPath $Paths.Config -AppDir $Paths.Root
    if (Test-DemoPortOpen -HostName "127.0.0.1" -Port $settings.ListenPort) {
        throw "Port $($settings.ListenPort) is still listening; no unverified process was terminated."
    }
}

Write-Host "DemoProxy disabled. Normal browser and system proxy settings were unchanged."
