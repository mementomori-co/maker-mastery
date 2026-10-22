# v1.0.0 — First Light

Maker Mastery is a Claude Code operating system for makers: rules, a cited knowledge library, specialist agents and
checking tools that turn Claude Code into a careful workshop partner for 3D printing, CAD, electronics, rendering and
more. 3D printing on Bambu Lab printers is the flagship: Claude Code researches, designs, slices and audits your files,
and you build and print.

> **No AI ever starts, sends, uploads or queues a print.** Claude Code, every agent, skill, command, hook and tool here
> may design, slice, audit and prepare print files. Only you press Print, in Bambu Studio, after you have read the
> pre-print checklist. The rule is written into the rules and enforced in `.claude/settings.json`.

## Highlights

- **Knowledge library: 94 notes in 16 domains**, every fact linked to its public source:
  - Printing: 01 printers (7), 02 Bambu Studio (19), 03 materials (11), 04 design for FDM (3), 12 failure
    diagnosis (3), 40 Bambu ecosystem (4).
  - Modeling and rendering: 05 CAD, hard surface (3), 06 organic modeling (1), 24 surfacing and rendering (5),
    26 AI to 3D (2).
  - Engineering and electronics: 07 engineering (6), 08 electronics and lighting (13), 39 Raspberry Pi and
    microcontrollers (4).
  - AI tooling and safety: 41 MCP (2), 42 agent engineering (7), 44 safety (4).
  - Plus a fill-in template for your own gear (`knowledge/00-gear-inventory/`) and the full domain map as a learning
    tracker in `CURRICULUM.md`.
- **Claude Code layer: 22 agents, 30 skills and 5 slash commands** in `.claude/`: research, independent
  fact-checking, filing knowledge, CAD and sculpting, design-for-FDM review, slicer questions, materials, electronics,
  safety sheets and the print-quality gate.
- **Tools: 27 files.** 21 Python tools in `tools/`, 3 Claude Code hook scripts in `tools/hooks/`, 2 MCP scripts in
  `tools/mcp/` (a read-only audit server) and the `tools/setup.ps1` setup script. They slice with the Bambu Studio
  command line and audit the 3MF, the G-code, the prime tower clearance, overhangs and how much of a part support hides.
- **Tests: 229 automated checks in 15 test files** in `tools/tests/`, run tool by tool by `tools/selftest.py`. No test
  needs Bambu Studio, Blender or the internet. On the build PC 2 of them were skipped because the PyYAML package was
  not installed in that Python; setup installs it from `requirements.txt`.
- **20 lessons** in `lessons/`: general post-mortems, each ending with the rule it created.
- **Privacy scanner** (`tools/privacy_scan.py`): checks file contents, file names, image metadata, ZIP and 3MF members
  and PDF metadata for user-folder paths, e-mail addresses, private IP addresses, secrets, printer-serial-like strings
  and your own denylist, before you share a folder or a fork. `tools/strip_metadata.py` removes personal metadata from PNG, JPEG and 3MF/ZIP files.
- Print-quality gate and pre-print checklist: nothing is called ready until a second, independent check has passed.
- Beginner guides in `docs/` (install, first run, daily workflow, print safety, tools reference, customizing,
  troubleshooting, FAQ) and a calibration-cube example.
- **Install guide for every system and method** (`docs/02-install.md`): Windows 11, macOS (Apple silicon and Intel)
  and Ubuntu; direct download, winget, Homebrew, apt and the vendor's own installer for each app, every package id and
  command read from the official source, each app with a "check it worked" command.
- **Install and check scripts** in `install/`: `windows.ps1` (winget), `macos.sh` (Homebrew) and `linux.sh` (Ubuntu)
  list what they would install, ask y/N per app, skip what is already there, log to `install/install.log` and have a
  dry-run mode; `check.ps1` and `check.sh` print a read-only PASS/FAIL table with versions. The Claude Code command
  line is optional (the VS Code extension works on its own), and the scripts point to Anthropic's native installer,
  which updates itself, before offering winget or Homebrew.
- **Recommended VS Code extensions** in `.vscode/extensions.json` (Claude Code, Python, YAML, Mermaid preview,
  markdownlint), so VS Code offers them when you open the folder; IDs and reasons in `docs/04-first-run.md`.
