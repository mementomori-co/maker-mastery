# Permission rules: syntax, evaluation order, the MCP exception

Applies to: Claude Code (any OS)
Verified: 2026-10-04

## Facts
- Rules take the form `Tool` or `Tool(specifier)`; parentheses inside the specifier are literal and need no escaping. Examples: `Bash(npm run build)`, `Read(./.env)`, `WebFetch(domain:example.com)`. - [Claude Code: permissions](https://code.claude.com/docs/en/permissions)
- Evaluation order is deny, then ask, then allow; the first match decides, and specificity does not change the order. - [Claude Code: permissions](https://code.claude.com/docs/en/permissions)
- Deny and ask rules can match a top-level input parameter of a built-in tool with `Tool(param:value)`, for example `Bash(run_in_background:true)`. A rule like `Bash(command:rm *)` could be bypassed by a compound command, so Claude Code ignores it with a startup warning. - [Claude Code: permissions](https://code.claude.com/docs/en/permissions)
- MCP exception: Claude Code skips any `mcp__` rule that has parentheses. Valid forms are `mcp__<server>`, `mcp__<server>__*` and `mcp__<server>__<tool>`; match an MCP tool's parameter with a `--disallowedTools` deny rule instead. Details in [../41-mcp/python-sdk-and-server-config.md](../41-mcp/python-sdk-and-server-config.md). - [Claude Code: permissions](https://code.claude.com/docs/en/permissions)
- Tool-name globs: deny and ask rules accept a glob over the full tool name, including the server segment, so `mcp__*` denies every MCP tool and `mcp__*__*print*` denies any MCP tool whose name contains "print". Allow rules are stricter: a glob only works after a literal `mcp__<server>__` prefix, and unanchored allow globs are skipped. This repo's `.claude/settings.json` relies on the deny form to block print-sending tools. - [Claude Code: permissions, "Tool name wildcards"](https://code.claude.com/docs/en/permissions)

## In practice
- Write built-in rules as `Tool` or `Tool(specifier)`; no escaping for literal parentheses.
- Never write `mcp__server__tool(param:value)`: it is silently skipped.
- A deny always beats an allow, however specific the allow looks. The repo's [.claude/settings.json](../../.claude/settings.json) uses deny rules for the print-sending tools for this reason.

## Not verified / open questions
- The Claude Code version that introduced `Tool(param:value)` matching is not stated on the page.

Sources:
- https://code.claude.com/docs/en/permissions - rule syntax, deny/ask/allow order, `Tool(param:value)`, MCP parentheses exception
