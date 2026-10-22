# Bambu Studio Preferences dialog (every option)
Applies to: both (H2C, P1S) · Bambu Studio 02.08.02.61 on Windows
Verified: 2026-10-06

Scope: source at tag `v02.08.02.61`. A config key lives in the `app` section of `%APPDATA%\BambuStudio\BambuStudio.conf` unless noted. The dialog has no dedicated Bambu wiki page. This note lists what each option does and its code default; it does not recommend personal values except where a sourced fact supports it.

Source abbreviations (all at tag v02.08.02.61):
- P = [Preferences.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp)
- A = [AppConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.cpp) (defaults in `set_defaults`)
- G = [GUI_App.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_App.cpp)
- MF = [MainFrame.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MainFrame.cpp)
- PL = [Plater.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp)
- PP = [ParamsPanel.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ParamsPanel.cpp)

## Facts

### Opening the dialog (Windows)
- Title bar: the unlabelled dropdown icon to the right of "File" > "Preferences", shortcut Ctrl+P (read from source, label not verified in the GUI). -- [BBLTopbar.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/BBLTopbar.cpp) L213-221, L629-636; [MF](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MainFrame.cpp) L737-743, L3548-3551

### General > General Settings
| UI label | config key | values / default | what it does | source |
|---|---|---|---|---|
| Language | `language` | no default | Changing it needs an app restart | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Login Region | `region` | Asia-Pacific, Chinese Mainland (stored "China"), Europe, North America, Others | Changing it logs your account out; Reset preferences keeps it | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Units | `use_inches` | Metric "0" / Imperial "1"; default "0". A separate `units` key exists but the dialog does not write it | Read by the G-code viewer renderer and the move/scale gizmo | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [A](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.cpp), [BaseRenderer.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GCodeRenderer/BaseRenderer.cpp), [GizmoObjectManipulation.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GizmoObjectManipulation.cpp) |
| Auto Flush | `auto_calculate_flush` | all / color change / disabled; default all | When flush volumes are recalculated; the choice is also sent as a tracking event | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [A](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.cpp) |
| Enable dark mode (Windows only) | `dark_color_mode` | default "0" | Dark UI theme | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [AppConfig.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.hpp) |
| Keep only one Bambu Studio instance | `single_instance` | default false | A second launch reactivates the running instance | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [A](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.cpp) |
| Filament Manager (Take effect after restarting Studio) | `studio_enable_fila_manager` | default true on Windows, false on macOS | Enables the Filament Manager | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [wgtFilaManagerFeature.h](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/fila_manager/wgtFilaManagerFeature.h) |
| Multi-device Management(Take effect after restarting Studio). | `enable_multi_machine` | default false | Send one task to several devices and manage them together | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Support beta version update. | `enable_beta_version_update` | default true | Adds a beta check on top of the always-run stable check; the only update-channel control | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [G](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_App.cpp), [BetaVersionDialog.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/BetaVersionDialog.cpp) |
| Join the User Experience Improvement Program. | `privacyuse` (section `firstguide`) | no default | Unticking disables tracking and removes the local tracking files | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Download path + Browse | `download_path` | default "" | Download folder | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |

### User > User Settings
| UI label | config key | values / default | what it does | source |
|---|---|---|---|---|
| time format for print progress | `use_12h_time_format` | default false (24-hour) | 12-hour AM/PM display | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Auto plate type | `user_bed_type` | default true | Remembers the last plate chosen per printer model | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Keep liveview when printing. | `auto_stop_liveview` (section `liveview`) | stored inverted: key true = box unticked; default true | Live view pauses after 15 minutes of computer inactivity unless ticked | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Automatically transfer modified value when switching process and filament presets | `auto_transfer_when_switch_preset` | default true | When off, a popup asks each time | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Remove the restriction on mixed printing of high and low temperature filaments. | `enable_high_low_temp_mixed_printing` | default false | Ticking shows a bed-temperature-difference warning linking to the [filament config limit wiki](https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit); any answer but Yes reverts it | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Auto sync user presets(Printer/Filament/Process) | `sync_user_preset` | default false | Starts or stops cloud sync of user presets; the post-login Synchronization dialog also writes this key | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [G](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_App.cpp) |
| Auto check for system presets updates | `sync_system_preset` | default true | Checks for system preset updates after startup | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Auto-fill previously logged-in accounts. (Windows) | `webview_auto_fill` | default true; empty tooltip | Not traced beyond the label | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |

