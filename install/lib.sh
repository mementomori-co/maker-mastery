# Shared list and helpers for install/macos.sh, install/linux.sh and install/check.sh (sourced, not run).
# Written for bash 3.2 (the bash that ships with macOS) and newer. Everything here only reads.
#
# One line per app, fields separated by "|":
#   key | name | required (1/0) | check | brew kind | brew name | linux mode | linux value | source URL
# check:      cmd:<command and args>  |  bin:<command name, only looked up>  |  app:<macOS .app path>
#             |  ext:<VS Code extension id>  |  cfg:<config key whose path must exist>
#             |  venv:<python command>  (passes only if that Python runs 'import ensurepip, venv', so it can
#                create the project's .venv; prints its --version)
#             several checks may be joined with ";" and the first that passes wins.
# brew kind:  formula | cask | ext (VS Code extension) | - (none)
# linux mode: apt (Ubuntu archive packages, installed with apt-get after your y) | script (the URL of the vendor's
#             official installer script, run as "curl -fsSL <url> | bash" after your y)
#             | ext (VS Code extension) | manual (the script prints the vendor's official steps; you run them) | - (none)
# The ids were checked on https://formulae.brew.sh and on Launchpad (Ubuntu 24.04 "noble"); see docs/02-install.md.
# The Claude Code command line is optional (required = 0): the VS Code extension bundles its own copy for the panel
# and works on its own. Anthropic recommends its native installer, which updates itself; Homebrew installs do not
# (https://code.claude.com/docs/en/setup). mm_cli_note prints that advice.

mm_cli_note() {
    mm_say "  Optional: the Claude Code extension for VS Code works on its own; you only need this for 'claude' in a terminal."
    mm_say "  Recommended route: Anthropic's native installer, which updates itself in the background:"
    mm_say "      curl -fsSL https://claude.ai/install.sh | bash"
    mm_say "    Source: https://code.claude.com/docs/en/setup (\"Native Install (Recommended)\")."
}

MM_APPS='git|Git|1|cmd:git --version|formula|git|apt|git|https://formulae.brew.sh/formula/git
vscode|Visual Studio Code|1|cmd:code --version;app:/Applications/Visual Studio Code.app|cask|visual-studio-code|manual|https://code.visualstudio.com/docs/setup/linux|https://formulae.brew.sh/cask/visual-studio-code
python|Python 3.12 (with venv)|1|venv:python3.12|formula|python@3.12|apt|python3.12 python3.12-venv|https://formulae.brew.sh/formula/python@3.12
claude-code|Claude Code command line|0|cmd:claude --version|cask|claude-code|script|https://claude.ai/install.sh|https://code.claude.com/docs/en/setup
claude-code-vscode|Claude Code extension for VS Code|1|ext:anthropic.claude-code|ext|anthropic.claude-code|ext|anthropic.claude-code|https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code
bambu-studio|Bambu Studio|1|cfg:bambu_studio_exe;app:/Applications/BambuStudio.app|cask|bambu-studio|manual|https://github.com/bambulab/BambuStudio/releases/latest|https://formulae.brew.sh/cask/bambu-studio
claude-desktop|Claude Desktop|0|app:/Applications/Claude.app;bin:claude-desktop|cask|claude|manual|https://support.claude.com/en/articles/10065433-installing-claude-desktop|https://formulae.brew.sh/cask/claude
github-desktop|GitHub Desktop|0|app:/Applications/GitHub Desktop.app|cask|github|-|-|https://formulae.brew.sh/cask/github
github-cli|GitHub CLI|0|cmd:gh --version|formula|gh|manual|https://github.com/cli/cli/blob/trunk/docs/install_linux.md|https://formulae.brew.sh/formula/gh
orcaslicer|OrcaSlicer|0|app:/Applications/OrcaSlicer.app|cask|orcaslicer|manual|https://github.com/OrcaSlicer/OrcaSlicer/releases/latest|https://formulae.brew.sh/cask/orcaslicer
blender|Blender|0|cfg:blender_exe;cmd:blender --version;app:/Applications/Blender.app|cask|blender|manual|https://www.blender.org/download/|https://formulae.brew.sh/cask/blender'

MM_INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MM_REPO_ROOT="$(dirname "$MM_INSTALL_DIR")"
MM_LOG="$MM_INSTALL_DIR/install.log"
MM_TAB="$(printf '\t')"

