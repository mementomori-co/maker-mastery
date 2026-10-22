# PLA vs PETG, and mixing them
Applies to: both (H2C and P1S) · Bambu Studio 2.8
Verified: 2026-10-02 (glue row corrected 2026-10-07)

See also: [bambu-petg-family.md](bambu-petg-family.md) (per-line PETG values), [translucent-vs-transparent.md](translucent-vs-transparent.md) (optics and the clarity recipe), [petg-third-party-on-h2c.md](petg-third-party-on-h2c.md) (third-party PETG and the Generic PETG preset).

## Facts
- PLA Basic: HDT 54 °C at 1.8 MPa and 57 °C at 0.45 MPa (ISO 75); Vicat 57 °C; Tg 60 °C. — [PLA Basic TDS V3.0](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf)
- PETG HF: HDT 62 °C at 1.8 MPa and 69 °C at 0.45 MPa (ISO 75); Vicat 70 °C; Tg 66 °C. — [PETG HF TDS V1.0](https://store.bblcdn.com/3a230e260a3a47c2b0db0156e07eef91.pdf)
- PETG HF is marked discontinued on the US store (no date given; seen 2026-10-07). Its replacement, PETG Basic (TDS V3.0), lists HDT 68 °C at 1.8 MPa and 71 °C at 0.45 MPa. — [PETG HF store page](https://us.store.bambulab.com/products/petg-hf), [PETG Basic TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf)
- HDT side by side (ISO 75, 100 % infill specimens; 1.8 / 0.45 MPa): PLA Basic 54 / 57 °C; PLA Matte 52 / 58 °C; PETG HF 62 / 69 °C; PETG Basic 68 / 71 °C; PETG Matte 71.2 / 72.3 °C. Each TDS states its own specimen conditioning (for example PLA annealed and dried at 55 °C for 8 h). At the same load PETG is 8-19.2 °C higher at 1.8 MPa and 11-15.3 °C higher at 0.45 MPa (arithmetic from these rows). — [PLA Basic TDS](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf), [PLA Matte TDS](https://store.bblcdn.com/s7/default/5b061f2feeac4ba88f355a33248bbda7/Bambu_PLA_Matte_Technical_Data_Sheet.pdf), [PETG HF TDS](https://store.bblcdn.com/3a230e260a3a47c2b0db0156e07eef91.pdf), [PETG Basic TDS](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf), [PETG Matte TDS](https://store.bblcdn.eu/s8/default/240fb0c791fb4903a9d72934895e9a16/PETG_Matte.pdf)
- Bambu says PLA is not recommended in environments at about 50 °C or higher. — [Bambu filament guide material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Bambu states that PLA and PETG "don't bond well to each other", which is why they work as a support pair. The bond is weak, not absent: the same page warns the support can come loose if used as the whole support base. That guide covers Bambu PLA Basic with PETG HF or PETG Basic only; PETG Translucent, PLA Matte, PLA Silk, PLA-CF and third-party filaments are listed as not supported. — [Bambu wiki: H2D PLA and PETG mutual support](https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support)
- Bambu publishes no bond-strength table for filament pairs. Its fused multi-material guidance is by temperature class only: low-temperature (PLA, PETG, TPU, PLA-CF, PVA and others) and high-temperature (ABS, ASA, PC, PA and others) filaments must not be printed together, and Bambu Studio enforces this when slicing. — [Bambu wiki: H2D/H2C filament config limit](https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit)
- AMS 2 Pro drying (maximum 65 °C, reached only at an ambient of 25 °C or more): PLA Basic and PLA Matte 45 °C for 12 h; PETG HF and PETG Translucent 65 °C for 12 h. "65 °C for 8 h" is the forced-air oven column, not the AMS. — [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function), [Bambu wiki: dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament), [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Glue: on Textured PEI glue is described as generally not necessary; on Smooth PEI it is to be applied for everything except PLA. — [Bambu wiki: how to use liquid glue](https://wiki.bambulab.com/en/general/how-to-use-bbl-liquid-glue)
- Glue for PETG: Bambu recommends glue stick or liquid glue on the plate for PETG, to improve adhesion, ease removal and protect the plate surface. The PETG Basic and PETG Matte TDS both list glue as "Recommended". — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [PETG Basic TDS](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf), [PETG Matte TDS](https://store.bblcdn.eu/s8/default/240fb0c791fb4903a9d72934895e9a16/PETG_Matte.pdf)
- Textured PEI bed temperature: PLA 45-65 °C; PETG, PETG HF and PETG Translucent 60-80 °C. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)

## In practice
- Do not fuse PLA to PETG in a cosmetic or structural joint. Use the same family for fused multi-material, or print separate pieces held together mechanically.
- A part that sits near electronics or a power supply inside a closed enclosure should not be PLA (the 50 °C guidance above). Use PETG or a higher-temperature material.
- Always state HDT with its load; the two loads differ by about 1-7 °C for the materials above.

## Not verified / open questions
- Bond strength numbers for PLA to PLA, PETG to PETG or PLA to TPU: Bambu publishes none.
- Whether the mutual-support exclusions (for example PETG Translucent) are about bonding or about print settings is not stated.
- Glue on Textured PEI for PETG: the material table recommends it, the glue and plate pages say it is usually not needed. Test on your own printer and plate.

Sources:
- https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf — PLA Basic TDS V3.0
- https://store.bblcdn.com/s7/default/5b061f2feeac4ba88f355a33248bbda7/Bambu_PLA_Matte_Technical_Data_Sheet.pdf — PLA Matte TDS V3.0
- https://store.bblcdn.com/3a230e260a3a47c2b0db0156e07eef91.pdf — PETG HF TDS V1.0
- https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf — PETG Basic TDS V3.0
- https://store.bblcdn.eu/s8/default/240fb0c791fb4903a9d72934895e9a16/PETG_Matte.pdf — PETG Matte TDS V1.0
- https://us.store.bambulab.com/products/petg-hf — PETG HF discontinued notice
- https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support — weak PLA/PETG bond, scope
- https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit — temperature classes
- https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function — AMS 2 Pro 65 °C maximum and ambient condition
- https://wiki.bambulab.com/en/filament-acc/filament/dry-filament — drying table
- https://wiki.bambulab.com/en/general/filament-guide-material-table — bed temperatures, glue, 50 °C PLA guidance
- https://wiki.bambulab.com/en/general/how-to-use-bbl-liquid-glue — glue per plate
