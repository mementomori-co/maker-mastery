<#
.SYNOPSIS
  Prints a PASS/FAIL table of every prerequisite in install\apps.json, with its version. Changes nothing.

.DESCRIPTION
  For each app it runs a read-only check: a "--version" command, a file path (Bambu Studio, Blender, read from
  config\paths.yaml when you set one there), "code --list-extensions" for the VS Code extension, or "winget list --id".
  Required apps print PASS or FAIL. Optional apps print PASS or "--" (optional, not installed); a missing optional
  app never makes the result FAIL. The Claude Code command line is optional: the VS Code extension works on its own.
  The last line is "RESULT: PASS" when every required app passed, otherwise "RESULT: FAIL"; the exit code is 0 or 1.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File install\check.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

$apps = Get-AppList
$rows = @()
$failed = 0
foreach ($a in $apps) {
    $r = Test-App $a
    if ($r.Ok) { $status = 'PASS' }
    elseif ($a.required) { $status = 'FAIL'; $failed++ }
    else { $status = '--' }
    $kind = 'optional'
    if ($a.required) { $kind = 'required' }
    $rows += [pscustomobject]@{ Status = $status; App = $a.name; Kind = $kind; Version = $r.Version; Detail = $r.Note }
}

Write-Host 'Maker Mastery prerequisite check (read-only)'
Write-Host ("PowerShell " +$PSVersionTable.PSVersion.ToString() + "; winget found: " + (Test-WingetPresent))
Write-Host ''
$rows | Format-Table -AutoSize -Wrap | Out-String -Width 220 | Write-Host
$cli = @($apps | Where-Object { $_.key -eq 'claude-code' }) | Select-Object -First 1
$cliRow = @($rows | Where-Object { $cli -and $_.App -eq $cli.name }) | Select-Object -First 1
if ($cliRow -and $cliRow.Status -eq '--') {
    Write-Host 'Note: the Claude Code command line is optional; the VS Code extension works on its own. If you want it,'
    Write-Host '  Anthropic recommends its native installer (it updates itself): see docs\02-install.md, section 4.'
    Write-Host ''
}
if ($failed -eq 0) {
    Write-Host 'RESULT: PASS - every required prerequisite was found.' -ForegroundColor Green
    exit 0
}
Write-Host "RESULT: FAIL - $failed required prerequisite(s) missing. See docs\02-install.md, or run install\windows.ps1." -ForegroundColor Yellow
exit 1
