# 24 Surfacing and rendering - index

Blender 5.2 LTS look development for printed parts: retopology and UVs, materials, lighting, colour management and headless rendering. Every note lists public sources, mostly the pinned 5.2 manual.

- [retopo-and-uv-blender-5-2.md](retopo-and-uv-blender-5-2.md) - Retopology overlay, Poly Build, snapping, Quadriflow (not for print cleanup; use Voxel), Shrinkwrap and Decimate modes, unwrap methods, Smart UV Project, Pack Islands options and texel density.
- [blender-5-2-materials-and-rendering.md](blender-5-2-materials-and-rendering.md) - Principled BSDF inputs (caption-vs-limit traps), Non-Color data textures, normal map conventions, EEVEE vs Cycles, baking, light power units and table, view transforms, PNG vs EXR, sampling and denoisers.
- [product-render-lighting.md](product-render-lighting.md) - light size vs softness, Normalize, Spread and MIS, AgX vs PBR Neutral vs ACES, False Color, where Exposure is baked in, depth of field, bounces and clamping, plus overreaching claims to avoid.
- [blender-headless-render-cli.md](blender-headless-render-cli.md) - `blender -b` flags and argument order, GPU/OptiX requirements, the engine-enum quirk, STL import and headless camera framing.
- [blender-render-helpers.md](blender-render-helpers.md) - three community Blender helpers for Claude Code compared: which run headless, what they install or delete, and mcp-for-blender's default telemetry and opt-out.
