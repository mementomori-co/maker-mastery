# Bambu PA, PET-CF, PPA/PPS-CF, PLA-CF, TPU, support and PVA lines: TDS, store, wiki and H2C preset values
Applies to: H2C (P1S where noted) · Bambu Studio 02.08.02.61, BBL profile bundle 02.08.00.0x
Verified: 2026-10-06

PETG-CF has its full entry in [bambu-petg-family.md](bambu-petg-family.md); ABS-GF and ASA-CF in [bambu-abs-asa-pc-families.md](bambu-abs-asa-pc-families.md). Drying by AMS type: [drying.md](drying.md).

## Facts

### Conditions behind every number below
- TDS values are Bambu lab values on standard specimens at 100 % infill: density ISO 1183, Vicat ISO 306, HDT ISO 75 at the load stated with each value (1.8 or 0.45 MPa), tensile/modulus ISO 527, bending ISO 178, Charpy impact ISO 179, DSC at 10 °C/min, water absorption at 25 °C / 55 % RH. XY = along the layers, Z = across. Each line states its print and anneal state. None describe an as-printed part at normal infill - [PA6-CF TDS V3.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/c750bddfb8e44af6ae9f7dd9625fa458.pdf)
- Use the TDS density for engineering. The preset `filament_density` is documented in the source as for statistics only; it changes the slicer's gram and cost estimate. Preset vs TDS: PPA-CF about 6 % low, Support for PA/PET about 4 % high, TPU 85A about 3 % high, TPU 90A about 2 % low - [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- Slicer drying arrays are ordered [AMS 2 Pro idle, AMS HT idle, AMS 2 Pro while printing, AMS HT while printing]. `filament_dev_ams_drying_ams_limitations` is a drying-adequacy flag, not a feeding flag: "0" = the AMS 2 Pro dries it completely, "1" = the AMS HT, "1,0" = both, "-1" = neither. Hardware limits: AMS 2 Pro 45-65 °C, AMS HT 45-85 °C, 1-24 h. If the selected AMS is not in the set, the GUI warns the filament may not be completely dried - [DevUtilBackend.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceCore/DevUtilBackend.cpp), [DevDefs.h v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceCore/DevDefs.h), [AMSDryControl.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/AMSDryControl.cpp)

