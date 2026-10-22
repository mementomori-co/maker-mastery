# 42 Agent engineering - index

How Claude Code's hooks, permissions, settings, skills, sub-agents, plugins and headless mode behave, from the official docs. Every note lists public sources; version-gated rows say which Claude Code version they need, so check `claude --version` before relying on one.

- [hooks-reference.md](hooks-reference.md) - which events can block on exit 2, exit-code rules, default timeouts, the 10,000-character context cap, `SessionStart` matchers, shell vs exec form, handler dedup, Windows `file_path` format, and why path rules bind only to `Edit` / `Read`.
- [permissions-reference.md](permissions-reference.md) - `Tool(specifier)` syntax, deny-then-ask-then-allow order, `Tool(param:value)` matching and its `Bash(command:...)` carve-out, and the MCP no-parentheses exception.
- [settings-reference.md](settings-reference.md) - user, shared project, project local and managed settings files, their precedence, and the shape and merge behaviour of the `hooks` key.
- [skills-reference.md](skills-reference.md) - `context: fork`, `agent:`, `disable-model-invocation`, `argument-hint` and the 500-line `SKILL.md` rule.
- [sub-agents-reference.md](sub-agents-reference.md) - frontmatter fields, `permissionMode` values, the colon-in-name ban, the 15,000-token description warning and location priority.
- [plugins-reference.md](plugins-reference.md) - plugin layout, the optional manifest, marketplaces and the `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` / `${CLAUDE_PROJECT_DIR}` variables.
- [headless-mode.md](headless-mode.md) - `claude -p`, `--output-format`, `--allowedTools` in auto mode, `--permission-mode`, and bounding unattended runs with `--max-turns` and `--max-budget-usd`.
