---
name: slicer-question
description: Use when a Bambu Studio setting, grouping, AMS mapping or 3MF question needs an answer with exact UI labels and config keys. Runs the bambu-studio-expert in a fresh context and writes the answer with sources to work\reports\answers\<slug>.md.
argument-hint: "<slug> | <question, with 3MF path if any>"
context: fork
agent: bambu-studio-expert
---
## Overview
Input: $ARGUMENTS as `<slug> | <question>`. Output: `work\reports\answers\<slug>.md` (60 lines or fewer; every claim with a URL or repo path; UI labels as Tab > Section > Setting with the config key; unverified labels marked "(label not verified)").

## When to use
Any slicer question: settings, grouping, prime tower, profiles, CLI, 3MF contents. Not for gating a file before printing (`/preprint-check`) and not for raw research of a new fact (`/research-one`).

## Steps
1. Read the notes in `knowledge\02-bambu-studio\` first; cite them rather than restating. Read `knowledge\00-gear-inventory\` for your printers and nozzles.
2. If the question names a 3MF, run `.venv\Scripts\python.exe tools\audit_3mf.py <3mf> --json` and quote the relevant keys; resolve profile values with `tools\resolve_profile.py`.
3. For anything not in a note, fetch the source (PrintConfig.cpp and GUI .cpp files of https://github.com/bambulab/BambuStudio via raw.githubusercontent.com, and https://wiki.bambulab.com; curl on 402/403) and quote briefly with line numbers. New facts also go to `research\inbox\bambu-studio\<slug>.md` for `/verify`.
4. Write the answer file; return the path.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "I know this setting." | Notes seeded from memory were wrong several times. Read the note or the source. |
| "The label is close enough." | You need Tab > Section > Setting exactly, or "(label not verified)". |

## Red flags
- A setting named without its config key or a URL.
- Editing or slicing a 3MF while `knowledge\00-gear-inventory\current-load.md` is missing or undated.

## Verification
- [ ] Answer file exists at the output path.
- [ ] Every claim has a URL or repo path; every UI label has its config key.
- [ ] New facts queued in `research\inbox\`.
