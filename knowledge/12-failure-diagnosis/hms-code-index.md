# HMS code index (H2C, P1S)

Applies to: H2C | P1S | both · Bambu Studio 2.x (wiki pages are undated per code; the index endpoint was checked live on the Verified date)
Verified: 2026-10-03

## Facts

### Where the index lives, and how to resolve a code reliably
- Bambu's master HMS (Health Management System) error-code index is a single wiki page with a printer-model dropdown; in that dropdown H2C is option value 10 and P1S is option value 4, and the page's search calls Bambu's `GetHmsWikiList.php` endpoint. The model list grows over time. — [source](https://wiki.bambulab.com/en/hms/home)
- The URL folder a code page lives under (`/en/x1/`, `/en/h2/`, `/en/h2c/`) does not tell you which printer the code applies to. The H2C index sends some codes to `/en/x1/` pages, and the P1S index sends some codes to `/en/h2/` and `/en/h2c/` pages. The reliable lookup is the model-filtered query `https://e.bambulab.com/wikijs/GetHmsWikiList.php?size=50&lang=en&id=<10 for H2C | 4 for P1S>&hms=<16-digit code, no dashes>`, reading the `wiki_en` field it returns. — [source](https://e.bambulab.com/wikijs/GetHmsWikiList.php?size=50&lang=en&id=4&hms=0700200000020012)
- Troubleshooting hubs for the H2C: the H2C page `/en/h2c` links the H2C clogging, unclogging, hotend-blob and hotend-upgrade-failure guides and individual code pages, and the H2-series page "H2 Series Troubleshooting" (`/en/h2/troubleshooting`) lists the shared H2 guides (clogging, extruder motor overload, homing and levelling failure and others). The path `/en/h2c/troubleshooting` itself has no hub page (HTTP 404 when checked). — [H2C hub](https://wiki.bambulab.com/en/h2c), [H2 Series Troubleshooting](https://wiki.bambulab.com/en/h2/troubleshooting)
- The "HMS" link in the wiki sidebar is site-wide navigation present on every page, not a per-printer HMS section. The code-numbering explainer (`intro-hms`) is reached from the HMS home page and is tagged for X1 in its own metadata. — [source](https://wiki.bambulab.com/en/hms/home), [source](https://wiki.bambulab.com/en/x1/troubleshooting/intro-hms)
- P1S codes are documented across the x1, h2 and h2c namespaces, not x1 alone: the P1S index resolves 0700-2000-0002-0012 to an `/en/h2/` page and 0700-9400-0001-0001 to an `/en/h2c/` page. — [source](https://e.bambulab.com/wikijs/GetHmsWikiList.php?size=50&lang=en&id=4&hms=0700940000010001)

### Code structure
- Bambu's numbering explainer splits a code into six elements: Module ID, Module No., Part ID, Part No., Alert level, Error code ID (the heading says "Four Element" although six are listed). It gives no digit width per element. — [source](https://wiki.bambulab.com/en/x1/troubleshooting/intro-hms)
- Module ID table on the same page: 03 = Motion Controller, 05 = Main Board, 07 = AMS, 08 = Tool Head, 0C = XCAM (micro lidar), 10 = Studio, 11 = Handy app, 12 = AMS Lite, 18 = AMS HT. It has no entry for `1A` (the prefix of H2C hotend-rack codes) and lists `05` as Main Board although H2C `0500-...` codes are hotend-authentication errors, so the table alone is not enough to decode H2C module IDs. — [source](https://wiki.bambulab.com/en/x1/troubleshooting/intro-hms)
- Alert levels: 0001 = Error (print stopped, must be cleared before a new job), 0002 = Warning (print paused, must be cleared before resuming), 0003 = Notification (informational). Reading the level from the third 4-digit group of a 16-digit code (for example 0C00-0300-**0003**-0008 = Notification) is an inference from element order, not a stated rule, but it matches every code checked here. — [source](https://wiki.bambulab.com/en/x1/troubleshooting/intro-hms)

### AMS feed / retract / runout codes
- `0700-2000-0002-0012` - AMS feeder motor overloaded and unable to turn the spool. First check: whether filament fed out more than about 30 cm before retracting (odometer fault). Both the H2C and P1S indexes map the code to this page. — [source](https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0700_2000_0002_0012)
- `0700-5500-0001-0004` - binding error between an AMS and the extruder. Fix: re-check the PTFE tube connections (AMS, buffer, toolhead) and re-initialise the AMS. Mapped by the H2C index only; the P1S index has no entry. — [source](https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0700_5500_0001_0004)
- `0700-2000-0002-0001` - AMS slot filament ran out; load new filament and press Retry. Hosted under x1, but both the P1S and H2C indexes map the code here. — [source](https://wiki.bambulab.com/en/x1/troubleshooting/hmscode/0700_2000_0002_0001)
- `07FE-2000-0002-0001` - H2C left-extruder external spool ran out; check the spool at the back of the printer and reload. The right-extruder equivalent is `07FF-2000-0002-0001`. No P1S entry. — [source](https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/07FE_2000_0002_0001)

### Clog and spaghetti codes
- `0700-7000-0002-0003` - extrusion-clog warning, tagged for many models including H2C and P1S. The page title carries a typo (shows 2000 instead of 7000). Its H2C section links to the H2C clogging (nozzle) and unclogging (extruder jam) guides; the X1/P1 section links to a different guide on finding which part is clogged. — [source](https://wiki.bambulab.com/en/x1/troubleshooting/hmscode/0700_7000_0002_0003)
- `0C00-0300-0003-0008` - possible spaghetti detected. Step 1: inspect the print and decide whether to stop, or use Skip Objects if only part of the plate failed; the detection must be enabled in the print options. The H2C index resolves to this `/en/h2/` page (there is no `/en/h2c/` page). The P1S index has no entry for this code. — [source](https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0C00_0300_0003_0008), [source](https://e.bambulab.com/wikijs/GetHmsWikiList.php?size=50&lang=en&id=10&hms=0C00030000030008)

### Bed / chamber codes
- `0300-0D00-0001-0003` - build plate may not be seated (Z-homing misdetection). X1/P1 step: lift the heatbed and check it is not touching the purge chute. P1S index only; the H2C index has no entry. — [source](https://wiki.bambulab.com/en/x1/troubleshooting/hmscode/0300_0D00_0001_0003)
- `0300-1800-0001-0006` - heatbed leveling data abnormal. Step 1: check for filament residue on the nozzle and bed, then re-level. H2C index only; no P1S entry. — [source](https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0300_1800_0001_0006)
- `0300-9400-0002-0003` - chamber did not reach its target temperature. If it is too hot: open the front door or top cover, or lower the bed temperature. If it is too cold: check that the door and top cover are closed. Mapped by the H2C index; the pictured sensor hardware is from the H2D. — [source](https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0300_9400_0002_0003)

### AMS heater and H2C induction-hotend rack codes
- `0700-9400-0001-0001` - AMS heater temperature-sensor fault, usually poor connector contact; reseat the sensor connector. Hosted under `/en/h2c/` but the P1S index maps it here too, so it is not H2C-only. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/0700_9400_0001_0001)
- `1A00-0100-0002-0032` - the toolhead failed to detect the hotend on the rack; check the induction-hotend mounting slot for debris. Slots 1 to 6 use `1A00-0100` to `1A00-0600`. No P1S entry (P1S has no rack). — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0032)
- `0500-0500-0001-0020` - hotend authentication failed. Fix: reseat the hotend on the rack and let the printer pick it again, or replace it per Bambu's induction-hotend replacement guide. Hotend positions use `0500` to `0505`. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/0500_0500_0001_0020)
- `1A00-0100-0002-0030` - no hotend found in the named rack slot; install one before pressing Continue. If the hotend's magnet is damaged or missing the hotend is defective; otherwise Bambu points to replacing the dock assembly. Step 2 on the live page was untranslated when checked. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0030)
- `1A00-0100-0002-0034` - hotend dropped while being fetched from the rack. Remove excess filament or debris from the top of the hotend, reinstall, then Continue. Cause given: rack calibration data no longer matches the structure, fixed by re-running the rack setup; also check the cutter for wear. The page's description names the wrong slot (a page error). — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0034)
- `1A00-0100-0002-0027` - toolhead re-centering failed while placing a hotend in the rack. Move the toolhead by hand to the centre of the plate and press Continue; causes are the toolhead stuck in a corner or an object at its travel limit. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0027)
- `1A00-0100-0002-0023` - the rack failed to detect the hotend on the toolhead. Escalation: clean the hotend heatsink surface, check whether the front magnet has fallen off (replace the hotend if so), recalibrate the rack (manual height calibration if that fails), and if it still fails Bambu suspects the dock's Hall sensor and the dock assembly is replaced. — [source](https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0023)

## In practice
- Never decide whether a code applies to your printer from its URL folder. Query `GetHmsWikiList.php` with `id=10` (H2C) or `id=4` (P1S) and the code without dashes, and follow the `wiki_en` link it returns.
- Rack codes (`1A00-...`) and hotend-authentication codes (`0500-...-0020`) are H2C hardware codes.
- Do not assume AMS or bed codes carry over between H2C and P1S; several codes above exist in one index and not the other. Check each code against your model.
- To judge severity of an unfamiliar code quickly, read the third 4-digit group: 0001 Error, 0002 Warning, 0003 Notification. Then look the code up.

## Not verified / open questions
- The alert-level-by-position decoding is an inference: the explainer page gives no digit widths, and its own worked example has 14 digits where real codes have 16.
- The model dropdown values (H2C = 10, P1S = 4) were checked live once; re-check them if the dropdown changes.
- No wiki page here names a firmware or Bambu Studio version; all facts are dated to the fetch date only.

Sources:
- https://wiki.bambulab.com/en/hms/home - master HMS index, model dropdown, search endpoint
- https://e.bambulab.com/wikijs/GetHmsWikiList.php?size=50&lang=en&id=10&hms=0C00030000030008 - per-printer lookup endpoint (H2C example)
- https://e.bambulab.com/wikijs/GetHmsWikiList.php?size=50&lang=en&id=4&hms=0700200000020012 - per-printer lookup endpoint (P1S example)
- https://e.bambulab.com/wikijs/GetHmsWikiList.php?size=50&lang=en&id=4&hms=0700940000010001 - P1S code resolving to an h2c page
- https://wiki.bambulab.com/en/h2c - H2C hub page, links the H2C troubleshooting guides
- https://wiki.bambulab.com/en/h2/troubleshooting - H2 Series Troubleshooting hub
- https://wiki.bambulab.com/en/x1/troubleshooting/intro-hms - code numbering, module IDs, alert levels
- https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0700_2000_0002_0012 - AMS feeder overload
- https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0700_5500_0001_0004 - AMS-extruder binding
- https://wiki.bambulab.com/en/x1/troubleshooting/hmscode/0700_2000_0002_0001 - AMS slot runout
- https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/07FE_2000_0002_0001 - H2C left external spool runout
- https://wiki.bambulab.com/en/x1/troubleshooting/hmscode/0700_7000_0002_0003 - clog warning
- https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0C00_0300_0003_0008 - spaghetti detection
- https://wiki.bambulab.com/en/x1/troubleshooting/hmscode/0300_0D00_0001_0003 - build plate misdetection (P1S)
- https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0300_1800_0001_0006 - bed leveling data abnormal (H2C)
- https://wiki.bambulab.com/en/h2/troubleshooting/hmscode/0300_9400_0002_0003 - chamber temperature not reached
- https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/0700_9400_0001_0001 - AMS heater sensor fault
- https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0032 - rack fetch failure
- https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/0500_0500_0001_0020 - hotend authentication failure
- https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0030 - no hotend in slot
- https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0034 - hotend dropped from rack
- https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0027 - toolhead re-centering failed
- https://wiki.bambulab.com/en/h2c/troubleshooting/hmscode/1A00_0100_0002_0023 - rack cannot detect hotend on toolhead
