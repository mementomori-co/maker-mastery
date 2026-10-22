<#
.SYNOPSIS
  One-time setup for the Maker Mastery tools: a private Python environment, your config file, and a self-test.

.DESCRIPTION
  What it does, in order (it prints each step before doing it):
    1. Finds Python 3.12 or newer ("py -3.12", then "python"). If there is none, it prints the download link and stops.
    2. Creates .venv inside this repository and installs requirements.txt into it. Nothing is installed globally.
       It asks Y/N before installing unless you pass -Yes.
    3. Copies config\paths.example.yaml to config\paths.yaml if you do not have one yet (never overwrites yours).
    4. Looks for Bambu Studio at the path in config\paths.yaml (default: the standard install folder) and tells you
       what to set if it is not there. It only reads; it never starts Bambu Studio.
    5. Runs tools\selftest.py. If you answered N in step 2 it skips the self-test, says "Setup paused" and exits 0.
  It changes nothing outside the repository folder. It never prints, slices or sends anything to a printer.

.PARAMETER Yes
  Answer yes to the install question (for a second run, or when you have read what it installs).

.PARAMETER Optional
  Also install requirements-optional.txt (open3d, used only by tools\render_critic.py).

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File tools\setup.ps1
.EXAMPLE
  pwsh -File tools\setup.ps1 -Yes
#>
[CmdletBinding()]
param(
    [switch]$Yes,
    [switch]$Optional
)

$ErrorActionPreference = 'Stop'
$Repo = Split-Path -Parent $PSScriptRoot
$Venv = Join-Path $Repo '.venv'
$VenvPy = Join-Path $Venv 'Scripts\python.exe'

function Step([string]$Text) { Write-Host ''; Write-Host "==> $Text" -ForegroundColor Cyan }
function Info([string]$Text) { Write-Host "    $Text" }
function Ask([string]$Question) {
    if ($Yes) { return $true }
    $a = Read-Host "    $Question [y/N]"
    return ($a -match '^(y|yes)$')
}

Write-Host "Maker Mastery setup - repository: $Repo"
Write-Host "Nothing outside this folder is changed. No AI ever starts, sends, uploads or queues a print."

# ---------------------------------------------------------------- 1. Python 3.12+
Step 'Step 1 of 5: looking for Python 3.12 or newer'
$PyCmd = $null
$PyArgs = @()
$candidates = @(
    @{ Exe = 'py'; Pre = @('-3.12') },
    @{ Exe = 'py'; Pre = @('-3') },
    @{ Exe = 'python'; Pre = @() }
)
foreach ($c in $candidates) {
    $exe = $c.Exe; $pre = @($c.Pre)
    if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
    try {
        $ver = & $exe @pre -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null
    } catch { continue }
    if ($LASTEXITCODE -ne 0 -or -not $ver) { continue }
    $parts = "$ver".Trim().Split('.')
    if ([int]$parts[0] -gt 3 -or ([int]$parts[0] -eq 3 -and [int]$parts[1] -ge 12)) {
        $PyCmd = $exe; $PyArgs = $pre
        Info "Found Python $ver with: $exe $($pre -join ' ')"
        break
    }
}
if (-not $PyCmd -and -not (Test-Path $VenvPy)) {
    Write-Host ''
    Write-Host 'Python 3.12 or newer was not found.' -ForegroundColor Yellow
    Write-Host 'Download it from https://www.python.org/downloads/windows/ , install it, then run this script again.'
    Write-Host '(The "py" launcher that comes with the python.org installer is what this script looks for first.)'
    exit 1
}