### 3D > 3D Settings
| UI label | config key | values / default | what it does | source |
|---|---|---|---|---|
| Display overview | `enable_assemble_view_preview` | Auto / Open / Close; default Auto | Auto writes `enable_bvh` true, Open writes it false | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Grabber scale | `grabber_size_factor` | 1.0-2.5; default 1.0 | Gizmo grabber size | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Tooltip offset (x and y) | `3d_middle_tooltip_offset_x` / `_y` | 0-150; default 0 | Offsets the 3D tooltip | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Toolbar Style | `toolbar_style` | Collapsible "0" / Uncollapsible "1"; empty = Collapsible | Toolbar layout | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Zoom to mouse position | `zoom_to_mouse` | default false | Zoom toward the pointer | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Always show shells in preview | `show_shells_in_preview` | default true | Reslice after changing it | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Show Thermal Preconditioning Area | `show_bed_heat_soak_area` | default true | Warns when a model extends past the heat-soak area, on printers that have one | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp), [commit 604b50a](https://github.com/bambulab/BambuStudio/commit/604b50a) |
| Show the step mesh parameter setting dialog. | `enable_step_mesh_setting` | default true | Mesh-parameter dialog on STEP import | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Import a single SVG and split it | `import_single_svg_and_split` | default true | Splits one imported SVG into parts | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Enable gamma correction for the imported obj file | `gamma_correct_in_import_obj` | default false | Colour gamma on OBJ import | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Remember last used color scheme | `enable_record_gcodeviewer_option_item` | default false | Restores the last preview colour scheme at startup | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Improve rendering performance by lod | `enable_lod` | default true | Level-of-detail rendering; restart needed | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Enable advanced gcode viewer | `enable_advanced_gcode_viewer_` (trailing underscore is real) | default true | Switches the G-code viewer | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Open full screen camera view on active monitor only. | `camera_fullscreen_active_monitor_only` | default true | Full-screen camera opens on the monitor holding Bambu Studio | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |

A row "Show assembly BVH primary bounds" (`show_assembly_bvh_bounds`) exists in the source only under `#if !BBL_RELEASE_TO_PUBLIC`, so it should not appear in official builds. -- [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp)

### Other tab
| Section > UI label | config key | values / default | what it does | source |
|---|---|---|---|---|
| Project > Maximum recent projects | `max_recent_count` | default 18 | Recent-projects list length | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Project > Auto-Backup | `backup_interval` (+ `backup_switch`) | seconds 10, 20, 30, 60, 120, 300, 600, 1800, 0; default 10; forced 0 if `backup_switch` is not true | Project backup period | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Project > No warnings when loading 3MF with modified G-codes | `no_warn_when_modified_gcodes` | no default | Suppresses that warning | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Online Models > Show online staff-picked models on the home page | `staff_pick_switch` | default true; shown only in regions with the model mall | Home page | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Online Models > Show history on the home page | `show_print_history` | default true | Home page | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Developer Mode > Develop mode | `developer_mode` | default false | On switches the UI to Develop mode, which unhides Develop-only settings; off returns to Advanced | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Developer Mode > Skip AMS blacklist check | `skip_ams_blacklist_check` | no default | Not traced beyond the label | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Developer Mode > Enable DevTools For Webview (Take effect after restarting Studio) | `enable_webview_devtools` | default false | Webview developer tools | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |
| Associate Files To Bambu Studio > .3mf / .stl / .step/.stp | `associate_3mf`, `associate_stl`, `associate_step` | default false each | Makes Bambu Studio the default app for that type | [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp) |

### Developer Tools tab (compiled out of public builds)
- The tab is added only under `#if !BBL_RELEASE_TO_PUBLIC`; `version.inc` defaults that flag to "0", so official builds must set it to 1. Its rows: Log Level (`severity_level`, default info), Internal developer mode, Enable SSL(MQTT), Enable SSL(FTP), Host Setting (`iot_environment`). -- [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp); [version.inc](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/version.inc)

### Bottom buttons
- Reset all warning dialogs: erases `sync_after_load_file_show_flag`, `skip_non_bambu_3mf_warning`, `post_process_script_choice` and `no_warn_mixed_sublayer_variable_layer`; sets `show_support_recommend_dialog` true and clears `save_project_choise`. -- [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp)
- Reset preferences: after a confirm, erases only the UI preference keys (list `kPrefKeys`; vendor, printer, preset state and Login Region are kept), then reapplies defaults. The erase loop works on section `app` only, so `privacyuse` (section `firstguide`) and `auto_stop_liveview` (section `liveview`) are listed but not actually reset. -- [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp)

### The open-time "Switch now / Later" prompt
- After a 3MF project loads, Studio checks the printer selected on the Device page. If that printer is online and ready, and the project's printer type or extruder-0 nozzle diameter differs, it shows a "Tips" dialog with "Switch now" / "Later" and a "Don't show again" box. An offline printer gives a "Sync printer information" warning instead. -- [PL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp)
- With Don't show again ticked, "Switch now" stores `sync_after_load_file_show_flag` true and "Later" stores false. Once the key exists the prompt never shows again; true means Studio switches silently whenever the printer differs. Reset all warning dialogs erases the key. -- [PP](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ParamsPanel.cpp); [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp)
- A separate slice-time "Sync now" / "Later" warning (nozzle type and AMS count not synced) has no Don't-show-again key here; see [sync-info.md](sync-info.md). -- [PL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp)

### Auto sync user presets
- Runs only while logged in: at app start and after a network restart when `sync_user_preset` is true, and immediately when the box is ticked. Logout or unticking stops it. -- [G](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_App.cpp)
- After every online login a "Synchronization" dialog asks whether to sync Process, Filament and Printer presets from Bambu Cloud. Yes writes `sync_user_preset` true and starts sync; No writes false. That answer overrides the Preferences checkbox. -- [MF](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MainFrame.cpp); [G](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_App.cpp)
- The loop downloads the cloud preset list, loads cloud user presets locally, then about every 2 s uploads changed user presets (system presets are skipped) and deletes cloud copies of locally deleted ones. -- [G](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_App.cpp)
- Bambu's wiki: user presets upload to Bambu Cloud under the logged-in account; presets for non-Bambu printers are not cloud-synced; a project preset is saved only in the 3MF and is not uploaded. -- [Preset wiki](https://wiki.bambulab.com/en/software/bambu-studio/preset)

### What Preferences does not control
- No Preferences option protects project settings from Sync. The real controls are the Don't-show-again key above and the 3MF load dialog's "Open as project" / "Import geometry only" (`import_3mf_as_project`, default true, not in Preferences). -- [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp); [PL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp); [A](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.cpp)
- Default presets come from the printer's machine profile (`default_print_profile`, `default_filament_profile`), not Preferences. H2C 0.4 nozzle: "0.20mm Standard @BBL H2C" with "Bambu PLA Basic @BBL H2C". P1S 0.4 nozzle: "0.20mm Standard @BBL X1C" with "Bambu PLA Basic @BBL P1S 0.4 nozzle". The `presets` section of the conf holds the last selection, not a default. -- [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); [H2C 0.4 machine profile](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.4%20nozzle.json); [P1S 0.4 machine profile](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20P1S%200.4%20nozzle.json)
- There is no stable/beta selector; the stable check always runs. -- [G](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_App.cpp)
- No network plug-in, LAN-mode, proxy, multicast or video-stream setting exists in the dialog (string search of the source). The network plug-in install is prompted from the main window instead. Bambu's wiki says the plug-in provides WAN/LAN printing, remote control and user data sync. -- [P](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp); [MF](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MainFrame.cpp); [Quick start wiki](https://wiki.bambulab.com/en/software/bambu-studio/studio-quick-start)

## In practice
- If you keep scripted or audited 3MF files, answer **Later** to the open-time prompt and leave Don't show again unticked. "Switch now" swaps to the connected printer's preset and can reset extruder edits; ticking Don't show again with "Switch now" makes that silent forever (until Reset all warning dialogs).
- Open project files with "Open as project", not "Import geometry only", so the project's own presets load.
- Consider turning off "Automatically transfer modified value when switching process and filament presets": with it on, unsaved edits ride silently into the next preset; off makes Studio ask each time (tooltip fact above). This is a judgement call.
- Keep "No warnings when loading 3MF with modified G-codes" unticked: a modified-G-code warning is something to read.
- If your notes or scripts cite a specific Bambu Studio tag, leave beta updates off and re-check those notes before accepting a stable update.
- Do not press Reset preferences or Reset all warning dialogs unless you mean to undo every choice above.
- To see what your own install is set to, read `%APPDATA%\BambuStudio\BambuStudio.conf` (read-only; it also holds account data, so never share it).

## Not verified / open questions
- Skip AMS blacklist check and Auto-fill previously logged-in accounts. (Windows): behaviour beyond the label not traced.
- Whether a cloud reload during Auto sync changes a user preset already selected in an open project: not traced.
- The sync loop and the login dialog are from code reading only, not GUI-tested.
- The "no network options" statement rests on a string search of Preferences.cpp, not on opening the dialog.
- Whether the Developer Tools tab is absent from your build: check the dialog yourself.
- The placement of the three Project rows under Other > Project follows on-screen order, not a source line.
- Whether "Keep only one Bambu Studio instance" also intercepts a command-line launch of `bambu-studio.exe`: not traced.
- Whether "Auto check for system presets updates" installs an update without asking: not traced.
- No Bambu wiki page for the Preferences dialog was found.

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Preferences.cpp -- every label, key, tooltip and reset behaviour
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.cpp -- defaults
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/AppConfig.hpp -- dark mode support flag
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_App.cpp -- sync thread, beta check
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/MainFrame.cpp -- Synchronization dialog, plug-in prompt, menu entry
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/BBLTopbar.cpp -- title-bar dropdown
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp -- open-time and slice-time prompts, Open as project
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ParamsPanel.cpp -- Don't show again key
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- default profile keys
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/BetaVersionDialog.cpp
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GCodeRenderer/BaseRenderer.cpp
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GizmoObjectManipulation.cpp
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/fila_manager/wgtFilaManagerFeature.h
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/version.inc
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.4%20nozzle.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20P1S%200.4%20nozzle.json
- https://github.com/bambulab/BambuStudio/commit/604b50a -- heat-soak area preference
- https://wiki.bambulab.com/en/software/bambu-studio/preset
- https://wiki.bambulab.com/en/software/bambu-studio/studio-quick-start
- https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit
