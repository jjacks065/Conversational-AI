Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$script:DemoTaskName = "DemoResponseProxy"

function Get-DemoProxyPaths {
    [CmdletBinding()]
    param([string]$AppDir = "")

    if (-not $env:LOCALAPPDATA) {
        throw "LOCALAPPDATA is required."
    }
    if ([string]::IsNullOrWhiteSpace($AppDir)) {
        $AppDir = Join-Path $env:LOCALAPPDATA "DemoResponseProxy"
    }
    $root = [System.IO.Path]::GetFullPath($AppDir)
    $runtime = Join-Path $root "runtime"
    $logs = Join-Path $root "logs"
    $mitmConf = Join-Path $runtime "mitmproxy"
    $state = Join-Path $runtime "state"

    return [pscustomobject]@{
        Root = $root
        Config = Join-Path $root "config\proxy.yaml"
        Logs = $logs
        Runtime = $runtime
        MitmConf = $mitmConf
        State = $state
        ChromeProfile = Join-Path $root "chrome-profile"
        ProxyState = Join-Path $state "proxy.status.json"
        ChromeState = Join-Path $state "chrome.status.json"
        CertificateState = Join-Path $state "certificate.json"
        ProxyStdout = Join-Path $logs "proxy.stdout.log"
        ProxyStderr = Join-Path $logs "proxy.stderr.log"
    }
}

function Assert-DemoInstallRoot {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$AppDir)

    if (-not $env:LOCALAPPDATA) {
        throw "LOCALAPPDATA is required."
    }
    $expected = [System.IO.Path]::GetFullPath(
        (Join-Path $env:LOCALAPPDATA "DemoResponseProxy")
    ).TrimEnd([System.IO.Path]::DirectorySeparatorChar)
    $actual = [System.IO.Path]::GetFullPath($AppDir).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar
    )
    if (-not [string]::Equals(
        $expected,
        $actual,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw "Unsafe application directory. Expected exactly: $expected"
    }
    return $actual
}

function New-DemoDirectories {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)]$Paths)

    foreach ($directory in @(
        $Paths.Root,
        (Split-Path -Parent $Paths.Config),
        $Paths.Logs,
        $Paths.Runtime,
        $Paths.MitmConf,
        $Paths.State,
        $Paths.ChromeProfile
    )) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }
}

function Write-DemoJsonState {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)]$Value
    )

    $parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    $temporary = "$Path.$([guid]::NewGuid().ToString('N')).tmp"
    try {
        $Value | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $temporary -Encoding UTF8
        Move-Item -LiteralPath $temporary -Destination $Path -Force
    } finally {
        if (Test-Path -LiteralPath $temporary) {
            Remove-Item -LiteralPath $temporary -Force
        }
    }
}

function Read-DemoJsonState {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $null
    }
    try {
        return Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
    } catch {
        throw "State file is invalid JSON: $Path"
    }
}

function Get-DemoConfigScalar {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ConfigPath,
        [Parameter(Mandatory = $true)][string]$Section,
        [Parameter(Mandatory = $true)][string]$Key
    )

    if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
        throw "Configuration file not found: $ConfigPath"
    }
    $activeSection = ""
    $escapedKey = [regex]::Escape($Key)
    foreach ($line in Get-Content -LiteralPath $ConfigPath -Encoding UTF8) {
        if ($line -match '^(?<section>[A-Za-z_][A-Za-z0-9_-]*):\s*$') {
            $activeSection = $Matches.section
            continue
        }
        if (
            $activeSection -eq $Section -and
            $line -match "^\s+$escapedKey\s*:\s*(?<value>.+?)\s*$"
        ) {
            $value = $Matches.value.Trim()
            if (
                ($value.StartsWith('"') -and $value.EndsWith('"')) -or
                ($value.StartsWith("'") -and $value.EndsWith("'"))
            ) {
                $value = $value.Substring(1, $value.Length - 2)
            }
            return $value
        }
    }
    throw "Missing configuration value: $Section.$Key"
}

function ConvertTo-DemoPort {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$Value,
        [Parameter(Mandatory = $true)][string]$Name
    )

    $port = 0
    if (-not [int]::TryParse($Value, [ref]$port) -or $port -lt 1 -or $port -gt 65535) {
        throw "$Name must be a port from 1 through 65535."
    }
    return $port
}

