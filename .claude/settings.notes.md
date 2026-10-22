# Notes on `.claude\settings.json`

JSON cannot carry comments: Claude Code reads settings files as strict JSON, so a `//` comment is a syntax error
(https://code.claude.com/docs/en/settings, "Edit a settings file"). This file explains every entry instead.
The old docs.anthropic.com URLs (https://docs.anthropic.com/en/docs/claude-code/settings and
https://docs.anthropic.com/en/docs/claude-code/hooks) redirect to the code.claude.com pages cited here (checked when this file was written).

## What the file holds
Only two keys: `permissions` and `hooks`. No MCP servers (see `.mcp.json.example`), no model, no environment
variables, no machine names and no absolute paths. Your personal overrides go in `.claude\settings.local.json`,
which Claude Code keeps out of git (https://code.claude.com/docs/en/settings, "Keep personal settings out of a repository").

## Deny rules: no AI ever starts, sends, uploads or queues a print
| Rule | Blocks |
|---|---|
| `mcp__*__*print*` | any MCP tool, on any server, whose name contains `print` (for example `print_3mf`, `start_print_job`) |
| `mcp__*__*upload_gcode*`, `mcp__*__*send_gcode*` | G-code upload or send tools on any server |
| `mcp__*__*queue*` | any MCP tool that queues a job |
| `mcp__*bambu*__*upload*`, `mcp__*bambu*__*start*` | upload and start tools on any server whose name contains `bambu` |
| `mcp__*printer*__*upload*`, `mcp__*printer*__*start*` | the same on any server whose name contains `printer` |
| `Read(./.env)`, `Read(./.env.*)` | Claude reading a local secrets file (pattern from the settings docs example) |

Why this syntax is valid:
- Deny and ask rules may use a glob where the tool name goes, and the glob has to match the whole tool name
  (paraphrased from https://code.claude.com/docs/en/permissions, "Tool name wildcards"). The same section says glob allow rules need a
  literal `mcp__<server>__` prefix, which is why these globs are deny rules only.
- Deny is checked first: "Rules are evaluated in order: deny, then ask, then allow" (same page), and a deny in any
  scope beats an allow in any other scope. A PreToolUse hook that returns "allow" does not bypass a deny rule (same page).
- Deny rules in a committed `.claude\settings.json` apply right away; only `allow` rules wait for workspace trust
  (https://code.claude.com/docs/en/settings, "A committed key doesn't reach teammates").
- Claude Code skips any `mcp__` rule written with parentheses (https://code.claude.com/docs/en/permissions), so none is used here.

Side effects you should know about:
- `*print*` also blocks harmless tools whose names contain "print" (a "fingerprint" or "blueprint" tool). That is the
  intended trade: a false block costs one manual step, a false allow could start a printer.
- These rules are a second line of defence. The first is that this project ships no MCP server that can talk to a printer.
  If you install one, keep its print, upload and start tools denied, and add its exact tool names to the deny list as well.

## Hooks
All four hooks use exec form: `command` is the project's Python and `args` holds the script path. Claude Code
substitutes `${CLAUDE_PROJECT_DIR}` (the project root where the session started) into `command` and each `args`
element itself, with no shell, so a folder path with spaces works and the same file works for everyone
(https://code.claude.com/docs/en/hooks, "Reference scripts by path" and "Exec form and shell form"). On Windows, exec
form needs `command` to be a real `.exe`, which `.venv\Scripts\python.exe` is (same page).

| Event | Script | What it does |
|---|---|---|
| `SessionStart` (`startup|resume|clear|compact`) | `tools\hooks\session_start.py` | prints the rule column of every lesson in `lessons\` so each session starts with them |
| `PreToolUse` (`Write|Edit|MultiEdit|NotebookEdit|Bash|PowerShell`) | `tools\hooks\guard_paths.py` | blocks writes into the folders listed under `protected_roots` in `config\paths.yaml` (exit code 2 blocks the call and sends the reason to Claude) |
| `PostToolUse` (`Write|Edit|MultiEdit`) | `tools\check_note.py` | checks the header and source format of a knowledge note right after it is written |
| `SubagentStop` (no matcher: every subagent) | `tools\hooks\log_run.py` | appends one JSON line per finished subagent to `work\agent-runs.log` (git-ignored), so silent subagent failures are visible; never blocks (exit 0) |

The guard hook also refuses a bare `python`, `py` or `pip` command (use `.venv\Scripts\python.exe`); see its docstring.
Event names, the `SessionStart` matcher values and the exit-code-2 behaviour come from https://code.claude.com/docs/en/hooks.
`timeout` is in seconds (same page; the default for a command hook is 600).

### The guard fails closed: `"onFailure": "block"`
The `PreToolUse` guard hook, and only that hook, sets `"onFailure": "block"`. The hooks reference documents the field
for command hooks: it decides whether the triggering action goes ahead when the hook fails (`"continue"` or
`"block"`), and it "Requires Claude Code v2.1.295 or later" (https://code.claude.com/docs/en/hooks, "Command hook fields"
and "Block the action when a hook fails"). Its own example sets it on an exec-form hook (`command` plus `args`), the
form used here.

What it changes, per the same page:
- Without it, a hook that fails or times out lets the call go ahead on most events: Claude Code "still carries out
  the action."
- With it, a failure "does what exit code 2 does on that event": on `PreToolUse` it blocks the tool call. The page
  counts as failures a hook that "fails to start, for example because the script or executable doesn't exist", an
  exit code other than 0 or 2, a timeout, and JSON output that cannot be parsed.
- So when `.venv\Scripts\python.exe` is missing (setup not run yet, or the venv deleted), every Write, Edit,
  MultiEdit, NotebookEdit, Bash and PowerShell call is **blocked** instead of passing unguarded. The error names the
  hook and says `failed; blocking because onFailure is "block"`. Fix: run `tools\setup.ps1` yourself in the VS Code
  terminal (Claude cannot run it for you while the guard is blocking), then start a new session.
- A crash inside `guard_paths.py` (an uncaught error exits with code 1) or a guard that takes longer than its 20-second
  `timeout` now blocks the call too.

Version note: the field needs Claude Code v2.1.295 or later. The VS Code extension carries its own copy of Claude
Code, so the extension's version is the one that counts for the panel; the separate command line (`claude --version`)
can be older. What an older version does with the field (ignore it, or report the settings file as invalid) is not
documented and not verified here. If your Claude Code is older, update it. If an older version ignores the field, the guard is fail-open
(a guard that cannot start lets the call through); if it rejects the file, choose Exit, never "continue without". The other three hooks do not set the field, so they stay fail-open on
purpose (a missing lesson list or note check must not stop your work).

VS Code will flag `onFailure` as not allowed, and this is expected. The SchemaStore schema named in `$schema`
(https://json.schemastore.org/claude-code-settings.json) sets `additionalProperties: false` on command hooks
(`$defs/hookCommand`), and its list of allowed fields (`type`, `command`, `args`, `timeout`, `async`, `asyncRewake`,
`shell`, `if`, `statusMessage`) has no `onFailure` (checked when this file was written). The settings docs say the
schema "can lag behind the newest CLI releases", so a warning on a recently documented key does not mean the file is
invalid (https://code.claude.com/docs/en/settings). Claude Code itself checks the file at start-up: if it ever shows a
Settings Error for `.claude\settings.json`, see [09 - Troubleshooting, section 4](../docs/09-troubleshooting.md#4-a-hook-error-when-claude-code-starts).

Requirements and limits:
- The hooks need `.venv\Scripts\python.exe`, which `tools\setup.ps1` creates. Before setup runs, the guard blocks every
  file write and shell command (see above) and the other hooks cannot start. Run setup first, from the VS Code terminal.
- The `args` field (exec form) is a recent hooks feature. The minimum Claude Code version that supports it is not
  verified here; if your version ignores `args`, update Claude Code.
- Hooks run with your user rights. Read every hook script before you trust this folder.
