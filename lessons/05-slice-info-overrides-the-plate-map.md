# Lesson 05: in a sliced 3MF, slice_info.config overrides the plate filament map

Area: Bambu Studio 3MF editing and CLI slicing

| What happened | Root cause | Rule now |
|---|---|---|
| To move all filaments to one extruder, a script set every plate's `filament_map_mode` to Manual and its `filament_maps` in `Metadata/model_settings.config`. A 3MF audit read the new map and passed, the CLI returned success, but every re-sliced G-code still carried the old `; filament_map =` line. | A previously sliced 3MF also stores per-plate `filament_maps` in `Metadata/slice_info.config`. The importer reads it after `model_settings.config`, so it overrides the plate map. The audit read only `model_settings.config` and passed the wrong file. | To regroup a sliced 3MF for the CLI, write Manual and the map in all three places: the project settings (`filament_map_mode`, `filament_map`), every plate in `model_settings.config`, and every plate in `slice_info.config`. Accept the grouping only from the sliced G-code header (`; filament_map =` and `; filament_map_mode =`), never from the input 3MF. |
| The order of precedence was not known when the edit was made. | It had not been read from the source. | Precedence when slicing from the CLI: command-line `--filament_map_mode` / `--filament_map` first, then the plate value, then the project `filament_map` (used only when the plate stores none). |

How to check: after any grouping edit, slice, then read the `; filament_map` and `; filament_map_mode` lines in each plate's G-code header and compare them with what you intended.

Sources (Bambu Studio source, tag v02.08.02.61):
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/BambuStudio.cpp
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/PartPlate.cpp
