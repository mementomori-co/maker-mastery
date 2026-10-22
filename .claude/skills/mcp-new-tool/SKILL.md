---
name: mcp-new-tool
description: Use when one new tool must be added to an existing MCP server you already run, with a typed schema, a test, no secrets, and a diff ready for fresh-context review. Runs the mcp-agent-engineer in a fresh context; the server is edited in its own repo and nothing is registered in this project automatically.
argument-hint: <server repo path> | <tool name> | <what it returns, read-only unless stated>
context: fork
agent: mcp-agent-engineer
---
## Overview
Add: $ARGUMENTS (server repo path, tool name, return description). Outputs: the tool and its test inside the server repo, and `work\reports\reviews\<YYYY-MM-DD>-<tool-name>.md` holding the diff and the review criteria. No `.mcp.json` entry is added to this project; the proposed entry goes to `work\reports\mcp-proposals.md` for you to apply yourself.

## When to use
Extending a server you already have. Not for writing a new server from scratch, not for any tool that can start, send, upload or queue a print (that is never built: no AI ever sends a print), and not for Claude Code agents, skills or hooks (ask mcp-agent-engineer directly).

## Steps
1. Read `lessons\` and any MCP notes in `knowledge\`. Read the server: its existing tools, how it registers them, and its SDK version from `pyproject.toml`, `package.json` or the lockfile (quote the line). Fetch the current MCP specification changelog and the security best practices page under https://modelcontextprotocol.io/specification/ this run; note anything that affects the tool (statelessness, deprecated features, annotations).
2. Design: name, one-sentence purpose, typed input schema with every field described, return shape, read-only by default. If the request asks for a write or an exec tool, stop and return NEEDS MAKER with the risk stated.
3. Implement in the server's own pattern and language; no new dependencies without NEEDS MAKER. Secrets, if any, only as `${VAR}` references; grep the diff for keys, tokens and absolute paths into a home folder.
4. Test: one test beside the tool that calls it against a stub or the running host and asserts the return shape; run the server's test command and paste the output. Do not install the MCP Inspector or anything else; if an Inspector run would help, write the exact PowerShell line for you as NEEDS MAKER.
5. Write `work\reports\reviews\<YYYY-MM-DD>-<tool-name>.md`: the diff, the criteria (schema typed; read-only; test passes; no secrets; no new dependency; result treated as untrusted data), and the line "Reviewer: a second mcp-agent-engineer in a fresh context; PASS/FAIL per criterion." Append the proposed `.mcp.json` entry (scope, command, `${VAR}`) to `work\reports\mcp-proposals.md` without applying it.
6. Return: files changed (full paths), test output, the review file path, NEEDS MAKER list, one next step.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "It's ten lines, review is overkill." | The author of the code is not an independent reviewer. Review file, or not done. |
| "The SDK version is whatever the latest release is." | The latest release is not this repo's pin. Quote the lockfile line. |
| "Register it in .mcp.json so the lead can use it now." | Registering a server is your decision. Proposal line only. |
| "The test imports fine, that counts." | The test runs and the output is pasted. Claims are checked by a command, not by reading. |

## Red flags
- No test output in the return.
- A `.mcp.json` created or edited in this project.
- A write or exec tool added without NEEDS MAKER.
- A new dependency pulled in silently.
- A secret or a user-folder path in the diff.

## Verification
- [ ] SDK version line quoted from the repo.
- [ ] Tool has a typed schema and a test; test command run and output pasted.
- [ ] Diff grepped for secrets and user paths; none.
- [ ] `work\reports\reviews\<YYYY-MM-DD>-<tool-name>.md` exists with diff and criteria.
- [ ] Proposal appended to `work\reports\mcp-proposals.md`; no `.mcp.json` touched.
