---
description: Gate a print file before you send it to the printer yourself
argument-hint: <path to .3mf>
---
Run the `print-qa` agent on $ARGUMENTS against templates\preprint-checklist.md. Read knowledge\00-gear-inventory\current-load.md first; if it is missing or undated, ask the maker which filament is in which AMS slot and which nozzle and plate are fitted, and FAIL the load items until it is recorded. Slice with the installed Bambu Studio CLI through tools\slice_cli.py, then read result.json and the G-code and run the audit tools. Report PASS/FAIL per checklist item, with the script line that proves it and the one fix for each FAIL. Nothing prints on a FAIL. No AI ever starts, sends, uploads or queues a print: the maker reviews the result and presses Print in Bambu Studio.
