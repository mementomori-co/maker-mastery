# Small DC fuses and holders: ratings, opening times, temperature re-rating
Applies to: any build (printer-independent) · 5 V to 24 V DC LED and fan circuits; Littelfuse, Eaton/Bussmann, Bel, Schurter, Keystone parts
Verified: 2026-10-05

## Facts

### Cartridge and subminiature fuses with a DC rating
- Littelfuse Nano2 0451.200 (0.2 A): 125 V; cold resistance 0.8372 Ω (at 10 % of rated current, 25 °C); interrupting rating 50 A at 125 VAC/VDC and 300 A at 32 VDC (one shared cell for 0.062 to 1.60 A); opens within 5 s at 200 %; -55 to 125 °C. Marks cULus / cURus / CSA (0.062 to 0.160 A show only cULus / CSA). Body 6.10 +/-0.20 mm x 2.69 +/-0.25 mm. - [Littelfuse 451/453 datasheet](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1); [Littelfuse 451 page](https://www.littelfuse.com/451); [451 datasheet 2010, Octopart host](https://datasheet.octopart.com/0451.500MRL-Littelfuse-datasheet-69198868.pdf)
- Littelfuse PICO II 0251 (leaded): 125 V; interrupting 300 A at 125 VDC and 50 A at 125 VAC for 0.062 to 10 A (12 A and 15 A are 32 V only); opens within 1 s at 200 % for 0.062 to 5 A (current revision; the 2018 revision said up to 7 A); at 100 % it carries 4 hours minimum. Cold resistance: 0.200 A 0.895 Ω, 0.250 A 0.665 Ω, 1 A 0.128 Ω, 2 A 0.0473 Ω. UL Recognized (cURus), not cULus Listed; UL file E10480. Body 7.11 mm long, 2.80 mm max diameter. The sheet has no 135 % or 150 % opening row. - [Littelfuse 251 datasheet](https://www.littelfuse.com/assetdocs/fuse-251-datasheet?assetguid=f47a0bb7-8ede-4679-9646-7114c3787688); [Littelfuse 251 page](https://www.littelfuse.com/251); [251/253 datasheet rev. 05/31/18, Rexel host](https://rexel-cdn.com/products/littelfusefuse251253datasheet.pdf?i=2A0248F5-797E-4B9C-B780-FA5A032DED3E)
- PICO II temperature re-rating curve (vector read, 2018 revision): (-55 °C, 110 %), (-13.7 °C, 105.2 %), (27.7 °C, 100.6 %), (76.3 °C, 95.7 %), (125 °C, 91.2 %). As drawn the line crosses 100 % at 33.9 °C, not 25 °C; normalised to 25 °C = 100 % it reads 98.5 % at 40 °C. The sheet says this re-rating is in addition to the standard 25 % derating for continuous operation. 0.250 A crosses 30 s at 0.3948 A. - [251/253 datasheet, Rexel host](https://rexel-cdn.com/products/littelfusefuse251253datasheet.pdf?i=2A0248F5-797E-4B9C-B780-FA5A032DED3E)

### Common 5 x 20 mm fuses: opening point and voltage type, as printed
- Littelfuse 216: 250 V AC only, 210 % within 30 minutes. 215/217/218: IEC points only (215/217 210 % in 30 min max; 218 in 120 s max); 217 has a DC rating only from 2 A (70 A at 60 VDC) and 215 only for 4 to 6.3 A (1000 A at 72 VDC). 217 (IEC 60127-2 sheet 2, fast-acting): 150 % 60 min minimum, 275 % 0.05 to 2 s, 400 % 0.01 to 0.3 s. - [216](https://www.littelfuse.com/assetdocs/fuse-216-lead-free-datasheet?assetguid=69cb9c39-1497-4ecc-b09a-c0168520688e), [215](https://www.littelfuse.com/assetdocs/fuse-215-datasheet?assetguid=990f7193-d9a2-48e4-b760-2b43514249cf), [217](https://www.littelfuse.com/assetdocs/fuse-217-datasheet?assetguid=af55be94-c42e-41b1-ad43-e070e09443fe), [218](https://www.littelfuse.com/assetdocs/fuse-218-datasheet?assetguid=a96d72b7-5296-4815-88b4-98b2f6738874)
- Littelfuse 235: 0.2 and 0.25 A at 250 V, 200 % within 5 s, AC interrupting only. 314/324: 125 VDC rated, 200 % within 15 s, but starts at 0.375 A. 312: 0.2 A at 250 VAC; 200 % within 10 s for 1 to 2 A. - [235P](https://www.littelfuse.com/assetdocs/fuse-235p-lead-free-datasheet?assetguid=79b16c87-8337-4c9c-96d1-6ac09ce4e440), [314/324](https://www.littelfuse.com/assetdocs/littelfuse_fuse_314_324_datasheet.pdf?assetguid=24deec6d-9c03-4f0e-b612-8499127355f3), [312, distributor host](https://media.distrelec.com/Web/Downloads/_t/ds/0312001.MXP_eng_tds.pdf)
- Eaton GMA: 200 % within 2 min, AC columns only. Eaton ABC: 200 % within 120 s; ABC-1/4 has a 125 VDC rating. Eaton S500/S501: 250 V, IEC points, no DC. Bel 5MF: 200 % within 5 s, AC only; Bel 5SF/5ST: AC only, no 200 % point. Schurter FSF and FST: 250 VAC only; SP and SPT start at 0.5 A (SPT carries a UL 300 VDC rating). - [GMA](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-gma-time-delay-glass-tube-fuses-data-sheet.pdf), [ABC](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-abc-fast-acting-ceramic-tube-fuses-data-sheet.pdf), [S500](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-s500-glass-tube-fuses-data-sheet.pdf), [S501](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-s501-ceramic-tube-fuses-data-sheet.pdf), [Bel 5MF](https://datasheet.octopart.com/5MF1.25-R-Bel-Fuse-datasheet-137317049.pdf), [Bel 5SF](https://media.digikey.com/pdf/Data%20Sheets/Bel%20Fuse%20PDFs/5SF.pdf), [Bel 5ST](https://media.digikey.com/pdf/Data%20Sheets/Bel%20Fuse%20PDFs/5ST.pdf), [Schurter FSF](https://www.schurter.com/en/datasheet/typ_FSF_5x20.pdf), [SP](https://www.schurter.com/en/datasheet/typ_sp_5x20.pdf), [FST](https://www.schurter.com/en/datasheet/typ_FST_5x20.pdf), [SPT](https://www.schurter.com/en/datasheet/typ_SPT_5x20.pdf)
- Across that set, no 5 x 20 mm or 1/4 x 1-1/4 in fuse at 0.2 to 0.25 A with a DC rating of at least 32.4 V and an opening time of 30 s or less at 200 % was found (a search result, not proof of absence); nearest were the 235 (AC only) and the 314 (125 VDC, 15 s, from 0.375 A). - [235P](https://www.littelfuse.com/assetdocs/fuse-235p-lead-free-datasheet?assetguid=79b16c87-8337-4c9c-96d1-6ac09ce4e440), [314/324](https://www.littelfuse.com/assetdocs/littelfuse_fuse_314_324_datasheet.pdf?assetguid=24deec6d-9c03-4f0e-b612-8499127355f3)

### Automotive blade fuses
- Littelfuse ATOF: 1 to 40 A, 32 VDC; UL Listed file AU1410, CSA file 29862; housing PA66, UL 94 V2. Opening times (min / max): 135 %: 1 and 2 A 0.35 s / 600 s, 3 to 40 A 0.75 s / 600 s; 160 %: 0.25 s / 50 s; 200 %: 1 and 2 A 0.1 / 5 s, 3 to 40 A 0.15 / 5 s. Typical cold resistance: 1 A 123 mΩ, 2 A 53.5 mΩ, 3 A 31.1 mΩ, 5 A 17.85 mΩ, 7.5 A 10.91 mΩ; typical voltage drop 2 A 141 mV, 3 A 137 mV, 5 A 128 mV (test current not stated). - [Littelfuse ATOF datasheet, distributor host](https://www.farnell.com/datasheets/3767635.pdf) (revised 08/18/2022)
- ATOF melting-element derating curve (vector read, ISO 8820-3 set-up, about +/-0.02 A): at 40 °C ambient a 2 A part carries about 1.98 to 2.00 A, 3 A 2.98 to 3.00 A, 4 A 3.78 to 3.80 A, 5 A 4.35 to 4.37 A, 7.5 A 6.40 to 6.42 A. The 3 A curve falls to 2.90 A at 50 °C, 2.72 A at 65 °C, 2.47 A at 85 °C and 2.10 A at 110 °C. The separate temperature table has no 40 °C column and rounds to whole amps (its "3" at 65 °C is the curve's 2.72 A rounded up). - [Littelfuse ATOF datasheet](https://www.farnell.com/datasheets/3767635.pdf) (p. 3)
- Littelfuse MINI 58 V (0997 series, 2 to 30 A): 58 V DC, 1000 A interrupting at 58 V DC, PA66 UL 94 V-2, complies with UL 248 special-purpose; 135 % 0.75 s / 600 s, 200 % 0.15 / 5 s, 350 % 0.08 / 0.5 s; no UL file number on the sheet. TAC ATO 58 V (1 to 40 A): cULus Recognized E211637, 1000 A at 58 VDC, UL 94-V0 body; 135 % 0.75 s / 1800 s, 200 % 0.15 / 5 s. - [Littelfuse MINI 58V datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-997-mini58v?assetguid=f4bf5724-5a40-4a44-8f08-c52ae959a5ef); [TAC ATO 58V, distributor host](https://www.mouser.com/datasheet/2/240/Littelfuse-Automotive-Blade-Fuse-TAC-ATO-58V-23798.pdf)

### Holders
- With a stated DC voltage: Schurter FEU panel holder (5 x 20 / 6.3 x 32 mm, M12.7 x 1.5 thread, 15 mm head, 45 or 46.5 mm long, panel up to 7 mm) rated 250 VAC 10 A (VDE) and 600 VAC/DC 20 A (UL/CSA), UR file E39328; Schurter OGN PCB holder 500 VAC/VDC (UL/CSA); Littelfuse 658/659/660 SMD block 500 Vac/dc (UL/CSA). - [Schurter FEU](https://www.schurter.com/en/datasheet/typ_FEU.pdf), [Schurter OGN](https://www.schurter.com/en/datasheet/typ_OGN.pdf), [Littelfuse 658/659/660](https://www.littelfuse.com/assetdocs/658-659-and-660-series-datasheet?assetguid=8563b5b9-30c3-4ebb-8e89-3cabf2bd05b5)
- Without AC/DC stated: Littelfuse 154 (125 V 10 A, UL Recognized, UL94 V-0), 348 (15 A up to 250 V), 345 ISF (no voltage); Schurter OG (600 V 10 A UL/CSA); Eaton HKP panel holder (250 V 30 A, cURus E14853, UL 94HB); Keystone 4528 (10 A at 500 V AC) and 4527/4628 (5 A at 250 V AC). - [154](https://www.littelfuse.com/assetdocs/littelfuse-fuse-154-series-data-sheet?assetguid=a8a8a462-7295-481b-a91b-d770dabf005b), [344/348](https://www.littelfuse.com/assetdocs/fuse-holder-344-348-datasheet?assetguid=2056a5c3-a2aa-404c-8a40-2c50a8fde13d), [345 ISF](https://www.littelfuse.com/assetdocs/345-isf-series-datasheet?assetguid=7b4eb031-9c1f-4100-93ae-fcc2804afc30), [Schurter OG](https://www.schurter.com/en/datasheet/typ_OG__Holder__5x20.pdf), [Eaton HKP](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-hkp-panel-mount-series-fuse-holders-data-sheet.pdf), [Keystone catalogue](https://www.keyelco.com/userAssets/file/k75p50.pdf)
- Blade-fuse holders: Littelfuse FHAC in-line ATO holder, 32 VDC, 20 / 25 / 30 A by part number, UL 94 V-0, IP67, with no UL statement on its sheet; Littelfuse FHM in-line MINI holder 0FHM0003ZXJB shows 58 V DC and 20 A in its part table (the family title says 32-58 V; Smart Glow parts are 32 V), no UL file stated; Keystone 3557-2 PCB ATO clip pair, 30 A, UL Recognized E354010; Bussmann HHC (up to 20 A, #16 lead rated 16 A) and HHD (up to 30 A, #12 lead rated 24 A), leads rated the lesser of that or 80 % of the fuse rating. The current HHC/HHD sheet's bullet says HHD up to 20 A, contradicting its own table and a 2003 edition (3 to 30 A). - [FHAC](https://www.littelfuse.com/assetdocs/ato-fhac-datasheet?assetguid=272e0b1a-a576-4173-8740-c1eb469efd79), [FHM](https://www.littelfuse.com/assetdocs/mini-fhm-datasheet?assetguid=339fa35e-eabc-45c5-9093-8abceaa8a2cf), [Keystone 3557-2](https://www.keyelco.com/product.cfm/product_id/296), [Bussmann HHC/HHD](https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/fuses/data-sheets/bus-ele-ds-2107-hhc-hhd.pdf), [2003 edition, third-party host](https://static.chipdip.ru/lib/554/DOC011554302.pdf)

## In practice
- Match the fuse's and holder's DC voltage rating to the highest voltage the circuit can reach, not its nominal. Worked example: an example 24 V supply whose over-voltage protection can trip as high as 32.4 V exceeds a 32 VDC ATOF/FHAC rating, so pick parts rated at least 32.4 V DC (Nano2 0451, PICO II 0251, or a 58 V blade fuse with a holder whose part table says 58 V).
- Quote the DC interrupting rating at your voltage: the 0451 gives 300 A only at 32 VDC (50 A at 125 V); the 0251 gives 300 A at 125 VDC.
- Size blade fuses from the derating curve at your enclosure's ambient, not from the rounded table. Example: a 5 A ATOF at 40 °C has a real ceiling of about 4.35 A; a 3 A ATOF at 65 °C about 2.72 A.
- Fuses for continuous loads are normally run at no more than 75 % of rating (Littelfuse's standard 25 % derating), then re-rated for temperature on top.
- None of the fuses checked guarantees opening within 30 s at 135 %; do not rely on a fuse to clear a small overload quickly.
- Never upgrade "UL Recognized" (component) to "UL Listed" in a parts list.

## Not verified / open questions
- Whether the 2026 PICO II curve matches the 2018 curve (the 2026 PDF curve was not extractable).
- Vector-read curve values depend on assigning curves to ratings by order.
- Nano2 0451 time-current curve points (0.200 A reaching 30 s at about 0.315 A; 0.250 A at about 0.391 A) were read from a distributor-hosted curve sheet whose URL carries an access key; not verified (no stable public source), so not filed as fact.
- No datasheet found for Littelfuse 346/653/654 or Bel holders; the icotek KEL-DPZ PDF returned 404.
- A trade-press "500 VDC" claim for Keystone 4528 contradicts the maker sheet (500 V AC) and is not filed.
- Whether FHAC carries any UL mark in another document was not checked.

Sources:
- https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1 - Nano2 0451 ratings
- https://www.littelfuse.com/451 - Nano2 marks
- https://datasheet.octopart.com/0451.500MRL-Littelfuse-datasheet-69198868.pdf - Nano2 body size
- https://www.littelfuse.com/assetdocs/fuse-251-datasheet?assetguid=f47a0bb7-8ede-4679-9646-7114c3787688 - PICO II ratings
- https://www.littelfuse.com/251 - PICO II marks
- https://rexel-cdn.com/products/littelfusefuse251253datasheet.pdf?i=2A0248F5-797E-4B9C-B780-FA5A032DED3E - PICO II body, re-rating and 30 s curves
- https://www.littelfuse.com/assetdocs/fuse-215-datasheet?assetguid=990f7193-d9a2-48e4-b760-2b43514249cf - 215
- https://www.littelfuse.com/assetdocs/fuse-216-lead-free-datasheet?assetguid=69cb9c39-1497-4ecc-b09a-c0168520688e - 216
- https://www.littelfuse.com/assetdocs/fuse-217-datasheet?assetguid=af55be94-c42e-41b1-ad43-e070e09443fe - 217
- https://www.littelfuse.com/assetdocs/fuse-218-datasheet?assetguid=a96d72b7-5296-4815-88b4-98b2f6738874 - 218
- https://www.littelfuse.com/assetdocs/fuse-235p-lead-free-datasheet?assetguid=79b16c87-8337-4c9c-96d1-6ac09ce4e440 - 235
- https://www.littelfuse.com/assetdocs/littelfuse_fuse_314_324_datasheet.pdf?assetguid=24deec6d-9c03-4f0e-b612-8499127355f3 - 314/324
- https://media.distrelec.com/Web/Downloads/_t/ds/0312001.MXP_eng_tds.pdf - 312
- https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-gma-time-delay-glass-tube-fuses-data-sheet.pdf - GMA
- https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-abc-fast-acting-ceramic-tube-fuses-data-sheet.pdf - ABC
- https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-s500-glass-tube-fuses-data-sheet.pdf - S500
- https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-s501-ceramic-tube-fuses-data-sheet.pdf - S501
- https://datasheet.octopart.com/5MF1.25-R-Bel-Fuse-datasheet-137317049.pdf - Bel 5MF
- https://media.digikey.com/pdf/Data%20Sheets/Bel%20Fuse%20PDFs/5SF.pdf - Bel 5SF
- https://media.digikey.com/pdf/Data%20Sheets/Bel%20Fuse%20PDFs/5ST.pdf - Bel 5ST
- https://www.schurter.com/en/datasheet/typ_FSF_5x20.pdf - Schurter FSF
- https://www.schurter.com/en/datasheet/typ_sp_5x20.pdf - Schurter SP
- https://www.schurter.com/en/datasheet/typ_FST_5x20.pdf - Schurter FST
- https://www.schurter.com/en/datasheet/typ_SPT_5x20.pdf - Schurter SPT
- https://www.farnell.com/datasheets/3767635.pdf - ATOF ratings, opening times, derating curve, cold resistance
- https://www.littelfuse.com/assetdocs/littelfuse-datasheet-997-mini58v?assetguid=f4bf5724-5a40-4a44-8f08-c52ae959a5ef - MINI 58 V
- https://www.mouser.com/datasheet/2/240/Littelfuse-Automotive-Blade-Fuse-TAC-ATO-58V-23798.pdf - TAC ATO 58 V
- https://www.schurter.com/en/datasheet/typ_FEU.pdf - FEU holder
- https://www.schurter.com/en/datasheet/typ_OGN.pdf - OGN holder
- https://www.littelfuse.com/assetdocs/658-659-and-660-series-datasheet?assetguid=8563b5b9-30c3-4ebb-8e89-3cabf2bd05b5 - 658/659/660
- https://www.littelfuse.com/assetdocs/littelfuse-fuse-154-series-data-sheet?assetguid=a8a8a462-7295-481b-a91b-d770dabf005b - 154
- https://www.littelfuse.com/assetdocs/fuse-holder-344-348-datasheet?assetguid=2056a5c3-a2aa-404c-8a40-2c50a8fde13d - 348
- https://www.littelfuse.com/assetdocs/345-isf-series-datasheet?assetguid=7b4eb031-9c1f-4100-93ae-fcc2804afc30 - 345 ISF
- https://www.schurter.com/en/datasheet/typ_OG__Holder__5x20.pdf - OG holder
- https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-hkp-panel-mount-series-fuse-holders-data-sheet.pdf - HKP holder
- https://www.keyelco.com/userAssets/file/k75p50.pdf - Keystone holders
- https://www.littelfuse.com/assetdocs/ato-fhac-datasheet?assetguid=272e0b1a-a576-4173-8740-c1eb469efd79 - FHAC
- https://www.littelfuse.com/assetdocs/mini-fhm-datasheet?assetguid=339fa35e-eabc-45c5-9093-8abceaa8a2cf - FHM
- https://www.keyelco.com/product.cfm/product_id/296 - Keystone 3557-2
- https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/fuses/data-sheets/bus-ele-ds-2107-hhc-hhd.pdf - Bussmann HHC/HHD
- https://static.chipdip.ru/lib/554/DOC011554302.pdf - 2003 HHC/HHD edition
