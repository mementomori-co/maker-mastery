---
name: gdd
description: Use when a game or mini-game needs a design document a second person could build from without questions. Runs the game-director in a fresh context and writes a one-page GDD to game\gdd.md in the project folder.
argument-hint: <project folder> | <one-line pitch> | <platform or cabinet>
context: fork
agent: game-director
---
## Overview
Design: $ARGUMENTS, three fields separated by ` | `: project folder, one-line pitch, target (PC, web, a retro-emulation cabinet, or "undecided"). Output: `<project folder>\game\gdd.md` (see `templates\project\` for the folder layout).

## When to use
A new game idea, a mini-game for a printed cabinet or toy, or a redesign that needs a written target before art, code or hardware starts. Not for an animatic or storyboard alone (ask the game-director directly for a pre-production brief).

## Steps
1. Read `lessons\INDEX.md` and any game-design notes in `knowledge\` (a missing folder means no verified note yet). Ask the lead for the project's style guide path; if none, write "style guide: none yet" in the GDD.
2. Write the one-page GDD: pitch, pillars (3), core loop, mechanics and systems, controls (per player: buttons, sticks, counted separately), win/lose and session length, scope (must / should / cut), art and audio direction (reference the style guide, not restated), platform and engine decision, risks, open questions.
3. Engine section: check what is installed before writing any engine step. Quote licence terms only from https://www.unrealengine.com/license, https://unity.com/pricing, https://godotengine.org/license/ fetched this run, with the page date; otherwise write `not verified`.
4. Audio section: one row per planned sound class with licence source; middleware terms from the vendor page fetched this run or `not verified`.
5. Run the test: read the GDD as a stranger; every place a builder would have to ask becomes a numbered NEEDS MAKER question at the end.
6. Any fact fetched this run goes to `research\inbox\<topic-slug>\<question-slug>.md` in the researcher's claims-table format for `/verify`.
7. Return the GDD path, the inbox paths, the NEEDS MAKER list, one next step.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "The mechanic is standard, no need to spell out controls." | Players, buttons and inputs are separate counts; implicit assumptions are where builds fail. |
| "Godot is MIT, that never changes." | Quote the licence page fetched this run with its date, or mark `not verified`. |
| "I'll describe the look here to save a hop." | Look and voice belong to the style guide; reference its path, do not restate. |

## Red flags
- A licence or fee without a URL fetched this run.
- An engine step written as if the engine were installed when it was not checked.
- Open design choices buried in prose instead of listed as NEEDS MAKER.
- Controls section with one combined number for players and buttons.

## Verification
- [ ] `<project folder>\game\gdd.md` exists with all sections from step 2.
- [ ] Every external fact carries a fetched URL or `not verified`.
- [ ] NEEDS MAKER list present (may be "none" only if a stranger read-through found no gaps).
- [ ] Claims written to `research\inbox\`, paths returned.