mm_log() {
    printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$MM_LOG" 2>/dev/null || true
}
mm_say() {
    printf '%s\n' "$*"
    mm_log "$*"
}

# Y/N question; works with typed or piped answers. Returns 0 for y/yes.
mm_ask() {
    local ans=""
    printf '%s [y/N] ' "$1"
    IFS= read -r ans || ans=""
    if [ ! -t 0 ]; then printf '%s\n' "$ans"; fi
    case "$ans" in
        y|Y|yes|YES|Yes) mm_log "Q: $1 -> '$ans' -> YES"; return 0 ;;
        *) mm_log "Q: $1 -> '$ans' -> NO"; return 1 ;;
    esac
}

# Value of a key in config/paths.yaml ("key: value" lines), or empty.
mm_config_value() {
    local cfg="$MM_REPO_ROOT/config/paths.yaml"
    [ -f "$cfg" ] || return 0
    sed -n "s/^[[:space:]]*$1[[:space:]]*:[[:space:]]*[\"']\{0,1\}\([^\"'#]*\).*/\1/p" "$cfg" | head -n 1 | sed 's/[[:space:]]*$//'
}

# Runs the checks of one app. Prints "OK<TAB>version-or-detail" or "NO<TAB>reason"; always returns 0.
mm_check() {
    local checks="$1" rest one kind val out first reason=""
    rest="$checks"
    while [ -n "$rest" ]; do
        one="${rest%%;*}"
        if [ "$one" = "$rest" ]; then rest=""; else rest="${rest#*;}"; fi
        kind="${one%%:*}"
        val="${one#*:}"
        case "$kind" in
            cmd)
                if command -v "${val%% *}" >/dev/null 2>&1; then
                    out="$($val 2>&1)" && { first="$(printf '%s\n' "$out" | sed -n '/[^[:space:]]/{p;q;}')"; printf 'OK\t%s\n' "$first"; return 0; }
                    reason="'${val%% *}' exited with an error"
                else
                    reason="'${val%% *}' not found on PATH"
                fi ;;
            venv)
                # Ubuntu/Debian ship ensurepip in the separate pythonX.Y-venv package (Debian's python3.11-venv
                # file list: https://packages.debian.org/bookworm/amd64/python3.11-venv/filelist), so a bare
                # "python3.12 --version" can pass while "python3.12 -m venv" fails.
                if command -v "$val" >/dev/null 2>&1; then
                    if "$val" -c "import ensurepip, venv" >/dev/null 2>&1; then
                        printf 'OK\t%s\n' "$("$val" --version 2>&1)"; return 0
                    fi
                    reason="'$val' runs but cannot import ensurepip and venv (on Ubuntu: sudo apt-get install ${val}-venv)"
                else
                    reason="'$val' not found on PATH"
                fi ;;
            bin)
                if command -v "$val" >/dev/null 2>&1; then printf 'OK\t%s\n' "$(command -v "$val")"; return 0; fi
                [ -n "$reason" ] || reason="'$val' not found on PATH" ;;
            app)
                [ "$(uname -s)" = "Darwin" ] || continue
                if [ -d "$val" ]; then
                    first="$(defaults read "$val/Contents/Info" CFBundleShortVersionString 2>/dev/null || true)"
                    printf 'OK\t%s %s\n' "$first" "$val"; return 0
                fi
                reason="not found at $val" ;;
            ext)
                if command -v code >/dev/null 2>&1; then
                    first="$(code --list-extensions --show-versions 2>/dev/null | grep -i "^$val@" | head -n 1)"
                    if [ -n "$first" ]; then printf 'OK\t%s\n' "${first#*@}"; return 0; fi
                    reason="$val is not in 'code --list-extensions'"
                else
                    reason="'code' not on PATH, so the extension list cannot be read"
                fi ;;
            cfg)
                first="$(mm_config_value "$val")"
                if [ -n "$first" ] && [ -e "$first" ]; then printf 'OK\t%s\n' "$first"; return 0; fi
                if [ -n "$first" ]; then reason="$val in config/paths.yaml points to a missing file: $first"
                else reason="not found ($val is not set in config/paths.yaml)"; fi ;;
        esac
    done
    printf 'NO\t%s\n' "${reason:-not found}"
}
