# 41 MCP - index

The Model Context Protocol: what the current spec requires, and how to configure and write MCP servers for Claude Code in Python. Every note lists public sources; version-gated rows say which Claude Code version they need.

- [mcp-protocol-spec-2026-07-28.md](mcp-protocol-spec-2026-07-28.md) - spec revision 2026-07-28: stdio and Streamable HTTP, deprecated HTTP+SSE / Sampling / Roots / Logging / Dynamic Client Registration, `ToolAnnotations` defaults, OAuth 2.1 and the STDIO exemption, confused-deputy, token-passthrough, state-handle and SSRF rules.
- [python-sdk-and-server-config.md](python-sdk-and-server-config.md) - Claude Code server scopes, `${VAR:-default}` expansion, output cap and timeouts, trust prompt and `--strict-mcp-config`, `claude mcp add`, tool naming and permission-rule forms, precedence; Python SDK v2 `MCPServer` pattern and the `FastMCP` rename.