# ---------------------------------------------------------------- 2. .venv + requirements
Step 'Step 2 of 5: private Python environment (.venv in this repository)'
if (Test-Path $VenvPy) {
    Info ".venv already exists: $Venv"
} else {
    Info "Creating $Venv"
    & $PyCmd @PyArgs -m venv $Venv
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VenvPy)) { Write-Host 'Could not create .venv.' -ForegroundColor Red; exit 1 }
}
$req = Join-Path $Repo 'requirements.txt'
Info 'These packages will be installed into .venv only (from requirements.txt):'
Get-Content $req | Where-Object { $_ -match '^\s*[A-Za-z]' } | ForEach-Object { Info ("  " + ($_ -replace '\s+#.*$', '')) }
if ($Optional) { Info 'Also the optional extras from requirements-optional.txt: open3d' }
$Installed = $false
if (Ask 'Install them now?') {
    $Installed = $true
    & $VenvPy -m pip install --disable-pip-version-check -r $req
    if ($LASTEXITCODE -ne 0) { Write-Host 'pip install failed (see the lines above).' -ForegroundColor Red; exit 1 }
    if ($Optional) {
        & $VenvPy -m pip install --disable-pip-version-check -r (Join-Path $Repo 'requirements-optional.txt')
        if ($LASTEXITCODE -ne 0) { Write-Host 'Optional install failed; the main tools still work.' -ForegroundColor Yellow }
    }
} else {
    Info 'Skipped. The tools need these packages; run this script again and answer y when you are ready.'
}

# ---------------------------------------------------------------- 3. config\paths.yaml
Step 'Step 3 of 5: your config file'
$cfg = Join-Path $Repo 'config\paths.yaml'
$example = Join-Path $Repo 'config\paths.example.yaml'
if (Test-Path $cfg) {
    Info "config\paths.yaml already exists; left as it is."
} else {
    Copy-Item -LiteralPath $example -Destination $cfg
    Info 'Copied config\paths.example.yaml to config\paths.yaml. Edit that copy if your paths differ.'
}
& $VenvPy -B (Join-Path $Repo 'tools\mm_config.py') | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host '    config\paths.yaml cannot be read (the message above says which line). Use forward slashes or single quotes' -ForegroundColor Yellow
    Write-Host '    for Windows paths, never backslashes inside double quotes. See docs\09-troubleshooting.md, section 6.' -ForegroundColor Yellow
}

# ---------------------------------------------------------------- 4. Bambu Studio
Step 'Step 4 of 5: looking for Bambu Studio (read-only check)'
$bambu = 'C:\Program Files\Bambu Studio\bambu-studio.exe'
$line = Select-String -LiteralPath $cfg -Pattern '^\s*bambu_studio_exe\s*:\s*["'']?([^"''#]*)["'']?' -ErrorAction SilentlyContinue | Select-Object -First 1
if ($line) { $v = $line.Matches[0].Groups[1].Value.Trim(); if ($v) { $bambu = $v -replace '/', '\' } }
if (Test-Path -LiteralPath $bambu) {
    Info "Found: $bambu"
} else {
    Write-Host "    Bambu Studio was not found at: $bambu" -ForegroundColor Yellow
    Info 'If it is installed somewhere else, set bambu_studio_exe in config\paths.yaml to the full path of bambu-studio.exe.'
    Info 'Only slicing (tools\slice_cli.py) and the profile checks need it; the other tools work without it.'
}

# ---------------------------------------------------------------- 5. self-test
Step 'Step 5 of 5: self-test (no printer, no Bambu Studio, no internet needed)'
if (-not $Installed) {
    Info 'Packages not installed yet (you answered N), so the self-test is not run now.'
    Write-Host ''
    Write-Host 'Setup paused: run tools\setup.ps1 again and answer y when ready.' -ForegroundColor Yellow
    exit 0
}
& $VenvPy -B (Join-Path $Repo 'tools\selftest.py')
$rc = $LASTEXITCODE
Write-Host ''
if ($rc -eq 0) {
    Write-Host 'Setup finished. Open this folder in VS Code and start Claude Code there.' -ForegroundColor Green
} else {
    Write-Host 'Setup finished, but the self-test reported a failure (see above).' -ForegroundColor Yellow
}
exit $rc
