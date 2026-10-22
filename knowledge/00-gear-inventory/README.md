# 00 - Gear inventory: your printers, your load, your PC

This folder is the only place where Claude learns what YOU own and what is physically on your machines right now.
Every agent reads it before it answers for "your printer". It ships nearly empty on purpose: nothing here may be assumed.

Rule: Claude never assumes a filament is loaded or owned. If a fact is not written here with a date, Claude asks you,
and the print-qa gate fails the load items until it is recorded.

## The files

| File | What it holds | Who fills it | How often |
|---|---|---|---|
| `printers.md` | each printer you own: model, nozzles you own, AMS units and slots, plates, firmware | you (Claude can write it from your answers) | when you buy or change hardware |
| `current-load.md` | what is on the machine today: filament per AMS slot or external spool, nozzle fitted, plate on the bed, with a `Verified: YYYY-MM-DD` line | you, every time you change the load | before every print file is built |
| `pc-and-software.md` (optional) | the software you have installed and its versions (Bambu Studio, Blender, CAD tools), and anything a helper agent needs to know about your PC | you | when you install or update |

`current-load.md` ships as an empty template; keep its headings and fill the rows. Do not delete it: a missing file makes
item 1 of `templates\preprint-checklist.md` FAIL.

## Fill it in (VS Code, first time)
1. Open the project folder in VS Code and open the Claude Code panel.
2. Paste this prompt:
   "Interview me about my printers and fill knowledge\00-gear-inventory\printers.md. Ask one numbered question at a time:
   printer model, nozzle sizes I own, AMS units and how many slots, plates I own, firmware version. Write only what I answer."
3. Then paste:
   "Ask me what is physically loaded right now and fill knowledge\00-gear-inventory\current-load.md, with today's date
   from the PC clock in the Verified line. Ask slot by slot: brand, line, material, colour; then nozzle fitted and plate."
4. Open both files and read them. Correct anything wrong yourself or tell Claude what to change.

## Suggested layout for `printers.md`
```markdown
# My printers
Verified: YYYY-MM-DD

## <Printer nickname> - <Bambu Lab model>
- Nozzles owned: <0.4 hardened steel, 0.2 stainless, ...>
- Filament feed: <AMS model, number of slots> | <external spool on the left/right extruder>
- Plates owned: <Textured PEI, Smooth PEI, ...>
- Firmware: <version, read from the printer screen or the Device tab in Bambu Studio (label not verified)>
- Notes: <anything special, e.g. which extruder the AMS feeds on a dual-nozzle printer>
```

## Keep it honest
- Date every change. An old `Verified:` date means "check again", not "still true".
- Write the exact product name from the spool label (brand, line, colour), not "white PLA".
- Do not store serial numbers, access codes, IP addresses or account details here. Nothing in this folder needs them,
  and the privacy scan (`tools\privacy_scan.py`) is there to catch them before you share the project.
- If you share or publish your copy of this project, decide whether your load and printer list should go with it.
