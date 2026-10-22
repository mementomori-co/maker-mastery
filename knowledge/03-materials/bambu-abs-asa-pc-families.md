# Bambu ABS, ABS-GF, ASA, ASA-CF, ASA Aero, PC and PC FR: TDS, store, wiki and H2C preset values
Applies to: H2C (P1S where the preset says) · Bambu Studio 02.08.02.61, BBL profile bundle 02.08.00.0x
Verified: 2026-10-06

## Facts

### Conditions behind every number below
- Mechanical, thermal and physical values are Bambu lab values on printed specimens at 100 % infill, annealed and dried at 80 °C for 12 h before testing. Tensile/modulus ISO 527, bending ISO 178, Charpy impact ISO 179 (unnotched unless marked), density ISO 1183, Vicat ISO 306, HDT ISO 75 at 1.8 and 0.45 MPa, Tg/Tm by DSC at 10 °C/min, water absorption at 25 °C / 55 % RH. XY and Z are print orientations - [ABS TDS V3.0](https://store.bblcdn.com/s7/default/23b4cf2b83d5470bb96d19970b5f3ae8/Bambu_ABS_Technical_Data_Sheet_V3.pdf)
- The TDS PDFs carry a version string but no date; only the HTTP Last-Modified header dates the file - [ABS TDS V3.0](https://store.bblcdn.com/s7/default/23b4cf2b83d5470bb96d19970b5f3ae8/Bambu_ABS_Technical_Data_Sheet_V3.pdf)
- Every TDS in this family lists the odour as "Odorless", while the store pages warn about styrene - [ABS TDS V3.0](https://store.bblcdn.com/s7/default/23b4cf2b83d5470bb96d19970b5f3ae8/Bambu_ABS_Technical_Data_Sheet_V3.pdf), [ABS store page](https://us.store.bambulab.com/products/abs-filament)
- None of the seven lines has a published UV test (method, hours or colour change) on any TDS, SDS, store or wiki page; UV statements are marketing wording only - [ASA store page](https://us.store.bambulab.com/products/asa-filament), [ASA TDS V3.0](https://store.bblcdn.com/ad7b08230c164e72856cffbe06bb7dc9.pdf)

### ABS (TDS V3.0; specimens 260 °C nozzle, 80 °C bed, 200 mm/s)
- Tensile 33 MPa XY / 28 MPa Z; Young's modulus 2200 / 1960 MPa; elongation 10.5 / 4.7 %; bending strength 62 / 39 MPa; bending modulus 1880 / 1590 MPa; Charpy XY 39.3 kJ/m² unnotched, 21.5 notched, Z 7.4 unnotched - [ABS TDS V3.0](https://store.bblcdn.com/s7/default/23b4cf2b83d5470bb96d19970b5f3ae8/Bambu_ABS_Technical_Data_Sheet_V3.pdf)
- HDT 84 °C @1.8 MPa / 87 °C @0.45 MPa; Vicat 94 °C; Tm 200 °C; density 1.05 g/cm³ (system preset `filament_density` 1.04); water absorption 0.65 % - [ABS TDS V3.0](https://store.bblcdn.com/s7/default/23b4cf2b83d5470bb96d19970b5f3ae8/Bambu_ABS_Technical_Data_Sheet_V3.pdf), [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- TDS print settings: nozzle 240-270 °C; bed 80-100 °C on Engineering, High Temperature or Textured PEI with glue; chamber 45-60 °C; fan 0-80 %; under 300 mm/s; nozzles 0.2-0.8 mm; max overhang about 70°; max bridge about 40 mm; annealing 80-90 °C for 6-12 h - [ABS TDS V3.0](https://store.bblcdn.com/s7/default/23b4cf2b83d5470bb96d19970b5f3ae8/Bambu_ABS_Technical_Data_Sheet_V3.pdf)
- The TDS notes ABS warps easily and smells when printing; the store warns it may release harmful gases including styrene and recommends an enclosed printer and an activated-carbon mask - [ABS TDS V3.0](https://store.bblcdn.com/s7/default/23b4cf2b83d5470bb96d19970b5f3ae8/Bambu_ABS_Technical_Data_Sheet_V3.pdf), [ABS store page](https://us.store.bambulab.com/products/abs-filament)
- Store compatibility: AMS 2 Pro, AMS HT and AMS yes; AMS lite no; enclosure required; not for Cool Plate SuperTack. Warping tips: enclosure, glue, lower speed, higher bed. The store's HDT of 87 °C is the 0.45 MPa value - [ABS store page](https://us.store.bambulab.com/products/abs-filament)
- System preset `Bambu ABS @BBL H2C` (0.4 mm): nozzle 270 °C (first layer 260 °C), range 240-280 °C; Textured PEI, Engineering and High Temp plates 90 °C; chamber 65 °C; vitrification 75 °C; fan 10-60 %, overhang fan 80 %, fan off for the first 3 layers; max volumetric speed 20 mm³/s standard / 30 high-flow on 0.4 mm, 2 mm³/s on 0.2 mm; air filtration on - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament) (file `Bambu ABS @BBL H2C.json` with its `@base` and `fdm_filament_abs.json` parents)
- System preset `Bambu ABS @BBL P1S 0.4 nozzle`: chamber 0, vitrification 100 °C, max volumetric speed 16 / 25 mm³/s (standard / high flow), plates 90 °C - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### ABS-GF (TDS V1.0; specimens 270 °C, 80 °C, 150 mm/s)
- Tensile 36 / 29 MPa; Young's modulus 3160 / 2250 MPa; bending strength 68 / 46 MPa; bending modulus 2860 / 1970 MPa; Charpy XY 14.5 unnotched / 4.2 notched kJ/m²; HDT 88 °C @1.8 MPa / 99 °C @0.45 MPa; Vicat 103 °C; density 1.08 g/cm³ (TDS = preset) - [ABS-GF TDS V1.0](https://store.bblcdn.com/69f0758087c943f8a0a87bffa6dc901b.pdf)
- TDS print settings: nozzles 0.4, 0.6 (recommended), 0.8 mm; nozzle 240-280 °C; bed 80-100 °C with glue; chamber 45-60 °C; under 180 mm/s; supports on - [ABS-GF TDS V1.0](https://store.bblcdn.com/69f0758087c943f8a0a87bffa6dc901b.pdf)
- Store: 0.2 mm nozzle not compatible; AMS lite no; enclosure required; dry before use; glass fibre may shed fine debris and gloves are highly recommended when loading - [ABS-GF store page](https://us.store.bambulab.com/products/abs-gf)
- The store prints ABS bending strength XY as 64 MPa, but the ABS TDS and the same page's lower table say 62 MPa; against 62 MPa, ABS-GF is about +9.7 % - [ABS-GF store page](https://us.store.bambulab.com/products/abs-gf), [ABS TDS V3.0](https://store.bblcdn.com/s7/default/23b4cf2b83d5470bb96d19970b5f3ae8/Bambu_ABS_Technical_Data_Sheet_V3.pdf)
- System preset `Bambu ABS-GF @BBL H2C` (main file 0.6/0.8 mm; separate 0.4 mm file; no 0.2 mm file): nozzle 270 °C, plates 90 °C, chamber 60 °C, max volumetric speed 12 mm³/s; `required_nozzle_HRC` keeps the inherited default, so the slicer will not warn about a stainless nozzle - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- The wiki marks a hardened steel nozzle as required for ABS-GF, says not to use stainless, brass or 0.2 mm nozzles, prefers 0.6 mm hardened steel, and recommends Bambu liquid glue - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)

### ASA (TDS V3.0; specimens 260 °C, 80 °C, 200 mm/s)
- Tensile 37 / 31 MPa; Young's modulus 2450 / 2120 MPa; bending strength 65 / 40 MPa; bending modulus 1920 / 1650 MPa; Charpy XY 41.0 unnotched / 19.6 notched kJ/m²; HDT 92 °C @1.8 MPa / 100 °C @0.45 MPa; Vicat 106 °C; density 1.05 g/cm³; water absorption 0.45 % - [ASA TDS V3.0](https://store.bblcdn.com/ad7b08230c164e72856cffbe06bb7dc9.pdf) (byte-identical copy: [EU CDN](https://store.bblcdn.eu/s8/default/cad72d633f104a1aa80dc6c5937cb642/Bambu_ASA_Technical_Data_Sheet.pdf))
- TDS print settings: nozzles 0.2-0.8 mm; nozzle 240-270 °C; bed 80-100 °C with glue; chamber 45-60 °C; under 250 mm/s; annealing 80-90 °C for 6-12 h - [ASA TDS V3.0](https://store.bblcdn.com/ad7b08230c164e72856cffbe06bb7dc9.pdf)
- Bambu positions ASA for outdoor parts; its store FAQ says ASA resists fading and yellowing from sunlight better than ABS (no test data), that its odour is lighter than ABS, and that it warps like ABS and needs an enclosure - [ASA store page](https://us.store.bambulab.com/products/asa-filament)
- Store compatibility: AMS 2 Pro, AMS HT, AMS yes; AMS lite no (the wiki material table says AMS lite compatible, a conflict) - [ASA store page](https://us.store.bambulab.com/products/asa-filament), [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- System preset `Bambu ASA @BBL H2C` (0.4 mm; separate 0.6 and 0.2 files): nozzle 270 °C, range 240-280 °C; plates 100 °C; chamber 65 °C; vitrification 85 °C; max volumetric speed 20 / 30 mm³/s on 0.4 mm, 2 on 0.2 mm; fan 10-35 %; air filtration on - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### ASA-CF (TDS V1.0)
- Tensile 34 / 30 MPa; Young's modulus 4200 / 2290 MPa; bending strength 72 / 33 MPa; bending modulus 3740 / 1350 MPa; Charpy XY 14.0 unnotched / 6.2 notched kJ/m²; HDT 102 °C @1.8 MPa / 110 °C @0.45 MPa; Vicat 108 °C; density 1.02 g/cm³ - [ASA-CF TDS V1.0](https://store.bblcdn.com/s7/default/44b0a48ab1d84e819647c980eb179ae9/Bambus_ASA-CF_Technical_Data_Sheet.pdf)
- The sheet's specimen table (220 °C / 35 °C) contradicts its footnote (275 °C nozzle, 90 °C bed, 200 mm/s); the footnote fits the sheet's own ranges and the H2C preset, so the table is probably a template leftover (inference) - [ASA-CF TDS V1.0](https://store.bblcdn.com/s7/default/44b0a48ab1d84e819647c980eb179ae9/Bambus_ASA-CF_Technical_Data_Sheet.pdf)
- The store claims 67 % more stiffness than ASA, but its own table and the TDS give bending modulus XY 3740 vs 1920 MPa, which is about +95 %; cite the moduli - [ASA-CF store page](https://us.store.bambulab.com/products/asa-cf)
- Store cautions: external spool holder recommended, limited compatibility with AMS, AMS 2 Pro and AMS HT; hardened steel nozzle mandatory; no 0.2 mm; enclosure required; no liquid glue; more brittle than ASA; wear cut-resistant gloves and goggles - [ASA-CF store page](https://us.store.bambulab.com/products/asa-cf). The wiki recommends Bambu glue stick for ASA-CF - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- System preset `Bambu ASA-CF @BBL H2C` (main file 0.6/0.8 mm, separate 0.4 file): nozzle 275 °C; chamber 60 °C; vitrification 95 °C on the H2C files (108 °C on `@base`); max volumetric speed 18 mm³/s; fan 10-25 % - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### ASA Aero (TDS V1.0; foaming filament)
- Tensile 32 / 21 MPa; bending modulus 1510 / 1220 MPa; HDT 78 °C @1.8 MPa / 85 °C @0.45 MPa; Vicat 80 °C; filament density 0.99 g/cm³; water absorption 0.80 % - [ASA Aero TDS V1.0](https://store.bblcdn.com/s1/default/02b005fdf02d450084e3128f7cf0c36f/Bambu_ASA_Aero_Technical_Data_Sheet.pdf)
- Printed density falls from about 0.97 to 0.45 g/cm³ as nozzle temperature rises from 220 to 280 °C (wiki test, 0.4 mm nozzle, 80 mm/s); the store says prints are 50-75 % the density of regular ASA - [ASA Aero printing guide](https://wiki.bambulab.com/en/filament-acc/filament/asa-aero-printing-guide), [ASA Aero store page](https://us.store.bambulab.com/products/asa-aero)
- The wiki recommends the Engineering Plate or Smooth PEI (Textured PEI can make the first layer too sticky), flow ratio 0.42-0.7 (the store table says 0.45-0.80), 0.48 mm line width, 1 wall, 0 % sparse infill, 80 mm/s - [ASA Aero printing guide](https://wiki.bambulab.com/en/filament-acc/filament/asa-aero-printing-guide)
- Store: highly sensitive to humidity, dry before use; enclosure required; lists hardened steel 0.6/0.8 mm hotends as not compatible - [ASA Aero store page](https://us.store.bambulab.com/products/asa-aero)
- System preset `Bambu ASA-Aero @BBL H2C` (main file 0.6/0.8 mm, separate 0.4 file): nozzle 270 °C, plates 90 °C, chamber 60 °C, max volumetric speed 12 mm³/s, flow ratio 0.52 - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PC (two TDS versions; design to V3.0)
- V3.0: tensile 55 MPa XY / 34 MPa Z; V2.0 (linked from the US store): 62 / 56 MPa. Other values match on both: Young's modulus 2110 / 1450 MPa, bending strength 108 / 55 MPa, bending modulus 2310 / 1620 MPa, Charpy XY 34.8 unnotched / 7.5 notched kJ/m², Vicat 119 °C, Tg 145 °C, density 1.20 g/cm³ (preset 1.185), water absorption 0.25 % - [PC TDS V3.0](https://store.bblcdn.eu/s8/default/ab03007d58814bc28a08145719b552de/Bambu_PC_Technical_Data_Sheet.pdf), [PC TDS V2.0](https://store.bblcdn.com/a52afdccddfd448583d119587122c8c5.pdf)
- Both sheets print HDT 117 °C @1.8 MPa and 112 °C @0.45 MPa, which reverses normal ISO 75 behaviour; the ASA store comparison table lists PC at 117 °C for 0.45 MPa. Likely true pair: about 112 °C @1.8 MPa, 117 °C @0.45 MPa; use 112 °C as the 1.8 MPa design value - [PC TDS V3.0](https://store.bblcdn.eu/s8/default/ab03007d58814bc28a08145719b552de/Bambu_PC_Technical_Data_Sheet.pdf), [ASA store page](https://us.store.bambulab.com/products/asa-filament), [ISO 75 overview (third party)](https://kunststoff-profi.de/en/standards/iso-75-heat-deflection/)
- V3.0 print settings: nozzles 0.2-0.8 mm; nozzle 260-280 °C; bed 90-110 °C with glue; fan 0-60 %; chamber 45-60 °C; annealing 85-100 °C 6-12 h; drying 80 °C 8 h oven or 90-100 °C 12 h heatbed; lists the material as flammable (no UL 94 rating) - [PC TDS V3.0](https://store.bblcdn.eu/s8/default/ab03007d58814bc28a08145719b552de/Bambu_PC_Technical_Data_Sheet.pdf)
- Store: AMS lite no; dry before use (highly moisture-absorbent); enclosure required; not for A-series printers, Cool Plate SuperTack or liquid glue; transparent PC can disturb Lidar extrusion calibration - [PC store page](https://us.store.bambulab.com/products/pc-filament)
- The wiki marks a 0.2 mm nozzle "Not Recommended" for PC; H2C 0.2 mm presets exist for PC and PC FR at 1 mm³/s - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- System preset `Bambu PC @BBL H2C` (0.4 mm): nozzle 280 °C (first layer 270 °C), range 260-290 °C; plates 110 °C; chamber 60 °C; vitrification 90 °C; max volumetric speed 20 / 30 mm³/s; air filtration off. `Bambu PC @BBL P1S`: plates 100 °C, vitrification 120 °C, 18 / 29 mm³/s - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### PC FR (TDS V1.0)
- Tensile 60 / 21 MPa; bending modulus 1890 / 1660 MPa; HDT 108 °C @1.8 MPa / 113 °C @0.45 MPa; Vicat 114 °C; Tg 145 °C; density 1.18 g/cm³ (preset 1.19); water absorption 0.12 % - [PC FR TDS V1.0](https://store.bblcdn.com/s1/default/4adf3c9827a0475d8777e9b8cfd11fbe.pdf)
- Flame: a CTI lab report published by Bambu records UL 94-2023 V-0 on 128 x 12.9 x 3.3 mm samples after standard preconditioning. It is a test report on the tested samples, not a UL listing, and holds for 3.3 mm only; it does not say whether specimens were printed or moulded - [CTI test report](https://store.bblcdn.com/s1/default/a7ac91acf11b41bea0883615f46ed557.pdf), [PC FR store page](https://us.store.bambulab.com/products/pc-fr)
- System presets `Bambu PC FR @BBL H2C` (0.2, 0.4 and 0.6/0.8 mm files): nozzle 280 °C, plates 110 °C, chamber 60 °C, max volumetric speed 18 mm³/s (1 on 0.2 mm) - [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

### Safety data sheets
- All seven SDS classify the filament as "Not classified", say to avoid fire, elevated temperatures and direct sunlight, and give no data for decomposition products or exposure limits - [ABS SDS](https://store.bblcdn.com/s7/default/56cffb6bd13040b0b2dd357ad6a987b5/SDS20250724B00_Bambu_ABS.pdf), [PC SDS](https://store.bblcdn.com/s7/default/4606ae672ba843c3944661016aa8f349/SDS20251127C00_Bambu_PC.pdf) (others in Sources)

### Chamber, nozzle and plate on the H2C
- H2C specs: active chamber heating to 65 °C; hardened steel nozzle; max nozzle 350 °C; supported plates Textured PEI and Engineering Plate; max bed 120 °C; ABS, ASA, PC and their CF/GF grades listed as supported - [H2C specs](https://bambulab.com/en/h2c/specs)
- The TDS gives a 45-60 °C chamber for all seven lines; the H2C presets set 65 °C for ABS and ASA and 60 °C for the other five. The wiki says these materials need higher bed and chamber temperatures to suppress warping and layer separation, and H2-series chamber control is on by default - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [PET-CF/PPA-CF guide](https://wiki.bambulab.com/en/filament/petcf_ppacf), [Chamber temperature](https://wiki.bambulab.com/en/software/bambu-studio/chamber-temperature)
- Plates (wiki: Cool / Engineering / Smooth PEI-High Temp / Textured PEI): ABS and ASA not recommended on Cool Plate, 90-100 °C on the others; PC not recommended on Cool Plate, 100-120 °C on the others - [Material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)

### Drying
- Dry-filament Appendix I: ABS, ASA oven 75-85 °C 8 h, AMS 2 Pro not compatible, AMS HT 80 °C 8 h; ASA-CF and ABS-GF AMS HT 80 °C 8 h; heatbed 90-100 °C 12 h. PC may become brittle after repeated drying cycles (filament breakage risk, not printed-part properties) - [Dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- Slicer drying arrays `filament_dev_ams_drying_temperature` / `_time` are indexed [AMS 2 Pro idle, AMS HT idle, AMS 2 Pro while printing, AMS HT while printing]. ABS and ABS-GF: [65, 80, 65, 75] °C; ASA, ASA-CF, ASA Aero, PC, PC FR: [65, 80, 65, 80] °C; times [12, 8, 12, 8] h. All seven set `filament_dev_ams_drying_ams_limitations` so that the AMS 2 Pro shows a "may not be completely dried" warning and caps at 65 °C (read from BambuStudio master, not a release tag) - [DevUtilBackend.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/DeviceCore/DevUtilBackend.cpp), [DevDefs.h](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/DeviceCore/DevDefs.h), [AMSDryControl.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/AMSDryControl.cpp), [BambuStudio BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)

## In practice
- For outdoor or sunlit parts, ASA is Bambu's own recommendation, but no line in this family has published UV test data.
- PC has the highest heat figures here (Vicat 119 °C, about 112 °C HDT at 1.8 MPa) and needs a 110 °C bed, 280 °C nozzle and thorough drying; design to the V3.0 tensile values.
- On the H2C expect a long chamber warm-up (60-65 °C) and plan for fume handling (styrene warnings on the ABS and ASA pages).
- With only an AMS 2 Pro, the slicer offers 65 °C 12 h with a warning; a full dry needs a 75-85 °C oven, heatbed drying or an AMS HT.
- ASA Aero wants the Engineering Plate; Textured PEI is not recommended. Stick to a 0.4 mm nozzle for Aero until the store's 0.6/0.8 mm exclusion is resolved.
- ABS-GF and ASA-CF are fibre-filled: wear gloves and goggles, and check yourself that a hardened nozzle is installed because the slicer will not warn.

## Not verified / open questions
- Whether the ASA Aero store exclusion of hardened steel 0.6/0.8 mm hotends applies to the H2C's hotends.
- No UV test exists for any of the seven lines.
- The PC HDT transposition is inferred from physics and the ASA store table; no corrected Bambu document.
- Why PC V3.0 tensile Z (34 MPa) is far below V2.0 (56 MPa).
- ASA-CF specimen conditions are internally inconsistent.
- Why the H2C ABS/ASA chamber preset (65 °C) sits above the TDS range (45-60 °C).
- Not published by Bambu: Tg for ABS/ABS-GF/ASA/ASA Aero/ASA-CF, notched Z impact, flame ratings for ABS/ASA/PC, PC FR UL 94 at other thicknesses, and emission figures.

Sources:
- https://store.bblcdn.com/s7/default/23b4cf2b83d5470bb96d19970b5f3ae8/Bambu_ABS_Technical_Data_Sheet_V3.pdf - ABS TDS V3.0
- https://store.bblcdn.com/69f0758087c943f8a0a87bffa6dc901b.pdf - ABS-GF TDS V1.0
- https://store.bblcdn.com/ad7b08230c164e72856cffbe06bb7dc9.pdf - ASA TDS V3.0
- https://store.bblcdn.eu/s8/default/cad72d633f104a1aa80dc6c5937cb642/Bambu_ASA_Technical_Data_Sheet.pdf - ASA TDS V3.0 (EU copy)
- https://store.bblcdn.com/s7/default/44b0a48ab1d84e819647c980eb179ae9/Bambus_ASA-CF_Technical_Data_Sheet.pdf - ASA-CF TDS V1.0
- https://store.bblcdn.com/s1/default/02b005fdf02d450084e3128f7cf0c36f/Bambu_ASA_Aero_Technical_Data_Sheet.pdf - ASA Aero TDS V1.0
- https://store.bblcdn.eu/s8/default/ab03007d58814bc28a08145719b552de/Bambu_PC_Technical_Data_Sheet.pdf - PC TDS V3.0
- https://store.bblcdn.com/a52afdccddfd448583d119587122c8c5.pdf - PC TDS V2.0
- https://store.bblcdn.com/s1/default/4adf3c9827a0475d8777e9b8cfd11fbe.pdf - PC FR TDS V1.0
- https://store.bblcdn.com/s1/default/a7ac91acf11b41bea0883615f46ed557.pdf - CTI UL 94 V-0 test report at 3.3 mm
- https://store.bblcdn.com/s7/default/56cffb6bd13040b0b2dd357ad6a987b5/SDS20250724B00_Bambu_ABS.pdf - ABS SDS
- https://store.bblcdn.com/s7/default/d438af84fa83457ca415f43ad2356d73/SDS20260701B50_Bambu_ABS_GF.pdf - ABS-GF SDS
- https://store.bblcdn.com/s7/default/10a896db93e04636a9f70b841867e7e6/SDS20251127B01_Bambu_ASA.pdf - ASA SDS
- https://store.bblcdn.com/s7/default/49cbb7bc9b7047fbb1c34a43fb209871/SDS20260701B51_Bambu_ASA_CF.pdf - ASA-CF SDS
- https://store.bblcdn.com/s7/default/e897527e7a5c426cbd3b4c920c63e270/SDS20251127B02_Bambu_ASA_Aero.pdf - ASA Aero SDS
- https://store.bblcdn.com/s7/default/4606ae672ba843c3944661016aa8f349/SDS20251127C00_Bambu_PC.pdf - PC SDS
- https://store.bblcdn.com/s7/default/6193891bd51e4a5d806125e1d6117583/SDS20250724C01_Bambu_PC_FR.pdf - PC FR SDS
- https://us.store.bambulab.com/products/abs-filament - ABS store page
- https://us.store.bambulab.com/products/abs-gf - ABS-GF store page
- https://us.store.bambulab.com/products/asa-filament - ASA store page and FAQ, PC HDT comparison row
- https://us.store.bambulab.com/products/asa-cf - ASA-CF store page
- https://us.store.bambulab.com/products/asa-aero - ASA Aero store page
- https://us.store.bambulab.com/products/pc-filament - PC store page
- https://us.store.bambulab.com/products/pc-fr - PC FR store page
- https://wiki.bambulab.com/en/general/filament-guide-material-table - nozzle, plate, glue, AMS tables
- https://wiki.bambulab.com/en/filament-acc/filament/dry-filament - drying appendix
- https://wiki.bambulab.com/en/filament-acc/filament/asa-aero-printing-guide - ASA Aero density, plate, flow
- https://wiki.bambulab.com/en/software/bambu-studio/chamber-temperature - chamber temperature guidance
- https://wiki.bambulab.com/en/filament/petcf_ppacf - H2-series chamber control default
- https://bambulab.com/en/h2c/specs - H2C chamber, nozzle, plates
- https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament - system filament presets
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/DeviceCore/DevUtilBackend.cpp - drying array index map
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/DeviceCore/DevDefs.h - AMS type identifiers
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/AMSDryControl.cpp - AMS 2 Pro cap and warning
- https://kunststoff-profi.de/en/standards/iso-75-heat-deflection/ - third-party ISO 75 overview
