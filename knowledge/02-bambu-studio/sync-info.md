# Bambu Studio "Sync info" and "Synchronize filament list from AMS"
Applies to: H2C | P1S (file-dependent) · Bambu Studio 02.08.02.61
Verified: 2026-10-05

All line references are at tag `v02.08.02.61`. Files: [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp), [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp), [SyncAmsInfoDialog.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/SyncAmsInfoDialog.cpp), [PresetBundle.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PresetBundle.cpp), [DeviceManager.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceManager.cpp).

## Facts
### The "Sync info" button
- Label "Sync info"; tooltip says it synchronizes nozzle information and the number of AMS units. Clicking runs the extruder sync, then shows a success popup. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L2701-2703, L4896-4898
- If the printer model differs from the connected printer, it asks "Sync printer information" with "Sync now" / "Cancel"; "Sync now" selects the connected machine's printer preset. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L1975-1994
- It sets each side's nozzle diameter and picks a matching printer preset; if left and right diameters differ it asks you to choose one, since one print cannot mix nozzle diameters. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L1904, L1922-1929, L2091-2094
- It sets the AMS count per extruder, counting 4-slot and 1-slot units (AMS HT) separately. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L2069, L2096-2097
- It writes the nozzle volume (flow) type per extruder after the preset switch, overriding the stored value; this goes into the project config `nozzle_volume_type`, not the process. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L2109, L2122; [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L7740-7746
- It sets the project flags `enable_filament_dynamic_map` and `has_filament_switcher` from the printer's filament-switcher state; every 3MF load first forces both to false. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L2146-2153, L8884-8888
- If the printer reports active arc fitting support, sync turns off Process > Quality > Arc fitting (`enable_arc_fitting`) on the edited process preset (only if it is currently on) and shows a warning notification (not a dialog) explaining it disabled arc fitting for curve planning. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L2134-2143; [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L1322-1330
- That printer flag is a firmware status bit, not a model list; the H2C printer JSONs have no arc key. Release notes for v02.05.03.62 give H2C firmware 01.02.00.00 as the minimum for this feature. -- [DeviceManager.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceManager.cpp) L4470; [release v02.05.03.62](https://github.com/bambulab/BambuStudio/releases/tag/v02.05.03.62)
- Reading the whole sync routine: the only process-preset write is the arc-fitting one; no per-object setting is written (source reading, not GUI-tested). -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L1944-2157

### Process overrides when the printer preset switches
- Process keys that differ from the system preset are saved in the 3MF as `different_settings_to_system` and reload as edits. -- [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1788-1789; [PresetBundle.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PresetBundle.cpp) L3544-3545, L3866-3879
- A printer switch keeps unsaved process and filament edits if they are compatible with the new printer. If they are incompatible, you are asked: accepting discards the edits, declining cancels the switch. Sync does not force the switch. -- [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L6675-6713, L6821-6822; [Tab.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.hpp) L348
- Switching to a printer with a different extruder type or count resets extruder and multi-nozzle parameter changes. -- [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L2884, L2959

### Prompts on opening a 3MF and on slicing
- On opening a project 3MF, Studio tries to match it to the connected printer. The prompt fires when the printer model or the extruder-0 nozzle diameter differs, and only while the "Don't show again" key `sync_after_load_file_show_flag` is absent. An offline printer gives a go-to-device warning instead. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L19634-19662, L19836-19842
- The prompt says the connected printer does not match the project preset and asks you to switch first, with "Switch now" / "Later". A saved "Don't show again" choice is reused silently. "Switch now" selects the printer preset, then syncs the extruder list on multi-extruder printers. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L19665-19696; [ParamsPanel.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ParamsPanel.cpp) L56, L171-179
- At slice time, on multi-extruder printers with objects on the plate, a separate prompt says nozzle type and AMS count were not synced from the printer and offers "Sync now" / "Later". It compares `nozzle_volume_type`, `nozzle_diameter` and the extruder nozzle stats with the printer, plus AMS counts. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L17056-17122, L17156-17200; [MainFrame.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MainFrame.cpp) L2071
- The 3MF stores AMS count and nozzle stats. On load, the file's AMS count is applied only if Studio's in-memory count is empty, so it rarely re-triggers the prompt; nozzle stats are restored per file and can. -- [PresetBundle.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PresetBundle.cpp) L3547-3548, L3826-3831; [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L8903-8904

### "Synchronize filament list from AMS" (separate button)
- This button runs the AMS filament sync; the Sync info success popup also offers "Continue to sync filaments". -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L2950-2952; [SyncAmsInfoDialog.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/SyncAmsInfoDialog.cpp) L3246-3260
- The dialog warns that the project's filament presets and colours will be replaced by the mapped ones and that this "cannot be undone", and that unsaved filament preset edits are discarded. -- [SyncAmsInfoDialog.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/SyncAmsInfoDialog.cpp) L89, L978-979
- Mapping mode syncs filament type and colour only, not slot info. Overwrite mode replaces the project list in printer order and appends unused printer filaments. -- [SyncAmsInfoDialog.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/SyncAmsInfoDialog.cpp) L902-903
- A change in filament count clamps painted colour regions and erases a volume's filament assignment when it is above the new count. -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L4699, L24313-24315; [Model.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp) L3422-3427
- Flush volumes are recalculated for new slots always, and for changed colours unless Preferences > Auto Flush is "disabled". -- [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp) L4709-4713
- Reset is not sync: the tab reset returns all settings to the last saved preset, and the per-option reset drops one change. -- [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L1497, L8475

### Bambu wiki
- The Bambu Studio 2.0.0 release note says dual-nozzle sync covers nozzle diameter, nozzle type and AMS count; that a mismatched 3MF prompts a preset switch; and that filament sync covers colour and type but not the slot. -- [Release note 2.0.0](https://wiki.bambulab.com/en/software/bambu-studio/release/release-note-2-0-0)
- Mapping sync updates project filaments and cannot be reversed automatically. -- [Multi-color printing wiki](https://wiki.bambulab.com/en/software/bambu-studio/multi-color-printing)

## In practice
- "Sync info" changes printer-side state only: printer preset (only if the model differs), nozzle diameter and flow type per side, AMS count per side, and two project flags.
- The only process key it can write is Arc fitting, and only when the printer's firmware reports the feature and the value is currently on. If you deliberately keep a file at `enable_arc_fitting = 0`, sync leaves it alone.
- Process overrides survive while the process preset stays compatible with the new printer preset. If they become incompatible, Studio asks first; declining cancels the switch.
- "Synchronize filament list from AMS" is destructive: it rewrites filament presets and colours with no undo and can drop filament assignments. Sync nozzles first; sync filaments only when you mean to.
- Two prompts exist: the open-time "Switch now / Later" (model and nozzle diameter; stops after Don't show again) and the slice-time "Sync now / Later" (nozzle type and stats restored from each 3MF, so each file can bring it back). See [preferences.md](preferences.md) for the Don't-show-again key and how to reset it.
- To see what a project will trigger, unzip the 3MF and read `Metadata/project_settings.config` for the printer preset, `nozzle_diameter`, the extruder nozzle stats and `different_settings_to_system`.

## Not verified / open questions
- Whether a given H2C reports the arc-fitting flag depends on its firmware version (01.02.00.00 or later per the release note); check your printer's firmware.
- The AMS-count behaviour with a connected printer that has already populated the count is from source reading, not GUI-tested.
- That sync writes no other process key is from source reading, not a GUI test.

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp -- sync routine, prompts, nozzle stats restore
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp -- disable_arc_fitting, preset-switch compatibility
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.hpp -- force_select default
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/SyncAmsInfoDialog.cpp -- filament sync dialog
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MainFrame.cpp -- slice-time AMS check
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceManager.cpp -- arc fitting firmware flag
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ParamsPanel.cpp -- Don't show again logic
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PresetBundle.cpp -- 3MF load of overrides and AMS count
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- different_settings_to_system
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp -- filament count clamp
- https://github.com/bambulab/BambuStudio/releases/tag/v02.05.03.62
- https://wiki.bambulab.com/en/software/bambu-studio/release/release-note-2-0-0
- https://wiki.bambulab.com/en/software/bambu-studio/multi-color-printing
