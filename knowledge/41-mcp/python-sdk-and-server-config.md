# MCP: Claude Code server config and the Python SDK v2 server pattern

Applies to: Claude Code (any OS; not printer-specific) · Python MCP SDK `mcp` 2.x, Python 3.10+
Verified: 2026-10-04

## Facts

### Claude Code server configuration
- Server scopes: Local and User scope are stored in the per-user `~/.claude.json`; Project scope is `.mcp.json` in the project root and is the only one shared through version control. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- `${VAR:-default}` expands to `VAR` when it is set, otherwise to `default`. A variable such as `${CLAUDE_PROJECT_DIR}` in a project `.mcp.json` entry needs a default such as `${CLAUDE_PROJECT_DIR:-.}`; the page states the same need for local- and user-scoped entries. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- Credential variables are read as empty only in a remote server's `url` and `headers` (to stop credential leakage there), not in every field. `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}` are plugin-provided placeholders, not general `.mcp.json` features. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- The page's `.mcp.json` examples: an `api-server` entry with `"url": "${API_BASE_URL:-https://api.example.com}/mcp"` and an `Authorization: Bearer ${API_KEY}` header, and a separate `shared-server` entry at `https://example.com/mcp` with no headers. They are two examples, not one block. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- MCP tool output is capped at 25,000 tokens by default; raise it with the `MAX_MCP_OUTPUT_TOKENS` environment variable. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- A per-server `timeout` field (milliseconds) overrides the tool-call timeout; values below 1000 ms are ignored and the call falls back to `MCP_TOOL_TIMEOUT`, whose default is about 28 hours. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- In interactive sessions Claude Code asks for approval before using project-scoped servers from `.mcp.json`; `claude mcp reset-project-choices` resets those choices. In `claude -p` runs, Agent SDK sessions and cloud sessions it cannot show the prompt and loads the servers without asking. The prompt is also skipped under `bypassPermissions` with `skipDangerousModePermissionPrompt`. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- `--strict-mcp-config` does not approve `.mcp.json` servers; it excludes them, so only the servers passed with `--mcp-config` are used. Skipping the approval prompt for the servers not loaded that way requires Claude Code v2.1.246 or later. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- `claude mcp add` forms: `claude mcp add --transport http <name> <url>`; `claude mcp add [options] <name> -- <command> [args...]` for stdio; `--transport sse` still exists but SSE is deprecated. WebSocket servers go in `.mcp.json` or `claude mcp add-json` (`--transport` does not accept `ws`). Automatic HTTP-to-SSE fallback requires v2.1.265 or later; on older versions pass `--transport sse` yourself. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)
- Tool names: `mcp__<server>__<tool>` (for example `mcp__puppeteer__puppeteer_navigate`); plugin servers use `mcp__plugin_<plugin>_<server>__<tool>`, with characters outside `A-Z a-z 0-9 _ -` replaced by `_`. Use the full name in permission rules, a skill's `allowed-tools`, a subagent's `tools` and hook matchers; a matcher written against the bare server key never fires for a plugin-bundled server. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp), [Claude Code: permissions](https://code.claude.com/docs/en/permissions)
- MCP permission rules do not take `Tool(specifier)` syntax: Claude Code skips any `mcp__` rule that has parentheses. Valid forms are `mcp__puppeteer`, `mcp__puppeteer__*` and `mcp__puppeteer__puppeteer_navigate`. To match a parameter on an MCP tool, pass a deny rule with `--disallowedTools`. - [Claude Code: permissions](https://code.claude.com/docs/en/permissions)
- When one server is defined in several places Claude Code connects once, using the highest-precedence definition: Local, then Project, then User, then plugin-provided servers, then claude.ai connectors. `managedMcpServers` ranks above all five and requires v2.1.259 or later. - [Claude Code: MCP](https://code.claude.com/docs/en/mcp)

### Python SDK v2
- Install with `uv add "mcp[cli]"` or `pip install "mcp[cli]"`; the `cli` extra adds the `mcp` command (`mcp dev`, `mcp run`, `mcp install`). Plain `mcp` is enough without it. Python 3.10+. - [python-sdk README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md)
- Server pattern: import `MCPServer` from `mcp.server` (not the older `FastMCP`), run with `mcp.run(transport="stdio")`, and never print to stdout in a stdio server, because that corrupts the protocol stream. The tutorial carries no SDK version, so pin `mcp>=2` to match it. - [Build an MCP server](https://modelcontextprotocol.io/docs/develop/build-server.md)
- In SDK v2 `FastMCP` was renamed to `MCPServer` and importing the old module fails; protocol types moved to a separate `mcp-types` distribution, and the guide says to keep importing them through `mcp` / `mcp.types`. - [v2 migration guide](https://py.sdk.modelcontextprotocol.io/v2/migration/#fastmcp-renamed-to-mcpserver)
- A tool function's return-type annotation is its output schema. Read-only tools are marked with `annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False)`. Raising `ToolError` (import path `mcp.server.mcpserver.exceptions`) sends its message to the model instead of a traceback. `Client(mcp)` talks to a server object in memory for tests. These pages describe v2, not `mcp` 1.x. - [structured output](https://py.sdk.modelcontextprotocol.io/servers/structured-output/index.md), [tools](https://py.sdk.modelcontextprotocol.io/servers/tools/index.md), [handling errors](https://py.sdk.modelcontextprotocol.io/servers/handling-errors/index.md), [testing](https://py.sdk.modelcontextprotocol.io/get-started/testing/index.md)
- The latest `mcp` on PyPI on the Verified date was 2.3.0, requiring Python 3.10 or newer. This goes stale; pin the version you install. - [PyPI: mcp JSON](https://pypi.org/pypi/mcp/json)

## In practice
- Write new servers against `MCPServer`, not `FastMCP`, and log to stderr only.
- Use `${CLAUDE_PROJECT_DIR:-.}`-style defaults in every scope, not only in project `.mcp.json`.
- If a tool call hangs far longer than expected, check whether its `timeout` is under 1000 ms (ignored) and fell through to the roughly 28-hour default.
- `--strict-mcp-config` drops `.mcp.json` servers from that run; it does not pre-approve them. Check your version with `claude --version` before relying on any version-gated row above.
- In permission rules, hook matchers and `allowed-tools`, always use the full `mcp__<server>__<tool>` name and never add parentheses.
- The repo's own read-only audit server in [tools/mcp](../../tools/mcp/) follows this pattern: stdio transport, read-only tools, no network.

## Not verified / open questions
- Read from the installed `mcp` 2.3.0 package source, not from a public doc page (not verified (no public source)): `mcp.server.fastmcp` is a removal shim that raises `ModuleNotFoundError`; `ToolError` text reaching the client is prefixed `Error executing tool <name>: `; `mcp.Client` also accepts a URL string, `StdioServerParameters`, or any `Transport`; `ConnectMode` is `"auto"` (default, probes `server/discover` then falls back) or `"legacy"`; `mcp-types` lists `2026-07-28` as its only modern protocol version and four older handshake versions; `ToolAnnotations` Python fields are snake_case with camelCase wire aliases. Read the package source of the version you install before relying on these.
- All Claude Code rows describe the docs as fetched on the Verified date; several are version-gated (v2.1.246, v2.1.259, v2.1.265). Re-check after any update.

Sources:
- https://code.claude.com/docs/en/mcp - scopes, variable expansion, examples, output cap, timeout, trust prompt, `--strict-mcp-config`, `claude mcp add`, tool naming, precedence
- https://code.claude.com/docs/en/permissions - MCP rule forms, parentheses-skipped rule, `--disallowedTools`
- https://modelcontextprotocol.io/docs/develop/build-server.md - `MCPServer` pattern, stdout rule
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md - install line, `cli` extra
- https://py.sdk.modelcontextprotocol.io/v2/migration/#fastmcp-renamed-to-mcpserver - FastMCP rename, `mcp-types` split
- https://py.sdk.modelcontextprotocol.io/servers/structured-output/index.md - return annotation as output schema
- https://py.sdk.modelcontextprotocol.io/servers/tools/index.md - `ToolAnnotations(read_only_hint=True)`
- https://py.sdk.modelcontextprotocol.io/servers/handling-errors/index.md - `ToolError`
- https://py.sdk.modelcontextprotocol.io/get-started/testing/index.md - in-memory `Client` testing
- https://pypi.org/pypi/mcp/json - latest version and Python requirement
