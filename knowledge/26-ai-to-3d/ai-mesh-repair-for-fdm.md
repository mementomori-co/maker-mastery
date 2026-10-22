# Cleaning AI-generated and scanned meshes for FDM printing

Applies to: any Bambu printer · Bambu Studio on Windows (Fix Model)
Verified: 2026-10-04

The mesh-validity tools used before this step are in [code-cad-toolchain.md](../05-cad-hard-surface/code-cad-toolchain.md) (trimesh, manifold3d) and [sculpt-to-printable.md](../06-organic-modeling/sculpt-to-printable.md) (Blender 3D Print Toolbox). This note covers the Bambu Studio side, the last resort after those.

## Facts
- Bambu Studio repairs models to a degree automatically; on Windows 10/11 it can also use Microsoft's Netfabb-based repair API, which is Windows-only. - [Bambu wiki: Fix Model](https://wiki.bambulab.com/en/software/bambu-studio/fix-model)
- Studio detects and repairs only some errors; some defects stay undetected and no repair prompt appears. - [Bambu wiki: Fix Model](https://wiki.bambulab.com/en/software/bambu-studio/fix-model)
- Bambu says models with uneven surfaces, such as 3D scans, often print poorly, worse with Arc Fitting on; it advises disabling Arc Fitting and smoothing in MeshLab or similar. - [Bambu wiki: Fix Model](https://wiki.bambulab.com/en/software/bambu-studio/fix-model)

## In practice
1. Run a generated or scanned mesh through the code checks first: `trimesh.load(..., process=True)`, then `is_watertight` / `is_volume`, then the 3D Print Toolbox Make Manifold or Hollow if needed. Check the generation service's output licence first ([generation-services-pricing-and-licences.md](generation-services-pricing-and-licences.md)).
2. Fall back to Bambu Studio's Fix Model only if the mesh still will not slice cleanly, remembering it can miss defects silently.
3. For noisy or uneven meshes (scans, low-detail AI output), slice with Arc Fitting off; see [quality-tab-settings.md](../02-bambu-studio/quality-tab-settings.md) for the setting.

## Not verified / open questions
- Fix Model's exact in-app location was not checked on screen; only the wiki text was read.
- Why Arc Fitting amplifies defects on uneven meshes is not explained on the page and was not measured.
- No dedicated Bambu wiki page on Arc Fitting was found (the guessed URL returned 404).

Sources:
- https://wiki.bambulab.com/en/software/bambu-studio/fix-model - Windows-only Netfabb repair; Arc Fitting advice for scanned meshes
