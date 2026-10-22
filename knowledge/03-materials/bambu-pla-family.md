# Bambu Lab PLA family: every current line (TDS, store, wiki, H2C presets)
Applies to: H2C presets (0.4 mm); TDS and wiki rows are printer-independent (no P1S preset was resolved) · Bambu Studio 02.08.02.61, profile bundle BBL 02.08.00.05
Verified: 2026-10-06

Store pages were read 2026-10-06; TDS carry a version (V1.0-V4.0) and no date. Preset values come from the Bambu Studio system profiles, public at [BBL filament folder, tag v02.08.02.61](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament). Full mechanical tables (tensile, bending, X-Y impact) are in each linked TDS; this note keeps the values most used for choosing a line.

Related: [pla-matte-vs-basic.md](pla-matte-vs-basic.md), [hdt-vicat-table.md](hdt-vicat-table.md), [drying.md](drying.md), [pla-vs-petg.md](pla-vs-petg.md), [translucent-vs-transparent.md](translucent-vs-transparent.md).

## Facts

### How to read the H2C preset file names
- The unsuffixed `... @BBL H2C.json` file is the 0.4 mm preset only for PLA Basic, PLA Matte, PLA Tough+, PLA Translucent and PLA Pure (its compatible printer is `Bambu Lab H2C 0.4 nozzle`). For PLA Silk+, Silk, Metal, Marble, Sparkle, Galaxy, Glow, Wood, PLA-CF, Aero, Support For PLA and Support For PLA/PETG, the unsuffixed file is the 0.6/0.8 mm preset and a separate `... @BBL H2C 0.4 nozzle.json` is the 0.4 mm one. Values match between the two files for the keys below except PLA-CF max volumetric speed. — [BBL filament folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament)
- The US store PLA collection lists 16 PLA lines plus bundles; the two support filaments are sold separately. Discontinued store pages (HTTP 404 on 2026-10-06): PLA Silk (replaced by Silk+), PLA Tough (replaced by Tough+), PLA Lite, PLA Dynamic, and the old Support for PLA page. A legacy `Bambu PLA Silk @BBL H2C` preset still ships. — [PLA collection](https://us.store.bambulab.com/collections/pla), [PLA Silk+ page](https://us.store.bambulab.com/products/pla-silk-upgrade)

### Class-wide rules (Bambu wiki)
- PLA needs no enclosure and is not prone to warping. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- In an enclosed printer, for filaments softening below 60 °C (PLA, PVA, TPU) with the bed above 45 °C, Bambu recommends opening the front door and/or removing the top glass. PLA presets set `temperature_vitrification` 45 °C; Studio's tooltip gives the same advice at or above that bed temperature to avoid clogging. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- H2D/H2C multi-material: PLA, PLA-CF and PLA Aero are low-temperature filaments that may soften and clog above 45 °C chamber; high- and low-temperature filaments must not be printed together, and Studio enforces it. — [H2D/H2C filament config limit](https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit)
- Service limit: PLA is not recommended in environments at about 50 °C or higher; it may slowly soften and deform. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Nozzle table, "PLA*" row: compatible with all nozzle types, hardened steel not required, 190-240 °C (±10 °C). The PLA* class includes Basic, Matte, Tough, Metal, Silk, Aero, Dynamic and others, and excludes filled types (PLA-CF, PLA-GF, Sparkle, Marble). PLA Metal has its own row, 190-230 °C. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Filled PLA (PLA-CF, Marble, Sparkle, Glow and similar): do not use a 0.2 mm nozzle (very high clogging risk); a 0.4 mm hardened-steel nozzle is the recommended first choice; layer 0.15-0.3 mm; about 100 mm/s maximum. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Bed by plate (PLA, PLA Metal/Wood/Marble): Cool Plate 35-45 °C; Engineering Plate 45-65 °C with glue; Smooth PEI / High-Temperature and Textured PEI 45-65 °C. PLA-CF: 45-65 °C on every plate. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Drying, material table: PLA rows oven 55 °C for 8 h; AMS 2 Pro and AMS HT 45 °C for 12 h. Drying guide (line-specific): PLA Basic/Matte oven 50 °C 8 h; Silk, Aero, Galaxy oven 55 °C 8 h; PLA-CF/GF oven 50-60 °C 8 h; PLA Wood oven 55-65 °C 8 h and drying "Required"; Support for PLA oven 55 °C, Support for PLA/PETG oven 75 °C, both AMS 60 °C 12 h. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- AMS 2 Pro static drying is not suitable for PLA, PVA, Support for PLA/PETG or TPU. Drying PLA while printing runs at 45 °C. — [dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- AMS (wiki joint "AMS / AMS lite" column): compatible for PLA*, PLA Metal/Wood/Marble and both support filaments; PLA Glow "Not Recommended"; PLA Wood compatible with the AMS but not recommended for the AMS lite. Rough or abrasive fillers (carbon fibre, glow) can wear the PTFE feed channels over time. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Preset key meanings: the nozzle temperature range is shown as "Recommended nozzle temperature", and a value outside it triggers a warning dialog (not a hard limit); `filament_density` is for statistics only (weight and cost); `required_nozzle_HRC` is the minimum nozzle hardness, 0 meaning no check. — [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp), [ConfigManipulation.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp)

### Rulings where sources differ
- Nozzle ranges have three meanings: the TDS range (recommended printing range), the preset range (Studio's warning window) and the wiki class value. PLA Pure is the one real tightening: TDS 190-230 °C but preset high 220 °C, so 221-230 °C triggers the warning. — [PLA Pure TDS V1.0](https://store.bblcdn.com/s7/default/18f44e818d5f41ed8876364ecbb7af8d/PLA_Pure-TDS.pdf), [ConfigManipulation.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp)
- Density: the TDS (ISO 1183) is the material property; the preset value is a slicer weight constant. Support for PLA/PETG is the big gap: TDS 1.28 vs preset 1.19 g/cm³, so Studio under-states its weight by about 7 %. — [Support for PLA/PETG TDS V1.0](https://store.bblcdn.com/d09d55778d42495db121e28a3b04a4c5.pdf)
- Bed temperature: older TDS (V1-V3) give 35-45 °C with specimens printed at 35 °C; newer TDS (Tough+, Translucent, Pure) give 35-65 °C on PEI/SuperTack; the wiki gives 45-65 °C on PEI. H2C presets use 55 °C on Textured PEI, above the 45 °C softening value, so the door/top-glass advice applies. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Oven drying 50 vs 55 °C: line values win. 50 °C 8 h for Basic, Matte, Translucent and Pure; 55 °C 8 h for most other lines. — [dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- PLA Glow in an AMS: the wiki says not recommended; the store says AMS 2 Pro, AMS HT and AMS work but wear faster, and AMS lite is not compatible. The preset enforces `required_nozzle_HRC` 40 (hardened steel). An external spool holder avoids AMS wear. — [PLA Glow store page](https://us.store.bambulab.com/products/pla-glow), [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Silk+ and Silk Multi-Color: the store says not compatible with Cool Plate SuperTack or hardened-steel 0.6/0.8 mm nozzles; the silk wiki says not recommended. The older Silk+ TDS still lists them. Presets do not block it. Use 0.2 or 0.4 mm and no SuperTack. — [Silk+ store page](https://us.store.bambulab.com/products/pla-silk-upgrade), [silk wiki](https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments)
- PLA Galaxy and PLA Translucent at 0.2 mm: TDS and presets allow it, but the store says the 0.2 mm stainless hotend is not compatible. Treat 0.2 mm as unsupported. — [Galaxy store page](https://us.store.bambulab.com/products/pla-galaxy), [Translucent store page](https://us.store.bambulab.com/products/pla-translucent)
- PLA Marble and hardened steel: the wiki table says not required, its filled-material paragraph says always use hardened steel; the preset does not check. Stainless 0.4 mm is permitted; hardened steel is better for nozzle life. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [Marble store page](https://us.store.bambulab.com/products/pla-marble)

### Summary by line (TDS values unless marked; HDT ISO 75; Z impact ISO 179, kJ/m²)
| Line (TDS) | Nozzle | Speed | HDT 1.8 / 0.45 MPa | Vicat | Density TDS / preset | Z impact | Oven drying | H2C 0.4 preset: nozzle, MVS (Std / HF / E3D HF) |
|---|---|---|---|---|---|---|---|---|
| Basic (V3.0) | 190-230 °C | < 300 mm/s | 54 / 57 °C | 57 °C | 1.24 / 1.26 | 13.8 | 50 °C 8 h | 220 °C; 25 / 40 / 25 |
| Basic Gradient (V2.0) | 190-230 °C | < 300 mm/s | 54 / 57 °C | 57 °C | 1.24 / (uses Basic) | 23.8 | 55 °C 8 h | no own preset; store says use PLA Basic |
| Matte (V3.0) | 190-230 °C | < 300 mm/s | 52 / 58 °C | 63 °C | 1.31 / 1.32 | 6.6 | 50 °C 8 h | 220 °C; 25 / 40 / 25 |
| Silk+ (V1.0) | 210-240 °C | < 250 mm/s | 56 / 60 °C | 66 °C | 1.27 / 1.27 | 8.5 | 55 °C 8 h | 230 °C; 12 ×3 |
| Silk Dual-Color (V3.0) | 210-240 °C | < 250 mm/s | 50 / 53 °C | 56 °C | 1.32 / 1.32 (legacy Silk preset) | 4.6 | 55 °C 8 h | legacy Silk preset 230 °C; 12 |
| Metal (V3.0) | 190-230 °C | < 300 mm/s | 58 / 62 °C | 62 °C | 1.25 / 1.25 | 16.8 | 55 °C 8 h | 220 °C; 21 ×3 |
| Marble (V3.0) | 190-230 °C | < 250 mm/s | 53 / 56 °C | 57 °C | 1.22 / 1.22 | 6.5 | 55 °C 8 h | 220 °C; 12 ×3 |
| Sparkle (V1.0) | 190-230 °C | < 250 mm/s | 53 / 55 °C | 57 °C | 1.26 / 1.26 | 10.3 | 55 °C 8 h | 220 °C; 12 |
| Galaxy (V1.0) | 190-230 °C | < 250 mm/s | 52 / 55 °C | 56 °C | 1.19 / 1.19 | 5.8 | 55 °C 8 h | 220 °C; 21 |
| Glow (V1.0) | 190-230 °C (wiki 210-240) | < 250 mm/s | 52 / 55 °C | 56 °C | 1.26 / 1.26 | 19.8 | 55 °C 8 h | 220 °C; 18; HRC 40 |
| Wood (V1.0) | 190-240 °C | < 250 mm/s | 57 / 60 °C | 64 °C | 1.21 / 1.21 | 5.6 | 55 °C 8 h | 220 °C; 18 |
| Tough+ (V3.0) | 220-250 °C | < 300 mm/s | 58 / 61 °C | 62 °C | 1.21 / 1.21 | 25.9 | 55 °C 8 h | 245 °C; 21 ×3 |
| PLA-CF (V2.0) | 210-240 °C | < 200 mm/s | 54 / 55 °C | 69 °C | 1.22 / 1.22 | see open questions | 55 °C 8 h | 230 °C; 15 ×3; HRC 40 |
| Aero (V4.0) | 210-260 °C | < 180 mm/s | 48 / 53 °C | 54 °C | 1.21 / 1.21 (filament) | 3.1 | 55 °C 8 h | 220 °C; 6; flow ratio 0.6 |
| Translucent (V3.0) | 200-240 °C | < 150 mm/s | 55 / 60 °C | 61 °C | 1.22 / 1.22 | 8.5 | 50 °C 8 h | 220 °C; 12 ×3 |
| Pure (V1.0) | 190-230 °C (preset high 220) | < 200 mm/s | 56 / 60 °C | 63 °C | 1.24 / 1.24 | 10.0 (un-notched) | 50 °C 8 h | 220 °C; 12 ×3 |
| Support for PLA (V1.0) | 220-230 °C | < 200 mm/s | N/A | N/A | 1.33 / 1.30 | N/A | 55 °C 8 h | 220 °C; 6 |
| Support for PLA/PETG (V1.0) | 190-240 °C | < 100 mm/s | N/A (0.45 MPa row) | not given | 1.28 / 1.19 | N/A | 75 °C 8 h | 210 °C; 6 |

TDS links per line: [Basic](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf), [Basic Gradient](https://cdn.shopify.com/s/files/1/0584/7236/6216/files/Bambu_PLA_Basic_Gradient_Technical_Data_Sheet.pdf), [Matte](https://store.bblcdn.com/s7/default/5b061f2feeac4ba88f355a33248bbda7/Bambu_PLA_Matte_Technical_Data_Sheet.pdf), [Silk+](https://cdn.shopify.com/s/files/1/0584/7236/6216/files/Bambu_PLA_Silk__Technical_Data_Sheet.pdf), [Silk Dual-Color](https://cdn.shopify.com/s/files/1/0584/7236/6216/files/Bambu_PLA_Silk_Dual_Color_Technical_Data_Sheet.pdf), [Metal](https://store.bblcdn.com/c6c28a13ba294c6f9fe62755ec9188fa.pdf), [Marble](https://store.bblcdn.com/b81e083c7d1f4e2182ef749d48f9ec86.pdf), [Sparkle](https://store.bblcdn.com/169532c9ce4d4610a9e85d92c0222bb9.pdf), [Galaxy](https://store.bblcdn.com/8f0b6b2741e3498689c2c7706374c482.pdf), [Glow](https://store.bblcdn.com/cd34cf072d14484bbf027290d16abe9b.pdf), [Wood](https://store.bblcdn.com/s4/default/6fda0ae88e5a4e66bb5d58f2968eee42/Bambus_PLA_Wood_Technical_Data_Sheet.pdf), [Tough+](https://store.bblcdn.com/s7/default/80a85371db2e40bda97069d283fed76c/BambuPLA_Tough_TechnicalData_Sheet_(2).pdf), [PLA-CF](https://store.bblcdn.com/842f399d4e274507953a5231126ec8c1.pdf), [Aero](https://store.bblcdn.com/cbc8b808aaf84ead9bb3b0b9b43e66af.pdf), [Translucent](https://store.bblcdn.com/s7/default/729a8bf233e9474db25c8d5be1e64a00/Bambu_PLA_Translucent_Technical_Data_Sheet.pdf), [Pure](https://store.bblcdn.com/s7/default/18f44e818d5f41ed8876364ecbb7af8d/PLA_Pure-TDS.pdf), [Support for PLA](https://store.bblcdn.com/s2/default/200ef29f5cd04b20ba6c2c86f0cc3ec0/Bambus_Support_for_PLA_Technical_Data_Sheet.pdf), [Support for PLA/PETG](https://store.bblcdn.com/d09d55778d42495db121e28a3b04a4c5.pdf). Preset columns: [BBL filament folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament). Most TDS specimens were printed at 220 °C nozzle, 35 °C bed, 200 mm/s, 100 % infill and annealed/dried at 55 °C for 8 h; Tough+, Translucent, Pure, Aero and PLA-CF state their own conditions on the sheet.

### Line-specific notes
- PLA Basic: nozzle sizes 0.2-0.8 mm; store gives up to 258 mm/s (0.4 mm nozzle, 0.4 mm line, 0.2 mm layer). Preset fan 60-80 %, flow 0.99. — [Basic TDS](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf), [store page](https://us.store.bambulab.com/products/pla-basic-filament)
- PLA Basic Gradient: the TDS says it performs like PLA Basic with higher toughness and Z strength; the store says to use the PLA Basic preset; gradient length 8-10 m. — [Gradient TDS](https://cdn.shopify.com/s/files/1/0584/7236/6216/files/Bambu_PLA_Basic_Gradient_Technical_Data_Sheet.pdf), [store page](https://us.store.bambulab.com/products/pla-basic-gradient)
- PLA Silk+: gloss tips from the silk wiki: outer wall 40-60 mm/s (try 50), layer 0.16 mm, top pattern Archimedean Chords or Concentric, 235 °C. — [silk wiki](https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments)
- PLA Silk Multi-Color: the store recommends 40 mm/s outer wall and says it is not recommended on A-series printers; each Silk Gradient colour segment is about 20 m. — [Silk Multi-Color store page](https://us.store.bambulab.com/products/pla-silk-multi-color)
- PLA Metal: metal-look surface with no actual metal filler. — [Metal store page](https://us.store.bambulab.com/products/pla-metal)
- PLA Marble and PLA Sparkle: particle-filled; the TDS advise against a 0.2 mm nozzle. Sparkle's TDS names PVP glue. — [Marble TDS](https://store.bblcdn.com/b81e083c7d1f4e2182ef749d48f9ec86.pdf), [Sparkle TDS](https://store.bblcdn.com/169532c9ce4d4610a9e85d92c0222bb9.pdf), [Sparkle store page](https://us.store.bambulab.com/products/pla-sparkle)
- PLA Galaxy: not compatible with the Engineering Plate or the 0.2 mm stainless hotend (store). — [Galaxy store page](https://us.store.bambulab.com/products/pla-galaxy)
- PLA Glow: hardened-steel nozzle required, stainless and 0.2 mm not compatible (store). The store says brief UV or sunlight exposure (about 2 h) recharges the glow but long exposure may speed aging; no test data. — [Glow store page](https://us.store.bambulab.com/products/pla-glow)
- PLA Wood: water absorption 1.25 % (TDS); the store recommends drying right after opening because the wood powder makes it moisture-sensitive. — [Wood TDS](https://store.bblcdn.com/s4/default/6fda0ae88e5a4e66bb5d58f2968eee42/Bambus_PLA_Wood_Technical_Data_Sheet.pdf), [Wood store page](https://us.store.bambulab.com/products/pla-wood)
- PLA Tough+: X-Y notched impact 72.3 kJ/m² vs 7.9 for Basic; TDS specimens at 245 °C nozzle, 55 °C bed; glue recommended; AMS 2 Pro / AMS HT drying 55 °C for 8 h (TDS). — [Tough+ TDS](https://store.bblcdn.com/s7/default/80a85371db2e40bda97069d283fed76c/BambuPLA_Tough_TechnicalData_Sheet_(2).pdf), [store page](https://us.store.bambulab.com/products/pla-tough-upgrade)
- PLA-CF: hardened steel required; wiki nozzle row: 0.2 mm not compatible, 0.4 mm recommended, 0.6 and 0.8 mm compatible, 0.4 mm High Flow not recommended. The store advises puncture-resistant gloves and goggles when handling, removing supports or sanding. The 0.6/0.8 mm presets use 18 mm³/s. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [PLA-CF store page](https://us.store.bambulab.com/products/pla-cf)
- PLA Aero (foaming): printed density falls as nozzle temperature rises (about 1.17 g/cm³ at 190 °C down to 0.35 at 260 °C, per the store table). The RC models wiki uses flow ratio 0.6 and 245 °C with fan at or below 30 %. The store warns it is soft and may fail AMS loading; feed from an external spool if so. Not compatible with hardened-steel 0.6/0.8 mm or the 0.2 mm stainless hotend. — [Aero store page](https://us.store.bambulab.com/products/pla-aero), [RC models wiki](https://wiki.bambulab.com/en/knowledge-sharing/studio-settings-for-rc-models), [Aero TDS](https://store.bblcdn.com/cbc8b808aaf84ead9bb3b0b9b43e66af.pdf)
- PLA Translucent: frosted, light-diffusing finish (a diffuser, not a clear material). The store claims it bonds with any PLA and has better aging resistance than generic translucent PLA, with no test method or number. — [Translucent store page](https://us.store.bambulab.com/products/pla-translucent)
- PLA Pure: glue not recommended (residue may affect contact safety; raise bed temperature instead); retraction 0.4-0.8 mm; re-dry about every 18 days (TDS). The store says not to expose prints above 60 °C, lists EU 10/2011, EN 71-3 and UL GREENGUARD, and says food-contact certification applies to the filament itself. — [Pure TDS](https://store.bblcdn.com/s7/default/18f44e818d5f41ed8876364ecbb7af8d/PLA_Pure-TDS.pdf), [Pure store page](https://us.store.bambulab.com/products/pla-pure)
- Support for PLA: interface material only, avoid printing whole models with it; highly moisture-absorbent, store sealed with desiccant. — [Support for PLA store page](https://us.store.bambulab.com/products/support-for-pla-new)
- Support for PLA/PETG: recommended for all PLA and PETG; select it under the support/raft interface filament; avoid it for the tree-support base. — [Support for PLA/PETG store page](https://us.store.bambulab.com/products/support-for-pla-petg)

### Translucency, UV and outdoor wording
- Bambu publishes no transmittance or haze number for PLA Translucent or Support for PLA/PETG. Its clarity tips are settings only (see [translucent-vs-transparent.md](translucent-vs-transparent.md)). — [Bambu wiki: transparent PETG](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)
- No UV or weathering data exists on any PLA TDS, on the SDS re-read (Basic, Matte, Glow, Translucent, PLA-CF, Pure) or on the wiki. The SDS say to avoid elevated temperatures and direct sunlight. The PLA Basic store page says to store filament cool, dark and dry. — [PLA Basic SDS](https://store.bblcdn.com/s7/default/6e47ce4e48b54b20b3afd3be7539ac27/SDS20250724A00_Bambu_PLA_Basic.pdf), [PLA Basic store page](https://us.store.bambulab.com/products/pla-basic-filament)

## In practice
- Picking a line: Basic is the fast reference; Matte trades Z toughness for finish (6.6 vs 13.8 kJ/m²); Silk+ is slow, hot and small-nozzle (12 mm³/s, 230 °C, 0.4 mm max); Tough+ is the only PLA with a large toughness step and wants 245 °C and glue; Translucent is strong in tension but slow (under 150 mm/s) and is a diffuser.
- No Bambu PLA is rated for outdoor use: there is no UV data, and the service limit is about 50 °C.
- On Textured PEI at the preset 55 °C bed in an enclosed printer, open the door or remove the top glass; above 45 °C chamber PLA may clog.
- For PLA Pure expect a warning above 220 °C even though the TDS allows 230 °C. Keep Silk+ and Silk Multi-Color at 0.2 or 0.4 mm and off SuperTack. Skip 0.2 mm for Galaxy and Translucent. For hand weight sums of Support for PLA/PETG use 1.28 g/cm³.
- When quoting a 0.4 mm preset, open the `... @BBL H2C 0.4 nozzle.json` file for every line except Basic, Matte, Tough+, Translucent and Pure.

## Not verified / open questions
- PLA-CF second impact row (7.8 ± 0.7 kJ/m²) is labelled X-Y on the TDS but sits where other TDS print Z; no Bambu page labels it Z.
- Only 6 of 17 SDS were re-read; the sunlight wording is verified for those 6 only.
- PLA Translucent's aging claim and PLA Glow's irradiation line have no test data.
- Whether presets remain for discontinued PLA Tough, Lite and Dynamic was not checked.
- The PLA Marble hardened-steel conflict inside the wiki is not resolved by Bambu.
- No P1S preset was resolved; preset values are H2C only.

Sources:
- https://us.store.bambulab.com/collections/pla — PLA collection
- https://us.store.bambulab.com/products/pla-basic-filament — PLA Basic store page
- https://us.store.bambulab.com/products/pla-basic-gradient — Gradient store page
- https://us.store.bambulab.com/products/pla-matte — PLA Matte store page
- https://us.store.bambulab.com/products/pla-silk-upgrade — Silk+ store page
- https://us.store.bambulab.com/products/pla-silk-multi-color — Silk Multi-Color store page
- https://us.store.bambulab.com/products/pla-metal — PLA Metal store page
- https://us.store.bambulab.com/products/pla-marble — PLA Marble store page
- https://us.store.bambulab.com/products/pla-sparkle — PLA Sparkle store page
- https://us.store.bambulab.com/products/pla-galaxy — PLA Galaxy store page
- https://us.store.bambulab.com/products/pla-glow — PLA Glow store page
- https://us.store.bambulab.com/products/pla-wood — PLA Wood store page
- https://us.store.bambulab.com/products/pla-tough-upgrade — PLA Tough+ store page
- https://us.store.bambulab.com/products/pla-cf — PLA-CF store page
- https://us.store.bambulab.com/products/pla-aero — PLA Aero store page
- https://us.store.bambulab.com/products/pla-translucent — PLA Translucent store page
- https://us.store.bambulab.com/products/pla-pure — PLA Pure store page
- https://us.store.bambulab.com/products/support-for-pla-new — Support for PLA store page
- https://us.store.bambulab.com/products/support-for-pla-petg — Support for PLA/PETG store page
- TDS for each line — linked in the summary table above
- https://store.bblcdn.com/s7/default/6e47ce4e48b54b20b3afd3be7539ac27/SDS20250724A00_Bambu_PLA_Basic.pdf — PLA Basic SDS
- https://wiki.bambulab.com/en/general/filament-guide-material-table — material table
- https://wiki.bambulab.com/en/filament-acc/filament/dry-filament — drying guide
- https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit — H2D/H2C temperature classes
- https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg — translucent printing tips
- https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments — silk guide
- https://wiki.bambulab.com/en/knowledge-sharing/studio-settings-for-rc-models — RC / Aero guide
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament — H2C filament presets
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp — key meanings
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp — "Recommended nozzle temperature" label
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp — out-of-range warning dialog
