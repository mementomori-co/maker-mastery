# Bambu PETG / PET family: PETG Basic, HF, Translucent, Matte, PETG-CF, PET-CF and support filaments
Applies to: H2C (TDS and wiki values are printer-independent) · Bambu Studio 02.08.02.61, BBL profile bundle 02.08.00.0x
Verified: 2026-10-07

Condition for every mechanical number: Bambu lab specimens (100 % infill, standard tests; XY = printed flat, Z = printed upright), not an as-printed part at normal infill. Values are given as XY / Z.

## Facts

### Rules that apply to the whole family
- Do not use a 0.2 mm nozzle for PETG Translucent. The store and the wiki material table both list 0.2 mm as not compatible; the older TDS V1.0 lists 0.2 mm, and the H2C 0.2 mm preset caps max volumetric speed at 1 mm³/s, so treat that preset as a placeholder - [PETG Translucent store page](https://us.store.bambulab.com/products/petg-translucent), [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- The wiki states its nozzle bands with a ±10 °C tolerance, so its 230-260 °C band for PETG Translucent does not truly conflict with the TDS 230-270 °C. Wiki bands: PETG 240-270, PETG HF 230-260, PETG-CF 240-270, PETG Translucent 230-260, PET-CF/GF 260-300, Support for PLA and PLA/PETG 190-240 °C - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- The H2C system presets run 245 °C (first layer 250 °C) for Basic, HF, Translucent and Matte; 255 °C for PETG-CF; 270 °C for PET-CF - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- Oven drying for PETG Basic: 65 °C for 8 h (TDS; the drying page gives 60-65 °C 8 h); the material table's 70 °C 8 h for plain "PETG" is the outlier. PETG HF and Translucent: 65 °C 8 h in every source - [PETG Basic TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf), [Dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament), [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- AMS drying time for PETG Basic: the TDS says 65 °C 8 h, while the material table, drying page and preset say 65 °C 12 h; use 12 h when idle (three sources against one) - [PETG Basic TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf), [Dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- The PET parent profile `fdm_filament_pet.json` sets AMS drying temperatures [65, 65, 55, 55] °C, 12 h in all slots; the slots mean [AMS 2 Pro idle, AMS HT idle, AMS 2 Pro while printing, AMS HT while printing]. While printing, the drying temperature is capped at the lowest of the drying value, softening temperature and heat-distortion temperature, giving 55 °C - [DevUtilBackend.cpp at v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceCore/DevUtilBackend.cpp), [AMSDryControl.cpp at v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/AMSDryControl.cpp), [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- No H2C-specific PETG enclosure guidance was found. The wiki's generic advice is that an enclosed printer helps keep low ambient temperature from reducing PETG interlayer strength; the H2C PETG presets (except PET-CF) set chamber 0 - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Wiki bed bands (Cool / Engineering / Smooth PEI-High Temp / Textured PEI): PETG, PETG HF, PETG Translucent, PETG-CF: not recommended / 60-80 / 60-80 / 60-80 °C; PET-CF: not recommended / 80-120 / 100-120 / 100-120 °C - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)

### PETG Basic (TDS V3.0; current standard PETG)
- Specimens printed on an X1-Carbon at 255 °C, 150 mm/s, 70 °C bed, 100 % infill; no anneal step stated - [PETG Basic TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf)
- Tensile 51 / 35 MPa; Young's modulus 2780 / 2550 MPa; elongation 9.5 / 5.2 %; bending strength 75 / 56 MPa; unnotched impact 34.2 / 10.5 kJ/m²; Tg 69 °C; Vicat 69 °C; HDT 68 °C @1.8 MPa / 71 °C @0.45 MPa; density 1.25 g/cm³; water absorption 0.45 % - [PETG Basic TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf)
- TDS print settings: 230-260 °C; bed 65-75 °C; fan 0-60 %; up to 200 mm/s; chamber 35-50 °C; nozzles 0.2-0.8 mm; glue recommended; pairs with Support for PLA/PETG. Annealing not recommended (if done, 60-70 °C for 6-12 h). Heatbed drying 80 °C 12 h - [PETG Basic TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf)
- UV and outdoor wording on the TDS and store is marketing only (no test or duration). The store claims less stringing due to lower moisture sensitivity but still recommends drying - [PETG Basic store page](https://us.store.bambulab.com/products/petg-basic)
- System preset `Bambu PETG Basic @BBL H2C 0.4 nozzle`: nozzle 250 °C (initial 245 °C), Textured PEI 70 °C, Cool Plate SuperTack 60 °C, flow ratio 0.97, density 1.25, `temperature_vitrification` 60 °C - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PETG HF (discontinued; TDS V1.0)
- The US store says PETG HF is discontinued and will not be restocked (no date on the notice) - [PETG HF store page](https://us.store.bambulab.com/products/petg-hf)
- Specimens annealed and dried at 75 °C 8 h, though the same sheet tells users not to anneal prints. Tensile 34 / 23 MPa; Young's modulus 1810 / 1540 MPa; bending strength 64 / 48 MPa; impact XY 31.5 unnotched / 6.2 notched kJ/m²; Tm 214 °C; Tg 66 °C; Vicat 70 °C; HDT 62 °C @1.8 MPa / 69 °C @0.45 MPa; density 1.28 g/cm³; drying oven 65 °C 8 h - [PETG HF TDS V1.0](https://store.bblcdn.com/3a230e260a3a47c2b0db0156e07eef91.pdf)
- System preset `Bambu PETG HF @BBL H2C` (a 0.4 mm preset): 245 °C, Textured PEI 70 °C, density 1.28, `temperature_vitrification` 55 °C - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PETG Translucent (TDS V1.0)
- Specimens annealed and dried 65 °C 8 h. Tensile 33 / 29 MPa; Young's modulus 1420 / 1230 MPa; bending strength 68 / 55 MPa; impact XY 37.4 unnotched / 8.6 notched kJ/m²; Tm 228 °C; Tg 70 °C; Vicat 79 °C; HDT 68 °C @1.8 MPa / 74 °C @0.45 MPa; density 1.25 g/cm³; water 0.30 % - [PETG Translucent TDS V1.0](https://store.bblcdn.com/s1/default/338c9cd853fd44d9b6ed354a49048e72/Bambu_PETG_Translucent_Technical_Data_Sheet.pdf)
- TDS print settings: 230-270 °C; Engineering, High Temperature or Textured PEI with glue; bed 65-75 °C; fan 0-60 %; under 220 mm/s; chamber 35-50 °C. Annealing not recommended - [PETG Translucent TDS V1.0](https://store.bblcdn.com/s1/default/338c9cd853fd44d9b6ed354a49048e72/Bambu_PETG_Translucent_Technical_Data_Sheet.pdf)
- Store: must be dried before use or prints show bubbles; all AMS series compatible; works in closed or open printers; UV wording without a test - [PETG Translucent store page](https://us.store.bambulab.com/products/petg-translucent)
- The store's variant selector lists nine colour codes (eight tints plus Clear 32101); the "12 colors" header is not supported by the selector, and the hex table lists the eight tints only - [PETG Translucent store page](https://us.store.bambulab.com/products/petg-translucent), [hex code table](https://store.bblcdn.com/s7/default/5c46875459bc4a27986707f49560a961/PETG_Translucent_Hex_Code_Table.pdf)
- System preset `Bambu PETG Translucent @BBL H2C 0.4 nozzle`: nozzle 245 °C (initial 250 °C), plates 70 °C, max volumetric speed 6 mm³/s, flow 0.97, retraction 0.4 mm, Spiral Lift z-hop, density 1.25, `temperature_vitrification` 55 °C. The 0.6 and 0.8 mm presets allow 16 mm³/s; the 0.2 mm preset 1 mm³/s. The bare `@BBL H2C` file is the 0.6 mm preset - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- Bambu's PLA/PETG mutual-support guide covers PLA Basic with PETG HF and PETG Basic only, and excludes PETG Translucent, PETG-CF and third-party PETG - [PLA and PETG mutual support](https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support)

### PETG Matte (TDS V1.0)
- Specimens: PETG Matte Violet dried 60 °C 8 h, printed on an H2-series printer (model not named in the extracted text) with a 0.4 mm hardened steel nozzle at 245 °C, 70 °C bed, 221 mm/s, 100 % infill. Not H2C data - [PETG Matte TDS V1.0](https://store.bblcdn.eu/s8/default/240fb0c791fb4903a9d72934895e9a16/PETG_Matte.pdf)
- Tensile 42.9 / 30.1 MPa; Young's modulus 3349 / 3174 MPa; bending strength 65 / 47 MPa; impact 32.6 / 10.0 kJ/m²; Tg 71 °C; Vicat 75.7 °C; HDT 71.2 °C @1.8 MPa / 72.3 °C @0.45 MPa; density 1.37 g/cm³; water 0.29 % - [PETG Matte TDS V1.0](https://store.bblcdn.eu/s8/default/240fb0c791fb4903a9d72934895e9a16/PETG_Matte.pdf)
- TDS print settings: 230-260 °C; Textured PEI, Smooth PEI or Cool Plate SuperTack; under 250 mm/s; chamber 35-50 °C; drying oven 65 °C 8 h; annealing 60-70 °C 6-12 h - [PETG Matte TDS V1.0](https://store.bblcdn.eu/s8/default/240fb0c791fb4903a9d72934895e9a16/PETG_Matte.pdf)
- The sheet prints a melting temperature of 160 °C, inconsistent with Bambu's other PETG sheets (HF 214, Translucent 228, PETG-CF 225 °C); treat it as a likely error - [PETG Matte TDS V1.0](https://store.bblcdn.eu/s8/default/240fb0c791fb4903a9d72934895e9a16/PETG_Matte.pdf), [PETG-CF TDS V3.0](https://store.bblcdn.com/626e4f424bf345ae965ad0ddfcaf2459.pdf)
- Profile name trap: the bare `Bambu PETG Matte @BBL H2C` and `Bambu PETG Basic @BBL H2C` are 0.6 mm presets; the 0.4 mm presets end in " 0.4 nozzle". `Bambu PETG HF @BBL H2C` is a 0.4 mm preset. Check `compatible_printers` before choosing - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PETG-CF (TDS V3.0)
- Specimens 255 °C, 150 mm/s, 70 °C bed, 100 % infill, annealed and dried 65 °C 8 h. Tensile 35 / 29 MPa; Young's modulus 2460 / 1340 MPa; bending strength 70 / 48 MPa; impact XY 41.2 unnotched / 15.7 notched kJ/m²; Tm 225 °C; Tg 68 °C; Vicat 85 °C; HDT 68 °C @1.8 MPa / 74 °C @0.45 MPa; density 1.25 g/cm³ - [PETG-CF TDS V3.0](https://store.bblcdn.com/626e4f424bf345ae965ad0ddfcaf2459.pdf)
- TDS print settings: 240-270 °C; Engineering, High Temperature or Textured PEI with glue; bed 65-75 °C; under 200 mm/s; nozzles 0.4-0.8 mm; drying oven 65 °C 8 h. The annealing time is printed as 65 to 70 hours, likely a typo (other PETG sheets give 4-12 h) - [PETG-CF TDS V3.0](https://store.bblcdn.com/626e4f424bf345ae965ad0ddfcaf2459.pdf)
- Store: 0.2 mm nozzle not compatible; stainless nozzle not recommended; AMS lite not compatible; 0.4 mm hardened steel works but 0.6 mm hardened steel lowers clog risk - [PETG-CF store page](https://us.store.bambulab.com/products/petg-cf)
- System preset `Bambu PETG-CF @BBL H2C 0.4 nozzle`: 255 °C, plates 70 °C, chamber 0, max volumetric speed 11.5 mm³/s, flow 0.95, `required_nozzle_HRC` 40 - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PET-CF (summary; full detail in [bambu-pa-tpu-cf-gf-families.md](bambu-pa-tpu-cf-gf-families.md))
- Nozzle 260-290 °C; hardened steel or high-flow nozzle only, 0.6 mm recommended; HDT 182 °C @1.8 MPa / 205 °C @0.45 MPa (annealed 80 °C 12 h specimens) - [PET-CF TDS V3.0](https://store.bblcdn.com/9690d6226f024acab2ba0dd52dabb654.pdf), [PET-CF/PPA-CF guide](https://wiki.bambulab.com/en/filament/petcf_ppacf)
- The store lists PET-CF as not compatible with any AMS, so feed it from an external spool; the H2C 0.4 mm preset uses 270 °C, Textured PEI 100 °C, chamber 50 °C, 5 mm³/s - [PET-CF store page](https://us.store.bambulab.com/products/pet-cf), [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### Support for PLA/PETG (TDS V1.0)
- Density 1.28 g/cm³; Tm 185 °C; water 1.02 %; mechanical values N/A; print 190-240 °C, bed 35-60 °C, under 100 mm/s; oven drying 75 °C 8 h - [Support for PLA/PETG TDS V1.0](https://store.bblcdn.com/d09d55778d42495db121e28a3b04a4c5.pdf)
- The H2C preset `Bambu Support For PLA/PETG @BBL H2C 0.4 nozzle` sets `filament_density` 1.19, so slicer weight reads about 7 % low against the TDS 1.28 - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- Store: for support interfaces only, not for whole models; all AMS series compatible - [Support for PLA/PETG store page](https://us.store.bambulab.com/products/support-for-pla-petg)
- Wiki drying: oven 75 °C 8 h, AMS 2 Pro and AMS HT 60 °C 12 h - [Dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)

### Support for PA/PET (discontinued; summary)
- Discontinued; Bambu suggests ABS or ASA instead; interface only; AMS lite not compatible; enclosure required - [Support for PA/PET store page](https://us.store.bambulab.com/products/support-for-pa-pet)
- TDS V1.0: nozzle 260-290 °C, bed 80-100 °C with glue, chamber 45-60 °C, oven 80 °C 8-12 h; HDT and Vicat N/A - [Support for PA/PET TDS V1.0](https://store.bblcdn.com/7e83189be1eb4a3dab8ce9b9a7b2065a.pdf)

## In practice
- Start normal PETG on the H2C from the PETG Basic 0.4 mm preset (245/250 °C, Textured PEI 70 °C). Dry first: oven 65 °C 8 h, or AMS 65 °C 12 h idle; the AMS holds 55 °C while printing.
- Pick presets by nozzle: names without " 0.4 nozzle" are often the 0.6 mm preset.
- Do not design to the PETG Matte melting point or the PETG-CF annealing hours.
- For Support for PLA/PETG weight, multiply the slicer figure by about 1.07.
- For clear or translucent results, see [translucent-vs-transparent.md](translucent-vs-transparent.md); for PLA vs PETG choice and mixing, see [pla-vs-petg.md](pla-vs-petg.md).

## Not verified / open questions
- PETG Matte test printer: text extraction says an H2-series model; an earlier rendered-page reading said H2D. Either way not H2C data.
- Date of the PETG HF discontinuation notice.
- PETG Matte Tm 160 °C and PETG-CF "65 to 70 hours" annealing: no Bambu correction found.
- H2C chamber behaviour for PETG is not documented; presets use chamber 0.
- UV and outdoor claims have no test method or duration.

Sources:
- https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf - PETG Basic TDS V3.0
- https://store.bblcdn.com/3a230e260a3a47c2b0db0156e07eef91.pdf - PETG HF TDS V1.0
- https://store.bblcdn.com/s1/default/338c9cd853fd44d9b6ed354a49048e72/Bambu_PETG_Translucent_Technical_Data_Sheet.pdf - PETG Translucent TDS V1.0
- https://store.bblcdn.eu/s8/default/240fb0c791fb4903a9d72934895e9a16/PETG_Matte.pdf - PETG Matte TDS V1.0
- https://store.bblcdn.com/626e4f424bf345ae965ad0ddfcaf2459.pdf - PETG-CF TDS V3.0
- https://store.bblcdn.com/9690d6226f024acab2ba0dd52dabb654.pdf - PET-CF TDS V3.0
- https://store.bblcdn.com/d09d55778d42495db121e28a3b04a4c5.pdf - Support for PLA/PETG TDS V1.0
- https://store.bblcdn.com/7e83189be1eb4a3dab8ce9b9a7b2065a.pdf - Support for PA/PET TDS V1.0
- https://store.bblcdn.com/s7/default/5c46875459bc4a27986707f49560a961/PETG_Translucent_Hex_Code_Table.pdf - PETG Translucent hex codes
- https://us.store.bambulab.com/products/petg-basic - PETG Basic store page
- https://us.store.bambulab.com/products/petg-hf - PETG HF discontinued notice
- https://us.store.bambulab.com/products/petg-translucent - PETG Translucent store page
- https://us.store.bambulab.com/products/petg-cf - PETG-CF store page
- https://us.store.bambulab.com/products/pet-cf - PET-CF store page
- https://us.store.bambulab.com/products/support-for-pla-petg - Support for PLA/PETG store page
- https://us.store.bambulab.com/products/support-for-pa-pet - Support for PA/PET store page
- https://wiki.bambulab.com/en/general/filament-guide-material-table - nozzle and bed bands, drying, enclosure note
- https://wiki.bambulab.com/en/filament-acc/filament/dry-filament - drying table
- https://wiki.bambulab.com/en/filament/petcf_ppacf - PET-CF guide
- https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support - PLA/PETG mutual support scope
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/DeviceCore/DevUtilBackend.cpp - drying array slots
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/AMSDryControl.cpp - while-printing drying cap
- https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament - system filament presets
