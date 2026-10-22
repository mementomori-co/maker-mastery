# 05 - Daily workflow

How to work with the project once it is set up: asking for a part or a print, using the knowledge library, calling the
agents, passing the gates, and the optional reviewer handoff. Next: [06 - Print safety](06-print-safety.md).

Every session starts the same way: open the project folder in VS Code (**File > Open Folder...**), open the Claude Code
panel (the Spark icon), and type. At session start a hook loads the lessons into Claude's context; you may not see it.

## Before anything that will be printed: update your load

1. Look at the printer: which spool is in which AMS slot or on the external holder, which nozzle is fitted, which plate is
   on the bed.
2. Tell Claude, for example: "Update knowledge\00-gear-inventory\current-load.md: AMS slot 1 now has Bambu PETG Basic,
   White; the other slots are empty; Textured PEI plate. Use today's date."
3. Open the file and check the rows yourself.

The audit compares every print file against this record (check C7). An old date triggers a warning; a wrong row stops
the print file from passing.

## Ask for a part

Describe what it is for, the size limits and where it will live. For example:

```text
I need a wall bracket for a 30 mm diameter pipe, screwed to the wall with two 4 mm screws, indoors, holding about 1 kg.
Make it in code-CAD with the script beside the STL, then run the DFM review. Tell me which filament you recommend and why,
with sources.
```

What happens, step by step (the build pipeline in [CLAUDE.md](../CLAUDE.md)):

1. **`cad-engineer`** (or **`organic-modeler`** for sculpted shapes) builds the part, saves the generating script beside
   the STL, runs the geometric checks and renders the real mesh for you to look at.
2. **`dfm-engineer`** reviews it for printing: orientation, which face goes on the plate, overhangs, bridges, floating
   islands, splits and the assembly path.
3. **`materials-scientist`** is consulted when the filament is not decided, with numbers from the data sheets.
4. You get a report with file paths and a "Known flaws" list. Read that list; it is where Claude tells you what it saw
   or suspects.

Useful skills for this: `/cad-build`, `/dfm-review`, `/material-pick`, `/coupon` (when a number such as a clearance is a
guess and a small test print can measure it).

## Ask for a print file

```text
Prepare a print file for the bracket on my printer with the filament in current-load.md. Start from the 0.20mm Standard
process, slice it with the CLI, run the audits and /preprint-check. Do not print.
```

1. **`bambu-studio-expert`** builds the 3MF: printer, process, filament and plate presets; on dual-nozzle printers the
   filament-to-extruder grouping. Every change from the `0.20mm Standard` process needs a sourced reason.
2. It slices with `tools\slice_cli.py`, which runs the Bambu Studio you installed and writes into `work\slice\<name>\`.
3. The audits run on the real output: `tools\audit_3mf.py`, `tools\gcode_audit.py`, `tools\tower_clearance.py` and, for
   display pieces, `tools\stability_check.py` and `tools\visible_ratio.py`. See [07 - Tools reference](07-tools-reference.md).
4. **`print-qa`** fills the pre-print checklist ([templates/preprint-checklist.md](../templates/preprint-checklist.md))
   item by item, quoting the tool output for each verdict. It cannot write files, so it cannot "fix" its own findings.
5. On **PASS**, you read the checklist and print it yourself ([06 - Print safety](06-print-safety.md)). On **FAIL**, the
   report names one fix per failing item; ask Claude to apply it and run the gate again.

## Use the knowledge library

The library is in [`knowledge/`](../knowledge/INDEX.md): 94 notes in 16 domains, each fact with its source link.

- **Ask from it:** "Using knowledge\08-electronics-lighting, how much current does a 60 LED/m WS2812B strip draw per
  metre, and what is the source?" Claude should answer with the note and the link.
- **When the answer is not there:** Claude says so, and you can ask it to research the question:

  ```text
  /research-topic heat-set insert hole sizes for M3 inserts in PETG
  ```

  This runs the knowledge pipeline: **`researcher`** agents find primary sources and write claims into
  `research\inbox\`, **`fact-checker`** re-derives each claim without seeing the researcher's reasoning and marks it
  VERIFIED, CONTRADICTED or UNVERIFIABLE, and **`librarian`** files only the VERIFIED rows into `knowledge\`, updates
  the category's `index.md` and your [CURRICULUM.md](../CURRICULUM.md).
- **One claim only:** `/verify-claim "PLA and PETG bond weakly to each other"` returns VERIFIED,
  CONTRADICTED or UNVERIFIABLE with the URL.
- **Your progress:** `/curriculum` shows what is covered and suggests the next three topics.

## The agents

The 22 agent definitions live in [`.claude/agents/`](../.claude/agents/). You rarely call them by name: the skills and
the rulebook route work to them. The main ones:

| Agent | Job |
|---|---|
| `researcher` | One narrow question, primary sources, a claims table with URLs |
| `fact-checker` | Re-checks each claim on its own; never sees the researcher's reasoning |
| `librarian` | Files verified facts into `knowledge\`, updates indexes |
| `cad-engineer`, `organic-modeler` | Build parts and sculptures, script beside the STL, render for review |
| `dfm-engineer` | Printability review before slicing |
| `bambu-studio-expert` | Slicer settings with exact labels and keys; builds and slices the 3MF |
| `print-qa` | Gates a 3MF against the checklist; cannot write files |
| `materials-scientist`, `electronics-engineer`, `systems-engineer` | Filament choice; LEDs, wiring and power; PC, Raspberry Pi and printer ecosystem |
| `safety-officer` | PASS/FAIL safety sheet for lasers, resin, solvents, wood dust, mains and fumes; another agent cannot overrule its FAIL |
| `test-coupon-designer` | Small measured test prints that replace a guessed number |

Others cover rendering (`surfacing-artist`), AI-to-3D and scans (`mesh-capture-specialist`), MCP and agent work
(`mcp-agent-engineer`), usefulness reviews (`vision-auditor`), games (`game-director`), media, branding, IP facts and
selling.

## The gates, in short

- **Sources gate:** no fact without a source; unverified means labelled "not verified".
- **Independent check:** nothing is called ready until a second agent that did not build it has checked it.
- **print-qa gate:** nothing prints on a FAIL, and even on a PASS, you press Print.
- **Approvals:** installs, deletions, purchases and account sign-ups wait for your explicit yes.
- **Protected folders:** for anything listed under `protected_roots` in `config\paths.yaml`, a hook blocks Claude's file
  tools and common shell writes. It is a safety net, not a sandbox: a determined command or an MCP server's own write
  tools can get around it. For strong isolation use Windows folder permissions, a separate Windows user or a VM
  ([troubleshooting, section 14](09-troubleshooting.md#14-claudes-command-was-blocked-by-guard_paths)).

When Claude stops, it reports what changed, the files to review (full paths), Known flaws and numbered questions marked
NEEDS MAKER. Answer the questions by number.

## When something goes wrong

Ask for a lesson: `/lesson-learned`. Claude writes a short post-mortem (what happened, root cause, rule now) into
`lessons\`. The next session starts with it.

## Optional: a second Claude chat as reviewer

If you like a second opinion, Claude Code can append a report to `plan\handoff\TO_CHAT.md` at every stop, and you paste
it into a separate Claude chat that reviews the evidence and answers the questions. You carry the replies back. Setup and
the rules (what a reviewer may decide, and what only you decide) are in
[templates/handoff/README.md](../templates/handoff/README.md).

Next: [06 - Print safety](06-print-safety.md).
