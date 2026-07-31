[CmdletBinding()]
param(
    [switch]$DevelopmentMode,
    [switch]$InstallStartupTask
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Common.ps1")

if ($env:OS -ne "Windows_NT") {
    throw "install.ps1 must run on Windows."
}
$architecture = if ($env:PROCESSOR_ARCHITEW6432) {
    $env:PROCESSOR_ARCHITEW6432
} else {
    $env:PROCESSOR_ARCHITECTURE
}
if ($architecture -notin @("AMD64", "ARM64")) {
    throw "Unsupported Windows architecture: $architecture"
}

$Paths = Get-DemoProxyPaths
Assert-DemoInstallRoot -AppDir $Paths.Root | Out-Null
$sourceRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))

try {
    New-DemoDirectories -Paths $Paths

    if (-not [string]::Equals(
        $sourceRoot,
        $Paths.Root,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        foreach ($relativeDirectory in @(
            "proxy",
            "pac",
            "scripts\common",
            "scripts\windows",
            "startup\windows"
        )) {
            $source = Join-Path $sourceRoot $relativeDirectory
            if (-not (Test-Path -LiteralPath $source -PathType Container)) {
                throw "Required install source directory is missing: $source"
            }
            $destination = Join-Path $Paths.Root $relativeDirectory
            New-Item -ItemType Directory -Path $destination -Force | Out-Null
            Get-ChildItem -LiteralPath $source -Force | Copy-Item `
                -Destination $destination `
                -Recurse `
                -Force
        }

        foreach ($relativeFile in @("requirements.txt", "pyproject.toml")) {
            $source = Join-Path $sourceRoot $relativeFile
            if (Test-Path -LiteralPath $source -PathType Leaf) {
                Copy-Item -LiteralPath $source -Destination (Join-Path $Paths.Root $relativeFile) -Force
            }
        }

        $packagedBin = Join-Path $sourceRoot "bin"
        if (Test-Path -LiteralPath $packagedBin -PathType Container) {
            $destinationBin = Join-Path $Paths.Root "bin"
            New-Item -ItemType Directory -Path $destinationBin -Force | Out-Null
            Get-ChildItem -LiteralPath $packagedBin -Force | Copy-Item `
                -Destination $destinationBin `
                -Recurse `
                -Force
        }

        if (-not (Test-Path -LiteralPath $Paths.Config -PathType Leaf)) {
            Copy-Item `
                -LiteralPath (Join-Path $sourceRoot "config\proxy.yaml") `
                -Destination $Paths.Config
        }
        $installedLock = Join-Path $Paths.Root "config\demo-lock.json"
        if (-not (Test-Path -LiteralPath $installedLock -PathType Leaf)) {
            Copy-Item `
                -LiteralPath (Join-Path $sourceRoot "config\demo-lock.json") `
                -Destination $installedLock
        }
        Copy-Item `
            -LiteralPath (Join-Path $sourceRoot "config\proxy.example.yaml") `
            -Destination (Join-Path $Paths.Root "config\proxy.example.yaml") `
            -Force
        Copy-Item `
            -LiteralPath (Join-Path $sourceRoot "config\demo-lock.example.json") `
            -Destination (Join-Path $Paths.Root "config\demo-lock.example.json") `
            -Force
    }

    if ($DevelopmentMode) {
        $venvPython = Join-Path $Paths.Root ".venv\Scripts\python.exe"
        if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
            $python = Get-Command "py.exe" -ErrorAction SilentlyContinue
            if ($null -ne $python) {
                & $python.Source -3 -m venv (Join-Path $Paths.Root ".venv")
            } else {
                $python = Get-Command "python.exe" -ErrorAction SilentlyContinue
                if ($null -eq $python) {
                    throw "Python 3 is required for -DevelopmentMode."
                }
                & $python.Source -m venv (Join-Path $Paths.Root ".venv")
            }
            if ($LASTEXITCODE -ne 0) {
                throw "Python virtual environment creation failed."
            }
        }
        & $venvPython -m pip install --disable-pip-version-check -r (Join-Path $Paths.Root "requirements.txt")
        if ($LASTEXITCODE -ne 0) {
            throw "Development dependencies failed to install."
        }
    }

    Get-DemoRuntimeExecutable -AppDir $Paths.Root | Out-Null
    & (Join-Path $Paths.Root "scripts\windows\verify.ps1") `
        -AppDir $Paths.Root `
        -ConfigurationOnly
    Test-DemoHardening -AppDir $Paths.Root

    & (Join-Path $Paths.Root "scripts\windows\start.ps1") -AppDir $Paths.Root
    $certificatePath = Join-Path $Paths.MitmConf "mitmproxy-ca-cert.cer"
    $deadline = [DateTime]::UtcNow.AddSeconds(15)
    while (
        -not (Test-Path -LiteralPath $certificatePath -PathType Leaf) -and
        [DateTime]::UtcNow -lt $deadline
    ) {
        Start-Sleep -Milliseconds 250
    }
    if (-not (Test-Path -LiteralPath $certificatePath -PathType Leaf)) {
        throw "mitmdump did not generate its local CA certificate."
    }
    & (Join-Path $Paths.Root "scripts\windows\install-ca.ps1") -AppDir $Paths.Root

    # Restart once so the health process inherits the verified trust state.
    & (Join-Path $Paths.Root "scripts\windows\stop.ps1") -AppDir $Paths.Root
    & (Join-Path $Paths.Root "scripts\windows\start.ps1") -AppDir $Paths.Root

    if ($InstallStartupTask) {
        $currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        $startScript = Join-Path $Paths.Root "scripts\windows\start.ps1"
        $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$startScript`" -AppDir `"$($Paths.Root)`""
        $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $arguments
        $trigger = New-ScheduledTaskTrigger -AtLogOn -User $currentUser
        $principal = New-ScheduledTaskPrincipal `
            -UserId $currentUser `
            -LogonType Interactive `
            -RunLevel Limited
        Register-ScheduledTask `
            -TaskName $script:DemoTaskName `
            -Action $action `
            -Trigger $trigger `
            -Principal $principal `
            -Description "Starts the per-user Demo Response Proxy on logon." `
            -Force | Out-Null
    }

    & (Join-Path $Paths.Root "scripts\windows\verify.ps1") -AppDir $Paths.Root
    Write-Host "DemoProxy installation completed for $architecture."
    Write-Host "Enable:  $($Paths.Root)\scripts\windows\enable.ps1"
    Write-Host "Rollback: $($Paths.Root)\scripts\windows\disable.ps1 -Force"
    Write-Host "Uninstall: $($Paths.Root)\scripts\windows\uninstall.ps1"
} catch {
    Write-Warning "Installation did not complete. Rollback with scripts\windows\disable.ps1 -Force, then uninstall-ca.ps1."
    throw
}
