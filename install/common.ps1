<#
  Shared helpers for install\windows.ps1 and install\check.ps1 (dot-sourced; not meant to be run on its own).
  Everything here only READS: it runs "--version" style commands, "winget list", "code --list-extensions",
  Get-AppxPackage and Test-Path. Works in Windows PowerShell 5.1 and PowerShell 7.
#>

$script:InstallDir = $PSScriptRoot
$script:RepoRoot = Split-Path -Parent $PSScriptRoot

function Get-AppList {
    $json = Get-Content -LiteralPath (Join-Path $script:InstallDir 'apps.json') -Raw -Encoding UTF8
    return @((ConvertFrom-Json $json).apps)
}

function Test-IsAdmin {
    try {
        $id = [Security.Principal.WindowsIdentity]::GetCurrent()
        $p = New-Object Security.Principal.WindowsPrincipal($id)
        return $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    } catch { return $false }
}

function Test-WingetPresent {
    return [bool](Get-Command winget -ErrorAction SilentlyContinue)
}

# Re-read PATH from the registry so programs installed a moment ago are found in this window.
function Update-SessionPath {
    $m = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $u = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = (@($m, $u) | Where-Object { $_ }) -join ';'
}

# Value of a key in config\paths.yaml (simple "key: value" lines), or '' when absent.
function Get-ConfigValue([string]$Key) {
    $cfg = Join-Path $script:RepoRoot 'config\paths.yaml'
    if (-not (Test-Path -LiteralPath $cfg)) { return '' }
    $pattern = '^\s*' + [regex]::Escape($Key) + '\s*:\s*["'']?([^"''#]*)["'']?'
    $line = Select-String -LiteralPath $cfg -Pattern $pattern -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $line) { return '' }
    return ($line.Matches[0].Groups[1].Value.Trim() -replace '/', '\')
}

# Runs one command line and returns @{ Ok; Text } with the first non-empty output line.
function Invoke-VersionCommand([string[]]$CommandLine) {
    $exe = $CommandLine[0]
    $rest = @()
    if ($CommandLine.Count -gt 1) { $rest = $CommandLine[1..($CommandLine.Count - 1)] }
    $cmd = Get-Command $exe -CommandType Application, ExternalScript -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $cmd) { return @{ Ok = $false; Text = "'$exe' not found on PATH" } }
    # The Windows "python" app execution alias opens the Microsoft Store instead of running Python: never call it.
    if ($exe -match '^python3?$' -and $cmd.Source -match '\\Microsoft\\WindowsApps\\') {
        return @{ Ok = $false; Text = "'$exe' is the Microsoft Store alias, not a real Python (see docs\02-install.md)" }
    }
    $old = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $out = & $cmd.Source @rest 2>&1 | ForEach-Object { "$_" }
        $rc = $LASTEXITCODE
    } catch {
        $ErrorActionPreference = $old
        return @{ Ok = $false; Text = "'$exe' failed to run: $($_.Exception.Message)" }
    }
    $ErrorActionPreference = $old
    $first = @($out | Where-Object { "$_".Trim() }) | Select-Object -First 1
    if ($rc -ne 0 -and $null -ne $rc) { return @{ Ok = $false; Text = "'$exe' exited with code $rc" } }
    return @{ Ok = $true; Text = "$first".Trim() }
}

# winget list --id <id> --exact --source winget : returns @{ Ok; Text } (Text = installed version or reason).
# --source winget is the same source windows.ps1 installs from ('--source', 'winget'), so both look at one catalog
# and winget does not query the msstore source for this check.
function Get-WingetInstalled([string]$Id) {
    if (-not $Id) { return @{ Ok = $false; Text = 'no winget id' } }
    if (-not (Test-WingetPresent)) { return @{ Ok = $false; Text = 'winget not found' } }
    $old = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $out = & winget list --id $Id --exact --source winget --disable-interactivity 2>&1 | ForEach-Object { "$_" }
    $rc = $LASTEXITCODE
    $ErrorActionPreference = $old
    if ($rc -ne 0) { return @{ Ok = $false; Text = 'not listed by winget' } }
    foreach ($l in $out) {
        $tok = @("$l".Trim() -split '\s+')
        $i = [Array]::IndexOf($tok, $Id)
        if ($i -ge 0) {
            $ver = ''
            if ($tok.Count -gt $i + 1) { $ver = $tok[$i + 1] }
            return @{ Ok = $true; Text = "winget lists $Id $ver".Trim() }
        }
    }
    return @{ Ok = $false; Text = 'not listed by winget' }
}

