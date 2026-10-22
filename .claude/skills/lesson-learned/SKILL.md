---
name: lesson-learned
description: Use when a mistake, a print-qa FAIL, a CONTRADICTED fact-check row, a correction from the maker or an agent that missed its output format has just happened. Writes the post-mortem to lessons\YYYY-MM-DD-<project>-<slug>.md in the standard table and rebuilds the lessons index.
argument-hint: <project-slug> | <lesson-slug> | <what happened, one line>
disable-model-invocation: true
---
## Overview
Input: $ARGUMENTS, three fields separated by ` | `: project slug, lesson slug, one-line description. Output: `lessons\YYYY-MM-DD-<project>-<slug>.md` (today's date) and a regenerated `lessons\INDEX.md`. Lead-run; writes nothing else.

## When to use
In the same session as the failure: any `print-qa` FAIL, any `fact-checker` CONTRADICTED row, any agent returning without its required output, any correction from the maker, any instruction given in the wrong form. Not for filing facts (`/file`). If a lesson with the same root cause already exists, add a row there instead of a new file.

## Steps
1. Glob `lessons\*.md` and Grep the folder for the slug and the root cause. If an existing lesson covers it, append a row to its table and go to step 4.
2. Write the file in the standard format (copy the layout of any existing lesson in `lessons\`):
   ```
   # Post-mortem: <title> (<YYYY-MM-DD>, <project or phase>)

   | What happened | Root cause | Rule now |
   |---|---|---|
   | <observable event, naming the file or print it touched, repo-relative path> | <why, one sentence that names the missing check> | <imperative rule with the number, condition, command or file that makes it checkable> |

   Fix applied: <what changed, paths>.

   Rule lives in: <path of CLAUDE.md, an agent or skill file, a tools\*.py or hook, or "not yet enforced">.
   ```
   Add a `Sources:` list with full URLs when the lesson corrects a fact.
3. If the rule does not yet live in anything executable (hook, script check, agent rationalization row), write "not yet enforced" and name the follow-up. Never claim enforcement that does not exist.
4. Run `.venv\Scripts\python.exe tools\build_indexes.py`; confirm the new line in `lessons\INDEX.md`.
5. Reply with the lesson path, the rule in one line, and where it lives (or "not yet enforced" plus the follow-up).

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "It was a small slip, no lesson needed." | Small slips (one wrong drying time, one wrong unit) repeat. Every correction gets a row. |
| "The rule is 'be more careful'." | Not checkable. A rule names a number, a condition, a command or a file. |
| "I'll write the lesson at the end of the session." | Sessions end abruptly. Same moment, same session. |
| "Rule lives in: CLAUDE.md" when it does not yet. | Write "not yet enforced" and name the hook or script that would. |

## Red flags
- A "Rule now" cell without a checkable element.
- A lesson that restates the event without a root cause.
- `build_indexes.py` not run.

## Verification
- [ ] File exists at `lessons\YYYY-MM-DD-<project>-<slug>.md` with the three-column table.
- [ ] "Rule lives in:" names a path or says "not yet enforced" with a follow-up.
- [ ] `build_indexes.py` printed the new lesson count; `lessons\INDEX.md` lists the file.
