# 06 - Print safety: you press Print, the AI never does

Next: [07 - Tools reference](07-tools-reference.md).

## The rule

> **No AI ever starts, sends, uploads or queues a print.** Not Claude Code, not an agent, not a skill, not a tool, by no
> route: an MCP server, Bambu Studio, the local network, the cloud or a script. Claude may design, slice, audit and
> prepare print-ready files. You review the pre-print checklist and press Print in Bambu Studio yourself.

The rule is written in [CLAUDE.md](../CLAUDE.md) (making rule 1), in [SECURITY.md](../SECURITY.md) (any route around it
is treated as a security problem) and in [CONTRIBUTING.md](../CONTRIBUTING.md) (a pull request that adds such a route is
closed).

## Why

- **A printer is a hot, moving machine in your home.** Someone has to look at it before it starts: is the plate clean
  and the right one, is the right spool loaded, is nothing left on the bed, is the area safe to leave. Software cannot see
  that; you can.
- **AI can be confidently wrong.** The gates catch many mistakes, but they check files, not the room. The last check is
  a human one by design.
- **Mistakes cost material and time, and can damage the printer.** A wrong filament-to-extruder map, a nozzle crash or a
  print on the wrong plate are all avoidable with one look.
- **You stay accountable for what your machine does.** Keeping the button with you keeps that clear.

## How the rule is enforced

1. **Nothing here can print.** No tool or MCP server in this project talks to a printer. `tools\slice_cli.py` only
   slices; the optional `mm-audit` MCP server is read-only (see [.mcp.json.example.md](../.mcp.json.example.md)).
2. **Deny rules in settings.** [`.claude/settings.json`](../.claude/settings.json) denies any MCP tool whose name
   contains `print`, `upload_gcode`, `send_gcode` or `queue`, and upload or start tools on any server whose name contains
   `bambu` or `printer`. Deny rules are checked before allow rules. The reasons are in
   [`.claude/settings.notes.md`](../.claude/settings.notes.md).
3. **The rulebook.** Every session and agent reads the rule in `CLAUDE.md`.

If you ever install a printer-control tool or MCP server yourself, keep its print, upload and start tools denied, and add
their exact names to the deny list. Do not remove the existing rules.

## The pre-print checklist

The `print-qa` agent fills [templates/preprint-checklist.md](../templates/preprint-checklist.md) item by item, with the
tool output that proves each verdict. Nothing prints on a FAIL. Start it with:

```text
/preprint-check work\slice\bracket\out.3mf
```

What the checklist covers, in short (read the file for the exact wording):

1. Your physical load is recorded with a date (`knowledge\00-gear-inventory\current-load.md`); undated means FAIL.
2. The project's filaments match the loaded spools, slot by slot (`tools\audit_3mf.py`).
3. On dual-nozzle printers, each filament goes to the extruder that can physically reach it.
4. One material per object unless multi-material is the point; PLA and PETG in one object always FAIL.
5. Every object sits inside the printable area of the extruder it uses.
6. The prime tower clears every object by at least 8 mm, measured from the G-code (`tools\tower_bounds.py`,
   `tools\tower_clearance.py --min-gap 8`).
7. The file was sliced with the installed Bambu Studio CLI, `result.json` warnings were read, and every change from the
   `0.20mm Standard` process has a sourced reason.
8. The face on the plate gives the finish the part needs.
9. Time and grams per plate are on the print sheet.
10. Display pieces pass the tip-over check (`tools\stability_check.py`).
11. Visible overhangs are designed out first; support is the last resort and its gap is read back from the G-code.
12. The verdict carries a sha256 hash of the gated file; a changed file is no longer gated.
13. You print the gated sliced file directly, without re-slicing; if Bambu Studio forces a re-slice, compare time and
    grams first.
14. The print's purpose is stated; display prints pass the visible-part ratio (`tools\visible_ratio.py`).
15. Tree supports have their trunk sizes reported.

Items that cannot apply to your printer are written "not applicable" with a reason, never left blank.

## How YOU send a print in Bambu Studio

These labels come from the Bambu Lab wiki's
[Bambu Studio Quick Start Guide](https://wiki.bambulab.com/en/software/bambu-studio/studio-quick-start), unless marked.

1. Read the print-qa report. Go on only if it says PASS and you have read every WARN.
2. Look at the printer: plate clean and the type the checklist names, spool(s) loaded as in `current-load.md`, nothing on
   the bed.
3. In Bambu Studio, open the gated sliced 3MF that the report names (the `_SLICED.3mf` or `out.3mf` path):
   **File > Open Project** (label not verified), or drag the file from File Explorer into the window.
4. If Bambu Studio shows the **Preview** pane with the sliced layers, go to step 6. If it shows the model unsliced and asks
   you to slice, the file is being re-sliced: compare the new time and grams with the numbers on the print sheet after
   the next step, and stop if they differ.
5. Only if needed: click **Slice** at the top right. Bambu Studio switches to the **Preview** pane.
6. Look at the preview: layers, supports, prime tower, nothing outside the plate.
7. Click **Print** at the top right (the wiki's section is called **Print plate**). A pop-up shows a preview, asks you to
   select the printer from a drop-down list, and offers options such as **Bed Leveling** and flow calibration.
8. Choose your printer and the options, then click **Send**. The wiki says this sends the file "to the printer and start
   printing".
9. Stay near the printer for the first layer.

Without a network connection, the wiki describes the SD-card route: click the arrow to the left of **Print plate**, choose
**Export plate sliced file**, save it to the printer's microSD card, then start it from the printer's screen
(**Print Files**, then **SD Card**).

Sending a print needs the Bambu Network plug-in and the printer and PC on the same network, according to the same wiki
page. Nothing in this project sets that up for you, on purpose.

Next: [07 - Tools reference](07-tools-reference.md).
