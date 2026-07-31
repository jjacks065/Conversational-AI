[CmdletBinding()]
param([string]$AppDir = "")

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Common.ps1")

$Paths = Get-DemoProxyPaths -AppDir $AppDir
Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null
$state = Read-DemoJsonState -Path $Paths.CertificateState
if ($null -eq $state) {
    Write-Host "No recorded DemoProxy certificate is installed."
    exit 0
}
if (
    $state.PSObject.Properties.Name -notcontains "thumbprint" -or
    $state.PSObject.Properties.Name -notcontains "subject"
) {
    throw "Certificate state is incomplete; refusing broad certificate removal."
}

$thumbprint = ([string]$state.thumbprint).ToUpperInvariant()
if ($thumbprint -notmatch '^[A-F0-9]{40,64}$') {
    throw "Recorded certificate thumbprint is invalid."
}
$storePath = "Cert:\CurrentUser\Root\$thumbprint"
if (Test-Path -LiteralPath $storePath) {
    $certificate = Get-Item -LiteralPath $storePath
    if ($certificate.Subject -ne [string]$state.subject) {
        throw "Recorded certificate subject does not match the trusted certificate."
    }
    Remove-Item -LiteralPath $storePath -Force
}
Remove-Item -LiteralPath $Paths.CertificateState -Force -ErrorAction SilentlyContinue

Write-Host "Recorded DemoProxy CA trust was removed for the current user."
