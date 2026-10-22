# Headless mode (`claude -p`): flags, output formats, budgets

Applies to: Claude Code (any OS; not printer-specific)
Verified: 2026-10-04

## Facts
- Add `-p` (or `--print`) to run Claude Code non-interactively, for example `claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"`. - [Claude Code: headless](https://code.claude.com/docs/en/headless)
- `--output-format` takes `text` (default), `json` (result, session ID and metadata) or `stream-json` (newline-delimited JSON for streaming). - [Claude Code: headless](https://code.claude.com/docs/en/headless)
- `--allowedTools` lets listed tools run without a prompt. In an auto-mode run Claude Code drops a bare `Bash` entry as a broad allow rule. - [Claude Code: headless](https://code.claude.com/docs/en/headless)
- The headless page lists `--permission-mode` values `auto`, `dontAsk` and `acceptEdits`; the permission-modes page adds `default`, `plan` and `bypassPermissions`. - [Claude Code: headless](https://code.claude.com/docs/en/headless), [Claude Code: permission modes](https://code.claude.com/docs/en/permission-modes)
- `--permission-prompts none` requires Claude Code v2.1.259 or later; earlier versions reject it as an unknown option. - [Claude Code: headless](https://code.claude.com/docs/en/headless)
- `--max-turns` and `--max-budget-usd` are on the CLI reference, not the headless page. `--max-turns` limits agentic turns in print mode, exits with an error at the limit, and has no limit by default. `--max-budget-usd` caps API spend in print mode; its cap enforcement requires v2.1.217 or later. - [Claude Code: CLI reference](https://code.claude.com/docs/en/cli-reference)

## In practice
- For a scheduled or unattended run, use `--output-format json` so the result is machine-readable, and set both `--max-turns` and `--max-budget-usd`; there is no turn limit unless you set one.
- Scope Bash allows to specific commands instead of a bare `Bash`, which auto mode drops.
- Check `claude --version` before using a version-gated flag; `--permission-prompts none` fails outright on older builds.

## Not verified / open questions
- Not run against a specific build; the rows describe the docs as fetched on the Verified date. Re-check the version gates after any update.

Sources:
- https://code.claude.com/docs/en/headless - `-p`, `--output-format`, `--allowedTools` auto-mode caveat, `--permission-mode`, `--permission-prompts` gate
- https://code.claude.com/docs/en/permission-modes - full permission-mode list
- https://code.claude.com/docs/en/cli-reference - `--max-turns`, `--max-budget-usd` and its v2.1.217 gate
