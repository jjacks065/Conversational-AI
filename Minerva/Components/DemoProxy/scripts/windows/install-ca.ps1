[CmdletBinding()]
param([string]$AppDir = "")

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Common.ps1")

$Paths = Get-DemoProxyPaths -AppDir $AppDir
Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null
$certificatePath = Join-Path $Paths.MitmConf "mitmproxy-ca-cert.cer"
if (-not (Test-Path -LiteralPath $certificatePath -PathType Leaf)) {
    throw "Local mitmproxy CA was not generated: $certificatePath"
}

$certificate = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new(
    $certificatePath
)
$thumbprint = $certificate.Thumbprint.ToUpperInvariant()
$storePath = "Cert:\CurrentUser\Root\$thumbprint"

if (-not (Test-Path -LiteralPath $storePath)) {
    Import-Certificate `
        -FilePath $certificatePath `
        -CertStoreLocation "Cert:\CurrentUser\Root" | Out-Null
}
if (-not (Test-Path -LiteralPath $storePath)) {
    throw "The DemoProxy CA was not found in Cert:\CurrentUser\Root after import."
}

Write-DemoJsonState -Path $Paths.CertificateState -Value ([ordered]@{
    thumbprint = $thumbprint
    subject = $certificate.Subject
    issuer = $certificate.Issuer
    installedAtUtc = [DateTime]::UtcNow.ToString("o")
    store = "CurrentUser\\Root"
})

Write-Host "DemoProxy CA trusted for the current user (thumbprint $thumbprint)."