- **Autonomy guide** (`docs/11-autonomous-mode.md`): permission modes, allow, ask and deny rules, what the shipped
  settings always deny, why the skip-all-permissions flag belongs only in a throwaway VM, parallel and background
  subagents, and the two-brain workflow with Claude Desktop.
- **Owner profile** (`templates/OWNER_PROFILE.md`): a generic example of how Claude addresses you, its reply format
  and the owner-only list (prints, purchases, installs, sign-ins, secrets, deletions, publishing, messages). Copy it to
  `OWNER_PROFILE.md`; `CLAUDE.md` reads it first.
- **The Memento Mori crest family** in `assets/brand/`: the printing crest as the main logo, the parent, streaming and
  apparel crests in the README (dark and light versions), and `org-avatar-500.png` for a GitHub organization's
  profile picture (steps in `docs/PUBLISHING.md`).
- **`constraints.txt`**: the exact version of every package a fresh install of `requirements.txt` produced; setup
  installs with it, so a new install gets the tested versions.
- **Hardened folder guard** (`tools/hooks/guard_paths.py`): follows junctions and symlinks, expands 8.3 short names,
  maps `\\?\` and network-share spellings back to the drive, fails closed when `config/paths.yaml` cannot be read, and
  is set to block the call when the guard itself cannot run (`"onFailure": "block"`, Claude Code v2.1.295 or later).

## Requirements

- Windows 11 (tested). The macOS and Linux install guides cover the prerequisites; running the project there is
  planned for v1.1.
- Python 3.12.
- VS Code with the Claude Code extension, and an Anthropic account that can use Claude Code. The Claude Code command
  line is optional.
- Claude Code v2.1.295 or later (the VS Code extension's version counts). The guard hook in `.claude/settings.json`
  uses `"onFailure": "block"`, which needs that version ([hooks reference](https://code.claude.com/docs/en/hooks)).
  How to check:
  [Check your Claude Code version](https://github.com/mementomori-co/maker-mastery/blob/main/docs/02-install.md#check-your-claude-code-version).
- Bambu Studio (for slicing and the print audits; the library, agents and most tools work without it).
- Git is recommended, but not required: you can use the ZIP instead.

## Install

Download `maker-mastery-v1.0.0.zip` below, or clone the repository. Then follow the install guide, click by click, or
use the install scripts in `install/` (try the dry run first):
[docs/02-install.md](https://github.com/mementomori-co/maker-mastery/blob/main/docs/02-install.md).

## What's next

**v1.1: the full library.** The remaining domains of the map, including game design and game development, plus
finishing, calibration and testing, workflows, project ops, creative direction, selling and IP, reference sheets,
scanning, media, and data and backups. Each domain goes through the same source and privacy review first.

## Known limitations

- **Windows only for running the project.** The setup script and the hooks assume Windows 11. macOS and Linux are not
  tested: the macOS and Linux install and check scripts only had a syntax check, and nothing was run on a Mac or on
  Linux.
- **The install scripts were not run as real installs.** `install/windows.ps1` was run as a dry run only (on a PC that
  already had the apps), `install/check.ps1` was run for real (it only reads), and no script has installed an app yet.
- **The guard hook is a safety net, not a sandbox.** It only sees paths written in the command text; a path built
  inside a script, or a deletion outside your protected folders, gets past it. Its fail-closed setting needs Claude
  Code v2.1.295 or later; an older version that ignores the setting lets the call through when the guard cannot start (what older versions do is not documented). See
  `docs/11-autonomous-mode.md`.
- **The small crest icons are clearest on high-density screens.** The 40-pixel icons in the README are exported at
  twice that size and shown at 40 px, so on a standard-density screen their fine detail is soft.
- **The family strip and footer crest have a soft dark outline on light backgrounds, on purpose.** It keeps their white
  lettering readable on GitHub's light theme.
- **Some UI labels are not verified.** A button or menu name marked "(label not verified)" was not found in the
  official docs; your screen may word it differently.
- **Knowledge is verified as of the date on each note.** Printers, firmware, slicers and materials change; check the
  linked source when a note's `Verified:` date is old.
- **Not yet tested by an outside user.** The tools pass their self-test, but no one outside the project has yet run
  the whole kit inside a live Claude Code session. Please report what breaks.

## Checksums

SHA-256 of maker-mastery-v1.0.0.zip: <filled at packaging>

---

Unofficial community project. Not affiliated with or endorsed by Anthropic or Bambu Lab. Claude and Bambu Lab are
trademarks of their owners.
