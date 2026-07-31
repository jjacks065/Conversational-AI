[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "Medium")]
param(
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Common.ps1")

$Paths = Get-DemoProxyPaths
Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null
if (-not (Test-Path -LiteralPath $Paths.Root -PathType Container)) {
    Write-Host "DemoProxy is not installed."
    exit 0
}
if (-not $PSCmdlet.ShouldProcess($Paths.Root, "Disable and uninstall DemoProxy")) {
    exit 0
}

& (Join-Path $PSScriptRoot "disable.ps1") -AppDir $Paths.Root -Force:$Force
& (Join-Path $PSScriptRoot "uninstall-ca.ps1") -AppDir $Paths.Root

$task = Get-ScheduledTask -TaskName $script:DemoTaskName -ErrorAction SilentlyContinue
if ($null -ne $task) {
    Unregister-ScheduledTask -TaskName $script:DemoTaskName -Confirm:$false
}

Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null
Remove-Item -LiteralPath $Paths.Root -Recurse -Force
Write-Host "DemoProxy was uninstalled. Normal browser and system proxy settings were unchanged."
