<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brand/banner-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/brand/banner-light.png">
    <img alt="Memento Mori Maker Mastery banner: crest and title" src="assets/brand/banner-light.png" width="100%">
  </picture>
</p>

<h1 align="center">MEMENTO MORI · MAKER MASTERY</h1>

<p align="center"><strong>A Claude Code operating system for makers — 3D printing, CAD, electronics, rendering, game dev and more. Research-backed, AI-checked, human-built.</strong></p>

Maker Mastery turns Claude Code into a careful workshop partner for any maker: 3D printing, CAD, electronics, rendering and more.
Its flagship is 3D printing on Bambu Lab printers, where Claude Code slices, audits and gates your files, and you press Print.

<!-- Badges. <owner> is the GitHub account name, filled in when the repository is published. -->
<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-2ea44f"></a>
  <a href="docs/02-install.md"><img alt="Platform: Windows 11" src="https://img.shields.io/badge/platform-Windows%2011-0078D6"></a>
  <a href="https://code.claude.com/docs/en/vs-code"><img alt="Built for Claude Code" src="https://img.shields.io/badge/Claude%20Code-VS%20Code%20extension-D97757"></a>
  <a href="https://wiki.bambulab.com/"><img alt="Bambu Lab ready" src="https://img.shields.io/badge/Bambu%20Lab-ready-00AE42"></a>
  <a href="https://www.python.org/downloads/windows/"><img alt="Python 3.12" src="https://img.shields.io/badge/python-3.12-3776AB"></a>
  <!-- <owner> below is filled in at publish time. -->
  <a href="https://github.com/<owner>/maker-mastery/releases"><img alt="Release downloads" src="https://img.shields.io/github/downloads/<owner>/maker-mastery/total"></a>
</p>

> [!IMPORTANT]
> **No AI ever starts, sends, uploads or queues a print.** Claude Code, every agent, every skill and every tool here may
> design, slice, audit and prepare print files. Only **you** press Print in Bambu Studio, after you have read the
> pre-print checklist. See [docs/06-print-safety.md](docs/06-print-safety.md).

## Contents

