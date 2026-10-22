# Settings files, precedence, and the `hooks` key

Applies to: Claude Code (any OS)
Verified: 2026-10-04

## Facts
- Settings files: User `~/.claude/settings.json` (you, in every project on the machine); Shared project `.claude/settings.json` (everyone working in that folder); Project local `.claude/settings.local.json` (you, in that project only); Managed `managed-settings.json` and other managed sources. - [Claude Code: settings](https://code.claude.com/docs/en/settings)
- Precedence, highest first: managed settings, command-line arguments, project local, shared project, user. - [Claude Code: settings](https://code.claude.com/docs/en/settings)
- The `hooks` key is an object keyed by hook event; each value is an array of `{ "matcher", "hooks" }` groups whose entries have `type` `command`, `prompt`, `agent`, `http` or `mcp_tool`. Hooks "merge across files rather than replacing each other", and managed hooks cannot be removed from other files. Default: unset, so no hooks run. - [Claude Code: settings reference](https://code.claude.com/docs/en/settings-reference)

## In practice
- Put machine-wide preferences in the user file, shared project policy in `.claude/settings.json` (this repo ships one: [.claude/settings.json](../../.claude/settings.json)), and personal overrides in `.claude/settings.local.json`.
- Because hooks merge, removing an unwanted hook means editing the file that defines it; an override elsewhere does not cancel it.

## Not verified / open questions
- The page does not say from which version each hook `type` is available; check your build before relying on `http` or `mcp_tool` hooks.

Sources:
- https://code.claude.com/docs/en/settings - settings files, precedence
- https://code.claude.com/docs/en/settings-reference - `hooks` key shape, merge behaviour, default
