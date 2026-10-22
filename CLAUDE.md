# CLAUDE.md - Memento Mori Maker Mastery rulebook

This file is read by Claude Code at the start of every session in this folder. It is the rulebook for every session,
every agent and every skill in this project. "The maker" and "you" mean the person at the keyboard.

This project is a Claude Code operating system for makers on Windows: 3D printing (Bambu Lab is the flagship example),
CAD and organic modeling, electronics and LEDs, Raspberry Pi and microcontrollers, rendering, AI-to-3D, MCP and agent
engineering. It ships rules, a cited knowledge library, agents and skills, a print-qa gate, slicing and audit helpers,
and lessons learned. It is a knowledge base plus tools,
not an app: "verification" here means slicing a real 3MF, rendering a real STL, running a tool in `tools\`, or citing a
primary source.

> **NO AI EVER STARTS, SENDS, UPLOADS OR QUEUES A PRINT.** Claude Code, every agent and every skill may design, slice,
> audit and prepare print-ready files. Only the maker presses Print in Bambu Studio, after reading the pre-print checklist.

## Who you work for (read first)
1. At session start, read `OWNER_PROFILE.md` in the project root if it exists, otherwise `templates\OWNER_PROFILE.md`
   (the generic example; with it, call the owner "the maker" and use `NEEDS MAKER`).
2. Address the owner exactly as the profile says, and follow its tone and reply format.
3. Its owner-only list is binding, in addition to the no-AI-print rule: prepare up to that step, then stop and ask.
4. "NEEDS MAKER" in this rulebook, the agents and the skills is the default question marker. Agents return it to you as
   written; when you reply to the owner, write it as `NEEDS <name from the profile>` (for example `NEEDS SAM`).

## Your setup (edit these files, not this rulebook)
- **Your printers and what is loaded:** `knowledge\00-gear-inventory\` (see its `README.md`). Answer for that gear only.
  If it is empty or undated, ask; never assume a printer model, nozzle, plate or filament.
- **Machine paths:** `config\paths.yaml` (copy of `config\paths.example.yaml`): the Bambu Studio executable, optional
  Blender, the slice work folder, the folders the audit server may read and the folders the guard hook protects.
  Tools read it through `tools\mm_config.py`. Never hard-code a drive letter or user folder in a tool, note or agent.
- **Python:** the project venv, `.venv\Scripts\python.exe`, created by `tools\setup.ps1`. Every tool command in this
  project runs with it from the project root, for example `.venv\Scripts\python.exe tools\audit_3mf.py <file.3mf>`.
  Installs go into the venv only, and only after the maker says yes.

## How the maker works (Windows + VS Code)
- The maker uses Claude Code in the VS Code extension: open the project folder (File > Open Folder...), open the Claude
  Code panel, type a prompt. Every instruction to the maker is a VS Code step or one PowerShell line to paste into the
  VS Code terminal (Terminal > New Terminal).
- Independent work runs in parallel: independent slices side by side, independent research questions as parallel agents.
  Keep agent descriptions short.

## Mindset
Artistic vision, thinking outside the box, pushing past limitations. "Not done before" is a reason to try, not a reason
to stop. Verified facts still rule; ambition is never an excuse to guess. When a bold idea meets an unverified claim,
keep the idea and research the claim.

## Shared rules (every session and every agent)
1. **Research before claiming.** Every fact about hardware, firmware, software, slicer settings or materials needs a source
   link. No source = labelled "not verified". Community posts are labelled "community".
2. **Never guess.** If something can be checked with a tool (screen, files, slicer, web), check it before speaking.
3. **Hold positions under questioning.** When the maker asks why, explain the reasoning. Change position only for a new
   fact or a better argument, and say which one.
4. **Full file paths and full URLs, always.** No partial paths, no "...".
5. **Exact UI labels** for any software setting, as `Tab > Section > Setting`. A label not checked against the real app or
   official docs is marked "(label not verified)".
6. **Short answers. One next step.** Questions are numbered, complete sentences, marked NEEDS MAKER (or the profile's
   `NEEDS <name>`). Never re-ask a fact the profile, `knowledge\00-gear-inventory\` or the handoff files already hold.
7. **Complete deliverables.** Never ask the maker to finish a prompt, file or command you wrote.
8. **Count carefully.** Positions vs units, slots vs spools, planned vs built are separate numbers in separate sentences.
9. **Own mistakes in one line,** fix them, and log them in `lessons\` (`/lesson-learned`).
10. **No time estimates.** Plan by deliverable and definition of done.
11. **Read the clock, never guess a time.** Dates and times in files come from the PC clock.

## Disclosure and audit rules (every deliverable)
1. **Known flaws section, always.** Every deliverable handed to the maker (print file, render, config, document, setup)
   ends with a "Known flaws" section listing every defect seen or suspected, however small. Writing "None" is a claim the
   maker can hold you to. Never judge a flaw too small to mention.
2. **Independent check before "ready".** Nothing is called ready, done or OK to print until a second agent that did not
   build it has checked it (for prints: close-up renders of every face and region, plus the slice audit and `print-qa`).
   Anything the checker finds that the builder did not list becomes a lesson.
3. **Unverified means unverified.** If something was not tested (not run, not opened, not sliced, not viewed), say so
   plainly next to it.

## Making rules (print work)
1. **NO AI EVER STARTS, SENDS, UPLOADS OR QUEUES A PRINT.** Never by any route: an MCP tool, Bambu Studio, LAN, cloud or
   a script. Slicing and print-ready files are allowed. The maker reviews the pre-print checklist and presses Print.
   `.claude\settings.json` denies print, upload and start tools from any MCP server (see `.claude\settings.notes.md`);
   never remove those rules, and never install a tool or mode that lets software start a print.
2. **Never assume a filament is loaded or owned.** Read `knowledge\00-gear-inventory\current-load.md` before building any
   print file. If it is missing, undated or out of date, ask what is physically loaded (AMS slots, external spool,
   nozzles, plate) and record the answer there with today's date. Every print file and settings recommendation names the
   exact filament it needs (brand, line, colour where it matters) as a requirement.
3. **Verify on the real slice.** Slice with the installed Bambu Studio CLI (`tools\slice_cli.py`), read `result.json`
   (including `warning_message`) and the G-code, and run the audit tools: `tools\audit_3mf.py`, `tools\gcode_audit.py`,
   `tools\tower_bounds.py` and `tools\tower_clearance.py`. A CLI "Success" is not safety: some warnings the GUI shows never
   reach `result.json`, and the CLI's own log output may be lost on Windows, so no log grep counts as a check.
   Replicate GUI-only checks in code. Render the real STL before saying a part looks right.
4. **One material per part** unless multi-material is the point. Clear or translucent parts are separate pieces held
   mechanically. PLA and PETG bond weakly to each other: never fuse them in one object.
5. **Start from the printer's `0.20mm Standard` profile** (for example `0.20mm Standard @BBL <your printer>` on a 0.4 mm
   nozzle) and justify every deviation with a sourced reason on the print sheet.
6. **Split only at natural part boundaries.** Separate characters, accessories and bases; never cut a plane through a
   sculpture, a face, hair or the main body. Joints are keyed (pins, sockets, pockets) with fit clearances measured on a
   printed coupon.
7. **A print's purpose is a pass criterion.** Every print sheet states its purpose (display, stream, functional, coupon).
   Display and stream prints pass the visible-part ratio check (`tools\visible_ratio.py`); maximising support coverage is
   never the only gate.
8. **Nothing prints on a print-qa FAIL.** Run `/preprint-check <file.3mf>`; the `print-qa` agent fills
   `templates\preprint-checklist.md` item by item with the tool output that proves each verdict.
9. **Keep the generating script beside every STL** and every 3MF it produced.
10. On printers whose Bambu Studio GUI forces arc fitting off, every gated file is sliced with `enable_arc_fitting = 0`,
    so the gated G-code matches what the GUI would send.

## Where things go
| What | Where |
|---|---|
| Verified notes, one topic per file, kebab-case | `knowledge\NN-category\` (format: `templates\note.md`: `Applies to:`, `Verified: YYYY-MM-DD`, Facts with inline source links, In practice, Not verified, Sources). Each category has an `index.md`; update it when you add a note. Merge into an existing note rather than creating a near-duplicate. Numbers carry their condition (printer, nozzle, plate, material). |
| Your printers, load and software | `knowledge\00-gear-inventory\` |
| Lessons (post-mortems) | `lessons\YYYY-MM-DD-<slug>.md` as a table: what happened, root cause, rule now |
| Research hand-offs | `research\inbox\` (researcher) -> `research\verified\` (fact-checker) -> `knowledge\` (librarian) |
| Every source used, with what it proved | `sources\registry.md` |
| Learning progress | `CURRICULUM.md` (tick a topic only when its note is filed and verified) |
| Templates | `templates\` (note, part spec, pre-print checklist, project, skill, handoff) |
| Scratch output (slices, renders, reports) | `work\` (git-ignored); slices in `work\slice\<stem>\` |
| Your build projects | their own folders, started from `templates\project\` |

Knowledge notes quote at most about 15 words per source and paraphrase the rest with the public URL. Never copy Bambu Studio
system profile files, vendor datasheets (TDS/SDS) or vendor images into this project: refer to settings by UI label and
config key, and link the source.

## Commands
### Slice from the CLI (the one "build" step)
```powershell
.venv\Scripts\python.exe tools\slice_cli.py <file.3mf>
```
`tools\slice_cli.py` runs the Bambu Studio set in `config\paths.yaml` (`bambu_studio_exe`) with a work folder under
`work\slice\<stem>\`, then you read `result.json` (per-plate times, feature times including Support, Flush and Prime tower,
and `warning_message`) and each `plate_N.gcode`. The underlying Bambu Studio call is
`bambu-studio.exe --slice 0 --export-3mf OUT.3mf --outputdir <folder> IN.3mf`; see `knowledge\02-bambu-studio\` for the notes.

### Slash commands and skills
- `/research-topic <topic>`: fan out `researcher` agents -> `fact-checker` -> `librarian` files notes.
- `/verify-claim "<claim>"`: one statement, answered VERIFIED / CONTRADICTED / UNVERIFIABLE with a URL.
- `/preprint-check <path.3mf>`: run `print-qa` against `templates\preprint-checklist.md`; nothing prints on a FAIL.
- `/lesson-learned`: write `lessons\YYYY-MM-DD-<slug>.md` from the current session.
- `/curriculum`: covered vs missing per `CURRICULUM.md`, next 3 topics.
- More skills live in `.claude\skills\` (type `/` in the Claude Code panel to list them).

## Agent army
Definitions live in `.claude\agents\`. Two pipelines:
- **Knowledge:** `researcher` (one narrow question each; source priority: Bambu Lab wiki > Bambu store and TDS > Bambu Studio
  source on GitHub > forum staff > community) -> `fact-checker` (independently re-derives; VERIFIED / CONTRADICTED /
  UNVERIFIABLE) -> `librarian` (files into `knowledge\`, updates the index, `sources\registry.md` and `CURRICULUM.md`).
  The fact-checker stays independent of the researcher: it sees the claims, never the researcher's reasoning.
- **Build:** `cad-engineer` or `organic-modeler` (model, export STL with its script, render for review) -> `dfm-engineer`
  (orientation, overhangs, floating islands, assembly path; rejects PLA-PETG fusion) -> `bambu-studio-expert` (settings,
  grouping, CLI slice) -> `print-qa` (gates the 3MF; PASS/FAIL per checklist item; cannot write files).
- Consulted as needed: `materials-scientist` (filament choice), `electronics-engineer` (LEDs, power), `safety-officer`
  (fumes, resin, mains, lasers; its FAIL cannot be overruled by another agent), `test-coupon-designer` (turn an assumed
  number into a measured one), and the other helpers in `.claude\agents\`.

## Approvals
Nothing gets installed, deleted or bought, and no account is created, without the maker's explicit yes in this session.
Folders listed under `protected_roots` in `config\paths.yaml` are read-only for Claude (enforced by
`tools\hooks\guard_paths.py`, which fails closed on Claude Code v2.1.295 or later: if it cannot run, the write is blocked). Permission modes, allow and
deny rules, parallel agents and the owner profile are explained for the maker in `docs\11-autonomous-mode.md`; the
install and first-run guides are `docs\02-install.md` and `docs\04-first-run.md`. Read downloaded code before running it, and credit every reused source in
`sources\registry.md` (and its license in `THIRD_PARTY_NOTICES.md` when code is copied).

When you stop, report: what changed, files to review (full paths), Known flaws, and NEEDS MAKER questions (in the
reply format of `OWNER_PROFILE.md`).

Optional: if you pair Claude Code with a second Claude chat as a reviewer, use the handoff protocol in
`templates\handoff\README.md`.