- [What is this](#what-is-this)
- [Why](#why)
- [Preview](#preview)
- [Domains](#domains)
- [How it works](#how-it-works)
- [Quick Start](#quick-start)
- [Guides](#guides)
- [FAQ](#faq)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## What is this

Maker Mastery is a ready-made project folder that you open in VS Code with the Claude Code extension. It gives Claude a
rulebook ([CLAUDE.md](CLAUDE.md)), a cited knowledge library ([knowledge/](knowledge/INDEX.md)), a team of specialist
agents and skills ([.claude/](.claude/)), checking tools ([tools/](tools/)) and a set of lessons learned
([lessons/](lessons/INDEX.md)). Ask it to research a material, design a bracket, plan an LED power budget, check a
render or prepare a print, and it works from sourced facts, checks its own output with real tools, and tells you what it
could not verify. 3D printing is the flagship example: Claude can slice your 3MF with the Bambu Studio you installed,
audit the project and the G-code, and fill a pre-print checklist, and then the last step, pressing Print, is always yours.

## Why

- **Facts with sources, not guesses.** Every fact in the library links its public source; anything unchecked is labelled
  "not verified", and a fact-checker that never sees the researcher's reasoning re-derives each claim.
- **Gates that use the real slice.** Print files are judged from the sliced G-code and the 3MF itself, by tools with
  their own tests, so a clean-looking preview cannot hide a bad plate.
- **You stay in charge.** Nothing is installed, deleted or printed without you. A hook blocks Claude's file tools and
  common shell writes into folders you protect (a safety net, not a sandbox; see
  [troubleshooting, section 14](docs/09-troubleshooting.md#14-claudes-command-was-blocked-by-guard_paths)), and the
  print rule is enforced in settings as well as in the rules.

## Preview

Real output from the shipped tools, run on small synthetic test files. Long lines are cut short with `...`; the full
samples are in [docs/tool-sample-outputs.md](docs/tool-sample-outputs.md).

**`tools/audit_3mf.py`** checks a sliced 3MF against your recorded filament load (excerpt):

```text
3MF audit: part.3mf
  printer=Bambu Lab H2C 0.4 nozzle  process=0.20mm Standard @BBL H2C  bed=Textured PEI Plate
  [OK] C7: L1: load_filled.md Verified: 2026-01-08 (2 day(s) before 2026-01-10)
  [OK] C7: L4: filament 1 filament_colour #000000 is a catalogue colour of Bambu PLA Basic ...
  [OK] C15: process preset '0.20mm Standard @BBL H2C' = the printer's default, ...
  [WARN] C8: filament 1 profile 'Bambu PLA Basic @BBL H2C' not found in the installed ...
VERDICT: WARN
```

**`tools/overhang_gate.py`** finds an unsupported overhang on a T-shaped test part:

```text
t_shape  pose (0.0, 0.0, 0.0)  watertight  24 faces  posed bbox [[-15.0, -5.0, 0.0], ...]
  overhang below 30 deg: 300.0 mm2 (min angle 0.0; bbox [[-15.0, -5.0, 20.0], ...])
  [WARN] per-layer cantilever 10.00 mm at posed z 20.10 (1 layer(s) over 0.5 mm, ...)
VERDICT: WARN
```

**`tools/tower_clearance.py`** measures the prime tower's gap to every object from the G-code:

```text
plate_1.gcode: tower all-layers [200.0, 200.0, 215.0, 215.0] ... (rule: gap >= 8.0 mm)
  [OK] object 1: bounds [100.0, 100.0, 136.0, 120.0] gap body 113.14 mm, first-layer 113.14 mm
  VERDICT: OK
```

## Domains

The domain map is numbered from 00 to 44. Version 1.0 ships 16 knowledge domains (✅) plus the gear template; the rest
arrive in v1.1 (⏳).
Track your own progress in [CURRICULUM.md](CURRICULUM.md).

| # | Making | Status |
|---|---|---|
| 00 | [Your gear (template)](knowledge/00-gear-inventory/README.md) | ✅ v1.0 (template) |
| 01 | [Printers](knowledge/01-printers/index.md) | ✅ v1.0 |
| 02 | [Bambu Studio](knowledge/02-bambu-studio/index.md) | ✅ v1.0 |
| 03 | [Materials](knowledge/03-materials/index.md) | ✅ v1.0 |
| 04 | [Design for FDM](knowledge/04-design-for-fdm/index.md) | ✅ v1.0 |
| 05 | [CAD, hard surface](knowledge/05-cad-hard-surface/index.md) | ✅ v1.0 |
| 06 | [Organic modeling](knowledge/06-organic-modeling/index.md) | ✅ v1.0 |
| 07 | [Engineering](knowledge/07-engineering/index.md) | ✅ v1.0 |
| 08 | [Electronics and lighting](knowledge/08-electronics-lighting/index.md) | ✅ v1.0 |
| 09 | Finishing | ⏳ v1.1 |
| 10 | Workflows | ⏳ v1.1 |
| 11 | Calibration and testing | ⏳ v1.1 |
| 12 | [Failure diagnosis](knowledge/12-failure-diagnosis/index.md) | ✅ v1.0 |
| 13 | Project ops | ⏳ v1.1 |

| # | <img src="assets/brand/crest-streaming-icon.png" width="40" align="absmiddle" alt="STREAM crest"> Creative, business and design | Status |
|---|---|---|
| 14 | Creative mindset | ⏳ v1.1 |
| 17 | Creative direction | ⏳ v1.1 |
| 18 | Selling 3D prints | ⏳ v1.1 |
| 20 | Woodworking | ⏳ v1.1 |
| 21 | MakerWorld | ⏳ v1.1 |
| 22 | IP and licensing | ⏳ v1.1 |
| 24 | [Surfacing and rendering](knowledge/24-surfacing-and-rendering/index.md) | ✅ v1.0 |
| 25 | Reference sheets | ⏳ v1.1 |
| 26 | [AI to 3D](knowledge/26-ai-to-3d/index.md) | ✅ v1.0 |
| 27 | Scanning and photogrammetry | ⏳ v1.1 |

| # | <img src="assets/brand/crest-streaming-icon.png" width="40" align="absmiddle" alt="STREAM crest"> Games, media, AI, tech and safety | Status |
|---|---|---|
| 28 | Game design | ⏳ v1.1 |
| 29 | Game development | ⏳ v1.1 |
| 30 | Visual pre-production | ⏳ v1.1 |
| 31 | Retro arcade | ⏳ v1.1 |
| 32 | Audio and sound | ⏳ v1.1 |
| 33 | Animation and motion | ⏳ v1.1 |
| 34 | Video editing | ⏳ v1.1 |
| 35 | AI image and video | ⏳ v1.1 |
| 37 | Photography | ⏳ v1.1 |
| 39 | [Raspberry Pi and microcontrollers](knowledge/39-raspberry-pi-and-microcontrollers/index.md) | ✅ v1.0 |
| 40 | [Bambu ecosystem](knowledge/40-bambu-ecosystem/index.md) | ✅ v1.0 |
| 41 | [MCP](knowledge/41-mcp/index.md) | ✅ v1.0 |
| 42 | [Agent engineering](knowledge/42-agent-engineering/index.md) | ✅ v1.0 |
| 43 | Data and backups | ⏳ v1.1 |
| 44 | [Safety](knowledge/44-safety/index.md) | ✅ v1.0 |

Numbers missing from the map are reserved and are not part of this project.

### The Memento Mori family

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brand/family-strip-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/brand/family-strip-light.png">
    <img alt="The four Memento Mori crests: MAKE · STREAM · CREATE · MEMENTO MORI" src="assets/brand/family-strip-light.png" width="572">
  </picture>
</p>

## How it works

### The system

```mermaid
flowchart TB
    you(["You"])
    subgraph vscode["VS Code"]
        cc["Claude Code"]
    end
    subgraph project["Project folder"]
        rules["CLAUDE.md"]
        know["Knowledge"]
        agents["Agents"]
        tools["Tools"]
        lessons["Lessons"]
    end
    bs["Bambu Studio"]
    printer["Printer"]
    you <--> cc
    cc <--> rules
    cc <--> know
    cc <--> agents
    cc <--> tools
    cc <--> lessons
    tools -- "slice + audit" --> bs
    you == "YOU press Print" ==> bs
    bs ==> printer
```

### The knowledge pipeline

```mermaid
flowchart TD
    q["A question"] --> r["researcher: claims with source URLs"]
    r --> fc["fact-checker: re-derives each claim on its own"]
    fc -- "VERIFIED" --> lib["librarian: files the note and updates the index"]
    fc -- "CONTRADICTED or UNVERIFIABLE" --> r
    lib --> k[("knowledge library")]
    lib -. "optional" .-> h["handoff file: plan/handoff/TO_CHAT.md"]
    h -. "you paste it" .-> rev["reviewer Claude chat"]
    rev -. "you paste the reply" .-> q
```

### The print-qa gate

```mermaid
flowchart TD
    d["Design: CAD or sculpt, STL with its script"] --> dfm["DFM review: orientation, overhangs, islands"]
    dfm --> s["Slice with the Bambu Studio CLI"]
    s --> a["Audits: audit_3mf, gcode_audit, tower_clearance, overhang_gate, visible_ratio"]
    a --> g{"print-qa checklist"}
    g -- "FAIL" --> fix["Fix the one thing it names"]
    fix --> d
    g -- "PASS" --> you["You read the checklist"]
    you --> p["YOU press Print in Bambu Studio"]
```

## Quick Start

**Platform:** Windows 11 is tested. The macOS and Linux install guides cover the prerequisites; running the project
there is planned for v1.1.

1. **Install the free tools:** Git, VS Code, Python 3.12, the Claude Code extension for VS Code and Bambu Studio. The
   Claude Code command line is optional: the VS Code extension works on its own. You need **Claude Code v2.1.295 or
   later (the VS Code extension's version counts)**, because the project's guard hook uses `"onFailure": "block"`
   ([how to check your version](docs/02-install.md#check-your-claude-code-version)). Every app, every system and every
   install method, click by click: [docs/02-install.md](docs/02-install.md).
   - **Quick route on Windows:** the [install scripts](install/README.md) ask y/N for each app and install nothing
     without your yes. They live in the project folder, so download the ZIP first (step 2). Then, in PowerShell in
     the project folder, run `install\windows.ps1` (try `-DryRun` first) and check the result with `install\check.ps1`
     ([the quick route](docs/02-install.md#the-quick-route-install-scripts)):

     ```powershell
     powershell -ExecutionPolicy Bypass -File install\windows.ps1 -DryRun
     powershell -ExecutionPolicy Bypass -File install\windows.ps1
     powershell -ExecutionPolicy Bypass -File install\check.ps1
     ```

2. **Get the project:** download the ZIP or clone it into a short folder path outside OneDrive.
   [docs/03-get-the-project.md](docs/03-get-the-project.md)
3. **Open it in VS Code and install the recommended extensions** (VS Code offers them from `.vscode\extensions.json`).
   [docs/04-first-run.md, step 2](docs/04-first-run.md#step-2-install-the-recommended-vs-code-extensions)
4. **Run setup once, before you open Claude Code:** in the VS Code terminal run this command
   ([docs/04-first-run.md](docs/04-first-run.md)):

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\tools\setup.ps1
   ```

5. **Tell it who you are:** copy `templates\OWNER_PROFILE.md` to `OWNER_PROFILE.md` in the project folder and fill it
   in (your name, tone, reply format and owner-only list). Claude reads it first in every session.
   [templates/OWNER_PROFILE.md](templates/OWNER_PROFILE.md)
6. **Tell it about your gear:** fill `knowledge\00-gear-inventory\` with your printers and what is loaded.
   [docs/04-first-run.md](docs/04-first-run.md)
7. **Pick how much Claude may do without asking:** permission modes, allow and deny rules, parallel agents, and what
   always stays yours. [docs/11-autonomous-mode.md](docs/11-autonomous-mode.md)
8. **Open the Claude Code panel and ask.** For example: "Read CLAUDE.md, then help me print the calibration cube in
   examples\calibration-cube." [docs/05-daily-workflow.md](docs/05-daily-workflow.md)

## Guides

| Guide | What it covers |
|---|---|
| [01 What this is](docs/01-what-this-is.md) | How the parts fit together, in plain English |
| [02 Install](docs/02-install.md) | Every app on Windows, macOS and Ubuntu, every install method, plus the [install and check scripts](install/README.md) |
| [03 Get the project](docs/03-get-the-project.md) | Download ZIP or git clone, and where to put the folder |
| [04 First run](docs/04-first-run.md) | Recommended VS Code extensions, setup script, config, your gear, your first prompt |
| [05 Daily workflow](docs/05-daily-workflow.md) | Asking for a part or a print, the library, the agents, the gates |
| [06 Print safety](docs/06-print-safety.md) | The no-AI-print rule, the checklist, how you send a print |
| [07 Tools reference](docs/07-tools-reference.md) | Every tool: inputs, outputs, example and sample output |
| [08 Customize](docs/08-customize.md) | Your printers, filaments, rules, knowledge, lessons and brand |
| [09 Troubleshooting](docs/09-troubleshooting.md) | The 15 most likely problems and their fixes |
| [10 FAQ](docs/10-faq.md) | Short answers to common questions |
| [11 Autonomous mode](docs/11-autonomous-mode.md) | Fewer approvals, still safe: permission modes, rules, parallel agents, the two-brain workflow, your owner profile |
| [Publishing](docs/PUBLISHING.md) (for maintainers) | Publishing the repository, the org avatar and the v1.0.0 release on GitHub |

## FAQ

<details>
<summary><strong>Do I need a Bambu Lab printer?</strong></summary>

No. The knowledge library, agents and most tools work for any maker. The slicing helper and the 3MF audit are written
for Bambu Studio and Bambu Lab printers; other printers get the general design, materials and engineering help.
</details>

<details>
<summary><strong>Can Claude start a print for me?</strong></summary>

No, by design. No tool here can start, send, upload or queue a print, and `.claude/settings.json` denies print, upload and
start tools from any MCP server. You press Print in Bambu Studio yourself.
</details>

<details>
<summary><strong>What does it cost?</strong></summary>

The project is free (MIT). Claude Code needs an Anthropic account: a paid Claude subscription or a Claude Console
account, according to the [Claude Code VS Code docs](https://code.claude.com/docs/en/vs-code). Git, VS Code, Python and
Bambu Studio are free downloads.
</details>

<details>
<summary><strong>Does it work on macOS or Linux?</strong></summary>

Windows 11 is tested. The macOS and Linux install guides cover the prerequisites; running the project there is planned
for v1.1. The Python tools are mostly portable, but the setup script and the hooks assume Windows, and nothing here has
been run on macOS or Linux.
</details>

<details>
<summary><strong>Is my data sent anywhere?</strong></summary>

The tools run on your PC and make no network calls. Your prompts and the files Claude reads go to Anthropic as part of
using Claude Code. Your load record and config stay on your PC; `config/paths.yaml` is ignored by git.
</details>

More answers: [docs/10-faq.md](docs/10-faq.md).

## Roadmap

- **v1.0.0 "First Light"** (this release): 16 knowledge domains, 22 agents, 30 skills, 5 commands, the print-qa gate,
  the slicing and audit tools with their self-test, 20 lessons, the calibration-cube example, the beginner guides, the
  install and check scripts, and the autonomy guide.
- **v1.1: the full library.** The remaining domains of the map, including game design and game development, plus
  finishing, calibration and testing, workflows, project ops, creative direction, selling and IP, reference sheets,
  scanning, media and data and backups, each after the same source and privacy review. Also planned: running the
  project itself on macOS and Linux.

## Contributing

Corrections, new notes, lessons and tool fixes are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first: every fact
needs a public source and an independent fact-check, run the privacy scan before every pull request, and nothing may add
a way for software to start a print. Security problems go through [SECURITY.md](SECURITY.md). Everyone follows the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Credits

### <img src="assets/brand/crest-apparel-icon.png" width="40" align="absmiddle" alt="Cap crest"> About the maker

Created by @OrcusMori.

Built with [Claude Code](https://code.claude.com/docs/en/vs-code). Third-party packages, adapted code and fonts are
credited in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## License

Code and documentation are released under the [MIT License](LICENSE). The Memento Mori name, crests, logos and every file
in `assets/brand/` are **not** covered by the MIT License; see [NOTICE.md](NOTICE.md). If you publish a fork, replace the
brand assets first.

<!--
Star history (fill <owner> when the repository is published, then uncomment):
[![Star History Chart](https://api.star-history.com/svg?repos=<owner>/maker-mastery&type=Date)](https://star-history.com/#<owner>/maker-mastery&Date)
-->

<p align="center">
  <img src="assets/brand/crest-parent-sign-off.png" width="160" alt="MEMENTO MORI crest">
</p>

---

<sub>Unofficial community project. Not affiliated with or endorsed by Anthropic or Bambu Lab. Claude and Bambu Lab are trademarks of their owners.</sub>
