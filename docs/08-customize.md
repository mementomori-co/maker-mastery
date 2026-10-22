# 08 - Make it yours

How to set the project up for your printers and filaments, adjust the rules, add knowledge and lessons, protect your
folders, and replace the brand if you publish a fork. Next: [09 - Troubleshooting](09-troubleshooting.md).

The easiest way to make any change below is to ask Claude in the panel, for example "Add my P1S to printers.md" or
"Protect the folder E:/Finished Prints". The steps show what it should change, so you can check it.

## Make it address you your way (OWNER_PROFILE)

Claude reads an owner profile at the start of every session: your name, tone, reply format, and the things only you
decide. Until you make your own, it uses the generic example
[templates/OWNER_PROFILE.md](../templates/OWNER_PROFILE.md) and calls you "the maker".

1. In the VS Code terminal (Terminal > New Terminal), from the project folder, paste:
   `Copy-Item templates\OWNER_PROFILE.md OWNER_PROFILE.md`
2. Open the new `OWNER_PROFILE.md` in the project root and replace the example answers ("Sam") with yours: the name to
   use, tone, reply format, owner-only list and preferences. Keep the headings.
3. Start a new Claude Code session, or type "Re-read OWNER_PROFILE.md" in the panel.

Your copy is git-ignored (`/OWNER_PROFILE.md` in [.gitignore](../.gitignore)), so it stays on your PC if you publish a
fork. You can add to the owner-only list, but the no-AI-print rule applies whatever the profile says. Never put
passwords or keys in it. For how the profile fits running with fewer approvals, see
[11 - Autonomous mode](11-autonomous-mode.md).

## Your printers

1. Open [knowledge/00-gear-inventory/README.md](../knowledge/00-gear-inventory/README.md) and use its interview prompt,
   or create `knowledge\00-gear-inventory\printers.md` from the layout shown there.
2. Keep the note format so the note checker accepts it: an `Applies to:` line, a `Verified: YYYY-MM-DD` line with today's
   date, and a `Sources:` line at the end with one entry such as `- my own look at the printer, measured`.
3. Write the model exactly as Bambu Studio names it (for example `X1C`, `P1S`, `A1 mini`, `H2C`); the load check matches
   on that name.

Things that assume a particular printer, and how to adjust them:

