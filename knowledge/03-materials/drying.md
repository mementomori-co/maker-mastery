# Filament drying: AMS 2 Pro, AMS HT, printer heatbed, blast oven
Applies to: H2C | P1S | both · Bambu Studio 2.x
Verified: 2026-10-03

## Facts

**Hardware limits**
- AMS 2 Pro has a built-in heater on both sides of the middle frame; its maximum drying temperature is 65 °C - [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)
- The AMS 2 Pro reaches 65 °C only at an ambient of about 25 °C or more; below that, heat loss can keep it under the maximum, which Bambu says is not a fault - [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)
- AMS HT has a heater below the middle frame, maximum 85 °C; its 170 W heater holds 85 °C at ambient 10-25 °C - [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)

**Per-filament AMS compatibility (use the per-filament table, not the blanket sentence)**
- The drying-function page says every filament type can be dried in an AMS 2 Pro or AMS HT, but Appendix I of the dry-filament page marks ABS, ASA, ASA-CF, ABS-GF, ASA Aero, PC, PVA, Support for PA/PET, PA6-CF/GF, PAHT-CF/GF, PET-CF, PPA-CF/PPS-CF and Support for ABS as not compatible with the AMS 2 Pro - [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function), [Dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- The AMS 2 Pro suits filaments that dry at 65 °C or less; when drying a high-temperature filament (for example ABS) in the same unit, take low-temperature filament (for example PLA) out first - [Dry filament, section 1.2](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- Before drying ABS or PETG in the AMS, remove PLA and TPU: their softening temperature is below the drying temperature and they can deform. Other filaments may stay in while PLA dries - [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)
- The AMS HT text says all filaments can be dried in it but that PVA, PPS-CF and PPA-CF may not dry fully, while Appendix I marks PPA-CF/PPS-CF not compatible with the AMS HT; the two statements conflict - [Dry filament, section 1.2 and Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)

**Drying one filament while printing another**
- Drying PETG while printing PLA caps the drying temperature at 45 °C; drying ABS while printing PETG caps it at 55 °C (each at or below the printing filament's softening temperature) - [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)
- Print-while-drying minimum firmware is listed for H2D, H2S, P2S, X2D and A2L; P1S, P1P, X1C, A1 and A1 mini are listed as not supported yet. The H2C is not named on the list, so do not assume the feature works on it - [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)
- On H2-series printers run without the power adapter, drying power is cut to 86 % - [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)

**Static (non-rotating) drying mode**
- In static mode the spool does not rotate and drying relies on hot-air circulation. From H2D firmware 01.03.00.00, PLA and TPU may use static drying; other printers and older firmware should use the rotating mode for PLA and TPU - [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)
- The dry-filament page says static mode does not suit PLA, PVA, Support for PLA/PETG or TPU, because low softening temperature lets layers stick together or deform. As the H2C is not named in the H2D exception, use rotating mode for PLA and TPU on it - [Dry filament, section 1.3](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)

**Heatbed drying (no AMS)**
- Open-frame printers (P1P, A1, A2L, A1 mini) cannot dry filament on the heatbed - [Dry filament, section 2](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- The P1S has no built-in filament-drying function: set the bed temperature by hand and time it yourself (the example given for ABS is a 100 °C bed) - [Dry filament, section 2.2](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)

**Per-filament values: bed / blast oven / AMS 2 Pro / AMS HT (dry-filament Appendix I unless noted)**
- PLA Basic / PLA Matte: bed 60-70 °C 12 h (flip every 6 h, covered); oven 50 °C 8 h; AMS 2 Pro 45 °C 12 h; AMS HT 45 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament). The material table gives generic "PLA" 55 °C 8 h in the oven - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- PLA Silk: bed 65-75 °C 12 h; oven 55 °C 8 h; AMS 2 Pro and AMS HT 45 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- PLA-CF / PLA-GF: bed 65-75 °C 12 h; oven 50-60 °C 8 h; AMS 2 Pro and AMS HT 45 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament); the material table gives PLA-CF 55 °C 8 h - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Support for PLA: bed 65-75 °C 12 h; oven 55 °C 8 h; AMS 2 Pro and AMS HT 60 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- Support for PLA/PETG: bed 65-75 °C 12 h; oven 75 °C 8 h; AMS 2 Pro and AMS HT 60 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- PETG, PETG-CF: bed 75-85 °C 12 h; oven 60-65 °C 8 h; AMS 2 Pro and AMS HT 65 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament); the material table's plain "PETG" and "PETG-CF" rows give 70 °C 8 h in the oven - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- PETG HF / PETG Translucent (material table): drying required; oven 65 °C 8 h; AMS 2 Pro and AMS HT 65 °C 12 h - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- ABS, ASA: bed 90-100 °C 12 h; oven 75-85 °C 8 h; AMS 2 Pro not compatible; AMS HT 80 °C 8 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament); the material table gives 80 °C 8 h oven and marks AMS 2 Pro not recommended - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- ASA-CF, ABS-GF, ASA Aero: bed 90-100 °C 12 h; oven 80 °C 8 h; AMS 2 Pro not compatible; AMS HT 80 °C 8 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- PC: bed 90-100 °C 12 h; oven 75-85 °C 8 h; AMS 2 Pro not compatible; AMS HT 80 °C 8 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament); the material table marks PC drying as required, 80 °C 8 h oven - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- PA6-CF/GF, PAHT-CF/GF: bed 90-100 °C 12 h; oven 75-85 °C 8-12 h; AMS 2 Pro not compatible; AMS HT 85 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament); material table: oven 80 °C 8-12 h, AMS HT 85 °C 12 h - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- TPU 95A HF: bed 80-90 °C 12 h; oven 70 °C 8 h; AMS 2 Pro 65 °C 12 h (the page warns it may not dry TPU fully; use the heatbed or AMS HT); AMS HT 75 °C 18 h. TPU 85A/90A: same AMS values, bed 90 °C 16 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament). The material table gives AMS HT 75 °C 12 h for TPU - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- PVA: oven 75-85 °C 8-12 h; AMS 2 Pro not compatible; AMS HT 85 °C 18 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament); the material table gives PVA 55 °C 8 h in the oven - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Support for PA/PET: oven 75-85 °C 8-12 h; AMS 2 Pro not compatible; AMS HT 80 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- PET-CF: oven 80 °C 8-12 h; AMS 2 Pro not compatible; AMS HT 80 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- PPA-CF / PPS-CF: oven 100-140 °C 8-12 h (a heatbed tops out at 110-120 °C and is less effective than a convection oven); AMS 2 Pro and AMS HT both not compatible - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- Support for ABS: oven 80 °C 4 h; AMS 2 Pro not compatible; AMS HT 80 °C 4 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- PLA oven values per line: the 50 °C vs 55 °C split is a scope difference. Basic, Matte, Translucent and Pure TDS give 50 °C 8 h; the generic material-table "PLA" row and the Silk, Silk+, Metal, Marble, Sparkle, Galaxy, Glow, Wood, Tough+, Aero, Gradient and Support for PLA sheets give 55 °C 8 h. Per-line detail is in [bambu-pla-family.md](bambu-pla-family.md) - [Dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)

## In practice
- For "can I dry this in the AMS 2 Pro?", use the per-filament Appendix I table, not the "all filament types" sentence.
- On the H2C, neither print-while-drying nor H2D-style static PLA/TPU drying is documented: use rotating-spool drying for PLA and TPU, and expect the drying temperature to be capped or paused if you print while drying.
- When the dry-filament page and the material table disagree on an oven number, prefer the dry-filament Appendix I (it is the dedicated per-filament page); for a specific product line, prefer that line's TDS.
- On the P1S, set the bed by hand (for example 100 °C for ABS) and time it yourself. Open-frame printers cannot heatbed-dry.
- Slicer drying presets for ABS/ASA/PC families: see [bambu-abs-asa-pc-families.md](bambu-abs-asa-pc-families.md). PA, TPU, CF/GF and support filaments: see [bambu-pa-tpu-cf-gf-families.md](bambu-pa-tpu-cf-gf-families.md).

## Not verified / open questions
- Bambu does not quantify partial drying for materials marked not compatible with the AMS 2 Pro.
- The "all filament types" sentence contradicts Appendix I for the AMS 2 Pro, and for PPA-CF/PPS-CF on the AMS HT; Bambu has not reconciled this.
- The dry-filament page and material table disagree on oven values for PLA (50 vs 55 °C), PLA-CF (50-60 vs 55 °C), PETG/PETG-CF (60-65 vs 70 °C), PVA (75-85 vs 55 °C) and on AMS HT time for TPU (18 h vs 12 h).
- Whether print-while-drying or static PLA/TPU drying will be supported on the H2C is not stated.

Sources:
- https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function - AMS 2 Pro / AMS HT limits, print-while-drying caps and firmware list, static drying, PLA/TPU removal rule
- https://wiki.bambulab.com/en/filament-acc/filament/dry-filament - Appendix I per-filament values, static-drying exclusions, heatbed drying rules
- https://wiki.bambulab.com/en/general/filament-guide-material-table - material-table drying column and its disagreements with the dry-filament page
