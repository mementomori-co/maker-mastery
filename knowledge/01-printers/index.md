# 01 Printers - index

Hardware facts for the Bambu Lab H2C and P1S and their AMS units: architecture, hotends, cooling, filament changes and spec limits. Every fact links a public source (Bambu wiki, store, or the bambulab/BambuStudio repository).

- [h2c-architecture.md](h2c-architecture.md) - H2C hotend positions and counts, combo contents, which inlet feeds which hotend, printable area per nozzle (and where official heights disagree), hotend memory, filament-to-hotend mapping, Sync info and the send-time check.
- [h2c-filament-change-dedicated-hotends.md](h2c-filament-change-dedicated-hotends.md) - the physical hotend-swap sequence, change G-code, flush = 0 while a tower prime remains, Purge mode (Standard / Prime Saving), and what the time estimate includes.
- [h2c-0p2-hotend-and-nozzle-mixing.md](h2c-0p2-hotend-and-nozzle-mixing.md) - one nozzle diameter per job, the 0.2 mm presets, the PETG 0.2 mm 1 mm3/s cap, and the Send-dialog blocks for a missing hotend or a full rack.
- [h2c-cooling-mode-and-auto-vent.md](h2c-cooling-mode-and-auto-vent.md) - how the H2C chooses its cooling mode for PLA from the start G-code, auto-vent behaviour, and Bambu's door and top-glass guidance compared with the P1S.
- [ams-2-pro-auto-refill-and-drying.md](ams-2-pro-auto-refill-and-drying.md) - turning on AMS filament backup (auto-refill), where its dialog lives, PLA and PETG drying presets, and the manual-vs-wiki conflict on drying while printing.
- [ams-compatibility-h2c.md](ams-compatibility-h2c.md) - using a first-generation AMS on the H2C: what is and is not officially covered, cabling, buffer and adapter, PTFE length, left-hotend TPU limits and a checklist.
- [p1s-vs-h2c-specs.md](p1s-vs-h2c-specs.md) - official P1S and H2C limits side by side (volume, temperatures, chamber, nozzles, filaments, speed, flow, AMS count, firmware), including the P1S 250 mm slicer Z limit.
