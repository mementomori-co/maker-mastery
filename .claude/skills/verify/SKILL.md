---
name: verify
description: Use when a research inbox file or one quoted claim must be fact-checked independently before it is filed or told to you. Runs the fact-checker in a fresh context that sees only the claims, never the researcher's reasoning.
argument-hint: <inbox file path | "quoted claim">
context: fork
agent: fact-checker
---
## Overview
Verify: $ARGUMENTS

If `$ARGUMENTS` is a file path, read that file only and verify every row. If it is a quoted claim, treat it as a one-row claims table with no source and find the primary source yourself.

## When to use
After every researcher run, and before any number, setting, licence term or hardware fact reaches `knowledge\` or you.

## Steps
1. Read the claims file (or the quoted claim). Do not open anything under `research\inbox\` other than the given file.
2. Fetch every cited URL yourself; on HTTP 402/403 use `curl -sL -A "Mozilla/5.0"` into a scratch file under `work\` and read the text.
3. Assign VERIFIED / CONTRADICTED / PARTIAL / UNVERIFIABLE per row with a short quote, URL and version dependence.
4. Write `research\verified\<topic-slug>\<question-slug>.md` (same slugs as the inbox file; for a quoted claim use `adhoc\<date>-<slug>.md`).
5. Return the path and counts.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "The URL looks official, skip fetching." | Official-looking URLs can be dead or wrong. Fetch it. |
| "I'll peek at the inbox folder for context." | Context is contamination. One file. |

## Red flags
- A verdict without a fetched URL and quote.
- Softened language on a CONTRADICTED row.

## Verification
- [ ] Every row has verdict, quote, fetched URL, version note.
- [ ] Output file written and path returned.
