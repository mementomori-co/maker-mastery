#!/usr/bin/env bash
# install/macos.sh - installs the Maker Mastery prerequisites on macOS with Homebrew, asking y/N for each app.
#
#   bash install/macos.sh --dry-run    print every command and ask the same questions, install nothing
#   bash install/macos.sh              install the apps you answer y to
#
# - The app list and the checked Homebrew names are in install/lib.sh (sources: https://formulae.brew.sh).
# - If Homebrew is missing, it prints Homebrew's official install command and stops. It never installs Homebrew.
# - Apps that are already installed are skipped (checked by command, by /Applications, or by "brew list").
# - Nothing installs silently: each "brew install" runs only after your y. Log: install/install.log.
# - Status: written for macOS and checked with "bash -n" only; it was NOT run on a Mac (see docs/02-install.md).
#   The project's own setup (tools\setup.ps1, hooks) is tested on Windows 11 only; macOS support is planned for v1.1.

set -u
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
        *) echo "Unknown option: $arg (use --dry-run or --help)"; exit 2 ;;
    esac
done

# shellcheck source=lib.sh
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"

mm_log "======== install/macos.sh started (dry run: $DRY_RUN)"
if [ "$DRY_RUN" = 1 ]; then mm_say "Maker Mastery prerequisites for macOS - mode: DRY RUN (nothing will be installed)"
else mm_say "Maker Mastery prerequisites for macOS - mode: INSTALL"; fi
mm_say "No AI ever starts, sends, uploads or queues a print. This script only installs the apps you say y to."
mm_say ""

if [ "$(uname -s)" != "Darwin" ]; then
    mm_say "This is not macOS ($(uname -s)). Use install/linux.sh on Ubuntu, or install/windows.ps1 on Windows."
    exit 1
fi
if [ "$(id -u)" = "0" ]; then
    mm_say "Do not run this with sudo or as root. Homebrew installs as your normal user. Run it again without sudo."
    exit 1
fi

ARCH="$(uname -m)"
if [ "$ARCH" = "x86_64" ]; then
    mm_say "This Mac reports an Intel (x86_64) processor."
    mm_say "  Homebrew lists Intel macOS as Tier 3 (not supported) and has stopped building Intel bottles:"
    mm_say "  https://docs.brew.sh/Support-Tiers . Formulae such as git, python@3.12 and gh may build from source."
    mm_say "  The direct downloads in docs/02-install.md are the safer route on an Intel Mac."
    mm_say "  The Homebrew blender cask installs Blender 4.5 on Intel Macs (5.x has no Intel build); not tested here."
    mm_say ""
fi

if ! command -v brew >/dev/null 2>&1; then
    mm_say "Homebrew (brew) was not found. This script does not install it for you."
    mm_say "Homebrew's official install command, from https://brew.sh/ :"
    mm_say ""
    mm_say '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    mm_say ""
    mm_say "Read https://docs.brew.sh/Installation first, run that command yourself in Terminal, follow the"
    mm_say "directions it prints for your shell's config file, open a new Terminal window, then run this script again."
    mm_say "Or use the direct downloads in docs/02-install.md."
    exit 1
fi
mm_say "Homebrew found: $(command -v brew)"
mm_say ""

# ------------------------------------------------------------------ plan
mm_say "Checking what is already installed (read-only)..."
TODO=""
while IFS='|' read -r key name req check bkind bname lmode lval src <&3; do
    [ -n "$key" ] || continue
    kind="optional"; [ "$req" = 1 ] && kind="required"
    res="$(mm_check "$check")"
    if [ "${res%%"$MM_TAB"*}" = "OK" ]; then
        mm_say "  [installed] $name ($kind) ${res#*"$MM_TAB"}"
        continue
    fi
    if [ "$bkind" = "formula" ] && brew list --formula "$bname" >/dev/null 2>&1; then
        mm_say "  [installed] $name ($kind) brew lists formula $bname (open a new Terminal if the command is not found)"; continue
    fi
    if [ "$bkind" = "cask" ] && brew list --cask "$bname" >/dev/null 2>&1; then
        mm_say "  [installed] $name ($kind) brew lists cask $bname"; continue
    fi
    mm_say "  [missing]   $name ($kind): ${res#*"$MM_TAB"}"
    TODO="$TODO$key|$name|$req|$check|$bkind|$bname|$lmode|$lval|$src
"
done 3<<EOF
$MM_APPS
EOF

if [ -z "$TODO" ]; then
    mm_say ""
    mm_say "Everything in the list is already installed. Nothing to do. Run: bash install/check.sh"
    exit 0
fi

# ------------------------------------------------------------------ one app at a time
INSTALLED=0; SKIPPED=0; FAILED=0
while IFS='|' read -r key name req check bkind bname lmode lval src <&3; do
    [ -n "$key" ] || continue
    kind="optional"; [ "$req" = 1 ] && kind="required"
    mm_say ""
    mm_say "== $name ($kind)"
    case "$bkind" in
        formula) cmd="brew install $bname" ;;
        cask)    cmd="brew install --cask $bname" ;;
        ext)     cmd="code --install-extension $bname" ;;
        *)       mm_say "  No Homebrew package for this app; see docs/02-install.md."; SKIPPED=$((SKIPPED+1)); continue ;;
    esac
    question="  Install $name?"
    if [ "$key" = "claude-code" ]; then
        mm_cli_note
        mm_say "    This script does not run it for you. The Homebrew cask below works, but Homebrew installations"
        mm_say "    do not auto-update (same page): run 'brew upgrade claude-code' from time to time."
        question="  Install $name with Homebrew (does not auto-update)?"
    fi
    mm_say "  Command: $cmd"
    mm_say "  Name checked at: $src"
    if ! mm_ask "$question"; then mm_say "  Skipped."; SKIPPED=$((SKIPPED+1)); continue; fi
    if [ "$DRY_RUN" = 1 ]; then mm_say "  DRY RUN: not run."; continue; fi
    if [ "$bkind" = "ext" ] && ! command -v code >/dev/null 2>&1; then
        mm_say "  'code' is not on PATH yet. Open a new Terminal window after VS Code is installed and run this script again."
        FAILED=$((FAILED+1)); continue
    fi
    if $cmd; then mm_say "  Done."; INSTALLED=$((INSTALLED+1))
    else mm_say "  The command failed (see above)."; FAILED=$((FAILED+1)); fi
done 3<<EOF
$TODO
EOF

mm_say ""
if [ "$DRY_RUN" = 1 ]; then
    mm_say "DRY RUN finished: no brew install and no code --install-extension was run."
else
    mm_say "Finished: $INSTALLED installed, $SKIPPED skipped, $FAILED failed."
    mm_say "Open a new Terminal window, then run: bash install/check.sh"
fi
mm_log "======== install/macos.sh finished"
[ "$FAILED" = 0 ]
