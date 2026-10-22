---
name: curriculum
description: Use when the maker asks where the learning stands or what to study next. Reads CURRICULUM.md and the knowledge indexes, then reports progress per domain and the next three topics; writes nothing.
argument-hint: domain letter or category number (optional)
---
## Overview
Report progress from `CURRICULUM.md` and the `index.md` in each `knowledge\` category, filtered to $ARGUMENTS when given. Read-only: no file is written; the output is the reply. A tick in `CURRICULUM.md` is changed only by the librarian when a note is filed.

## When to use
Session-start reviews, "what next", before choosing a `/research-topic`. Not for ticking boxes (librarian via `/file`) and not for build planning.

## Steps
1. Read `CURRICULUM.md`; count `[x]` and `[ ]` per category and per domain. Cross-check every `[x]` against a note listed in that category's `knowledge\<NN-category>\index.md`; report a tick with no note as "tick without note" (never silently accept it).
2. List the unticked lines for the lowest-progress categories, printing and slicing categories first, then the categories the maker's active projects need (ask if unknown).
3. Pick the next three topics: each an unticked curriculum line with its category and a one-line question that `/research-topic` can take verbatim.
4. Reply:
   ```
   # Curriculum status <YYYY-MM-DD>
   | domain | categories | ticked / total | notes on disk |
   Ticks without a note: <none | item: expected note path>
   Next 3: 1. <category> - <question> . 2. ... . 3. ...   (rule that picked them: <priority order>)
   NEEDS MAKER: <numbered, when a priority choice is the maker's>
   ```

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "The box is ticked, so it is known." | Ticks seeded from memory turn out wrong. A tick needs a note listed in the category index. |
| "Tick it now, the note is nearly done." | Only the librarian ticks, only after `check_note.py` PASS. |
| "Next topic: whatever is interesting." | Name the priority rule that picked each topic. |

## Red flags
- A progress number not derived from counting the file.
- A next topic not tied to a curriculum line.
- Any write to `CURRICULUM.md`.

## Verification
- [ ] Counts per domain quoted from `CURRICULUM.md`.
- [ ] Every `[x]` reconciled with a category `index.md`.
- [ ] Three next topics, each tied to a curriculum line.
- [ ] No file modified.
