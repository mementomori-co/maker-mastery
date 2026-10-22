# Hotend clog diagnosis and swap procedures (H2C induction hotends + left hotend, P1S)

Applies to: H2C | P1S | both · Bambu Studio 2.x · firmware current at each wiki page's update date (pages name no firmware version)
Verified: 2026-10-03

## Facts

### H2C clog diagnosis and manual clearing (both hotends)
- Clog symptoms listed by Bambu: little or no extrusion, clicking from the extruder, under-extrusion or layer separation, and a print that starts moving with no filament coming out. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/clogging)
- Diagnostic order: at room temperature, press the cutter handle to cut the filament and pull it up by hand. Strong resistance means the blockage is on the extruder side. If it comes out smoothly, load new filament and tap Extrude on the printer screen. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/clogging)
- To remove an induction hotend for inspection, pull out its latch and lift it out; the right hotend is the worked example and the left follows the same steps. Wait for room temperature before cutting, because cutting hot can cause a second clog at the cutter. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/clogging)
- Needle clearing: on the screen go to Control > Nozzle & Extruder, choose the side, set the temperature a little above the normal print temperature (Bambu's PLA example is 220 °C; PLA only), wait for it to reach temperature, then move the cleaning needle gently up and down in the nozzle. Menu labels depend on firmware. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/clogging)
- Front guide cover removal: take out both cutters, then three M2.5 x 7 screws with an H2.0 hex key, and pull the cover straight out by its side tabs; refit the same screws. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/clogging)
- Severe jams escalate to Bambu's idler-arm jam guide and then to idler-arm replacement via the extruder disassembly guide; Bambu describes this case as very rare. Those sub-guides were not checked here. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/clogging)
- Three-tier clearing order for both H2C hotends: (1) extrude the clog out manually, (2) cleaning needle (not for nozzles smaller than 0.4 mm), (3) cold pull. For the left hotend, select the left side in the same menus. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/unclogging)
- On-screen cold-pull wizard: Settings > Toolbox > Nozzle Cold Pull Maintenance, then choose the nozzle side, a cleaning filament (PLA or PETG recommended), the nozzle size and the residual filament type, and start. The menu name is firmware-dependent. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/unclogging)
- Bambu states the three tiers clear about 99% of nozzle clogs (its own unsourced figure), says 0.2 mm nozzles are harder to clear, and says to replace a nozzle that is worn or deformed. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/unclogging)
- Hotend blob (clumping) cleaning on an induction hotend: under Hotends & Rack choose Uninstall (Bambu suggests slot 6), heat the hotend (PLA example 230 °C), and wipe the hot tip firmly with a paper towel; then fetch it normally. Do not press the homing button during this procedure. Blobs on the left nozzle follow a separate H2D guide. **Hot surface: this step wipes a nozzle at print temperature; protect your hand.** — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/hotend_blob)

### General clog causes and fixes (any Bambu printer)
- Clogs are either extruder-side or nozzle-side. Listed causes: chamber too hot so the filament softens and the drive gear flattens it; a faulty drive gear; very soft or wet filament (for example TPU 85A or damp PVA); inconsistent diameter; nozzle temperature too low; speed too high; fibre-filled filaments building up particles in the nozzle. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/clog)
- Fixes: lower the chamber temperature, confirm the print temperature, slow down or raise temperature slightly. For fibre-filled residue only, heat to 250-280 °C and scrape the nozzle bore with a metal tool such as a hex key; then push PLA through at 220 °C to confirm flow. Prefer a 0.6 or 0.8 mm nozzle for fibre-filled filament, not 0.2 mm. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/clog)

### H2C induction-hotend rack: swap, nest, fetch, calibrate
- Rack capacity: up to 6 induction hotends without manual handling (1 on the toolhead + 5 on the rack). With the fixed left hotend that is 7 hotends in total. Counting: 6 rack positions; at most 6 induction hotends, so one position is always free to receive the hotend being put away. — [source](https://wiki.bambulab.com/en/h2c/manual/induction-hotend-rack-workflow), [source](https://us.store.bambulab.com/products/h2c)
- Nest (put away): Hotends & Rack > choose an empty holder > Nest. Fetch (pick up): choose the hotend number > Fetch. Labels are firmware-dependent. — [source](https://wiki.bambulab.com/en/h2c/maintenance/replace-induction-hotend)
- Manual removal from the toolhead: printer at room temperature and powered off; move the lifting linkage first so the flow blocker is not bent; slide the latch right to unlock, pinch the nozzle tip and pull it out diagonally. Manual install: latch left to lock, the end with two openings faces forward, and a firm shake should show no play. — [source](https://wiki.bambulab.com/en/h2c/maintenance/replace-induction-hotend)
- Replacing a hotend on the rack: choose it > Uninstall; the toolhead moves up and you swap the hotend in the holder by hand. If the new hotend has a different diameter or material, press Read on the Hotend & Rack screen. Bambu recommends calibrating after a replacement but does not name which items. — [source](https://wiki.bambulab.com/en/h2c/maintenance/replace-induction-hotend)
- When several holders are empty, the printer uses the lowest-numbered one first. Coarse homing finds the rack centre with a magnet; fine homing finds the upper and lower limits. Manual homing applies only when a rack row is raised. — [source](https://wiki.bambulab.com/en/h2c/manual/induction-hotend-rack-workflow)
- Automatic rack calibration: Settings > Calibration > Induction Hotend Rack Setup > Start. A different Bambu page calls the same item by another name, so read the label on your screen. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0034), [source](https://wiki.bambulab.com/en/h2c/maintenance/hotend-rack-manual-position-calibration)
- Manual rack height calibration: loosen (do not remove) the four side locking screws with an H2.0 hex driver; tightening raises the rack and loosening lowers it; set it so the nozzle barely touches the adjustment block, with no gap and no compression; confirm by running calibration. — [source](https://wiki.bambulab.com/en/h2c/maintenance/hotend-rack-manual-position-calibration)
- Rack assembly replacement: remove the latch actuator (3 screws), then the four assembly screws with a 2.0 mm driver while supporting the assembly, then run the rack setup and confirm hotends are picked, placed and read normally. — [source](https://wiki.bambulab.com/en/h2c/maintenance/replace-induction-hotend-rack-assembly)
- Induction hotends come in 0.2, 0.4, 0.6 and 0.8 mm plus a high-flow option; the firmware did not yet support mixing nozzle sizes within one print when checked. — [source](https://wiki.bambulab.com/en/h2c/maintenance/replace-induction-hotend), [source](https://us.store.bambulab.com/products/h2c)

### H2C maintenance intervals
- When only printing is used (the laser version needs more), the X rail, the left-nozzle lifting rail and the induction-hotend rack are maintained monthly; the exterior, heatbed, toolhead, cameras and side panels every 3 months. On-screen reminders need firmware 01.01.00.00 or later; without them Bambu says to service everything monthly. — [source](https://wiki.bambulab.com/en/h2c/maintenance/period-maintenance)
- Rack cleaning: wipe the dock surfaces and four linear rods with a cloth dampened with alcohol, wipe the six etched markings carefully, lubricate the rods, move the rack by hand, wipe off excess. Latch: pull out, wipe, oil lightly, reinsert. Left lifting rail: remove the left nozzle and front guide cover, clean the rail with an alcohol swab, apply a little lubricant, then switch nozzles 3-5 times from the screen. — [source](https://wiki.bambulab.com/en/h2c/maintenance/period-maintenance)
- The "every 5 rolls (2 for carbon fibre)" figure is a cleaning interval for the left (standard) hotend only, not a replacement interval and not for the induction hotends, which have no roll-based interval on the page. — [source](https://wiki.bambulab.com/en/h2c/maintenance/period-maintenance)
- After any maintenance Bambu recommends a full calibration from the screen (motor noise, vibration compensation, bed leveling, nozzle offset). — [source](https://wiki.bambulab.com/en/h2c/maintenance/period-maintenance)
- Rack-related HMS codes are in [hms-code-index.md](hms-code-index.md).

### X1/P1 series (incl. P1S) clog clearing and hotend replacement
- Pin unclog: set the hotend to 250 °C (stated for PLA/PETG/TPU/ABS) in the temperature/axis screen, push the pin up through the nozzle tip (skip for 0.2 mm nozzles), and do not push it too far into the hotend. — [source](https://wiki.bambulab.com/en/x1/troubleshooting/nozzle-clog)
- Cold pull: remove the front cover and PTFE tube; load filament at 220 °C (PLA example); cool to 100 °C; press retract on screen while pulling gently (not hard) on the filament until it comes out clean; set the PTFE support as high as it goes when refitting. — [source](https://wiki.bambulab.com/en/x1/troubleshooting/nozzle-clog)
- Full hotend removal (P1 series): nozzle below 50 °C and printer off; remove the front cover; unplug fan, thermistor and heater cables; remove two screws with an H2.0 hex key; strip fan, silicone sock, clip, heater and thermistor in that order. On install, apply new thermal paste, update the nozzle information on the printer screen, and run the device calibration (about 20 minutes per Bambu); passing it confirms the swap. — [source](https://wiki.bambulab.com/en/p1/maintenance/complete-hot-end-assembly)
- The same page says the nozzle-information field under Printer Parts in Bambu Studio was disabled as of Studio 02.01.01.52, so nozzle changes are entered on the printer. Not checked on later Studio versions. — [source](https://wiki.bambulab.com/en/p1/maintenance/complete-hot-end-assembly)

### P1 series preventive maintenance
- Z lead screws: check and grease every 3 months. X-axis carbon rods: check monthly and never grease them (grease causes buildup and wear). Y/Z rods: check monthly, clean every 5 rolls when printing ABS/ASA, anti-rust every 3 months. Cutter: check every 3-5 rolls (regular filament) or 1-2 rolls (abrasive). PTFE tube: check after about 10 rolls regular or 5 rolls abrasive; replace when worn. — [source](https://wiki.bambulab.com/en/p1/maintenance/p1p-maintenance)

## In practice
- On an H2C clog, try the three tiers before taking anything apart: manual extrude, needle (skip on 0.2 mm), on-screen cold-pull wizard. Replace a nozzle that shows wear after clearing.
- Treat "5 rolls / 2 rolls CF" as a left-hotend cleaning interval only.
- Read the real label on your printer screen before following written menu paths; Bambu's own pages name the rack calibration differently.
- Work on hotends cold and powered off unless the procedure explicitly requires heat; the blob-wipe and needle steps are done at print temperature.

## Not verified / open questions
- Sub-guides referenced but not checked: idler-arm jam handling, extruder disassembly, dock assembly replacement, latch actuator, the rack calibration-block model.
- Whether current Bambu Studio versions still disable the nozzle-information field (only stated for 02.01.01.52).
- No page states a firmware version for its procedure.

Sources:
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/clog - general clog causes and fixes
- https://wiki.bambulab.com/en/h2c/troubleshooting/clogging - H2C clog symptoms, cut test, needle, guide cover, escalation
- https://wiki.bambulab.com/en/h2c/troubleshooting/unclogging - three-tier order, cold-pull wizard
- https://wiki.bambulab.com/en/h2c/troubleshooting/hotend_blob - hotend blob cleaning
- https://wiki.bambulab.com/en/h2c/maintenance/replace-induction-hotend - nest/fetch/uninstall, manual removal, Read step, nozzle sizes
- https://wiki.bambulab.com/en/h2c/manual/induction-hotend-rack-workflow - rack capacity, slot priority, homing
- https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0034 - rack setup menu path
- https://wiki.bambulab.com/en/h2c/maintenance/hotend-rack-manual-position-calibration - manual rack height calibration
- https://wiki.bambulab.com/en/h2c/maintenance/replace-induction-hotend-rack-assembly - rack assembly replacement
- https://wiki.bambulab.com/en/h2c/maintenance/period-maintenance - H2C maintenance intervals and cleaning steps
- https://us.store.bambulab.com/products/h2c - rack capacity and nozzle-size cross-check
- https://wiki.bambulab.com/en/x1/troubleshooting/nozzle-clog - X1/P1 pin unclog and cold pull
- https://wiki.bambulab.com/en/p1/maintenance/complete-hot-end-assembly - P1 hotend replacement
- https://wiki.bambulab.com/en/p1/maintenance/p1p-maintenance - P1 series maintenance intervals
