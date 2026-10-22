# Sub-agents: frontmatter fields, description-length warning, location priority

Applies to: Claude Code (any OS)
Verified: 2026-10-04

## Facts
- Frontmatter: `name` (required), `description` (required), `tools` (optional), `model` (optional: `sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit`). - [Claude Code: sub-agents](https://code.claude.com/docs/en/sub-agents)
- `permissionMode` accepts `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, or `manual` (an alias for `default`, requires v2.1.200 or later), and is ignored for plugin subagents. - [Claude Code: sub-agents](https://code.claude.com/docs/en/sub-agents)
- A colon in a subagent `name` is banned from v2.1.218. - [Claude Code: sub-agents](https://code.claude.com/docs/en/sub-agents)
- When the combined descriptions of non-built-in subagents exceed 15,000 tokens, Claude Code shows a startup warning with the total. It is a warning, not a cap: every subagent still loads. - [Claude Code: sub-agents](https://code.claude.com/docs/en/sub-agents)
- Location priority, highest first: managed settings, the `--agents` CLI flag, `.claude/agents/` (project), `~/.claude/agents/` (user), a plugin's `agents/` directory. - [Claude Code: sub-agents](https://code.claude.com/docs/en/sub-agents)

## In practice
- Never put a colon in a subagent name.
- Keep descriptions short: the 15,000-token figure is a useful budget for a large agent set (this repo's agents are in [.claude/agents](../../.claude/agents/)), and short descriptions also keep the main context clean.
- To override a project subagent for one session, pass `--agents`; a managed-settings subagent cannot be overridden.

## Not verified / open questions
- Whether a given build prints the 15,000-token warning exactly as documented was not tested.

Sources:
- https://code.claude.com/docs/en/sub-agents - frontmatter fields, `permissionMode` list and `manual` gate, colon ban, 15,000-token warning, location priority
