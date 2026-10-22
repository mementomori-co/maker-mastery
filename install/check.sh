#!/usr/bin/env bash
# install/check.sh - prints a PASS/FAIL table of every prerequisite (macOS or Linux), with its version. Changes nothing.
#
#   bash install/check.sh
#
# Required apps print PASS or FAIL; optional apps print PASS or "--" and never make the result FAIL. The Claude Code
# command line is optional: the VS Code extension works on its own. The last line is "RESULT: PASS" when every
# required app passed, otherwise "RESULT: FAIL"; the exit code is 0 or 1.
# Python passes only if python3.12 can "import ensurepip, venv", so it can create the project's .venv (on Ubuntu that
# needs the python3.12-venv package).
# On Linux, Bambu Studio is an AppImage with no fixed place: set bambu_studio_exe in config/paths.yaml to its path.
# Status: checked with "bash -n" and run in Git Bash on Windows 11, where it reports FAIL for Python 3.12 and Bambu
# Studio as expected (this script is for macOS and Linux); NOT run on macOS or Linux.

set -u
# shellcheck source=lib.sh
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"

echo "Maker Mastery prerequisite check (read-only) - $(uname -s) $(uname -m)"
echo ""
printf '%-6s %-35s %-9s %s\n' "Status" "App" "Kind" "Version / detail"
printf '%-6s %-35s %-9s %s\n' "------" "---" "----" "----------------"
FAILED=0
while IFS='|' read -r key name req check bkind bname lmode lval src <&3; do
    [ -n "$key" ] || continue
    kind="optional"; [ "$req" = 1 ] && kind="required"
    res="$(mm_check "$check")"
    if [ "${res%%"$MM_TAB"*}" = "OK" ]; then status="PASS"
    elif [ "$req" = 1 ]; then status="FAIL"; FAILED=$((FAILED+1))
    else status="--"; fi
    printf '%-6s %-35s %-9s %s\n' "$status" "$name" "$kind" "${res#*"$MM_TAB"}"
done 3<<EOF
$MM_APPS
EOF
echo ""
if [ "$FAILED" = 0 ]; then
    echo "RESULT: PASS - every required prerequisite was found."
    exit 0
fi
echo "RESULT: FAIL - $FAILED required prerequisite(s) missing. See docs/02-install.md."
exit 1