# Checks one app from apps.json. Returns @{ Ok; Version; Note }.
function Test-App($App) {
    $c = $App.check
    switch ($c.type) {
        'command' {
            $last = $null
            foreach ($alt in @($c.alternatives)) {
                $r = Invoke-VersionCommand -CommandLine @($alt)
                if ($r.Ok -and $c.expect -and ($r.Text -notmatch $c.expect)) {
                    $r = @{ Ok = $false; Text = "$($alt[0]) reports '$($r.Text)', need a match for $($c.expect)" }
                }
                if ($r.Ok) { return @{ Ok = $true; Version = $r.Text; Note = ($alt -join ' ') } }
                $last = $r
            }
            $w = Get-WingetInstalled $App.winget_id
            if ($w.Ok) { return @{ Ok = $false; Listed = $true; Version = ''; Note = "$($w.Text), but the command is not found: open a NEW PowerShell window and run the check again" } }
            return @{ Ok = $false; Version = ''; Note = $last.Text }
        }
        'path' {
            $p = ''
            if ($c.config_key) { $p = Get-ConfigValue $c.config_key }
            if (-not $p -and $c.path) { $p = [Environment]::ExpandEnvironmentVariables($c.path) }
            if ($p -and (Test-Path -LiteralPath $p)) {
                $v = (Get-Item -LiteralPath $p).VersionInfo
                $ver = $v.ProductVersion
                if (-not $ver) { $ver = $v.FileVersion }
                return @{ Ok = $true; Version = "$ver".Trim(); Note = $p }
            }
            $w = Get-WingetInstalled $App.winget_id
            if ($w.Ok) {
                $n = $w.Text
                if ($p) { $n = "$n (not at $p; set $($c.config_key) in config\paths.yaml)" }
                return @{ Ok = $true; Version = ''; Note = $n }
            }
            if ($p) { return @{ Ok = $false; Version = ''; Note = "not found at $p" } }
            return @{ Ok = $false; Version = ''; Note = "not found ($($c.config_key) is empty in config\paths.yaml and winget does not list it)" }
        }
        'vscode-extension' {
            $code = Get-Command code -CommandType Application, ExternalScript -ErrorAction SilentlyContinue | Select-Object -First 1
            if (-not $code) { return @{ Ok = $false; Version = ''; Note = "'code' not on PATH, so the extension list cannot be read" } }
            $old = $ErrorActionPreference
            $ErrorActionPreference = 'Continue'
            $list = & $code.Source --list-extensions --show-versions 2>&1 | ForEach-Object { "$_" }
            $ErrorActionPreference = $old
            $hit = @($list | Where-Object { $_ -like ($c.id + '@*') }) | Select-Object -First 1
            if ($hit) { return @{ Ok = $true; Version = ($hit -split '@')[1]; Note = $c.id } }
            return @{ Ok = $false; Version = ''; Note = "$($c.id) is not in 'code --list-extensions'" }
        }
        'appx' {
            try {
                $pkg = Get-AppxPackage -Name $c.name -ErrorAction Stop | Select-Object -First 1
                if ($pkg) { return @{ Ok = $true; Version = "$($pkg.Version)"; Note = "app package $($c.name)" } }
            } catch { }
            $w = Get-WingetInstalled $App.winget_id
            if ($w.Ok) { return @{ Ok = $true; Version = ''; Note = $w.Text } }
            return @{ Ok = $false; Version = ''; Note = 'not installed' }
        }
        'winget' {
            $w = Get-WingetInstalled $App.winget_id
            return @{ Ok = $w.Ok; Version = ''; Note = $w.Text }
        }
        default { return @{ Ok = $false; Version = ''; Note = "unknown check type '$($c.type)'" } }
    }
}
