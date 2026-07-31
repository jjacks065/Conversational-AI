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
$stopped = Stop-DemoTrackedProcess `
    -StatePath $Paths.ProxyState `
    -ExpectedKind "proxy" `
    -Force:$Force

if ($stopped) {
    Write-Host "DemoProxy stopped."
} else {
    Write-Host "DemoProxy was not running."
}
