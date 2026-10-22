#!/usr/bin/env bash
# install/linux.sh - installs the Maker Mastery prerequisites on Ubuntu, asking y/N for each app.
#
#   bash install/linux.sh --dry-run    print every command and ask the same questions, install nothing
#   bash install/linux.sh              install the apps you answer y to
#
# UNTESTED: written for Ubuntu 24.04 and checked with "bash -n" only; it was NOT run on Linux.
# The project's own setup (tools\setup.ps1, hooks) is tested on Windows 11 only; Linux support is planned for v1.1.
#
# What it automates (each only after your y):
#   - apt-get install of packages from Ubuntu's own archive: git, python3.12, python3.12-venv (uses sudo);
#   - Claude Code with Anthropic's official installer: curl -fsSL https://claude.ai/install.sh | bash (no sudo);
#   - the Claude Code VS Code extension: code --install-extension anthropic.claude-code.
# What it only PRINTS (vendor repositories and AppImages you add yourself, following the vendor's page):
#   VS Code, Bambu Studio, Claude Desktop, GitHub CLI, OrcaSlicer, Blender. GitHub Desktop has no official Linux build.
# Apps that are already installed are skipped. Log: install/install.log.

set -u
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
        *) echo "Unknown option: $arg (use --dry-run or --help)"; exit 2 ;;
    esac
done

# shellcheck source=lib.sh
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"

mm_log "======== install/linux.sh started (dry run: $DRY_RUN)"
if [ "$DRY_RUN" = 1 ]; then mm_say "Maker Mastery prerequisites for Ubuntu - mode: DRY RUN (nothing will be installed)"
else mm_say "Maker Mastery prerequisites for Ubuntu - mode: INSTALL"; fi
mm_say "UNTESTED script: read each command before you answer y."
mm_say "No AI ever starts, sends, uploads or queues a print. This script only installs the apps you say y to."
mm_say ""

if [ "$(uname -s)" != "Linux" ]; then
    mm_say "This is not Linux ($(uname -s)). Use install/macos.sh on macOS, or install/windows.ps1 on Windows."
    exit 1
fi
if ! command -v apt-get >/dev/null 2>&1; then
    mm_say "apt-get was not found. This script is for Ubuntu (and other apt-based systems); see docs/02-install.md."
    exit 1
fi
if [ "$(id -u)" = "0" ]; then
    mm_say "Run this as your normal user, not with sudo: it asks for sudo itself only for apt-get,"
    mm_say "and the Claude Code installer must run as your own user."
    exit 1
fi
if [ -r /etc/os-release ]; then mm_say "System: $(. /etc/os-release; printf '%s' "${PRETTY_NAME:-unknown}")"; fi
mm_say ""

