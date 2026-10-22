# AI-to-3D generation services: pricing, output licences, API details

Applies to: any printer (cloud and local generators, not slicer settings) · Hyper3D Rodin Gen-2.5 API, Tripo, Meshy, Tencent Hunyuan3D-2 and 2.1 (pages read 2026-10-04; prices and terms change)
Verified: 2026-10-04

This is a summary of public pages, not legal advice. Re-read each service's terms before you sell anything.

## Facts

### Hyper3D Rodin (Gen-2.5 API)
- `tier` selects the generation family and detail level and combines freely with `mesh_mode`, `quality` and `texture_mode`. - [Rodin Gen-2.5 API spec](https://docs.hyper3d.ai/en/api-specification/rodin-gen2-5)
- `tier` is required; if omitted the endpoint falls back to "Regular" and generates a Gen-1/1.5 asset instead of Gen-2.5. - [Rodin Gen-2.5 API spec](https://docs.hyper3d.ai/en/api-specification/rodin-gen2-5)
- Five Gen-2.5 tiers: Extreme-Low, Low, Medium, High and Extreme-High (which also returns an extra mesh up to 10M faces). - [Rodin Gen-2.5 API spec](https://docs.hyper3d.ai/en/api-specification/rodin-gen2-5)
- `geometry_file_format`: `glb` (default), `usdz`, `fbx`, `obj`, `stl`. - [Rodin Gen-2.5 API spec](https://docs.hyper3d.ai/en/api-specification/rodin-gen2-5)
- `texture_mode`: `legacy`, `extreme-low`, `low`, `medium`, `high`, `extreme-high`, each tier with its own default; resolution also depends on the HighPack add-on and `uhd_texture` (for example `extreme-high` from 6K to 12K). - [Rodin Gen-2.5 API spec](https://docs.hyper3d.ai/en/api-specification/rodin-gen2-5)
- Credits add to a 0.5-credit base: the Extreme-High tier adds 0.5, `texture_mode=extreme-high` adds 2.0. - [Rodin Gen-2.5 API spec](https://docs.hyper3d.ai/en/api-specification/rodin-gen2-5)
- Rodin output: Hyper3D says it "will not limit your use of such Output", subject to its agreements, law and third-party terms, and makes no warranty about copyrightability. - [Hyper3D Terms](https://hyper3d.ai/legal/terms)
- ChatAvatar output is for personal entertainment use by default; commercial use needs a purchased licence for that output. The Business plan bundles a ChatAvatar commercial licence. - [Hyper3D Terms](https://hyper3d.ai/legal/terms), [Hyper3D Pricing](https://hyper3d.ai/pricing)
- Pricing as read: Free tier pays per confirmed result at $1.5 per credit; Creator from $30/month ($24 billed yearly, about 60 models); Business with API access from $120/month ($96 yearly, about 416 models); Enterprise custom; education pricing with verification. - [Hyper3D Pricing](https://hyper3d.ai/pricing)

### Tripo
- Free: $0, 200 monthly credits (about 13 models), public models, non-commercial use. Pro: $20/month billed annually ($240/year), 3,000 credits (about 200 models), private models, commercial use. The page refused a minimal browser User-Agent. - [Tripo Pricing](https://www.tripo3d.ai/pricing)

### Meshy
- Free-plan output is owned by Meshy and licensed to you under CC BY 4.0, so commercial use requires credit to Meshy (Terms section 3.2). - [Meshy Terms of Use](https://www.meshy.ai/terms-of-use), [Meshy Pricing](https://www.meshy.ai/pricing)
- On a paid plan you own your output (section 3.2), but anything posted to the Meshy Community page is licensed CC0 regardless of plan (section 3.3). - [Meshy Terms of Use](https://www.meshy.ai/terms-of-use)
- The terms live at /terms-of-use; /terms returns 404. - [Meshy Terms of Use](https://www.meshy.ai/terms-of-use)

### Tencent Hunyuan3D (2.0 and 2.1)
- Both community licences exclude the European Union, the United Kingdom and South Korea from the licensed Territory. - [Hunyuan3D-2 LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE), [Hunyuan3D-2.1 LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE)
- Above 1 million monthly active users in the preceding month you must request a separate licence from Tencent (same in both). - [Hunyuan3D-2 LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE)
- Hunyuan3D-2.1 needs 10 GB VRAM for shape, 21 GB for texture and 29 GB for both; the often-quoted 6/16 GB figures come from the separate Hunyuan3D-2 README. A 24 GB card is below the 29 GB combined figure; the README documents a `--low_vram_mode` flag (effect not measured). - [Hunyuan3D-2.1 README](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/README.md), [Hunyuan3D-2 README](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/README.md)

## In practice
- Always send Rodin's `tier` explicitly.
- Before selling a generated model: Rodin output is not limited by Hyper3D (law and third-party rights still apply); Tripo Free is non-commercial; Meshy Free needs visible credit; Hunyuan3D weights are not licensed in the EU, UK or South Korea.
- Do not post Meshy assets you want to keep exclusive to the Meshy Community page.
- Re-check pricing pages before spending; both Hyper3D and Tripo use sliders and undated prices.
- Clean every generated mesh before slicing: [ai-mesh-repair-for-fdm.md](ai-mesh-repair-for-fdm.md).

## Not verified / open questions
- Hyper3D publishes an MCP page describing a hosted Rodin MCP server with Claude Code listed as a client; not independently re-checked or tested. - https://hyper3d.ai/features/mcp
- Tripo's Terms of Service reportedly contain free-user and paid-user rights clauses; not independently re-read. - https://www.tripo3d.ai/terms
- Whether Tripo's Free plan states "no commercial rights" in words, and Tripo Pro's monthly (non-annual) price, are not confirmed.

Sources:
- https://docs.hyper3d.ai/en/api-specification/rodin-gen2-5 - Gen-2.5 API parameters and credits
- https://hyper3d.ai/pricing - Hyper3D plans
- https://hyper3d.ai/legal/terms - Rodin and ChatAvatar output terms
- https://hyper3d.ai/features/mcp - Hyper3D MCP page (not re-verified)
- https://www.tripo3d.ai/pricing - Tripo plans
- https://www.tripo3d.ai/terms - Tripo terms (not re-verified)
- https://www.meshy.ai/pricing - Meshy plan summary
- https://www.meshy.ai/terms-of-use - Meshy sections 3.2 and 3.3
- https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE - Hunyuan3D-2 licence
- https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE - Hunyuan3D-2.1 licence
- https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/README.md - 2.1 VRAM figures
- https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/README.md - 2.0 VRAM figures
