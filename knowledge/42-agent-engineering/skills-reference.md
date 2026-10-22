# Skills: frontmatter fields and the 500-line rule

Applies to: Claude Code (any OS)
Verified: 2026-10-04

## Facts
- `context: fork` runs the skill in a forked subagent context. - [Claude Code: skills](https://code.claude.com/docs/en/skills)
- `agent:` picks the subagent type used with `context: fork`: a built-in (`Explore`, `Plan`, `general-purpose`) or any custom subagent from `.claude/agents/`. Default is `general-purpose`. - [Claude Code: skills](https://code.claude.com/docs/en/skills)
- `disable-model-invocation: true` stops Claude from loading the skill on its own (for workflows you trigger with `/name`) and also blocks preloading it into subagents. The page documents its scheduled-task interaction "As of v2.1.196". - [Claude Code: skills](https://code.claude.com/docs/en/skills)
- `argument-hint` is the hint shown during autocomplete for expected arguments. - [Claude Code: skills](https://code.claude.com/docs/en/skills)
- "Keep `SKILL.md` under 500 lines"; move detailed reference material to separate files. - [Claude Code: skills](https://code.claude.com/docs/en/skills)

## In practice
- Use `disable-model-invocation: true` for skills that must only run when you type them (release, publish, anything with side effects).
- With `context: fork` and no `agent:`, the skill runs as `general-purpose`; set `agent:` when you want a narrower tool set, such as one of the repo's agents in [.claude/agents](../../.claude/agents/).
- Split a `SKILL.md` that nears 500 lines into the main file plus reference files.

## Not verified / open questions
- Not tested against a specific build; the rows describe the docs as fetched on the Verified date.

Sources:
- https://code.claude.com/docs/en/skills - `context`, `agent`, `disable-model-invocation`, `argument-hint`, 500-line rule