# ------------------------------------------------------------------ plan
mm_say "Checking what is already installed (read-only)..."
TODO=""
while IFS='|' read -r key name req check bkind bname lmode lval src <&3; do
    [ -n "$key" ] || continue
    kind="optional"; [ "$req" = 1 ] && kind="required"
    res="$(mm_check "$check")"
    if [ "${res%%"$MM_TAB"*}" = "OK" ]; then
        mm_say "  [installed] $name ($kind) ${res#*"$MM_TAB"}"; continue
    fi
    if [ "$lmode" = "apt" ]; then
        # Skip only when dpkg lists EVERY package of the app (python3.12 without python3.12-venv is not enough),
        # and never for a venv check, which mm_check above has already failed.
        allpk=1
        for p in $lval; do dpkg -s "$p" >/dev/null 2>&1 || allpk=0; done
        if [ "$allpk" = 1 ] && [ "${check%%:*}" != "venv" ]; then
            mm_say "  [installed] $name ($kind) dpkg lists $lval"; continue
        fi
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
INSTALLED=0; SKIPPED=0; FAILED=0; APT_UPDATED=0
while IFS='|' read -r key name req check bkind bname lmode lval src <&3; do
    [ -n "$key" ] || continue
    kind="optional"; [ "$req" = 1 ] && kind="required"
    mm_say ""
    mm_say "== $name ($kind)"
    case "$lmode" in
        apt)
            for p in $lval; do
                if ! apt-cache show "$p" >/dev/null 2>&1; then
                    mm_say "  Package $p is not in this system's apt sources. Ubuntu 24.04 (noble) has it; see docs/02-install.md."
                fi
            done
            mm_say "  Command: sudo apt-get update   (once, before the first apt install)"
            mm_say "  Command: sudo apt-get install $lval"
            mm_say "  Source: https://launchpad.net/ubuntu/noble/+package/${lval%% *}"
            if ! mm_ask "  Install $name?"; then mm_say "  Skipped."; SKIPPED=$((SKIPPED+1)); continue; fi
            if [ "$DRY_RUN" = 1 ]; then mm_say "  DRY RUN: not run."; continue; fi
            if [ "$APT_UPDATED" = 0 ]; then sudo apt-get update && APT_UPDATED=1; fi
            # shellcheck disable=SC2086
            if sudo apt-get install $lval; then mm_say "  Done."; INSTALLED=$((INSTALLED+1))
            else mm_say "  apt-get failed (see above)."; FAILED=$((FAILED+1)); fi ;;
        script)
            mm_say "  Command: curl -fsSL $lval | bash"
            mm_say "  This downloads and runs Anthropic's official installer as your user (source: $src)."
            if ! command -v curl >/dev/null 2>&1; then mm_say "  curl is missing: install it first with: sudo apt-get install curl"; fi
            if [ "$key" = "claude-code" ]; then mm_say "  Optional: the Claude Code extension for VS Code works on its own. This is Anthropic's recommended native installer; it updates itself."; fi
            if ! mm_ask "  Install $name?"; then mm_say "  Skipped."; SKIPPED=$((SKIPPED+1)); continue; fi
            if [ "$DRY_RUN" = 1 ]; then mm_say "  DRY RUN: not run."; continue; fi
            if curl -fsSL "$lval" | bash; then mm_say "  Done. Open a new terminal, then run: claude --version"; INSTALLED=$((INSTALLED+1))
            else mm_say "  The installer failed (see above and $src)."; FAILED=$((FAILED+1)); fi ;;
        ext)
            mm_say "  Command: code --install-extension $lval"
            if ! mm_ask "  Install $name?"; then mm_say "  Skipped."; SKIPPED=$((SKIPPED+1)); continue; fi
            if [ "$DRY_RUN" = 1 ]; then mm_say "  DRY RUN: not run."; continue; fi
            if ! command -v code >/dev/null 2>&1; then
                mm_say "  'code' is not on PATH. Install VS Code first (docs/02-install.md), then run this script again."
                FAILED=$((FAILED+1)); continue
            fi
            if code --install-extension "$lval"; then mm_say "  Done."; INSTALLED=$((INSTALLED+1))
            else mm_say "  code failed (see above)."; FAILED=$((FAILED+1)); fi ;;
        manual)
            mm_say "  Not automated: follow the vendor's official Linux steps here:"
            mm_say "    $lval"
            mm_say "  docs/02-install.md repeats those steps with the source of each command."
            SKIPPED=$((SKIPPED+1)) ;;
        *)
            mm_say "  No official Linux build; see docs/02-install.md."
            SKIPPED=$((SKIPPED+1)) ;;
    esac
done 3<<EOF
$TODO
EOF

mm_say ""
if [ "$DRY_RUN" = 1 ]; then
    mm_say "DRY RUN finished: no apt-get, installer or code --install-extension was run."
else
    mm_say "Finished: $INSTALLED installed, $SKIPPED skipped or manual, $FAILED failed."
    mm_say "Open a new terminal, then run: bash install/check.sh"
fi
mm_log "======== install/linux.sh finished"
[ "$FAILED" = 0 ]
