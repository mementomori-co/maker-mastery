# Blender 5.2 headless (background) render recipe

Applies to: any printer (render-side only) - Blender 5.2 LTS; run Blender from your Blender install path, set in config\paths.yaml (key `blender_exe`)
Verified: 2026-10-03

## Facts

### Command-line flags
- `-b` / `--background` runs Blender without a UI, usually for rendering; audio is off in background mode unless re-enabled with `-setaudio Default`. - [Command Line Arguments](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html)
- `-P` / `--python <filepath>` runs a Python script file; `--python-expr <expression>` runs an expression, which may be a whole multi-line script, limited only by the platform's maximum argument length. - [Command Line Arguments](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html)
- `-o` / `--render-output` sets the output path and name: `//` makes it relative to the .blend file, path templates such as `{blend_name}` work, and a `####` frame suffix is added when the name has no `#`. - [Command Line Arguments](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html)
- `-F` / `--render-format` accepts `TGA RAWTGA JPEG IRIS PNG BMP HDR TIFF`, plus build-dependent `OPEN_EXR OPEN_EXR_MULTILAYER FFMPEG CINEON DPX JP2 WEBP`. - [Command Line Arguments](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html)
- `-f` / `--render-frame <frame>` renders one frame; `+N`/`-N` are relative to start/end, and comma lists and inclusive `a..b` ranges work. `-E` / `--engine` sets the engine; `-E help` lists engines. - [Command Line Arguments](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html)
- `--cycles-device <device>` goes after a literal `--`. Values: `CPU CUDA OPTIX HIP ONEAPI METAL`; add `+CPU` to a GPU device to use both. Manual example: `blender -b file.blend -f 20 -- --cycles-device OPTIX`. - [Command Line Arguments](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html)
- Arguments run in the order given: a frame rendered before `--render-output` is set ignores that path, and loading the .blend (the positional file name) overwrites an output path set before it. Correct order: `blender --background test.blend --render-output /tmp --render-frame 1`. - [Command Line Arguments](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html)
- Single-frame example: `blender -b file.blend -f 10`. The manual says to keep `-f` or `-a` last and that arguments are case sensitive (`-F` is not `-f`). Engine and threads example: `blender -b file.blend -E CYCLES -s 10 -e 500 -t 2 -a`. - [Command Line Rendering](https://docs.blender.org/manual/en/5.2/advanced/command_line/render.html)

### GPU rendering (Cycles)
- To render on a GPU, pick the backend (CUDA, OptiX, HIP, oneAPI or Metal) in the Cycles Render Devices preference, enable the devices, then set each scene's Device to GPU Compute. - [GPU Rendering](https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html)
- OptiX runs on Windows and Linux and needs an NVIDIA card with compute capability 5.0 or higher and driver 575 or newer. - [GPU Rendering](https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html)
- Blender 5.2 raised the minimum OptiX driver to 575. - [5.2 Cycles release notes](https://developer.blender.org/docs/release_notes/5.2/cycles/)
- The GPU Rendering page has no Python example for enabling devices (checked on that page only). - [GPU Rendering](https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html)

### Render engine in the Python API
- `Scene.cycles` is a read-only property of type `CyclesRenderSettings`. - [bpy.types.Scene](https://docs.blender.org/api/5.2/bpy.types.Scene.html)
- `bpy.types.CyclesPreferences` and `bpy.types.CyclesRenderSettings` had no API page in 5.2 (both URLs returned 404 at check; only these two URLs were tried). - [CyclesPreferences URL](https://docs.blender.org/api/5.2/bpy.types.CyclesPreferences.html), [CyclesRenderSettings URL](https://docs.blender.org/api/5.2/bpy.types.CyclesRenderSettings.html)
- `scene.render.engine` is a dynamic enum whose RNA item list can under-report: in one background session the list read back as only `BLENDER_EEVEE`, yet `BLENDER_WORKBENCH` and `CYCLES` both assigned, and a bogus value raised a `TypeError` naming all three accepted engines. Not verified (no public source; a single local measurement).

### STL import and camera framing
- `bpy.ops.wm.stl_import(...)` imports an STL as an object; the page documents the full signature, including `global_scale`, `use_scene_unit`, `forward_axis`, `up_axis` and `use_mesh_validate`. - [bpy.ops.wm](https://docs.blender.org/api/5.2/bpy.ops.wm.html)
- `bpy.ops.view3d.camera_to_view_selected()` moves the camera to frame the selected objects. In the 5.2 source its poll is `ED_operator_scene_editable` (no 3D viewport needed) and the code treats the 3D view as possibly null and falls back to `scene->camera`, so it can run in `-b` mode when `scene.camera` is set and objects are selected. - [bpy.ops.view3d](https://docs.blender.org/api/5.2/bpy.ops.view3d.html), [view3d_view.cc](https://projects.blender.org/blender/blender/raw/branch/blender-v5.2-release/source/blender/editors/space_view3d/view3d_view.cc)
- A background run that called it returned `{'FINISHED'}` and moved the camera; in that run `window_manager.windows` had 1 entry, not 0. Not verified (no public source; a single local measurement that agrees with the source code above).

## In practice
- Minimal headless render of one STL: `blender -b --factory-startup --python script.py -- --cycles-device OPTIX`, where `script.py` imports the STL with `wm.stl_import`, sets `scene.render.engine` inside `try/except TypeError` (do not trust the enum list), frames the camera, sets `render.filepath` and the image format, then calls `bpy.ops.render.render(write_still=True)`.
- Quick render-time check: `blender -b file.blend -E CYCLES -t 2 -f 10`; use `-a` for the whole range, and keep `-f`/`-a` last. Add `--python-exit-code 1` so a script error fails the run.
- Do not rely on the Cycles API doc pages to discover GPU-device properties in 5.2; read them from a running instance.
- `camera_to_view_selected()` is a valid headless framing option; computing the camera position and orthographic scale yourself is an equally valid alternative.
- For OptiX, confirm the driver is 575 or newer before blaming your script.

## Not verified / open questions
- Whether other `view3d.*` operators need a real 3D viewport in `-b` mode was not checked; each has its own poll.
- The "no API page" result for the two Cycles classes covers only the two URLs tried, not the whole API tree.
- The engine-enum under-report was seen once on one Windows build; whether it happens on every platform is unknown.

Sources:
- https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html - command-line flags and argument order
- https://docs.blender.org/manual/en/5.2/advanced/command_line/render.html - background render examples, `-f`/`-a` last, case sensitivity
- https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html - GPU enable steps, OptiX requirements
- https://developer.blender.org/docs/release_notes/5.2/cycles/ - OptiX driver minimum 575
- https://docs.blender.org/api/5.2/bpy.types.Scene.html - `Scene.cycles` read-only
- https://docs.blender.org/api/5.2/bpy.types.CyclesPreferences.html - 404 at check
- https://docs.blender.org/api/5.2/bpy.types.CyclesRenderSettings.html - 404 at check
- https://docs.blender.org/api/5.2/bpy.ops.wm.html - `wm.stl_import` signature
- https://docs.blender.org/api/5.2/bpy.ops.view3d.html - `camera_to_view_selected`
- https://projects.blender.org/blender/blender/raw/branch/blender-v5.2-release/source/blender/editors/space_view3d/view3d_view.cc - operator poll and null-view fallback
