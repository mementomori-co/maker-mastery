---
name: <kebab-case, equals folder name>
description: Use when <trigger in one sentence>. <What it produces, in one sentence.> (2 sentences at most; "Use when" is required. Format adapted from addyosmani/agent-skills, MIT)
argument-hint: <args>
# optional: context: fork / agent: <agent-name> / disable-model-invocation: true / allowed-tools: Bash(curl *)
---
## Overview
What this skill does and the one output it leaves on disk (repo-relative path).

## When to use
Trigger conditions. When NOT to use (name the neighbouring skill).

## Steps
1. Numbered, each ending in a checkable artifact or value.
2. Every fact fetched this run has a URL or a repo-relative path; numbers carry their condition.
3. Hand-offs are file paths inside the repo (never pasted content).

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "<excuse the agent will think>" | "<why it is wrong, tied to a lesson in lessons\>" |

## Red flags (stop and fix)
- Observable signs the skill is going wrong.

## Verification
- [ ] Evidence-only checkboxes naming the command or artifact (for example `check_note.py PASS`, file exists at path).
