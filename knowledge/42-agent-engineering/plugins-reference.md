# Plugins: standard layout, manifest, marketplaces, path variables

Applies to: Claude Code (any OS)
Verified: 2026-10-04

## Facts
- Standard layout: manifest `.claude-plugin/plugin.json` (optional); skills in `skills/`; commands in `commands/` (the page prefers `skills/` for new plugins); agents in `agents/`; hooks in `hooks/hooks.json`; MCP servers in `.mcp.json`. - [Claude Code: plugins reference](https://code.claude.com/docs/en/plugins-reference)
- "`name` is the only required key" in `plugin.json`, and the manifest itself is optional: without it Claude Code loads what it finds in the standard layout. - [Claude Code: plugins reference](https://code.claude.com/docs/en/plugins-reference)
- In the manifest field table, `hooks` and `mcpServers` are loaded together with `.mcp.json`, and a server name declared later replaces an earlier one. - [Claude Code: plugins reference](https://code.claude.com/docs/en/plugins-reference)
- A marketplace is a repository or directory with a `.claude-plugin/marketplace.json` listing plugins and where to fetch them; the page calls it "a catalog, not a hosted store". You add it once, then install by name, such as `commit-commands@claude-plugins-official`. - [Claude Code: plugins](https://code.claude.com/docs/en/plugins)
- Path variables: `${CLAUDE_PLUGIN_ROOT}` is the absolute path of the installed plugin version; `${CLAUDE_PLUGIN_DATA}` is `~/.claude/plugins/data/<id>/`, created on first reference and kept across updates; `${CLAUDE_PROJECT_DIR}` is the project root. - [Claude Code: plugins reference](https://code.claude.com/docs/en/plugins-reference)

## In practice
- A plugin without a manifest still loads from the standard layout; add `plugin.json` only when you need a field beyond `name`.
- When two sources declare the same MCP server name, the one loaded later wins.
- Reference files inside the plugin with `${CLAUDE_PLUGIN_ROOT}`; keep anything that must survive an update under `${CLAUDE_PLUGIN_DATA}`.

## Not verified / open questions
- Not tested against a specific build; the rows describe the docs as fetched on the Verified date.

Sources:
- https://code.claude.com/docs/en/plugins-reference - layout, manifest keys, `hooks`/`mcpServers` loading, path variables
- https://code.claude.com/docs/en/plugins - marketplace definition
