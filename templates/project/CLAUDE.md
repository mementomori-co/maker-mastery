# <Project name> - Claude Code project memory (Memento Mori Maker Mastery project template)
<!-- <brain> in this file and in openspec\ means the folder where you put Memento Mori Maker Mastery
     (the folder that holds its CLAUDE.md, knowledge\, lessons\ and tools\). Write that full path in the
     "Brain" line of "This project" below, and replace <brain> in the three import lines with the same path,
     written with forward slashes. Claude Code imports a file named with @path/to/file
     (https://code.claude.com/docs/en/memory). Never wrap these lines in an OpenSpec-managed marker block
     (OPENSPEC:START/END): OpenSpec's legacy cleanup deletes such blocks. -->
@<brain>/CLAUDE.md
@<brain>/knowledge/INDEX.md
@<brain>/lessons/INDEX.md

## Constitution
Non-negotiables for this build. Declarative and testable; every change gets a **Constitution check**
(`openspec/changes/<name>/constitution-check.md`, one row per principle, before a proposal is written; repeated in design).
A conflict is CRITICAL and is fixed by changing the idea, option or scope, never by softening a principle.

I. **Plan before build.** No CAD, slicing or code until `openspec/changes/<name>/tasks.md` exists and the maker approved the proposal.
II. **Verified on the real thing.** Every print file is sliced with the installed Bambu Studio CLI; `result.json` and the
   G-code are read; the real STL is rendered before a part is called right. Evidence lives in `_tests/` and `renders/`.
III. **Physical load first.** No print file is built before AMS slots, nozzles and plate are confirmed with the maker and recorded in
   `<brain>\knowledge\00-gear-inventory\current-load.md`.
IV. **One material per part** unless multi-material is the point; clear parts are separate pieces held mechanically.
V. **Source or label.** Every hardware, material or slicer number cites a full URL or a brain note path, carries its
   condition (printer, nozzle, plate, load), or is labeled "not verified".
VI. **Script beside output.** Every file in `out/` has its generating script in `src/`; nothing prints on a print-qa FAIL
   or an incomplete `<brain>\templates\preprint-checklist.md`.
VII. **The brain is the source of truth.** Rules and facts are never copied into this repo; lessons and facts are written back
   (see Write-back). `openspec/specs/` is the source of truth only for how this project's parts behave.
VIII. **No AI ever starts, sends, uploads or queues a print.** Claude prepares and checks print files; the maker reviews the
   checklist and presses Print in Bambu Studio.

Amendments: MAJOR = a principle removed or redefined, MINOR = a principle added, PATCH = wording. The maker ratifies; bump the footer.
**Version**: 1.0.0 | **Ratified**: <YYYY-MM-DD> | **Last amended**: <YYYY-MM-DD>

## This project
- **Name / purpose**: <name> - <one sentence>
- **Brain**: <full path of your Memento Mori Maker Mastery folder>
- **Printer**: <model, from <brain>\knowledge\00-gear-inventory\> - nozzle(s): <0.4 ...> - plate: <Textured PEI | Smooth PEI | ...>
- **Materials** (copy from `<brain>\knowledge\00-gear-inventory\current-load.md`, dated): <slot -> brand / material / colour>
- **Part list**: <part-a>, <part-b>, ... (one `<brain>\templates\part-spec.md` block per part, filed under `openspec/specs/<part>/`)
- **Approvals**: <what the maker approves before the first slice> - <what the maker approves before the first print>
- **Status**: <idea | assessed | proposed | building | printed | archived>

## OpenSpec workflow (schema `maker`)
- `/opsx:*` runs in the Claude Code panel; `openspec ...` runs in the VS Code terminal (see `README.md`).
- Order per change: `assessment.md` (VERDICT: go) -> `constitution-check.md` (GATE: PASS) -> `proposal.md` -> `specs/` + `design.md`
  -> `tasks.md` -> apply -> archive. A `needs-clarification` or `kill` verdict stops the change there.
- Spec format: `### Requirement:` + one SHALL sentence, `#### Scenario:` with WHEN / THEN; behaviour only - profile and
  material values go in `design.md`. `openspec/changes/<name>/.openspec.yaml` is created by OpenSpec, never by hand.
- `/opsx:archive` only after the part printed and was measured against the spec. Say "file the lesson", not "archive", to
  keep the OpenSpec archive skill from firing on lesson work.

## Layout
- `openspec/` - OpenSpec tree: `specs/` (source of truth for part behaviour, grows by archive), `changes/<name>/`,
  `changes/archive/`, `config.yaml` (schema `maker`, gear context, per-artifact rules), `schemas/maker/` (forked workflow).
- `src/` - generating scripts (Python code-CAD, Blender scripts), one per part, named like its output.
- `out/stl/`, `out/3mf/` - outputs only; every file has its script in `src/`.
- `renders/` - renders of the real STL/3MF, named `<part>-<view>-<YYYY-MM-DD>.png`.
- `_tests/` - slice logs, `result.json`, G-code audits, print-qa records, measurements.
- `lessons/` - pointer lines only (`- <brain>\lessons\YYYY-MM-DD-<slug>.md - one line`); the lesson text lives in the brain.
- `.claude/settings.json` - project hooks (path guard, note check), made from `.claude/settings.example.json`; `.claude/rules/` - project-only path-scoped rules.

## Write-back
- **Lessons**: every mistake -> `<brain>\lessons\YYYY-MM-DD-<slug>.md` (root cause + the rule that prevents it),
  one pointer line in this repo's `lessons/`.
- **Facts**: anything learned about hardware, materials or slicer goes `/research-one` -> `/verify` -> `/file` into
  `<brain>\knowledge\` with `Applies to:` naming the printer and conditions; this repo links the note, never copies the numbers.
- **Gear state**: what is loaded -> `<brain>\knowledge\00-gear-inventory\current-load.md` (dated), not here.
- **Sources**: every URL or repo reused -> `<brain>\sources\registry.md`.