function Test-DemoConfig {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ConfigPath,
        [string]$AppDir = ""
    )

    $listenHost = Get-DemoConfigScalar $ConfigPath "proxy" "listen_host"
    if ($listenHost -ne "127.0.0.1") {
        throw "proxy.listen_host must be 127.0.0.1 for Windows integration."
    }
    $listenPort = ConvertTo-DemoPort (
        Get-DemoConfigScalar $ConfigPath "proxy" "listen_port"
    ) "proxy.listen_port"
    $healthPort = ConvertTo-DemoPort (
        Get-DemoConfigScalar $ConfigPath "platform" "health_port"
    ) "platform.health_port"
    $pacPort = ConvertTo-DemoPort (
        Get-DemoConfigScalar $ConfigPath "platform" "pac_port"
    ) "platform.pac_port"
    if (@($listenPort, $healthPort, $pacPort) | Group-Object | Where-Object Count -gt 1) {
        throw "Proxy, health, and PAC ports must be distinct."
    }
    if (-not [string]::IsNullOrWhiteSpace($AppDir)) {
        $packagedValidator = Join-Path $AppDir "bin\mitmdump.exe"
        $python = Join-Path $AppDir ".venv\Scripts\python.exe"
        $validator = Join-Path $AppDir "scripts\common\verify_config.py"
        if (Test-Path -LiteralPath $packagedValidator -PathType Leaf) {
            & $packagedValidator --demo-verify-config $ConfigPath | Out-Null
            if ($LASTEXITCODE -ne 0) {
                throw "Packaged configuration validation failed."
            }
        } elseif (
            (Test-Path -LiteralPath $python -PathType Leaf) -and
            (Test-Path -LiteralPath $validator -PathType Leaf)
        ) {
            & $python $validator $ConfigPath | Out-Null
            if ($LASTEXITCODE -ne 0) {
                throw "Python configuration validation failed."
            }
        }
    }
    return [pscustomobject]@{
        ListenHost = $listenHost
        ListenPort = $listenPort
        HealthPort = $healthPort
        PacPort = $pacPort
    }
}

function Get-DemoRuntimeExecutable {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$AppDir)

    $candidates = @(
        (Join-Path $AppDir "bin\mitmdump.exe"),
        (Join-Path $AppDir ".venv\Scripts\mitmdump.exe")
    )
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return [System.IO.Path]::GetFullPath($candidate)
        }
    }
    throw "DemoProxy runtime was not found. Reinstall with a packaged runtime or -DevelopmentMode."
}

function Test-DemoHardening {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$AppDir)

    $configPath = Join-Path $AppDir "config\proxy.yaml"
    $lockPath = Join-Path $AppDir "config\demo-lock.json"
    if (-not (Test-Path -LiteralPath $lockPath -PathType Leaf)) {
        throw "Frozen demo rule lock not found: $lockPath"
    }
    $packagedRuntime = Join-Path $AppDir "bin\mitmdump.exe"
    $python = Join-Path $AppDir ".venv\Scripts\python.exe"
    $checker = Join-Path $AppDir "scripts\common\hardening_check.py"
    if (Test-Path -LiteralPath $packagedRuntime -PathType Leaf) {
        & $packagedRuntime --demo-hardening-check $AppDir $configPath $lockPath | Out-Null
    } elseif (
        (Test-Path -LiteralPath $python -PathType Leaf) -and
        (Test-Path -LiteralPath $checker -PathType Leaf)
    ) {
        & $python $checker --project-root $AppDir --config $configPath --lock $lockPath | Out-Null
    } else {
        throw "No hardening checker is available in $AppDir."
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Demo hardening preflight failed."
    }
}

