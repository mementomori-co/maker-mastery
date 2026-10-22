# Current load - what is physically in your printers (TEMPLATE)

Applies to: every printer you list below - Bambu Studio 02.08
Verified: YYYY-MM-DD

This file is your load record. `tools\audit_3mf.py` check C7 reads it before it calls a print file ready: every filament in
the 3MF must match a loaded slot, on the right side, and the plate type must match. While every slot says EMPTY and the date
above is the placeholder, C7 FAILs on purpose: nothing is confirmed loaded until you look at the printer and write it here.

## How to fill it in (the format C7 reads)

1. Replace `YYYY-MM-DD` in the `Verified:` line above with today's date after you have looked at the printer.
   C7 warns when the date is more than 7 days old (`--load-max-age-days` changes that).
2. Keep only the rows of printers you own, and add rows for any other printer. One row per filament position.
3. The FIRST cell of a row must start with the printer model exactly as it appears in Bambu Studio's printer name
   ("Bambu Lab **H2C** 0.4 nozzle" -> `H2C`, "Bambu Lab **X1C** 0.4 nozzle" -> `X1C`, "Bambu Lab **A1 mini** 0.4 nozzle"
   -> `A1 mini`), then ` - ` (space, hyphen, space; a middle dot also works), then the position.
   - A filament position must contain `AMS` or `spool` in the first cell.
   - On a dual-extruder printer, write `RIGHT` or `LEFT` in the first cell: C7 checks that each filament is mapped to that side
     (RIGHT = extruder 2, LEFT = extruder 1).
   - The plate row must contain `plate` in the first cell.
4. The SECOND cell says what is there:
   - `EMPTY` (or `none`, `no filament`) for an empty position.
   - `unknown` or `not reported` when you have not looked: C7 warns.
   - A loaded Bambu spool, in bold, product then colour: `**Bambu PLA Basic, Black**`. The product and colour names are the
     ones Bambu Studio's filament list and colour catalogue use; C7 checks the filament id and the colour against them.
   - A third-party spool, in bold, vendor and product then colour: `**Acme PETG, Grey**`. C7 matches it on the filament's
     vendor and type and warns that the colour cannot be checked from a catalogue.
   - The plate row: the plate name as Bambu Studio writes it without the word "Plate", e.g. `Textured PEI`.
     If the row says `not re-confirmed`, C7 warns that the plate was not physically checked.
5. The THIRD cell says how you know (for example "looked at the AMS screen", "read the spool label").
6. Run `.venv\Scripts\python.exe tools\audit_3mf.py <your file>.3mf` and read the C7 lines.

## Load table

| Position | Content | How known |
|---|---|---|
| H2C - AMS 2 Pro slot 1 (RIGHT inlet) | EMPTY | example row: replace with what you see |
| H2C - AMS 2 Pro slot 2 (RIGHT inlet) | EMPTY | example row |
| H2C - AMS 2 Pro slot 3 (RIGHT inlet) | EMPTY | example row |
| H2C - AMS 2 Pro slot 4 (RIGHT inlet) | EMPTY | example row |
| H2C - LEFT external spool holder | EMPTY | example row |
| H2C - plate on the bed | not re-confirmed | example row: write the plate name, e.g. Textured PEI |
| P1S - AMS slot 1 | EMPTY | example row |
| P1S - AMS slot 2 | EMPTY | example row |
| P1S - AMS slot 3 | EMPTY | example row |
| P1S - AMS slot 4 | EMPTY | example row |
| P1S - external spool | EMPTY | example row |
| P1S - plate on the bed | not re-confirmed | example row |

## Facts
- The rows above are measured by you at the printer; nothing here is read from the printer by software.

Sources:
- Your own look at the printer: measured by you (record the date in the `Verified:` line).
- Bambu Lab wiki, for product and plate names: https://wiki.bambulab.com/
