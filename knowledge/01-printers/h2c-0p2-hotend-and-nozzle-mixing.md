# H2C 0.2 mm hotend and nozzle-size mixing
Applies to: H2C · Bambu Studio 2.8.2.61 (source and profiles at tag v02.08.02.61)
Verified: 2026-10-17

## Facts
- One nozzle diameter per job. The H2C FAQ says the firmware does not yet support mixing nozzle sizes, left vs right or within Vortek hotend sets. Mixed types of the same size (0.4 standard flow + 0.4 high flow) are supported. - [H2C FAQ](https://bambulab.com/en/h2c/faq)
- Bambu Studio release note v02.04.00.70 (2025-11-18): "Slicing with mixed nozzle diameters is not supported." - [release v02.04.00.70](https://api.github.com/repos/bambulab/BambuStudio/releases/tags/v02.04.00.70)
- Wiki: with different diameters on the rack, you must manually select one diameter on the information synchronization interface. - [Bambu Studio H2C operation](https://wiki.bambulab.com/en/h2c/manual/bambu-studio-h2c-operation)
- GitHub feature requests #12431 (opened 2026-10-01) and #8051 (opened 2025-08-30) asking for mixed diameters were both open as of 2026-10-17. Community requests, not Bambu statements. - [#12431](https://github.com/bambulab/BambuStudio/issues/12431), [#8051](https://github.com/bambulab/BambuStudio/issues/8051)
- Printer preset "Bambu Lab H2C 0.2 nozzle" sets `nozzle_diameter` 0.2 on both extruders, inherits the 0.4 preset, and defaults to the process "0.10mm Standard @BBL H2C 0.2 nozzle". - [Bambu Lab H2C 0.2 nozzle.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.2%20nozzle.json)
- Layer-height limits (`min_layer_height` / `max_layer_height`): 0.2 nozzle 0.04-0.14 mm; 0.4 nozzle 0.08-0.28 mm (inherited from `fdm_bbl_3dp_002_common.json`). - [Bambu Lab H2C 0.2 nozzle.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.2%20nozzle.json), [fdm_bbl_3dp_002_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/fdm_bbl_3dp_002_common.json)
- Three 0.2 process presets: layer height 0.08 / 0.10 / 0.12 mm; line widths 0.22 mm, `initial_layer_line_width` 0.25 mm; `wall_loops` 4; `wall_generator` classic (inherited from `fdm_process_common.json`); each is compatible only with "Bambu Lab H2C 0.2 nozzle". - [process folder at v02.08.02.61](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process), [0.10mm Standard @BBL H2C 0.2 nozzle.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.10mm%20Standard%20@BBL%20H2C%200.2%20nozzle.json)
- "Generic PETG @BBL H2C 0.2 nozzle" exists (`setting_id` GFSG99_20, compatible only with the H2C 0.2 printer preset). - [Generic PETG @BBL H2C 0.2 nozzle.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/Generic%20PETG%20@BBL%20H2C%200.2%20nozzle.json)
- Every PETG H2C 0.2 preset (Generic PETG, Generic PETG HF, Bambu PETG Basic, HF, Matte, Translucent) sets `filament_max_volumetric_speed` to 1 mm3/s. For comparison the 0.4 presets: Generic PETG 12, PETG Translucent 6, PETG Basic 18-21 mm3/s. - [filament folder at v02.08.02.61](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament)
- Store rating for the 0.2 induction nozzle: 2 mm3/s, tested with Bambu PLA Basic (not PETG). Store compatibility table, 0.2 column: PETG HF and PETG Basic supported; PETG Translucent "Not recommended"; PETG-CF not supported. - [H2C induction hotend store page](https://us.store.bambulab.com/products/h2c-induction-hotend-right)
- Send dialog (`SelectMachine.cpp` L5725-5727): for the right extruder with the rack supported, Send is blocked with "No hotends available." unless a hotend matching diameter and flow type is on the toolhead or in the rack. - [SelectMachine.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/SelectMachine.cpp), [DevNozzleSystem.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceCore/DevNozzleSystem.cpp)
- Send is also blocked when the toolhead holds a hotend and all 6 rack slots are full; the message asks you to remove at least one hotend before printing (`IsRackMaximumInstalled`). - [DevNozzleSystem.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceCore/DevNozzleSystem.cpp)

## In practice
- A 0.2 job is a whole-job 0.2 job: slice with the "Bambu Lab H2C 0.2 nozzle" printer preset and a 0.2 process preset; do not plan a 0.2 + 0.4 mix in one file.
- PETG on 0.2: expect the 1 mm3/s cap, so slow, and avoid PETG Translucent.
- Before sending, have a 0.2 hotend on the toolhead or in the rack, and keep at least one rack slot free if the toolhead is occupied.

## Not verified / open questions
- Not verified (community only): that the printer swaps the 0.2 hotend in from the rack automatically at print start. - [Bambu forum (community)](https://forum.bambulab.com/t/h2c-thoughts-on-nozzles-aka-vortek-nozzle-configuration/220788). No official sentence found.
- Not behaviour-tested: whether a right-only 0.2 plate is blocked by a 0.4 on the left.
- The profile `nozzle_type` says hardened steel while the store names the 0.2 "Stainless Steel"; not reconciled.

Sources:
- https://bambulab.com/en/h2c/faq - firmware does not support mixing nozzle sizes
- https://wiki.bambulab.com/en/h2c/manual/bambu-studio-h2c-operation - one diameter selected at sync
- https://us.store.bambulab.com/products/h2c-induction-hotend-right - 2 mm3/s (PLA Basic), PETG compatibility
- https://api.github.com/repos/bambulab/BambuStudio/releases/tags/v02.04.00.70 - mixed diameters unsupported
- https://github.com/bambulab/BambuStudio/issues/12431 - open feature request (community)
- https://github.com/bambulab/BambuStudio/issues/8051 - open feature request (community)
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.2%20nozzle.json - 0.2 printer preset
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/fdm_bbl_3dp_002_common.json - 0.4 layer-height limits
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process - 0.2 process presets
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament - PETG 0.2 presets, volumetric caps
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/SelectMachine.cpp - send-dialog rule
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceCore/DevNozzleSystem.cpp - nozzle match and rack-full rule
- https://forum.bambulab.com/t/h2c-thoughts-on-nozzles-aka-vortek-nozzle-configuration/220788 - community: auto swap at print start
