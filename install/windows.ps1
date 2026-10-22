<#
.SYNOPSIS
  Installs the Maker Mastery prerequisites on Windows 11 with winget, one app at a time, asking Y/N for each.

.DESCRIPTION
  The app list (with each verified winget id and its source) is install\apps.json.
  What it does:
    1. Checks that winget is present, and whether this window runs as administrator.
    2. Checks every app (read-only) and prints a plan: which are already installed (skipped) and which can be installed.
    3. For each missing app, prints the exact command and asks "Install <app>? [y/N]". Only "y" or "yes" installs it.
    4. Logs every decision and command to install\install.log (this file is not committed to git).
  Nothing installs silently: it never passes --silent, and it adds --accept-package-agreements and
  --accept-source-agreements only after you answered y for that app (they accept the package's license and the
  winget source's terms, which winget would otherwise ask you about).
  Run it again at any time: apps that are already installed are skipped.

  Administrator: run it in a NORMAL PowerShell window. Apps marked "user" scope install without administrator rights.
  Apps marked "machine" scope (Bambu Studio, OrcaSlicer, Blender) make Windows show an administrator (UAC) prompt
  during their install; answer it, or the install fails. See docs\02-install.md, "Windows: normal or administrator?".

.PARAMETER DryRun
  Prints every command it would run and asks the same questions, but never runs winget install or
  code --install-extension. The read-only checks still run.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File install\windows.ps1 -DryRun
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File install\windows.ps1
#>
[CmdletBinding()]
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

$LogFile = Join-Path $PSScriptRoot 'install.log'

function Log([string]$Text) {
    $line = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + '  ' + $Text
    try { Add-Content -LiteralPath $LogFile -Value $line -Encoding UTF8 } catch { }
}
function Say([string]$Text, [string]$Color = '') {
    if ($Color) { Write-Host $Text -ForegroundColor $Color } else { Write-Host $Text }
    Log $Text
}
# Y/N question. Reads piped input when stdin is redirected (used by the self-test), otherwise Read-Host.
function Ask([string]$Question) {
    Write-Host -NoNewline "$Question [y/N] "
    $a = $null
    if ([Console]::IsInputRedirected) {
        $a = [Console]::In.ReadLine()
        Write-Host $a
    } else {
        $a = Read-Host
    }
    if ($null -eq $a) { $a = '' }
    $yes = ("$a".Trim() -match '^(y|yes)$')
    Log ("Q: $Question -> answer '" + "$a".Trim() + "' -> " + $(if ($yes) { 'YES' } else { 'NO' }))
    return $yes
}

Log '======== install\windows.ps1 started'
$mode = 'INSTALL'
if ($DryRun) { $mode = 'DRY RUN (nothing will be installed)' }
Say "Maker Mastery prerequisites for Windows - mode: $mode"
Say "PowerShell $($PSVersionTable.PSVersion); log file: install\install.log"
Say 'No AI ever starts, sends, uploads or queues a print. This script only installs the apps you say y to.'

# ------------------------------------------------------------------ 1. winget and admin
$isAdmin = Test-IsAdmin
Say ''
if ($isAdmin) {
    Say 'This window runs AS ADMINISTRATOR.' 'Yellow'
    Say '  User-scope apps would then be installed for the administrator account you are signed in with, and VS Code'
    Say '  says its User setup disables updates while VS Code runs as Administrator. Prefer a normal window:'
    Say '  close this one, open PowerShell from Start without "Run as administrator", and run the script again.'
    if (-not (Ask 'Continue in this administrator window anyway?')) { Say 'Stopped by your answer. Nothing was installed.'; exit 0 }
} else {
    Say 'This window runs as a normal user (recommended). "machine" scope apps will show a Windows administrator prompt.'
}

if (-not (Test-WingetPresent)) {
    Say ''
    Say 'winget was not found.' 'Yellow'
    Say 'winget comes with the App Installer on Windows 11. Microsoft explains how to get it here:'
    Say '  https://learn.microsoft.com/en-us/windows/package-manager/winget/'
    Say 'Or install every app by hand with the direct download links in docs\02-install.md.'
    exit 1
}

# ------------------------------------------------------------------ 2. plan
$apps = Get-AppList
$todo = @()
Say ''
Say 'Checking what is already installed (read-only)...'
foreach ($a in $apps) {
    $r = Test-App $a
    $kind = 'optional'
    if ($a.required) { $kind = 'required' }
    if ($r.Ok) {
        $v = $r.Version; if (-not $v) { $v = $r.Note }; Say ("  [installed] {0} ({1}) {2}" -f $a.name, $kind, $v)
    } elseif ($r.Listed) {
        Say ("  [not on PATH] {0} ({1}): {2}. Not reinstalled." -f $a.name, $kind, $r.Note) 'Yellow'
    } else {
        Say ("  [missing]   {0} ({1}): {2}" -f $a.name, $kind, $r.Note)
        $todo += $a
    }
}
if ($todo.Count -eq 0) {
    Say ''
    Say 'Everything in install\apps.json is already installed. Nothing to do.' 'Green'
    Say 'Run install\check.ps1 for the full PASS/FAIL table.'
    exit 0
}

Say ''
Say 'Plan: you will be asked y/N for each of these, one at a time:'
foreach ($a in $todo) {
    if ($a.winget_id) {
        $sc = 'no --scope'
        if ($a.scope) { $sc = "$($a.scope) scope" }
        Say ("  - {0}: winget id {1} ({2}); id source: {3}" -f $a.name, $a.winget_id, $sc, $a.source_url)
    } else {
        Say ("  - {0}: VS Code extension {1}; source: {2}" -f $a.name, $a.vscode_extension, $a.source_url)
    }
}

# ------------------------------------------------------------------ 3. one app at a time
$installed = 0; $skipped = 0; $failed = 0
foreach ($a in $todo) {
    Say ''
    $kind = 'optional'
    if ($a.required) { $kind = 'required' }
    Say ("== {0} ({1})" -f $a.name, $kind) 'Cyan'

    if ($a.vscode_extension) {
        $argList = @('--install-extension', $a.vscode_extension)
        Say ("  Command: code " + ($argList -join ' '))
        Say '  This asks VS Code to download the extension from the Visual Studio Marketplace.'
        if (-not (Ask "  Install $($a.name)?")) { Say '  Skipped.'; $skipped++; continue }
        if ($DryRun) { Say '  DRY RUN: not run.'; continue }
        Update-SessionPath
        $code = Get-Command code -CommandType Application, ExternalScript -ErrorAction SilentlyContinue | Select-Object -First 1
        if (-not $code) {
            Say "  'code' is not on PATH in this window yet. Open a new PowerShell window after VS Code is installed and run this script again." 'Yellow'
            $failed++; continue
        }
        & $code.Source @argList
        $rc = $LASTEXITCODE
        Log "  exit code $rc"
        if ($rc -eq 0) { Say '  Done.' 'Green'; $installed++ } else { Say "  code exited with $rc." 'Yellow'; $failed++ }
        continue
    }

    foreach ($n in @($a.notes)) { if ($n) { Say ("  " + $n) } }
    $base = @('install', '--id', $a.winget_id, '--exact', '--source', 'winget')
    if ($a.scope) { $base += @('--scope', $a.scope) }
    $agree = @('--accept-package-agreements', '--accept-source-agreements')
    Say ('  Command: winget ' + (($base + $agree) -join ' '))
    if ($a.scope -eq 'machine' -and -not $isAdmin) {
        Say '  This is a machine-wide installer: Windows will show an administrator (UAC) prompt. Answer Yes there, or the install fails.'
    } elseif ($a.scope -eq 'user') {
        Say '  User scope: installs for your Windows account only, no administrator needed.'
    } else {
        Say '  No --scope here, as in the vendor''s own command: winget picks the installer from the manifest (an administrator prompt may appear).'
    }
    Say '  The two --accept-... flags accept this package''s license and the winget source terms on your behalf;'
    Say '  they are added only because you answer y below. Without them winget would ask you itself.'
    $q = "  Install $($a.name)?"
    if ($a.winget_label) { $q = "  Install $($a.name) $($a.winget_label)?" }
    if (-not (Ask $q)) { Say '  Skipped.'; $skipped++; continue }
    if ($DryRun) { Say '  DRY RUN: not run.'; continue }
    & winget @($base + $agree)
    $rc = $LASTEXITCODE
    Log "  exit code $rc"
    if ($rc -eq 0) { Say '  Done.' 'Green'; $installed++ } else { Say "  winget exited with $rc. See the lines above; docs\09-troubleshooting.md may help." 'Yellow'; $failed++ }
    Update-SessionPath
}

# ------------------------------------------------------------------ 4. summary
Say ''
if ($DryRun) {
    Say 'DRY RUN finished: no winget install and no code --install-extension was run.' 'Green'
} else {
    Say ("Finished: {0} installed, {1} skipped, {2} failed." -f $installed, $skipped, $failed)
    Say 'Close this window, open a NEW PowerShell window (so it sees the new programs), then run:'
    Say '  powershell -ExecutionPolicy Bypass -File install\check.ps1'
}
Log '======== install\windows.ps1 finished'
if ($failed -gt 0) { exit 1 }
exit 0
