# 02 Bambu Studio - index

Bambu Studio settings, presets and tools, cited by UI label and config key with links to the Bambu wiki and the bambulab/BambuStudio source. Preset values are read from Bambu's published profiles; check them against the profile bundle you have installed.

## Process settings, tab by tab
- [quality-tab-settings.md](quality-tab-settings.md) - every Process > Quality setting (layer height, line width, seam and scarf, precision, ironing, wall generator, advanced), including Develop-mode-only rows.
- [strength-tab-settings.md](strength-tab-settings.md) - every Process > Strength setting, including infill rows that only appear for certain patterns.
- [speed-tab-settings.md](speed-tab-settings.md) - every Process > Speed setting and how the H2C's 5-value arrays map to nozzle variants.
- [support-settings.md](support-settings.md) - what actually controls support: Enable support, Max bridge length vs Don't support bridges, Default style becoming Tree Organic, blockers and missing options.
- [others-tab-settings.md](others-tab-settings.md) - every Process > Others setting (brim, prime tower, flush options, special modes, fuzzy skin, interlocking, G-code output) with defaults and H2C preset values.
- [h2c-process-presets.md](h2c-process-presets.md) - the five H2C 0.4 mm process presets compared setting by setting, plus seam, brim, wall and chamber rules.

## Choosing settings
- [speed-quality-method.md](speed-quality-method.md) - picking an outer-wall speed for display surfaces: preset speeds, settings that do nothing on Bambu presets, minimum layer time, the volumetric cap, gloss and silk guidance.
- [pattern-selection-guide.md](pattern-selection-guide.md) - choosing top, bottom, internal solid and sparse infill patterns, the `zig-zag`/`zigzag` stored-value trap and a table by part type.
- [ironing-and-top-surface-pattern.md](ironing-and-top-surface-pattern.md) - ironing type and pattern, H2C ironing values, how ironing flow is calculated, top surface patterns and per-object overrides.
- [seam-painting.md](seam-painting.md) - the seam painting tool's labels, keys and mouse actions, how Seam position = Back chooses its point, and how paint is stored in the 3MF.
- [support-enforcers-and-critical-regions.md](support-enforcers-and-critical-regions.md) - how enforcers and "Support critical regions only" behave in Tree Hybrid: the area rules, tip rules and roof merging.
- [support-top-z-same-filament.md](support-top-z-same-filament.md) - support gap settings, what a typed Top Z becomes in each support style, and how to read the real gap back from the G-code.

## Multi-material and the H2C
- [grouping-and-purge.md](grouping-and-purge.md) - H2C filament grouping modes and storage, LEFT = 1 / RIGHT = 2, which file wins in a sliced 3MF, purge and pre-cooling, prime-tower settings and clearance checks.
- [sync-info.md](sync-info.md) - what Sync info changes, the two mismatch prompts, and why "Synchronize filament list from AMS" overwrites your list.

## Checking a slice
- [cli-slicing.md](cli-slicing.md) - CLI slice flags, `result.json` fields and their limits, return codes, which keys work as CLI flags, preset inheritance, and why stdout/stderr text is lost on Windows.
- [gui-checks.md](gui-checks.md) - checks the GUI shows that the CLI does not reliably report, and how to repeat each one in your own code.

## App and camera
- [preferences.md](preferences.md) - every option in the Preferences dialog with its config key and default, the 3MF "Switch now / Later" prompt, and Auto sync user presets.
- [live-view-limits-and-camera-full-screen.md](live-view-limits-and-camera-full-screen.md) - live-view idle timeouts, "Keep liveview when printing.", viewer limits, the Camera Full Screen window and H2C camera specs.
- [go-live-virtual-camera.md](go-live-virtual-camera.md) - the Go Live virtual camera: its preconditions, LAN vs cloud route, the access code stored in `url.txt`, supported printers and OBS setup.
