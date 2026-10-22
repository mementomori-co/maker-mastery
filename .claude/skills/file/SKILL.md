---
name: file
description: Use when a fact-checked file under research\verified\ is ready to become or update a verified note. Runs the librarian in a fresh context; files VERIFIED rows only, updates index, registry and curriculum, and runs check_note.py.
argument-hint: <verified file path>
context: fork
agent: librarian
---
## Overview
File: $ARGUMENTS

## When to use
After `/verify` has written a verified file. Never on an inbox file.

## Steps
1. Read the verified file. Separate VERIFIED and corrected-PARTIAL rows (they go to Facts) from CONTRADICTED and UNVERIFIABLE rows (they go to Not verified / open questions).
2. Pick the `knowledge\<NN-category>\` folder that fits; Grep it for an existing note on the topic and merge into it if found.
3. Write or update the note per `templates\note.md` with `Applies to:`, `Verified: <today>`, conditions on every number, a public source URL on every fact.
4. Run `.venv\Scripts\python.exe tools\check_note.py <note path>` until PASS.
5. Update the category `index.md`, add new URLs to `sources\registry.md`, tick `CURRICULUM.md` only where the note covers the line.
6. Return: note path, rows filed, rows deferred, files touched, check_note result.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "New note is cleaner than merging." | Grep first. One topic, one file. |
| "The curriculum line is close enough." | Tick only what the note verifies. |

## Red flags
- check_note.py not run.
- A Facts bullet without a URL.

## Verification
- [ ] check_note.py PASS.
- [ ] index, registry, curriculum updated where true.
- [ ] Paths returned.
