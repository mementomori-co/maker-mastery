# Third-party PETG on the H2C: Generic PETG preset, ELEGOO and SUNLU PETG
Applies to: H2C (0.4 mm hotend, AMS 2 Pro, Textured PEI) · Bambu Studio 02.08.02.61 (system profile bundle BBL 02.08.00.05)
Verified: 2026-10-17

Preset and document checks only; nothing here was measured on a print. Bambu wiki ranges are written for Bambu filaments; applying them to ELEGOO or SUNLU is an inference the pages do not make. Preset files are public in the Bambu Studio repository: [BBL filament folder at v02.08.02.61](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament).

Related: [bambu-petg-family.md](bambu-petg-family.md), [pla-vs-petg.md](pla-vs-petg.md), [pla-matte-vs-basic.md](pla-matte-vs-basic.md) (what the 3-value preset arrays mean).

## Facts

### Generic PETG @BBL H2C 0.4 nozzle
- Compatible printers: H2C 0.4 mm only. Chain: `Generic PETG @BBL H2C 0.4 nozzle` -> `Generic PETG @base` -> `fdm_filament_pet` -> `fdm_filament_common`, plus the include `fdm_filament_template_direct_dual_e3d`; `filament_id` GFG99. — [Generic PETG @BBL H2C 0.4 nozzle.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Generic%20PETG%20%40BBL%20H2C%200.4%20nozzle.json)
- Siblings: `Generic PETG @BBL H2C` covers the 0.6 and 0.8 mm nozzles (255 °C, 12 mm³/s, flow 0.97, retraction 0.4 mm); the `0.2 nozzle` file sets max volumetric speed 1 mm³/s (a placeholder). Generic PETG HF and Generic PETG-CF also have H2C files. — [Generic PETG @BBL H2C.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Generic%20PETG%20%40BBL%20H2C.json), [BBL filament folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament)
- Values in the 0.4 mm file: nozzle 255 °C on all three array entries (initial layer 255 °C); range 220-270 °C; Textured PEI, hot and engineering plate 70 °C; Cool Plate 0 (not supported); SuperTack 70 °C; `filament_max_volumetric_speed` 12 mm³/s ×3; flow ratio 0.97 ×3; density 1.27 g/cm³; `temperature_vitrification` 60 °C; retraction 0.4 mm ×3, wipe on, Z-hop type Spiral Lift; retraction speed and Z-hop "nil" (the printer value applies). — [Generic PETG @BBL H2C 0.4 nozzle.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Generic%20PETG%20%40BBL%20H2C%200.4%20nozzle.json), "nil" semantics: [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- Fans (from `Generic PETG @base` and parents): minimum 40 %, maximum 90 %, cooling layer time 30 s, slow-down layer time 12 s, overhang fan 90 % at threshold 10 %, fan off for the first 3 layers, aux fan 0. — [Generic PETG @base.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Generic%20PETG%20%40base.json)
- PETG drying keys in `fdm_filament_pet`: `filament_dev_ams_drying_temperature` ["65","65","55","55"] °C, drying time 12 h, softening temperature 60 °C. Many PETG presets inherit or restate these. — [fdm_filament_pet.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_pet.json)

### Bambu PETG Basic vs PETG Translucent, H2C 0.4 mm presets
| Key | PETG Basic | PETG Translucent |
|---|---|---|
| Nozzle / initial layer | 250 / 245 °C | 245 / 250 °C |
| Max volumetric speed | [18, 21, 18] mm³/s | 6 mm³/s ×3 |
| Fan min / max | 20 / 30 % | 10 / 30 % |
| Overhang fan | 50 % | 90 % |
| `temperature_vitrification` | 60 °C | 55 °C |
| Slow-down layer time | 12 s | 8 s |

Both: Textured PEI 70 °C, flow 0.97, density 1.25 g/cm³, retraction 0.4 mm. — [Bambu PETG Basic @BBL H2C 0.4 nozzle.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PETG%20Basic%20%40BBL%20H2C%200.4%20nozzle.json), [Bambu PETG Translucent @BBL H2C 0.4 nozzle.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PETG%20Translucent%20%40BBL%20H2C%200.4%20nozzle.json)

### Preset coverage for ELEGOO and SUNLU
- No ELEGOO filament preset exists in the BBL vendor folder. The separate Elegoo printer vendor ships only Generic PLA/PETG/ABS presets for its own printers, not usable on an H2C. — [BBL filament folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament), [Elegoo vendor filament folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/Elegoo/filament)
- SUNLU ships PETG presets for A1, A1 mini and X1C (with 0.2 and 0.8 mm variants); none names the H2C, and there is no Translucent or Transparent file. — [SUNLU filament folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament/SUNLU)
- `SUNLU PETG @BBL X1C` (compatible with X1 Carbon, X1, P1P, P1S, X1E at 0.4 mm): nozzle 245 °C (initial 250 °C), range 230-280 °C, max volumetric speed 14 mm³/s, flow 0.95, Textured PEI 60 °C, density 1.27, `temperature_vitrification` 68 °C, fan 10-30 %. The A1 file uses 9 mm³/s and flow 0.94. A P1S reaches it through the X1C file; the H2C does not. — [SUNLU PETG @BBL X1C.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/SUNLU/SUNLU%20PETG%20%40BBL%20X1C.json)

### ELEGOO PETG lines (US store, read 2026-10-16/17; stores change without notice)
- Lines sold: Rapid PETG, PETG Pro, PETG-CF, PETG-GF, PETG Translucent, PETG HF, PETG Glitter. — [ELEGOO PETG collection](https://us.elegoo.com/collections/petg-filaments/products.json?limit=100)
- Rapid PETG: nozzle 240-270 °C; bed 65-75 °C; chamber 25-50 °C; under 600 mm/s; density 1.29 g/cm³; dry 60 ± 5 °C for 8 h (required before use); textured or smooth PEI, glue recommended; Vicat 70 °C; HDT 72 °C at 0.45 MPa. — [Rapid PETG](https://us.elegoo.com/products/rapid-petg-filament-1-75mm-colored-1kg)
- PETG Pro: nozzle 230-260 °C; bed 65-75 °C; under 270 mm/s; density 1.27 g/cm³; dry 60 ± 5 °C for 8 h; glue recommended; Vicat 71 °C; HDT 73 °C at 0.45 MPa. — [PETG Pro](https://us.elegoo.com/products/petg-pro-filament-1-75mm-colored-1kg)
- PETG HF: nozzle 230-260 °C; bed 65-75 °C; under 600 mm/s; density 1.29 g/cm³; dry 60 °C for 8 h; glue recommended; Vicat 70 °C; HDT 69 °C at 0.45 MPa. — [PETG HF](https://us.elegoo.com/products/petg-hf)
- None of these three pages gives volumetric speed, flow ratio, retraction or fan values. — pages above
- Plain "PETG" (not Rapid, Pro or HF) appears only as a 3 kg spool variant. Its comparison column gives nozzle 230-260 °C, bed 65-75 °C, under 250 mm/s, and X-Y mechanical values with no test standard named (tensile 37 ± 2 MPa). No density, drying or diameter tolerance is published for it. — [ELEGOO 3 kg spool page](https://us.elegoo.com/products/orangestorm-giga-large-3kg-filament)

### SUNLU PETG
- "Transparent" is a colour option of the one SUNLU PETG product (Clear and several transparent colours), not a separate product. — [SUNLU PETG store page](https://store.sunlu.com/products/over-6kg-bundle-sale-petg-3d-printer-filament-1-75mm-1kg-roll)
- Store table: nozzle 240-260 °C at up to 300 mm/s; bed 60-65 °C with glue; density 1.27 g/cm³; drying 50 °C. The page contradicts itself on glue (also says no glue needed when heated to 60-70 °C). — [SUNLU PETG store page](https://store.sunlu.com/products/over-6kg-bundle-sale-petg-3d-printer-filament-1-75mm-1kg-roll)
- TDS SL-TE-WI-074 A/1: nozzle 240-260 °C; plate 60-70 °C; retraction 0.8-1.2 mm at 30-40 mm/s; drying 60-65 °C; density 1.27 g/cm³ (ISO 1183); HDT 70 ± 5 °C at 0.45 MPa (ISO 75); Tg 79.4 °C. — [SUNLU PETG TDS](https://cdn.shopify.com/s/files/1/0152/6507/1190/files/TDS_PETG_A1.pdf?v=1779680389)
- SUNLU's drying advice disagrees across its sources (store 50 °C, TDS 60-65 °C, blog 60 °C for 4-6 h in humid areas); the blog also suggests a 235 °C start, below the TDS range. — [SUNLU blog](https://store.sunlu.com/blogs/products-knowledge/why-sunlu-petg-popular-easy-durable-prints)

### Bambu wiki rules for PETG (written for Bambu filament)
- Plates for PETG, PETG HF and PETG Translucent: Textured PEI, Smooth PEI, High-Temperature and Engineering plates 60-80 °C; Cool Plate not recommended. With the bed above 60 °C for filaments that soften at 60-80 °C, Bambu suggests opening the front door and/or removing the top glass. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Glue: the material table recommends glue stick or liquid glue for PETG; the plates page says Textured PEI usually needs no adhesive. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [Bambu wiki: plates](https://wiki.bambulab.com/en/filament-acc/acc/plates)
- Nozzle ranges (Bambu lines, ±10 °C): PETG 240-270 °C, PETG HF 230-260 °C, PETG Translucent 230-260 °C; hardened steel not required; an enclosed printer is recommended. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- AMS 2 Pro drying for PETG and PETG-CF: 65 °C for 12 h. While printing PETG (or drying PETG while printing ABS), the drying temperature drops to 55 °C. While printing with PLA in the AMS it drops to 45 °C, and Bambu says to remove PLA and TPU before drying ABS or PETG. — [dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament), [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)
- For clear PETG see [translucent-vs-transparent.md](translucent-vs-transparent.md). — [Bambu wiki: transparent PETG](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)

## In practice
- For ELEGOO or SUNLU PETG on the H2C, start from `Generic PETG @BBL H2C 0.4 nozzle`, then justify each change from the maker's TDS: density (ELEGOO Pro 1.27, Rapid and HF 1.29, SUNLU 1.27) and a nozzle temperature inside the maker's range. Verify on your own printer.
- For plain ELEGOO "PETG": nozzle 230-260 °C, bed 65-75 °C, under 250 mm/s. Using 1.27 g/cm³ (the PETG Pro value) for density is a stand-in, not a published fact.
- Glue stick on Textured PEI is the safe choice for PETG (Bambu's material table and ELEGOO both recommend it). Open the door when the bed is above 60 °C.
- AMS 2 Pro drying at the PETG setting (65 °C, 12 h) only when no PLA or TPU is in that AMS. The makers' own figures (60 °C) are lower.

## Not verified / open questions
- ELEGOO plain PETG HDT (69 °C) has no stated load on the 3 kg page, so it is not comparable with the 0.45 MPa figures.
- Whether ELEGOO plain PETG and PETG Pro are the same material: no ELEGOO statement found.
- The meaning of each slot in the 4-value `filament_dev_ams_drying_temperature` array: not found.
- SUNLU drying temperature (50 vs 60-65 vs 60 °C) is unresolved; no drying time on store or TDS.
- Glue on Textured PEI for PETG: Bambu's two pages disagree in tone.
- ELEGOO stores outside the US not checked.

Sources:
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament — Generic PETG, Bambu PETG Basic and Translucent, SUNLU PETG presets
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/Elegoo/filament — Elegoo printer-vendor presets
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp — "nil" semantics
- https://us.elegoo.com/collections/petg-filaments/products.json?limit=100 — ELEGOO PETG line names
- https://us.elegoo.com/products/rapid-petg-filament-1-75mm-colored-1kg — Rapid PETG
- https://us.elegoo.com/products/petg-pro-filament-1-75mm-colored-1kg — PETG Pro
- https://us.elegoo.com/products/petg-hf — PETG HF
- https://us.elegoo.com/products/orangestorm-giga-large-3kg-filament — plain PETG (3 kg)
- https://store.sunlu.com/products/over-6kg-bundle-sale-petg-3d-printer-filament-1-75mm-1kg-roll — SUNLU PETG store table
- https://cdn.shopify.com/s/files/1/0152/6507/1190/files/TDS_PETG_A1.pdf?v=1779680389 — SUNLU PETG TDS A/1
- https://store.sunlu.com/blogs/products-knowledge/why-sunlu-petg-popular-easy-durable-prints — SUNLU blog drying
- https://wiki.bambulab.com/en/general/filament-guide-material-table — PETG plates, door, glue, nozzle ranges
- https://wiki.bambulab.com/en/filament-acc/acc/plates — Textured PEI adhesion
- https://wiki.bambulab.com/en/filament-acc/filament/dry-filament — PETG drying row
- https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function — 45 °C with PLA, remove PLA/TPU
- https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg — translucent PETG tips
