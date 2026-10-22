# 12 V / 24 V LED power: analog and COB strips, Mean Well bricks, DC-DC converters and mains cords
Applies to: any build (printer-independent) · Mean Well LRS / GST / DDR / RSD / PSD / SD families, Traco TMDC 40, analog RGB and COB strips, IEC C13/C14 cords
Verified: 2026-10-04

## Facts

### Open-frame supplies (Mean Well LRS, sheets dated 2025-04-07; efficiency at 230 VAC, rated load, 25 °C)
- LRS-35-12: 12 V, 3 A, 36 W; case 99 x 82 x 30 mm, 0.21 kg; efficiency typ. 86 %. - [LRS-35 datasheet](https://www.meanwell.com/Upload/PDF/LRS-35/LRS-35-SPEC.PDF)
- LRS-50-24: 24 V, 2.2 A, 52.8 W; efficiency typ. 88 %. - [LRS-50 datasheet](https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF)

### Sealed desktop bricks with an IEC C14 inlet
- GST60A24 (sheet 2026-04-03): 24 V, 2.5 A, 60 W; efficiency typ. 90.5 % (230 VAC, rated load, 25 °C, 70 % RH); ripple 150 mVp-p (20 MHz, 12 in twisted pair with 0.1 µF and 47 µF); AC input current typ. 1.4 A at 115 VAC, 1 A at 230 VAC; 24 to 48 V models use a UL1185 18 AWG cord, 1800 +/-50 mm; P1J plug, centre positive, -V not connected to FG. Overload 105 to 150 % with hiccup auto-recovery; OVP 25.2 to 32.4 V, re-power to recover. Safety: UL 62368-1, CSA C22.2 No. 62368-1, EN 62368-1 and others. - [GST60A datasheet](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF)
- GST60A24 derating (page 3 curves, horizontal mounting, below 2000 m): 100 % load from -30 to 50 °C, falling linearly to 50 % at 70 °C; only these endpoints are reliable because the drawn axis ticks are uneven. Input: 90 % load at 90 VAC, 100 % from 100 to 264 VAC. Above 2000 m, derate ambient 3.5 °C per 1000 m (fanless). - [GST60A datasheet](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF)
- The GST60A C14 inlet is not dimensioned on the drawing (case tolerance +/-1 mm, and the end view is drawn at a different scale on each axis); position estimates read from the artwork are not reliable to +/-1 mm. - [GST60A datasheet](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF) (p. 3)
- GST90A24 (sheet 2026-04-03): 24 V, 3.75 A, 90 W; ripple 200 mVp-p; tolerance +/-3.0 %; efficiency typ. 90 %; derating flat to 40 °C (not 50 °C as on the GST60A), then linear to 50 % at 70 °C; 80 % load at 90 VAC; case 145 x 60 x 32 mm, 0.45 kg; 19 to 48 V models use UL1185 16 AWG, 1200 +/-50 mm (12 to 15 V models 14 AWG, 1000 mm); P1M plug (2.5 x 5.5 x 11 mm). Overload 110 to 150 % hiccup; OVP 105 to 135 % of rated voltage, latching. The sheet contains no LPS text; Mean Well's separate table lists GST90A as PS3, does not meet LPS. - [GST90A datasheet](https://www.meanwell.com/Upload/PDF/GST90A/GST90A-SPEC.PDF); [Mean Well ES/PS/LPS table](https://www.meanwell.com/Upload/PDF/62368%20ES%20PS%20LPS%2061558%20OVC%2060335.pdf)
- GST120A24: 24 V, 5 A, 120 W; efficiency 90.5 % (R7B DIN option) / 89.5 % (P1M plug); case 167 x 67 x 35 mm; overload 105 to 160 %; -V is connected to AC FG (the GST90A's is not). The value pages are dated 2025-03-28 although the cover says 2026-04-03. - [GST120A datasheet](https://www.meanwell.com/Upload/PDF/GST120A/GST120A-SPEC.PDF)
- Mean Well's generic adaptor manual says nothing about cutting, splicing, extending or repairing the DC output cord (a text search for those words finds nothing); it warns against opening the case and against forcing a wrong DC plug into equipment. Silence is not permission. - [Mean Well Adaptor manual](https://www.meanwell.com/Upload/PDF/Adaptor_EN.pdf)

### 24 V to 5 V DC-DC converters
- DDR-60G-5 (DIN rail, sheet 2026-03-31; 24 Vdc in, rated load, 25 °C): 9 to 36 Vdc in, 5 V 10.8 A, 54 W, ripple 60 mVp-p, adjustable 4.5 to 5.5 V, tolerance +/-2.0 %, efficiency 87.5 %; overload 105 to 135 % constant-current limiting; OVP 5.75 to 7 V; UL 62368-1; 4 kVdc isolation; inrush typ. 20 A at 24 Vdc; case 52.5 x 90 x 54.5 mm with a 58.4 mm depth also drawn (use 58.4 mm for clearance). Derating (vertical) above 18 Vdc input: 100 % to 50 °C, about 60 % at 70 °C, about 35 % at 85 °C; a separate curve for 18 Vdc or less starts at only 75 %. The DDR-60L-5 is a different part. - [DDR-60 datasheet](https://www.meanwell.com/Upload/PDF/DDR-60/DDR-60-SPEC.PDF)
- DDR-30G-5 (sheet 2026-03-31): 6 A only at 12 to 36 Vin, 5.1 A at 9 to 12 Vin; adjustable 4.5 to 5.5 V; efficiency 85 %; UL/IEC 62368-1; case 35 x 90 x 54.5 mm (58.4 mm also drawn). Derating is not linear: 100 % at 60 °C, 50 % at 75 °C, 40 % at 85 °C on a non-uniform axis. - [DDR-30 datasheet](https://www.meanwell.com/Upload/PDF/DDR-30/DDR-30-SPEC.PDF)
- The DDR installation manual allows only vertical mounting with input terminals at the bottom, with clearances of 5 mm left and right, 40 mm above and 20 mm below; DDR-15/30 maximum operating temperature is 60 °C. - [Mean Well DDR installation manual](https://www.meanwell.com/Upload/PDF/DDR%20DIN%20rail%20power%20supply.pdf)
- RSD-60G-5 (sheet 2026-07-09): 5 V 12 A, 60 W, efficiency 88 %, no output adjustment; -40 to +55 °C without derating, +70 °C at 60 % load in free air; 128 x 60 x 25 mm; UL 62368-1. RSD-30G-5: 6 A, 84 %, no adjustment, 113 x 60 x 25 mm, semi-potted so one derating curve covers its mounting methods. - [RSD-60 datasheet](https://www.meanwell.com/Upload/PDF/RSD-60/RSD-60-SPEC.PDF); [RSD-30 datasheet](https://www.meanwell.com/Upload/PDF/RSD-30/RSD-30-SPEC.PDF)
- Traco TMDC 40-2411 (rev. September 4, 2026): 9 to 36 VDC in, 5.1 V 8 A, 90 %; case 112.0 x 63.8 x 25.6 mm, UL 94 V-0 resin; case max +95 °C but approved ambient (60950-1) +65 °C max; no trim; terminal wire up to 1.5 mm2 at 0.5 Nm max; 4 x 3.5 mm holes on 100.0 x 50.0 mm. The input-fuse row gives no value and says the need for a fuse must be assessed in the final product. The installation instructions require it to be built into an enclosure and not accessible in operation. UL Recognized component (E188913, UL 62368-1 2nd Ed.), not a listed end product. - [TMDC 40 datasheet](https://www.tracopower.com/sites/default/files/products/datasheets/tmdc40_datasheet.pdf); [TMDC 40 installation](https://www.tracopower.com/sites/default/files/products/installation_instructions/tmdc40_installation.pdf); [TMDC 40 UL CoC](https://www.tracopower.com/sites/default/files/products/certifications/tmdc40_ul62368_1_coc.pdf)
- Ruled out by their own sheets: DDR-120 has no 5 V model (12 / 24 / 48 V only); PSD-45B-05 (9 A) lists no UL standard; SD-50 and SD-100 list no UL. - [DDR-120](https://www.meanwell.com/Upload/PDF/DDR-120/DDR-120-SPEC.PDF), [PSD-45](https://www.meanwell.com/Upload/PDF/PSD-45/PSD-45-SPEC.PDF), [SD-50](https://www.meanwell.com/Upload/PDF/SD-50/SD-50-SPEC.PDF), [SD-100](https://www.meanwell.com/Upload/PDF/SD-100/SD-100-SPEC.PDF)

### Mains side: cords, splitters, C13 size
- Eaton P004-18N-2C13 (C14 to 2 x C13, 18 in): 10 A input (one figure, not per outlet), 100 to 250 VAC, UL / cUL Listed and CSA, -20 to 60 °C; 6 in from the C14 to the split, then 12 in per C13 leg; 18 AWG 3-conductor SJT, 7.8 mm OD. The 6 ft P004-006-2C13 has the same ratings but no stated leg length. The EU variant P004-02M-2C13EU has no UL/cUL/CSA line. - [P004-18N-2C13 page](https://www.eaton.com/us/en-us/skuPage.P004-18N-2C13.html); [P004-18N-2C13 spec sheet](https://assets.tripplite.com/product-pdfs/en/p00418n2c13.pdf); [P004-006-2C13 spec sheet](https://assets.tripplite.com/product-pdfs/en/p0040062c13.pdf); [P004-02M-2C13EU spec sheet](https://assets.tripplite.com/product-pdfs/en/p00402m2c13eu.pdf)
- StarTech PXT101Y (NEMA 5-15P to 2 x C13): 10 A, 125 VAC, 18 AWG, UL Listed. Tripp Lite/Eaton P006-006 and P006-010 (NEMA 5-15P to C13, 6 ft and 10 ft): 10 A, 125 V, 18 AWG SJT, UL / cUL Listed. - [StarTech PXT101Y](https://www.startech.com/en-us/cables/pxt101y); [P006-006](https://assets.tripplite.com/product-pdfs/en/p006006.pdf); [P006-010](https://assets.tripplite.com/product-pdfs/en/p006010.pdf)
- Interpower's cord reference gives 18 AWG flexible cord at 30 °C ambient as 7 A (NEC column A, three current-carrying conductors) and 10 A (column B, two current-carrying conductors, including a 3-conductor cord on a single-phase load); it cites NEC Article 400 Table 400-5(A) in a 2004 issue. SJT is a hard-service cord type. - [Interpower cord-type reference](https://www.interpower.com/docs/connections02-05icl.pdf)
- Interpower C13 connector drawings: face 25 x 19 mm to 25.5 x 19.3 mm, body length 72.7 mm. A 25.5 x 19.3 mm face has a 31.98 mm diagonal (computed). - [Interpower 86611010](https://www.interpower.com/drawings/86611010.pdf); [Interpower 70403020214](https://www.interpower.com/drawings/70403020214.pdf); [Interpower 86286110](https://www.interpower.com/drawings/86286110.pdf)

### Analog RGB and COB strips (vendor pages; figures apply to the exact item)
- A 12 V 5050 RGB strip at 18 LEDs/ft: 10 mm wide, 4.9 A per 5 m reel, 299 mA/ft, 3.6 W/ft, longest single run 4.5 m. A 24 V RGB COB strip: 12 mm wide, 3.1 A per 5 m, 191 mA/ft, 4.6 W/ft, 6 m Class 2 run; marked discontinued. - [Super Bright LEDs 5050 RGB](https://www.superbrightleds.com/5m-rgb-led-strip-light-color-changing-led-tape-light-12v-24v-ip20); [Super Bright LEDs RGB COB](https://www.superbrightleds.com/5m-rgb-cob-led-strip-light-cob-series-led-tape-light-24v-ip20)
- COB cut pitch varies by product: a 24 V RGBCCT COB cuts every 35.7 mm (12 mm wide at IP20, 20 W/m); a 24 V RGBW COB at 840 LEDs/m every 33.33 mm (12 mm, 20 W/m); a 24 V single-colour dotless COB every 50 mm (2 mm tall, 8 or 10 mm wide). - [FCOB-24V-RGBCCT-THICK spec](https://www.superlightingled.com/PDF/SPEC/FCOB-24V-RGBCCT-THICK.pdf); [840 LEDs/m RGBW COB](https://www.superlightingled.com/24v-high-density-rgbw-cob-led-strip-with-a-thinner-cover-layer-840-leds-m-p-6411.html); [Dotless COB data sheet](https://www.solidapollo.com/PDF/Dotless-COB-LED-Strip-Lights-Data-Sheet.pdf)

### A 24 V fan on the same rail (Sunon MF40202VX-1000U-A99)
- 40 mm, 24 VDC, 39 mA rated (45 mA max), -10 to +70 °C; PBT UL 94V-0 frame and blade, UL/CUR file E77551; restarts within 10 s after a locked rotor. Sunon recommends adding a thermal or current fuse or thermal protector in the application. - [Sunon spec](https://www.sunonusa.com/wp-content/uploads/2026/05/MF40202VX-1000U-A99-D04115190G-03-1.pdf)

## In practice
- Every efficiency figure holds at 230 VAC, rated load and 25 °C. Expect less at 115 VAC or part load.
- Do not reuse one brick's derating curve for another (GST60A flat to 50 °C, GST90A only to 40 °C). Plan to run a brick at or below about 75 % of its derated rating (a margin choice, not a Mean Well rule).
- Worked example, an example 24 V, 3 A enclosure: 3 A exceeds a GST60A24 (2.5 A), so step up. A GST90A24 (3.75 A) would run at 80 %, above a 75 % margin target and inside its flat region only up to 40 °C ambient; a GST120A24 (5 A) runs at 60 % (its derating curve was not read for this note, so check it before relying on that). If 5 V is also needed, feed a DDR-60G-5 from the 24 V rail and budget its input current (about 54 W / 0.875 / 24 V = 2.6 A at full output) against the brick too.
- Use the "above 18 Vdc" curve for a DDR-60G-5 on a 24 V rail; never average it with the 18 V-or-less curve. Mount DDR units only vertically, input terminals down.
- Two GST60A bricks on one 10 A splitter draw at most about 2.8 A at 115 VAC, well inside its single rating.
- An 18 AWG 3-conductor SJT cord on a single-phase 120 V load is a 10 A cord (column B); match the column to the load.
- Prefer a mating plug or in-line jack over cutting a brick's captive DC cord; the maker documents neither cutting nor splicing.
- Measure a real brick before cutting a window for its C14 inlet; size any opening for the C13 plug body, not the drawn inlet.
- Confirm the exact strip SKU before sizing; one product page can sell several densities and voltages.

## Not verified / open questions
- P004-006-2C13 leg length (about 3 ft per leg) appears only in reseller copy, not from Eaton.
- Whether the P004-18N-2C13's 12 in leg is measured to the connector face or the moulding.
- Which LRS-35-12 / LRS-50-24 safety marks cover the 12 V / 24 V variants was not re-checked.
- The NEC table numbering in the Interpower source (2004) was not checked against the current NEC.
- The "PCB height 2.2 mm" store option on the 840 LEDs/m COB page does not say what it measures.

Sources:
- https://www.meanwell.com/Upload/PDF/LRS-35/LRS-35-SPEC.PDF - LRS-35-12
- https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF - LRS-50-24
- https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF - GST60A24 ratings, derating, protections
- https://www.meanwell.com/Upload/PDF/GST90A/GST90A-SPEC.PDF - GST90A24
- https://www.meanwell.com/Upload/PDF/GST120A/GST120A-SPEC.PDF - GST120A24
- https://www.meanwell.com/Upload/PDF/62368%20ES%20PS%20LPS%2061558%20OVC%2060335.pdf - Mean Well ES/PS/LPS table
- https://www.meanwell.com/Upload/PDF/Adaptor_EN.pdf - adaptor manual, silent on cord cutting
- https://www.meanwell.com/Upload/PDF/DDR-60/DDR-60-SPEC.PDF - DDR-60G-5
- https://www.meanwell.com/Upload/PDF/DDR-30/DDR-30-SPEC.PDF - DDR-30G-5
- https://www.meanwell.com/Upload/PDF/DDR%20DIN%20rail%20power%20supply.pdf - DDR mounting rules
- https://www.meanwell.com/Upload/PDF/RSD-60/RSD-60-SPEC.PDF - RSD-60G-5
- https://www.meanwell.com/Upload/PDF/RSD-30/RSD-30-SPEC.PDF - RSD-30G-5
- https://www.tracopower.com/sites/default/files/products/datasheets/tmdc40_datasheet.pdf - TMDC 40
- https://www.tracopower.com/sites/default/files/products/installation_instructions/tmdc40_installation.pdf - TMDC 40 enclosure rule
- https://www.tracopower.com/sites/default/files/products/certifications/tmdc40_ul62368_1_coc.pdf - TMDC 40 UL recognition
- https://www.meanwell.com/Upload/PDF/DDR-120/DDR-120-SPEC.PDF - DDR-120, no 5 V model
- https://www.meanwell.com/Upload/PDF/PSD-45/PSD-45-SPEC.PDF - PSD-45, no UL
- https://www.meanwell.com/Upload/PDF/SD-50/SD-50-SPEC.PDF - SD-50, no UL
- https://www.meanwell.com/Upload/PDF/SD-100/SD-100-SPEC.PDF - SD-100, no UL
- https://www.eaton.com/us/en-us/skuPage.P004-18N-2C13.html - splitter ratings
- https://assets.tripplite.com/product-pdfs/en/p00418n2c13.pdf - splitter leg lengths, cord
- https://assets.tripplite.com/product-pdfs/en/p0040062c13.pdf - 6 ft splitter
- https://assets.tripplite.com/product-pdfs/en/p00402m2c13eu.pdf - EU splitter, no UL line
- https://www.startech.com/en-us/cables/pxt101y - NEMA to 2 x C13 splitter
- https://assets.tripplite.com/product-pdfs/en/p006006.pdf - NEMA to C13 cord, 6 ft
- https://assets.tripplite.com/product-pdfs/en/p006010.pdf - NEMA to C13 cord, 10 ft
- https://www.interpower.com/docs/connections02-05icl.pdf - cord types, 18 AWG columns A/B
- https://www.interpower.com/drawings/86611010.pdf - C13 25.5 x 19.3 mm face
- https://www.interpower.com/drawings/70403020214.pdf - C13 25 x 19 mm face
- https://www.interpower.com/drawings/86286110.pdf - C13 25 x 19 mm face
- https://www.superbrightleds.com/5m-rgb-led-strip-light-color-changing-led-tape-light-12v-24v-ip20 - 12 V 5050 RGB strip
- https://www.superbrightleds.com/5m-rgb-cob-led-strip-light-cob-series-led-tape-light-24v-ip20 - 24 V RGB COB (discontinued)
- https://www.superlightingled.com/PDF/SPEC/FCOB-24V-RGBCCT-THICK.pdf - RGBCCT COB cut pitch
- https://www.superlightingled.com/24v-high-density-rgbw-cob-led-strip-with-a-thinner-cover-layer-840-leds-m-p-6411.html - RGBW COB cut pitch
- https://www.solidapollo.com/PDF/Dotless-COB-LED-Strip-Lights-Data-Sheet.pdf - dotless COB
- https://www.sunonusa.com/wp-content/uploads/2026/05/MF40202VX-1000U-A99-D04115190G-03-1.pdf - 24 V 40 mm fan