### PA6-CF (TDS V3.0; specimens 280 °C, 100 °C bed, 100 mm/s, annealed and dried 80 °C 12 h)
- Tensile 102 / 48 MPa; Young's modulus 4430 / 2170 MPa; bending strength 151 / 80 MPa; bending modulus 5460 / 2240 MPa; impact XY 40.3 unnotched / 13.4 notched, Z 15.5 kJ/m²; Tg 68 °C; Tm 223 °C; Vicat 212 °C; HDT 164 °C @1.8 MPa / 186 °C @0.45 MPa; water absorption 2.35 %; density 1.09 g/cm³ (preset 1.10) - [PA6-CF TDS V3.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/c750bddfb8e44af6ae9f7dd9625fa458.pdf)
- The wiki gives "humid" values well below dry: bending strength XY 151 dry vs 95 MPa humid, modulus 5460 vs 3560 MPa (no humidity condition stated) - [PET-CF/PPA-CF guide](https://wiki.bambulab.com/en/filament/petcf_ppacf)
- TDS print settings: nozzles 0.4, 0.6 (recommended), 0.8 mm; 260-290 °C; Engineering, High Temperature or Textured PEI with glue; bed 80-100 °C; under 100 mm/s; chamber 45-60 °C; support filament Support for PA/PET; drying oven 80 °C 8-12 h; annealing 80-130 °C 6-12 h - [PA6-CF TDS V3.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/c750bddfb8e44af6ae9f7dd9625fa458.pdf)
- System preset `Bambu PA6-CF @BBL H2C 0.4 nozzle`: 275 °C, range 260-300 °C; plates 100 °C; chamber 60 °C; max volumetric speed 8 mm³/s; `required_nozzle_HRC` 40; drying [65, 85, 65, 85] °C, 12 h - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- Store and wiki: not compatible with any AMS; 0.2 mm nozzle not compatible; stainless not recommended; needs an enclosed printer, hardened steel or high-flow nozzle (0.6 mm recommended) and glue - [PA6-CF store page](https://us.store.bambulab.com/products/pa6-cf), [PET-CF/PPA-CF guide](https://wiki.bambulab.com/en/filament/petcf_ppacf)

### PA6-GF (TDS V1.0; specimens 265 °C, 100 °C bed, annealed and dried 80 °C 12 h)
- Tensile 75 / 27 MPa; Young's modulus 2850 / 1950 MPa; bending strength 120 / 51 MPa; impact XY 27.2 unnotched / 7.2 notched, Z 4.1 kJ/m²; Vicat 210 °C; HDT 158 °C @1.8 MPa / 182 °C @0.45 MPa; water 2.56 %; density 1.14 g/cm³. Print 260-290 °C, bed 80-100 °C, under 130 mm/s - [PA6-GF TDS V1.0](https://wiki.bambulab.com/filament-acc/absgf-pa6gf/bambu_pa6-gf_technical_data_sheet.pdf)
- Store: AMS 2 Pro, AMS HT and AMS compatible; AMS lite not; stainless not recommended. Wiki: hardened steel or tungsten carbide, 0.6 mm recommended, no 0.2 mm; AMS HT drying 85 °C 12 h - [PA6-GF store page](https://us.store.bambulab.com/products/pa6-gf), [ABS-GF / PA6-GF guide](https://wiki.bambulab.com/en/filament/absgf_pa6gf)
- System preset `Bambu PA6-GF @BBL H2C 0.4 nozzle`: 265 °C; plates 100 °C; chamber 60 °C; 10.5 mm³/s; `required_nozzle_HRC` 40 - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PAHT-CF (TDS V3.0; specimens 290 °C, 100 °C bed, annealed and dried 80 °C 12 h)
- Composition: PA12 and other long-chain PA with carbon fibre. Tensile 92 / 47 MPa; Young's modulus 3860 / 2180 MPa; bending strength 125 / 61 MPa; impact XY 57.5 unnotched / 22.8 notched, Z 13.3 kJ/m²; Vicat 220 °C; HDT 170 °C @1.8 MPa / 194 °C @0.45 MPa; water 0.88 %; density 1.06 g/cm³. Print 260-290 °C, bed 80-100 °C with glue, under 100 mm/s - [PAHT-CF TDS V3.0](https://wiki.bambulab.com/filament-acc/asacf-pahtcf/65f1b18a6d6142d794a1a6a00f1496ef.pdf)
- Store: 0.6 mm nozzle recommended; AMS 2 Pro, AMS HT and AMS compatible; AMS lite not - [PAHT-CF store page](https://us.store.bambulab.com/products/paht-cf)
- System preset `Bambu PAHT-CF @BBL H2C 0.4 nozzle`: 290 °C; plates 100 °C; chamber 60 °C; 8 mm³/s; `required_nozzle_HRC` 40 - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PPA-CF (TDS V1.0; specimens on an X1C, 52 °C chamber, 290 °C, 110 °C bed, NOT annealed)
- Tensile 168 / 57 MPa; Young's modulus 11800 / 4300 MPa; bending strength 208 / 63 MPa; impact XY 41.7 unnotched / 6.5 notched, Z 4.3 kJ/m²; Tg 85 °C; Tm 258 °C; Vicat 232 °C; HDT 196 °C @1.8 MPa / 227 °C @0.45 MPa; water 1.30 %; density 1.25 g/cm³ (preset 1.17) - [PPA-CF TDS V1.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/c07c8b26f3ef44c8a2fcfc3fc11768b0.pdf)
- The sheet notes that a higher chamber (about 70-80 °C) would give higher properties, especially in Z - [PPA-CF TDS V1.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/c07c8b26f3ef44c8a2fcfc3fc11768b0.pdf)
- TDS print settings: nozzles 0.4-0.8 mm (0.6 recommended); 280-310 °C; Smooth or Textured PEI with glue stick; bed 100-120 °C; chamber 50-80 °C; oven drying 100-140 °C 8-12 h; annealing 120-140 °C 6-12 h; the cardboard spool is rated to 145 °C - [PPA-CF TDS V1.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/c07c8b26f3ef44c8a2fcfc3fc11768b0.pdf)
- The store's "up to 227 °C" wording matches the 0.45 MPa HDT and gives no load or duration; it is not a continuous-use rating. Store: no AMS, hardened steel mandatory, no stainless hotends, no liquid glue - [PPA-CF store page](https://us.store.bambulab.com/products/ppa-cf)
- System preset `Bambu PPA-CF @BBL H2C 0.4 nozzle`: 290 °C, range 280-320 °C; plates 100 °C; chamber 60 °C; 8 mm³/s; `filament_printable` 1 (left extruder only); drying flag "-1" - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PPS-CF (TDS V1.0; specimens on an X1E, 60 °C chamber, 320 °C, 110 °C bed, NOT annealed)
- Tensile 87 / 24 MPa; Young's modulus 8230 / 2850 MPa; bending strength 142 / 36 MPa; impact XY 27.8 unnotched / 6.2 notched, Z 2.8 kJ/m²; Tg 100 °C; Tm 284 °C; Vicat 268 °C; HDT 235 °C @1.8 MPa / 264 °C @0.45 MPa; water 0.05 %; density 1.26 g/cm³ - [PPS-CF TDS V1.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/26f4f40359484040a8660c9150a90fc0.pdf)
- The sheet lists acid, alkali, organic solvent, oil and grease resistance and describes the material as self-extinguishing and flame-retardant (no UL rating). Higher properties are noted at 90 °C chamber and 335 °C nozzle. Print 310-340 °C, bed 100-120 °C, chamber 60-90 °C; annealing 180-220 °C 6-12 h - [PPS-CF TDS V1.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/26f4f40359484040a8660c9150a90fc0.pdf)
- Store: for X1E and H2-series printers only; no AMS; recommended chamber 60-90 °C; the "continuously operate above 200 °C" wording has no load or duration. Wiki: supported only on X1E, H2D, H2S and H2C - [PPS-CF store page](https://us.store.bambulab.com/products/pps-cf), [PET-CF/PPA-CF guide](https://wiki.bambulab.com/en/filament/petcf_ppacf)
- System preset `Bambu PPS-CF @BBL H2C 0.4 nozzle`: 320 °C; plates 110 °C; chamber 65 °C; 6 mm³/s; `filament_printable` 1; drying flag "-1" - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PET-CF (TDS V3.0; specimens 270 °C, 80 °C bed, 100 mm/s, annealed and dried 80 °C 12 h)
- Tensile 74 / 35 MPa; Young's modulus 4730 / 2160 MPa; bending strength 131 / 49 MPa; impact XY 36.0 unnotched / 8.6 notched, Z 4.5 kJ/m²; Tg 75 °C; Tm 250 °C; Vicat 226 °C; HDT 182 °C @1.8 MPa / 205 °C @0.45 MPa; water 0.37 %; density 1.29 g/cm³ - [PET-CF TDS V3.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/07689de83afd4cc480f136c7697e6de3.pdf) (identical copy: [store CDN](https://store.bblcdn.com/9690d6226f024acab2ba0dd52dabb654.pdf))
- TDS print settings: nozzles 0.4-0.8 mm (0.6 recommended); 260-290 °C; glue; bed 80-100 °C; under 100 mm/s; chamber 45-60 °C; max bridge about 30 mm; oven drying 80 °C 8-12 h; annealing 80-140 °C 6-12 h - [PET-CF TDS V3.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/07689de83afd4cc480f136c7697e6de3.pdf)
- Wiki: PET-CF, PPA-CF and PPS-CF are brittle and prone to breakage; hardened steel or high-flow nozzle only; no AMS. Humid bending strength 127 vs 131 MPa dry - [PET-CF/PPA-CF guide](https://wiki.bambulab.com/en/filament/petcf_ppacf), [PET-CF store page](https://us.store.bambulab.com/products/pet-cf)
- System preset `Bambu PET-CF @BBL H2C 0.4 nozzle`: 270 °C; plates 100 °C; chamber 50 °C; 5 mm³/s (the wiki suggests up to 8 mm³/s); `required_nozzle_HRC` 40 - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament), [PET-CF/PPA-CF guide](https://wiki.bambulab.com/en/filament/petcf_ppacf)

### PLA-CF (TDS V2.0; specimens 230 °C, 35 °C bed, annealed and dried 55 °C 8 h)
- Tensile 38 / 26 MPa; Young's modulus 2790 / 2160 MPa; bending strength 89 / 49 MPa; impact XY 23.2 unnotched / 7.6 notched kJ/m²; Tg 63 °C; Tm 165 °C; Vicat 69 °C; HDT 54 °C @1.8 MPa / 55 °C @0.45 MPa; water 0.42 %; density 1.22 g/cm³. Print 210-240 °C, bed 35-45 °C, under 200 mm/s, max overhang 55° - [PLA-CF TDS V2.0](https://store.bblcdn.com/842f399d4e274507953a5231126ec8c1.pdf) (the EU "_V3" file still prints V2.0: [copy](https://store.bblcdn.eu/s8/default/aefa8303ad8d40248b0d86dfdad46518/Bambu_PLA-CF_Technical_Data_Sheet_V3.pdf))
- System preset `Bambu PLA-CF @BBL H2C 0.4 nozzle`: 230 °C; Textured PEI 55 °C; 15 mm³/s (18 on 0.6/0.8 mm); `required_nozzle_HRC` 40; drying 45 °C 12 h with flag "1,0" (both AMS types dry it) - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### TPU 95A HF (TDS V1.0; specimens 230 °C, 35 °C bed, annealed and dried 70 °C 12 h)
- Young's modulus 9.8 / 7.4 MPa; tensile 27.3 / 22.3 MPa; elongation over 650 / 480 %; Tm 183 °C; Tg, Vicat and HDT N/A; water 1.08 %; density 1.22 g/cm³. Print 220-240 °C, bed 30-35 °C - [TPU 95A HF TDS V1.0](https://store.bblcdn.com/58df32731eab4c90a7dac9b12e13ba88.pdf)
- System preset `Bambu TPU 95A HF @BBL H2C 0.4 nozzle`: 230 °C; plates 35 °C; 12 mm³/s; drying [65, 75, 45, 45] °C, [12, 18, 12, 18] h - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- H2 TPU guide: 0.4/0.6/0.8 mm or TPU high-flow nozzle; no 0.2 mm or ordinary high-flow nozzle; AMS, AMS lite and AMS 2 Pro not compatible, AMS HT compatible; non-"for AMS" TPU must be fed manually. The store lists it as not compatible with any AMS - [H2 TPU guide](https://wiki.bambulab.com/en/h2/h2d-tpu-printing-guide), [TPU 95A HF store page](https://us.store.bambulab.com/products/tpu-95a-hf), [TPU guide](https://wiki.bambulab.com/en/knowledge-sharing/tpu-printing-guide)

### TPU for AMS 68D (TDS V1.0)
- Shore 68D; Young's modulus 1190 / 600 MPa; tensile 22.4 / 11.2 MPa; elongation over 650 / 31 %; Tm 183 °C; water 1.20 %; density 1.26 g/cm³; print 220-240 °C, bed 30-35 °C, under 250 mm/s - [TPU for AMS TDS V1.0](https://store.bblcdn.com/s5/default/0a98353dce6d486ca848b21d2b19a207.pdf)
- Compatible with all AMS series per the store and TPU guide; the H2 guide excludes 0.2 mm and high-flow nozzles - [TPU for AMS store page](https://us.store.bambulab.com/products/tpu-for-ams), [TPU guide](https://wiki.bambulab.com/en/knowledge-sharing/tpu-printing-guide), [H2 TPU guide](https://wiki.bambulab.com/en/h2/h2d-tpu-printing-guide)

### TPU 85A and TPU 90A (TDS V1.0; dried 70 °C 12 h, not annealed)
- TPU 85A: tensile 12.0 / 10.5 MPa, elongation over 700 / 350 %, Tm 177 °C, density 1.18 g/cm³. TPU 90A: tensile 12.5 / 10.1 MPa, elongation over 650 / 350 %, Tm 180 °C, density 1.24 g/cm³. Both: bed 30-35 °C, under 200 mm/s, max bridge 10 mm, heatbed drying 90 °C 16 h - [TPU 85A TDS V1.0](https://store.bblcdn.eu/s8/default/7b6892a53de543c2a357415aff537f49/Bambu_TPU_85A_Technical_Data_Sheet_a7233668-497b-487f-af8a-3adb49fafaa1.pdf), [TPU 90A TDS V1.0](https://store.bblcdn.eu/s8/default/8140c9d50a6049a3b634fa1387518d8d/Bambu_TPU_90A_Technical_Data_Sheet_582bf8f6-1f0a-474c-aeda-9e72af3689dc.pdf)
- TPU 85A is not supported on a 0.4 mm nozzle: the TDS, store, H2 TPU guide and TPU guide agree on 0.6/0.8 mm only; the material table's 0.4 mm "Compatible" cell is outvoted - [TPU 85A/90A store page](https://us.store.bambulab.com/products/tpu-85a-tpu-90a), [H2 TPU guide](https://wiki.bambulab.com/en/h2/h2d-tpu-printing-guide), [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- System presets: `Bambu TPU 85A @BBL H2C` targets 0.6 and 0.8 mm only, 2.2 mm³/s, `filament_printable` 2 (right only); `Bambu TPU 90A @BBL H2C 0.4 nozzle`, 2.8 mm³/s, `filament_printable` 3 - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- The store says TPU 90A on H2D/H2C uses the right inlet only, AMS/AMS lite/AMS 2 Pro not compatible, AMS HT compatible, and that mixed printing with PLA/PETG is available only with TPU 90A. The H2 guide says TPU 85A must be fed directly into the extruder, not through a PTFE tube - [TPU 85A/90A store page](https://us.store.bambulab.com/products/tpu-85a-tpu-90a), [H2 TPU guide](https://wiki.bambulab.com/en/h2/h2d-tpu-printing-guide)

### Support for PA/PET, Support for ABS, PVA
- Support for PA/PET (discontinued; Bambu suggests ABS or ASA instead): nylon based; density 1.17 g/cm³; Tm 255 °C; water 1.23 %; 260-290 °C; bed 80-100 °C; mechanical values not supplied; oven 80 °C 8-12 h (the store page gives 80 °C 8 h oven or 90 °C 10 h heatbed) - [Support for PA/PET TDS V1.0](https://store.bblcdn.com/7e83189be1eb4a3dab8ce9b9a7b2065a.pdf), [Support for PA/PET store page](https://us.store.bambulab.com/products/support-for-pa-pet)
- Support for ABS: HIPS based; density 1.16 g/cm³; 240-270 °C; bed 80-100 °C; oven 80 °C 4 h. The wiki says it dissolves in d-limonene and usually needs no drying - [Support for ABS TDS V1.0](https://store.bblcdn.com/4ea7b59ca78c485f828115735ed35050.pdf), [Support for ABS guide](https://wiki.bambulab.com/en/filament-acc/filament/support-for-abs), [Support for ABS store page](https://us.store.bambulab.com/products/support-for-abs)
- PVA: density 1.27 g/cm³; water absorption 6.25 %; 220-250 °C; bed 35-45 °C; nozzles 0.2-0.8 mm; oven 80 °C 8-12 h. The wiki says left-plus-right dual-hotend PVA printing is not supported on the H2 series; the store says all AMS series are compatible when dry - [PVA TDS V1.0](https://store.bblcdn.com/s7/default/868930e5a44944258586caa250cc8143/Bambu_PVA_Technical_Data_Sheet.pdf), [Support filament guide](https://wiki.bambulab.com/en/filament/support), [PVA store page](https://us.store.bambulab.com/products/pva)

### Legacy lines
- PA-CF (legacy) and TPU 95A (non-HF) presets remain in Bambu Studio, but no Bambu-hosted TDS was found and the PA-CF store page returns 404. Preset `Bambu PA-CF @BBL H2C 0.4 nozzle`: 290 °C, plates 100 °C, chamber 60 °C, 8 mm³/s. Preset `Bambu TPU 95A @BBL H2C 0.4 nozzle`: 230 °C, plates 35 °C, 3.6 mm³/s - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament), [engineering filament collection](https://us.store.bambulab.com/collections/engineering-filament)

### Nozzle rules
- Wiki rule for CF/GF lines: no 0.2 mm nozzle; no stainless or brass; first choice 0.6 mm hardened steel, second 0.4 mm hardened steel (layer 0.15-0.3 mm, about 100 mm/s max). Material-table bands (±10 °C): PA and PET-CF/GF 260-300 °C, PPA 285-320 °C, PPS 310-340 °C, TPU 200-250 °C - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- `required_nozzle_HRC` is the minimum nozzle hardness for the filament (0 = no check). It is 40 for PA6-CF, PA6-GF, PAHT-CF, PA-CF, PPA-CF, PPS-CF, PET-CF, PLA-CF and PETG-CF, but 3 for ABS-GF, ASA-CF, all TPU, PVA and both support filaments. With nozzle ratings hardened 55, stainless 20, tungsten carbide 85, brass 2, a value of 3 blocks only brass, so the slicer will not warn about a stainless nozzle on ABS-GF, ASA-CF or Support for PA/PET even though Bambu requires hardened steel for them - [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), [Plater.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp), [nozzle_info.json](https://github.com/bambulab/BambuStudio/blob/master/resources/info/nozzle_info.json)
- The H2C hotend store page lists a stainless 0.2 mm nozzle and hardened steel 0.4/0.6/0.8 mm (standard and high-flow) nozzles, and says CF/GF filaments are not compatible with stainless nozzles. The H2C 0.2 mm machine preset declares `nozzle_type` hardened steel, which disagrees - [H2C induction hotend store page](https://us.store.bambulab.com/products/h2c-induction-hotend-right), [BambuStudio BBL machine profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/machine)
- After printing CF or GF filament, do several cold pulls before TPU (the H2 guide says 3-5) - [TPU guide](https://wiki.bambulab.com/en/knowledge-sharing/tpu-printing-guide), [H2 TPU guide](https://wiki.bambulab.com/en/h2/h2d-tpu-printing-guide)

### Extruder side
- `filament_printable` is a bit field (bit 0 left extruder, bit 1 right): 1 = left only, 2 = right only, 3 = both. PPA-CF 1, PPS-CF 1, PET-CF 0.6/0.8 mm preset 1, PET-CF 0.4 mm preset 3, TPU 85A 2, TPU 90A 3 - [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### AMS rules
- PA6-CF: no AMS feeds it. The AMS HT store page lists PLA-CF, PAHT-CF and PETG-CF for normal feeding and sends other CF/GF filaments, generic TPU, PET-CF and TPU 95A to the bypass outlet - [PA6-CF store page](https://us.store.bambulab.com/products/pa6-cf), [AMS HT store page](https://us.store.bambulab.com/products/ams-ht)
- With TPU, the AMS HT acts only as a sealed dry box; the filament feeds through the dedicated TPU outlet at the back, and the AMS HT cannot dry while feeding through the bypass. Bambu printers do not support TPU softer than 85A - [TPU guide](https://wiki.bambulab.com/en/knowledge-sharing/tpu-printing-guide), [AMS HT workflow](https://wiki.bambulab.com/en/ams-ht/Intr-to-ams-ht-workflow-and-features)
- Very soft, brittle, or hard and rough filaments wear or break in the AMS; abrasive filaments can grind down the PTFE feed channels over time - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- With an AMS 2 Pro and no AMS HT, PA6-CF, PET-CF, PPA-CF, PPS-CF, TPU 85A, TPU 90A and TPU 95A HF need an external spool. Store pages list PA6-GF, PAHT-CF, PETG-CF, PLA-CF, ABS-GF, Support for PA/PET, Support for ABS, PVA and TPU for AMS as AMS 2 Pro compatible; ASA-CF has limited compatibility - [PA6-GF store page](https://us.store.bambulab.com/products/pa6-gf), [TPU for AMS store page](https://us.store.bambulab.com/products/tpu-for-ams), [ASA-CF store page](https://us.store.bambulab.com/products/asa-cf)

### Drying
- PPS-CF and PPA-CF: oven 100-140 °C 8-12 h; heatbed 110-120 °C is less effective; no AMS dries them completely (Appendix I, AMS HT wiki and presets agree). The PET-CF/PPA-CF wiki drying rows that list 80-85 °C contradict both TDS - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament), [PPA-CF TDS V1.0](https://wiki.bambulab.com/filament-acc/petcf-ppacf/c07c8b26f3ef44c8a2fcfc3fc11768b0.pdf), [AMS HT workflow](https://wiki.bambulab.com/en/ams-ht/Intr-to-ams-ht-workflow-and-features)
- PA family on the AMS HT: 85 °C 12 h; PA6-CF/GF and PAHT-CF/GF heatbed 90-100 °C 12 h, oven 75-85 °C 8-12 h, AMS 2 Pro not compatible. PET-CF on the AMS HT: 80 °C 12 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- PA-based filaments left in open air for about 3 months absorb so much moisture that an 80-90 °C convection oven struggles to dry them - [Dry filament, Appendix II](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- PVA: oven 80 °C 8-12 h (TDS; Appendix I 75-85 °C; AMS HT 85 °C 18 h); the material table's 55 °C is an outlier. The AMS 2 Pro maxes at 65 °C - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament), [AMS 2 Pro drying function](https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function)
- TPU: the AMS 2 Pro may not fully dry it; use heatbed 80-90 °C 12 h (95A HF, TPU for AMS) or 90 °C 16 h (85A, 90A), oven 70 °C 8 h, or AMS HT 75 °C 18 h - [Dry filament, Appendix I](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)

### Chamber
- The H2C chamber heats to 65 °C and the nozzle reaches 350 °C. 65 °C sits inside the PPA-CF (50-80 °C) and PPS-CF (60-90 °C) TDS chamber ranges and above the chambers used for their TDS specimens, but below the "higher properties" conditions - [H2C specs](https://bambulab.com/en/h2c/specs), [H2C store page](https://us.store.bambulab.com/products/h2c)
- The slicer chamber field accepts up to 80 °C although the H2C hardware maximum is 65 °C. The tooltip recommends 0 (off) for PLA, PETG, TPU, PVA and other low-temperature materials; the softening-temperature tooltip recommends opening the door or removing the top glass when the bed is at or above it - [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- H2-series and X1E printers enable active chamber temperature control by default - [PET-CF/PPA-CF guide](https://wiki.bambulab.com/en/filament/petcf_ppacf)

### Plates, glue, enclosure, handling
- Bed by plate (wiki): PLA-CF 45-65 °C; PVA 35-45 °C; TPU 30-45 °C (not recommended on Cool Plate); PETG-CF 60-80 °C; PA family 100-120 °C (not on Cool Plate); PET-CF/GF 80-120 °C; PPA/PPS 100-120 °C - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Glue: glue stick for ASA-CF, PA6-GF/CF, PPA-CF, PPS-CF, PET-CF and PAHT-CF; liquid glue for ABS-GF; liquid glue not compatible with PET-CF/GF and not recommended for PA lines - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- ABS, ASA, PC, PA and their CF/GF grades need an enclosed printer; PLA, PETG and TPU work open or enclosed (enclosure recommended for PETG) - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Fibre-filled filaments can carry invisible barbs; wear puncture- and cut-resistant gloves and safety goggles when handling, removing supports or sanding - [ABS-GF / PA6-GF guide](https://wiki.bambulab.com/en/filament/absgf_pa6gf), [ASA-CF / PAHT-CF guide](https://wiki.bambulab.com/en/filament/asacf_pahtcf), [PET-CF/PPA-CF guide](https://wiki.bambulab.com/en/filament/petcf_ppacf)

## In practice
- Dry where the temperature fits: PPA-CF and PPS-CF need a 100-140 °C oven; PA lines 80 °C oven or 90-100 °C heatbed; TPU on the heatbed; PVA 80 °C oven. The AMS 2 Pro tops out at 65 °C.
- Design to the Z column: Z tensile is 24-57 MPa on the CF/GF nylons, PPA and PPS against 75-168 MPa XY, and Z impact drops further. TDS values are annealed or dried 100 %-infill specimens, so treat them as an upper bound.
- The H2C's 65 °C chamber covers the TDS baseline for PPA-CF and PPS-CF but not the "higher properties" settings.
- Do not rely on the slicer to catch a stainless nozzle with ABS-GF, ASA-CF or Support for PA/PET; check the installed hotend yourself.
- TPU 85A needs a 0.6 or 0.8 mm nozzle. Do not use an ordinary high-flow nozzle for TPU 95A HF. Cold-pull after CF/GF before TPU.
- Rough heat ladder at 1.8 MPa: PLA-CF 54, PETG-CF 68, PA6-GF 158, PA6-CF 164, PAHT-CF 170, PET-CF 182, PPA-CF 196, PPS-CF 235 °C.

## Not verified / open questions
- Legacy PA-CF and TPU 95A TDS exist only on reseller mirrors, not Bambu domains; their values are not used here.
- Whether the material table marks the 0.8 mm nozzle "Not Recommended" for PLA-CF/GF and PETG-CF: a parse of the table reads the 0.8 mm cell as "Compatible".
- No Bambu source gives UV data for PA/PPA/PPS, a continuous-use temperature with load and duration, Shore numbers for TPU 95A HF/85A/90A, or the humidity behind the wiki "humid" columns.
- PPA-CF drying on the AMS HT: one wiki table says 80 °C 12 h, other Bambu sources say not compatible.
- TPU 90A feed side: the store says right inlet only; the wiki and preset allow either side.
- TPU 85A multi-material: the store says not supported; the wiki says mixed printing is supported.
- PET-CF volumetric speed: wiki 8 mm³/s vs preset 5 mm³/s.
- H2C 0.2 mm machine preset (hardened steel) vs store (stainless).
- On printers without hardened steel nozzles, the HRC 3 blind spot matters; check your installed nozzle.

Sources:
- https://wiki.bambulab.com/filament-acc/petcf-ppacf/c750bddfb8e44af6ae9f7dd9625fa458.pdf - PA6-CF TDS V3.0
- https://wiki.bambulab.com/filament-acc/absgf-pa6gf/bambu_pa6-gf_technical_data_sheet.pdf - PA6-GF TDS V1.0
- https://wiki.bambulab.com/filament-acc/asacf-pahtcf/65f1b18a6d6142d794a1a6a00f1496ef.pdf - PAHT-CF TDS V3.0
- https://wiki.bambulab.com/filament-acc/petcf-ppacf/c07c8b26f3ef44c8a2fcfc3fc11768b0.pdf - PPA-CF TDS V1.0
- https://wiki.bambulab.com/filament-acc/petcf-ppacf/26f4f40359484040a8660c9150a90fc0.pdf - PPS-CF TDS V1.0
- https://wiki.bambulab.com/filament-acc/petcf-ppacf/07689de83afd4cc480f136c7697e6de3.pdf - PET-CF TDS V3.0
- https://store.bblcdn.com/9690d6226f024acab2ba0dd52dabb654.pdf - PET-CF TDS V3.0 (store copy)
- https://store.bblcdn.com/842f399d4e274507953a5231126ec8c1.pdf - PLA-CF TDS V2.0
- https://store.bblcdn.eu/s8/default/aefa8303ad8d40248b0d86dfdad46518/Bambu_PLA-CF_Technical_Data_Sheet_V3.pdf - PLA-CF "_V3" copy
- https://store.bblcdn.com/58df32731eab4c90a7dac9b12e13ba88.pdf - TPU 95A HF TDS V1.0
- https://store.bblcdn.com/s5/default/0a98353dce6d486ca848b21d2b19a207.pdf - TPU for AMS TDS V1.0
- https://store.bblcdn.eu/s8/default/7b6892a53de543c2a357415aff537f49/Bambu_TPU_85A_Technical_Data_Sheet_a7233668-497b-487f-af8a-3adb49fafaa1.pdf - TPU 85A TDS V1.0
- https://store.bblcdn.eu/s8/default/8140c9d50a6049a3b634fa1387518d8d/Bambu_TPU_90A_Technical_Data_Sheet_582bf8f6-1f0a-474c-aeda-9e72af3689dc.pdf - TPU 90A TDS V1.0
- https://store.bblcdn.com/7e83189be1eb4a3dab8ce9b9a7b2065a.pdf - Support for PA/PET TDS V1.0
- https://store.bblcdn.com/4ea7b59ca78c485f828115735ed35050.pdf - Support for ABS TDS V1.0
- https://store.bblcdn.com/s7/default/868930e5a44944258586caa250cc8143/Bambu_PVA_Technical_Data_Sheet.pdf - PVA TDS V1.0
- https://us.store.bambulab.com/products/pa6-cf - PA6-CF store page
- https://us.store.bambulab.com/products/pa6-gf - PA6-GF store page
- https://us.store.bambulab.com/products/paht-cf - PAHT-CF store page
- https://us.store.bambulab.com/products/ppa-cf - PPA-CF store page
- https://us.store.bambulab.com/products/pps-cf - PPS-CF store page
- https://us.store.bambulab.com/products/pet-cf - PET-CF store page
- https://us.store.bambulab.com/products/asa-cf - ASA-CF store page
- https://us.store.bambulab.com/products/tpu-95a-hf - TPU 95A HF store page
- https://us.store.bambulab.com/products/tpu-for-ams - TPU for AMS store page
- https://us.store.bambulab.com/products/tpu-85a-tpu-90a - TPU 85A/90A store page
- https://us.store.bambulab.com/products/support-for-pa-pet - Support for PA/PET store page
- https://us.store.bambulab.com/products/support-for-abs - Support for ABS store page
- https://us.store.bambulab.com/products/pva - PVA store page
- https://us.store.bambulab.com/products/h2c - H2C store page
- https://us.store.bambulab.com/products/h2c-induction-hotend-right - H2C hotend variants
- https://us.store.bambulab.com/products/ams-ht - AMS HT feed and bypass lists
- https://us.store.bambulab.com/collections/engineering-filament - engineering filament collection
- https://bambulab.com/en/h2c/specs - H2C specs
- https://wiki.bambulab.com/en/general/filament-guide-material-table - material table
- https://wiki.bambulab.com/en/filament-acc/filament/dry-filament - drying Appendix I and II
- https://wiki.bambulab.com/en/filament/petcf_ppacf - PET-CF/PPA-CF/PPS-CF guide
- https://wiki.bambulab.com/en/filament/absgf_pa6gf - ABS-GF / PA6-GF guide
- https://wiki.bambulab.com/en/filament/asacf_pahtcf - ASA-CF / PAHT-CF guide
- https://wiki.bambulab.com/en/h2/h2d-tpu-printing-guide - H2 TPU guide
- https://wiki.bambulab.com/en/knowledge-sharing/tpu-printing-guide - TPU guide
- https://wiki.bambulab.com/en/filament/support - support filament guide
- https://wiki.bambulab.com/en/filament-acc/filament/support-for-abs - Support for ABS guide
- https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function - AMS 2 Pro drying
- https://wiki.bambulab.com/en/ams-ht/Intr-to-ams-ht-workflow-and-features - AMS HT workflow
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp - filament_density, required_nozzle_HRC, filament_printable, chamber tooltips
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceCore/DevUtilBackend.cpp - drying array order
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceCore/DevDefs.h - AMS type identifiers
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/AMSDryControl.cpp - AMS drying limits and warning
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Plater.cpp - nozzle-hardness warning
- https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament - system filament presets
- https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/machine - system machine presets
- https://github.com/bambulab/BambuStudio/blob/master/resources/info/nozzle_info.json - nozzle HRC ratings
