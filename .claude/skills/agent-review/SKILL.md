---
name: agent-review
description: Use when hooks, settings, agent files, skills or MCP configuration must be reviewed in a fresh context against the Claude Code and MCP docs for security and compliance. Runs the mcp-agent-engineer in a fresh context and writes a ranked findings file to work\reports\reviews\<date>-<slug>.md.
argument-hint: "<slug> | <files or folders to review>"
context: fork
agent: mcp-agent-engineer
---
## Overview
Input: $ARGUMENTS, as `<slug> | <paths>`. Output: `work\reports\reviews\YYYY-MM-DD-<slug>.md` with findings ranked by severity, each with a docs quote or a test result and a concrete fix. No installs, no settings changes.

## When to use
After any change to `.claude\settings.json`, `tools\hooks\`, `.claude\agents\`, `.claude\skills\` or `.mcp.json`, or before a new MCP server is proposed. Not for building a new MCP tool (use `/mcp-new-tool`).

## Steps
1. Fetch the relevant docs this run (https://docs.anthropic.com/en/docs/claude-code/hooks, https://docs.anthropic.com/en/docs/claude-code/settings, https://docs.anthropic.com/en/docs/claude-code/sub-agents, https://docs.anthropic.com/en/docs/claude-code/skills, https://docs.anthropic.com/en/docs/claude-code/mcp, https://modelcontextprotocol.io/specification/latest; curl fallback on HTTP 402/403) and quote the lines you rely on.
2. Read the files. Run the shipped checks with `.venv\Scripts\python.exe`: the tests under `tools\tests\` that cover the reviewed files (for example the guard-hook tests) and `tools\check_skill.py` on any skill. Add targeted probes (crafted hook inputs on stdin) without modifying anything.
3. Write the review: closed / open / new findings, severity, fix, evidence. Secrets never appear in the file.
4. Return the path and the open-finding count.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "The hook fired once, it works." | A guard hook that passed its first run can still be bypassed by another tool name, path form or quoting. Probe the edge cases. |
| "I'll just fix it while I'm here." | Reviewer and fixer are different contexts. Report; the lead fixes. |

## Red flags
- A finding without a docs quote or a test result.
- Any edit to settings or hooks during the review.

## Verification
- [ ] Review file written; findings ranked with fixes.
- [ ] Tests run and results quoted.