| Where | Default | Change it when |
|---|---|---|
| `knowledge\00-gear-inventory\current-load.md` | example rows for an H2C and a P1S | always: keep only your printers' rows |
| `tools\gcode_audit.py` | allowed X range 25..325 mm (one dual-nozzle printer's shared area) | pass `--xmin 0 --xmax <bed width>` for your printer, or ask Claude to |
| `tools\audit_3mf.py` C1, C2, C7 L6 | LEFT/RIGHT extruder rules for dual-nozzle printers | written for dual-nozzle printers; on a single-nozzle printer read their lines as information (not tested on a single-nozzle 3MF) |
| `CLAUDE.md` making rule 5 | start from `0.20mm Standard @BBL <your printer>` | if your printer's standard process has another name |
| `knowledge\01-printers\` | notes on the H2C and P1S | add notes for your model with `/research-topic` |

## Your filaments

Filaments live in your load record, not in a list of what you own:

1. Each time you change a spool, update the row in `current-load.md` and the `Verified:` date.
2. Bambu spools: `**Bambu PLA Basic, Black**` (product and colour as Bambu Studio names them). The audit checks the
   filament id and the colour against Bambu Studio's catalogue.
3. Other brands: `**<Vendor> <Product>, <Colour>**`. The audit matches vendor and type, and warns that the colour cannot
   be checked against a catalogue.
4. For a filament choice with numbers and sources, ask `/material-pick`.

## Machine paths

Everything machine-specific is in `config\paths.yaml` (your copy, never committed). Each key is explained in
[config/paths.example.yaml](../config/paths.example.yaml):

- `bambu_studio_exe`: where `bambu-studio.exe` is.
- `bambu_profiles_dir`: leave empty unless the profile checks cannot find your profiles.
- `blender_exe`: optional; enables the stability render.
- `slice_workdir`: where slices go (default `work/slice`, no spaces).
- `allowed_roots`: folders the optional audit MCP server may read, for example `[".", "E:/Prints"]`.
- `protected_roots`: folders Claude must never write to, for example `["E:/Finished Prints"]`. The guard hook blocks
  every write and write-like command that targets them.

Check with `.venv\Scripts\python.exe tools\mm_config.py`.

## The rules

- The rulebook is [CLAUDE.md](../CLAUDE.md). Edit it like any text file, or ask Claude to change one rule and show you
  the diff. Keep it short: Claude reads it in every session.
- **Do not remove the no-AI-print rule** or the deny rules in `.claude\settings.json`. See [06 - Print safety](06-print-safety.md).
- Personal settings that should not be shared go in `.claude\settings.local.json`, which git ignores
  ([.claude/settings.notes.md](../.claude/settings.notes.md) explains every entry of the shared file).
- Agents are Markdown files in `.claude\agents\`, skills are folders in `.claude\skills\`. Start a new skill from
  [templates/skill/SKILL.md](../templates/skill/SKILL.md) and lint it with
  `.venv\Scripts\python.exe tools\check_skill.py .claude\skills`.

## Adding knowledge

1. The quick way: `/research-topic <your topic>`. The researcher, fact-checker and librarian do the work and file only
   verified facts.
2. By hand: copy [templates/note.md](../templates/note.md) into `knowledge\<NN-category>\<topic-in-kebab-case>.md`, keep
   its header lines and sections, give every fact its source URL, and add a one-line summary to that category's
   `index.md`. Check it: `.venv\Scripts\python.exe tools\check_note.py <your note>`.
3. Search the category first and merge into an existing note rather than adding a near-duplicate.
4. When a topic is covered and verified, tick its box in your [CURRICULUM.md](../CURRICULUM.md).
5. A new category gets a folder named with its number from the curriculum (for example `09-finishing`), an `index.md`,
   and a row in [knowledge/INDEX.md](../knowledge/INDEX.md).

## Adding lessons

After a mistake is fixed, run `/lesson-learned`, or write the file yourself in the format of
[lessons/README.md](../lessons/README.md): a title, an `Area:` line, a table with "What happened | Root cause | Rule now",
and a `How to check:` line. Add one line to [lessons/INDEX.md](../lessons/INDEX.md); that index is what the session-start
hook loads.

File names: the shipped lessons use `NN-short-slug.md`; the `/lesson-learned` skill and `CLAUDE.md` name new ones
`YYYY-MM-DD-<slug>.md`. Both work; the index line is what matters.

## Starting your own build projects

Copy [templates/project/](../templates/project/README.md) to a new folder for each build. It has its own `CLAUDE.md`,
folders for source, STLs, 3MFs and renders, and an optional spec-driven workflow.

## Replacing the brand (forks)

The Memento Mori name, crests and banners are not covered by the MIT License ([NOTICE.md](../NOTICE.md)). For a private
copy you change nothing. **If you publish a fork:**

1. Replace every image in `assets\brand\` with your own: `banner-dark.png`, `banner-light.png` (1600x420 in this
   project), `social-preview.png` (1280x640), the two SVG banners and the crest PNGs. Or delete them and remove their
   references.
2. In [README.md](../README.md), change the `<picture>` block at the top, the title and the preview image.
3. Change the project name in `README.md`, `CLAUDE.md`, `LICENSE` (the copyright line names the copyright holder),
   `CHANGELOG.md` and anywhere else it appears. Ask Claude: "Find every place the project name appears and list them".
4. The build scripts in `assets\brand\src\` are MIT code; you may reuse them for your own images
   ([assets/brand/src/README.md](../assets/brand/src/README.md) explains how).
5. Run the privacy scan on your fork before you publish (see [CONTRIBUTING.md](../CONTRIBUTING.md)).

Next: [09 - Troubleshooting](09-troubleshooting.md).