function Test-DemoTrackedProcess {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$StatePath,
        [Parameter(Mandatory = $true)][string]$ExpectedKind
    )

    $state = Read-DemoJsonState $StatePath
    if ($null -eq $state) {
        return [pscustomobject]@{ IsRunning = $false; IsOwned = $false; Reason = "no-state"; Process = $null }
    }
    foreach ($property in @("pid", "executable", "kind", "commandLineMarkers")) {
        if ($state.PSObject.Properties.Name -notcontains $property) {
            return [pscustomobject]@{ IsRunning = $false; IsOwned = $false; Reason = "invalid-state"; Process = $null }
        }
    }
    if ($state.kind -ne $ExpectedKind) {
        return [pscustomobject]@{ IsRunning = $false; IsOwned = $false; Reason = "kind-mismatch"; Process = $null }
    }
    $process = Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = $($state.pid)" -ErrorAction SilentlyContinue
    if ($null -eq $process) {
        return [pscustomobject]@{ IsRunning = $false; IsOwned = $false; Reason = "not-running"; Process = $null }
    }
    $expectedExecutable = [System.IO.Path]::GetFullPath([string]$state.executable)
    $actualExecutable = if ($process.ExecutablePath) {
        [System.IO.Path]::GetFullPath([string]$process.ExecutablePath)
    } else {
        ""
    }
    if (-not [string]::Equals(
        $expectedExecutable,
        $actualExecutable,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        return [pscustomobject]@{ IsRunning = $true; IsOwned = $false; Reason = "executable-mismatch"; Process = $process }
    }
    $commandLine = [string]$process.CommandLine
    foreach ($marker in @($state.commandLineMarkers)) {
        if (
            [string]::IsNullOrWhiteSpace([string]$marker) -or
            $commandLine.IndexOf(
                [string]$marker,
                [System.StringComparison]::OrdinalIgnoreCase
            ) -lt 0
        ) {
            return [pscustomobject]@{ IsRunning = $true; IsOwned = $false; Reason = "command-line-mismatch"; Process = $process }
        }
    }
    return [pscustomobject]@{ IsRunning = $true; IsOwned = $true; Reason = "owned"; Process = $process }
}

function Stop-DemoTrackedProcess {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$StatePath,
        [Parameter(Mandatory = $true)][string]$ExpectedKind,
        [switch]$Force
    )

    $status = Test-DemoTrackedProcess -StatePath $StatePath -ExpectedKind $ExpectedKind
    if (-not $status.IsRunning) {
        if (Test-Path -LiteralPath $StatePath) {
            Remove-Item -LiteralPath $StatePath -Force
        }
        return $false
    }
    if (-not $status.IsOwned) {
        if ($Force -and (Test-Path -LiteralPath $StatePath)) {
            Remove-Item -LiteralPath $StatePath -Force
        }
        throw "Refusing to terminate PID $($status.Process.ProcessId): $($status.Reason)."
    }
    Stop-Process -Id $status.Process.ProcessId -Force:$Force -ErrorAction Stop
    $deadline = [DateTime]::UtcNow.AddSeconds(10)
    do {
        Start-Sleep -Milliseconds 100
        $remaining = Get-Process -Id $status.Process.ProcessId -ErrorAction SilentlyContinue
    } while ($null -ne $remaining -and [DateTime]::UtcNow -lt $deadline)
    if ($null -ne $remaining) {
        throw "Process $($status.Process.ProcessId) did not stop."
    }
    Remove-Item -LiteralPath $StatePath -Force -ErrorAction SilentlyContinue
    return $true
}

function Test-DemoPortOpen {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$HostName,
        [Parameter(Mandatory = $true)][int]$Port,
        [int]$TimeoutMilliseconds = 750
    )

    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $task = $client.ConnectAsync($HostName, $Port)
        if (-not $task.Wait($TimeoutMilliseconds)) {
            return $false
        }
        return $client.Connected
    } catch {
        return $false
    } finally {
        $client.Dispose()
    }
}

function Wait-DemoUri {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$Uri,
        [int]$TimeoutSeconds = 15
    )

    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    do {
        try {
            return Invoke-WebRequest -Uri $Uri -UseBasicParsing -TimeoutSec 2
        } catch {
            Start-Sleep -Milliseconds 250
        }
    } while ([DateTime]::UtcNow -lt $deadline)
    throw "Timed out waiting for: $Uri"
}

function Test-DemoCertificateTrust {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$CertificateStatePath)

    $state = Read-DemoJsonState $CertificateStatePath
    if ($null -eq $state -or $state.PSObject.Properties.Name -notcontains "thumbprint") {
        return $false
    }
    $thumbprint = ([string]$state.thumbprint).ToUpperInvariant()
    if ($thumbprint -notmatch '^[A-F0-9]{40,64}$') {
        return $false
    }
    return Test-Path -LiteralPath "Cert:\CurrentUser\Root\$thumbprint"
}
