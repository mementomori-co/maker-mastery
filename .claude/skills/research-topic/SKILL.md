---
name: research-topic
description: Use when you want a topic researched into verified notes. Splits the topic into narrow questions, fans out researcher agents in parallel, then runs /verify on each inbox file and /file on each verified file; lead-run, it does not write notes itself.
argument-hint: <topic>
disable-model-invocation: true
---
## Overview
Topic: $ARGUMENTS. This skill is the knowledge pipeline entry point: researcher, then fact-checker, then librarian, with on-disk hand-offs under `research\`.

## When to use
You ask to research, learn or verify a topic, or an item from your research backlog is picked up. Not for a single quoted claim (use `/verify "<claim>"`).

## Steps
1. Read `CURRICULUM.md` and the `knowledge\` category indexes to pick the category the topic belongs to.
2. Split the topic into 3 to 8 narrow questions, each answerable from one or two primary pages. Choose a `<topic-slug>`.
3. Launch one `researcher` subagent per question **in the same message** so they run in parallel (`/research-one` does one). Each gets: the question, the topic slug, the question slug, and the source priority reminder. Expect back a path under `research\inbox\<topic-slug>\`.
4. For each inbox file, run `/verify research\inbox\<topic-slug>\<q>.md`. Pass only the path, never the researcher's output.
5. For each verified file, run `/file research\verified\<topic-slug>\<q>.md`.
6. Reply: what was VERIFIED (with URLs), what was CONTRADICTED or UNVERIFIABLE, which notes changed (full paths), and the next topic. Mark questions NEEDS MAKER.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "I already know the answer, skip the researcher." | Notes written from memory are where errors come from. Run the pipeline. |
| "Pass the researcher's reasoning to the fact-checker so it works faster." | Independence is the point. Path only. |
| "The fact-checker said PARTIAL; file it and move on." | PARTIAL is filed as the corrected value with the correction named. |

## Red flags
- Fewer than 3 questions for a broad topic, or a question that needs opinion rather than a source.
- Running researchers one at a time.
- A note written by the lead instead of the librarian.

## Verification
- [ ] Every question has an inbox file, a verified file, and a librarian result.
- [ ] `tools\check_note.py` PASS reported for every touched note.
- [ ] Reply lists full paths and URLs.
