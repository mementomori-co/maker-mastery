# Hooks reference: blocking, timeouts, context caps, matchers, path rules

Applies to: Claude Code (any OS; Windows notes marked)
Verified: 2026-10-03

## Facts

### Which events can block
- `PreToolUse` is the event where exit code 2 reliably blocks the tool call; Claude sees the hook's stderr as the denial reason, routed like a permission deny. On other blocking events such as `Stop` / `SubagentStop`, exit 2 does not necessarily put stderr in Claude's context; it may only be shown to the user. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- `PostToolUse` exit 2 cannot block (the tool already ran); stderr is shown to Claude. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- `SessionStart` exit 2 cannot block; its stderr goes to the user only. `SessionStart`, `UserPromptSubmit`, `UserPromptExpansion` and `PostModelSwitch` are the events where plain stdout is added as context Claude can see. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- `SubagentStop` exit 2 blocks by keeping the subagent from stopping. It also fires for internal agents (prompt suggestions, `/btw`), so a gate should filter on `agent_type`. Its input includes `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` and `last_assistant_message`. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- For most events only exit 2 blocks by exit code alone; exit 1 without valid JSON on stdout is a non-blocking error. Exception: any non-zero exit aborts `WorktreeCreate` and fails `WorktreeRemove`. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- A hook that cannot start (mistyped path, script not executable) falls into the same non-blocking bucket, so the gate is effectively off; the transcript shows a "Failed with non-blocking status code" notice. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- Fail-closed option (added after the note's Verified date, read on the hooks page on 2026-10-22): a `command` or `http` hook may set `"onFailure": "block"` (values `"continue"`, the default, or `"block"`; requires Claude Code v2.1.295 or later). A hook that cannot start, exits with a code other than 0 or 2, times out or prints unparsable JSON then does what exit 2 does on that event, so a `PreToolUse` failure blocks the tool call. It has no effect on `Stop`, `SubagentStop`, `TaskCompleted`, `TeammateIdle` or async hooks. The page's example uses exec form (`command` + `args`). - [Claude Code: hooks, "Block the action when a hook fails"](https://code.claude.com/docs/en/hooks)

### Timeouts and output caps
- Default timeout is 600 s for `command`, `http` and `mcp_tool` hooks (this applies to `PreToolUse`); 30 s on `UserPromptSubmit`, `PreModelSwitch` and `PostModelSwitch`; 10 s on `MessageDisplay`. The `prompt` type defaults to 30 s and `agent` to 60 s. A timed-out hook does not block, except a timed-out `PreModelSwitch` hook, which does. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- `additionalContext`, `systemMessage`, `initialUserMessage` and plain stdout are capped at 10,000 characters, with no setting to raise it. Beyond that, the full output is saved to a file in the session directory and replaced by its path plus a preview of up to 2,000 characters; Claude is not told to read the file. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)

### Matchers, shells and inputs
- `SessionStart` matchers: `startup`, `resume`, `clear`, `compact`, `fork`. `fork` requires v2.1.214 or later; before that, forked sessions reported `resume`. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- A `command` hook runs under `sh -c` on macOS and Linux, Git Bash on Windows, or PowerShell when Git Bash is not installed. Setting `args` runs it in exec form without a shell. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- The same handler defined in several settings files runs once; a plugin's or skill's copy is not deduplicated against it. Hooks from settings files, managed policy and plugins also run inside subagents. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- For `Write`, `Edit` and `Read`, `tool_input.file_path` is always absolute; on Windows it arrives with backslashes even when the hook runs under Git Bash. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- The `if` filter on a matcher is best-effort; use the permission system when a hard allow or deny is required. - [Claude Code: hooks](https://code.claude.com/docs/en/hooks)

### Permission path rules (related)
- Path rules are consulted only for `Edit(path)` and `Read(path)`. A path rule for `Write`, `NotebookEdit`, `Glob` or `MultiEdit` is accepted but never consulted (startup warning). Exceptions: a `Glob` rule passed with `--allowedTools`, and a tool-name rule with no path (for example a bare `Write` deny), enforced for the whole tool. Requires v2.1.210 or later. - [Claude Code: permissions](https://code.claude.com/docs/en/permissions)
- `//path` is absolute from the filesystem root. On Windows paths are normalised to POSIX form before matching (for example `C:\work\app` becomes `/c/work/app`; the docs use a home-folder path), so write `//c/**/.env`. - [Claude Code: permissions](https://code.claude.com/docs/en/permissions)
- Bash output redirects (`>`, `>>`, `2>`) are checked against the same `Edit` rules, protected paths and working-directory limits as the `Edit` tool. - [Claude Code: permissions](https://code.claude.com/docs/en/permissions)

## In practice
- Enforce with `PreToolUse` exit 2; treat `PostToolUse` and `SessionStart` exit 2 as reporting, not enforcement.
- A blocking `SubagentStop` hook must check `agent_type`.
- To protect a folder, combine an `Edit`/`Read` path rule with a `PreToolUse` hook; a `Write(path)` rule is ignored. The repo's guard hook in [tools/hooks](../../tools/hooks/) and its registration in [.claude/settings.json](../../.claude/settings.json) follow this pattern.
- On Windows, write path rules in POSIX form (`//c/...`).
- After editing hook config, check the transcript for "Failed with non-blocking status code": a broken hook fails silently as a gate.

## Not verified / open questions
- Whether a path guard can be bypassed with Windows 8.3 short names, `\\?\` prefixes or UNC paths was explored in a local test harness but never independently reproduced: not verified (no public source). Test your own guard against those forms.
- The rows describe the docs as fetched on the Verified date; re-check version-gated rows (v2.1.210, v2.1.214) after any update.

Sources:
- https://code.claude.com/docs/en/hooks - blocking by event, exit codes, timeouts, context caps, matchers, shell vs exec form, dedup, `file_path`, `SubagentStop` input, `if` filter
- https://code.claude.com/docs/en/permissions - Edit/Read-only path rules, Windows normalisation, Bash redirects
