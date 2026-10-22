# Enclosure thermal budget: sealed-box temperature rise, forced-air flow, PSU derating, printed-wall limits

Applies to: any printed or moulded electronics enclosure (method); Raspberry Pi 5 figures where named; Bambu PLA Basic and PETG Basic wall limits
Verified: 2026-10-04

## Facts

### Limits inside the box
- Raspberry Pi 5: the Arm cores throttle progressively from 80 C to 85 C; at 85 C both the cores and GPU throttle. The 85 C limit applies to all models and can be lowered, not raised. - [Raspberry Pi docs: frequency management](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)
- The Pi 5 product brief lists an operating temperature of 0-70 C without saying whether that is ambient air, board or component temperature. - [Raspberry Pi 5 product brief](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008348-DS-8-raspberry-pi-5-product-brief.pdf)
- Pi 5 peak power under "power virus" workloads is around 12 W (launch article, not a datasheet value). - [Raspberry Pi 5 launch article](https://www.raspberrypi.com/news/introducing-raspberry-pi-5/)
- The default Pi 5 fan curve keys on SoC temperature (30 % at 50 C up to 100 % at 75 C, 5 C hysteresis), not enclosure air temperature. - [frequency-management.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)
- `vcgencmd measure_temp` reports the SoC's internal sensor; `vcgencmd get_throttled` bit 2 means currently throttled. Neither reads enclosure air. - [Raspberry Pi OS documentation](https://www.raspberrypi.com/documentation/computers/os.html)
- The official Active Cooler moves at most 1.09 CFM at up to 8,000 rpm and is a heatsink-mounted blower. That it mostly recirculates air over the Pi's own heatsink rather than ventilating a closed box is an engineering inference, not a source statement. - [Active Cooler product brief](https://pip-assets.raspberrypi.com/categories/993-raspberry-pi-active-cooler/documents/RP-008188-DS-2-raspberry-pi-active-cooler-product-brief.pdf)
- Bambu PLA Basic HDT: 54 C at 1.8 MPa, 57 C at 0.45 MPa (ISO 75, 100 % infill, specimens annealed and dried 55 C for 8 h, so not as-printed values). - [PLA Basic TDS V3.0](https://wiki.bambulab.com/filament-acc/abs-asa-pc/bambu_pla_basic_technical_data_sheet.pdf)
- Bambu PETG Basic HDT: 68 C at 1.8 MPa, 71 C at 0.45 MPa (ISO 75, 100 % infill, printed, not annealed). - [PETG Basic TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf)
- Bambu does not recommend PLA for environments around 50 C or higher (it may slowly soften and deform). - [Bambu filament guide material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)

### Power supply derating (how to read a curve)
- Rated efficiency is quoted at one condition only. Example: Mean Well LRS-50-5 (5 V, 10 A, 50 W) typ. 83 % at 230 VAC input, rated load, 25 C ambient; working temperature -30 to +70 C. - [LRS-50 spec](https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF)
- The LRS-50-5 derating curve allows 100 % load to 50 C on the 230 VAC curve or to 40 C on the 100 VAC curve, then falls linearly to 60 % at 70 C. No curve is labelled for 120 VAC, so the 100 VAC curve is the conservative one for North American mains. Values read from the PDF's drawn curve. - [LRS-50 spec](https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF)
- A second example: Mean Well GST60A05-P1J (5 V, 6 A, 30 W) allows 100 % load to 50 C, falling linearly to 50 % at 70 C. - [GST60A spec](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF)

### Airflow
- Required airflow to carry heat q (watts) with an air temperature rise dT: CFM = 1.8 q / dT(C), or 3.2 q / dT(F). - [Same Sky: understanding airflow fundamentals](https://www.sameskydevices.com/blog/understanding-airflow-fundamentals-for-proper-dc-fan-selection)
- A fan's catalogue CFM is its maximum (free-air) flow. The real flow is the operating point where the fan's pressure-airflow (P-Q) curve meets the system's pressure-drop curve, so it is always lower. - [Same Sky](https://www.sameskydevices.com/blog/understanding-airflow-fundamentals-for-proper-dc-fan-selection)
- Free-air ratings of 40 mm fans span a wide range, for example Noctua NF-A4x10 5V 4.82 CFM and Delta AFB0412VHB (12 V) 13.00 CFM. Noise figures are measured differently by each maker and do not compare directly. - [Noctua NF-A4x10 5V spec (archived)](http://web.archive.org/web/20250825231620/https://noctua.at/en/nf-a4x10-5v/specification), [Delta AFB0412VHB](https://www.delta-fan.com/AFB0412VHB.html)
- Some catalogues publish the full P-Q curve per model (for example Sunon's DC fan catalogue), which is what you need to find the operating point. - [Sunon DC fan catalogue](https://www.sunon.com/en/MANAGE/Docs/WEBCONT/Files/824/DC%20Fan_20260210(255-A).pdf)

## In practice
Worked example with made-up inputs (not a real build): a box 300 x 200 x 80 mm holding 20 W of electronics, room at 25 C.
1. Envelope area that sheds heat (top + 4 sides): 0.30 x 0.20 + 2 x 0.30 x 0.08 + 2 x 0.20 x 0.08 = 0.14 m2.
2. Sealed-box rise dT = Q / (h A). With h = 5-10 W/m2K (an assumed natural-convection range, not verified (no public source)): dT = 20 / (5 x 0.14) = 28.6 K to 20 / (10 x 0.14) = 14.3 K, so inside air about 39-54 C.
3. Check limits: 54 C is at PLA Basic's annealed HDT and above Bambu's ~50 C PLA guidance, so a PLA wall is marginal; PETG Basic (68 C HDT) has 14-29 K margin.
4. Check the PSU if it is inside: on the LRS-50-5 100 VAC curve, 54 C allows 100 - (54 - 40) x 40/30 = about 81 % load. A sealed box or a failed fan is the worst case to check.
5. Forced air to hold a 15 K rise: 1.8 x 20 / 15 = 2.4 CFM; for 10 K, 3.6 CFM. These are floors at the fan's operating point, not free-air ratings. The Pi Active Cooler's 1.09 CFM does not meet them and does not ventilate the box.
6. Before choosing a fan, estimate the vent pressure drop and read the operating point off the fan's P-Q curve.
- Cheapest heat reductions: put the power supply outside the box and cap LED brightness (LED current: [ws2812b-power.md](../08-electronics-lighting/ws2812b-power.md)).
- Verify with a log: SoC temperature (`vcgencmd measure_temp`) and a separate air sensor inside the box under the worst load. The h value is an assumption until measured.
- Do not double-seal a box (two gaskets or films in series); it raises thermal resistance and every margin shrinks.

## Not verified / open questions
- The h = 5-10 W/m2K natural-convection range: not verified (no public source); measure instead.
- What the Pi 5 brief's 70 C refers to (ambient, board or component).
- Whether the Active Cooler moves any air through a closed box (inference only).
- Which test standard and voltage Sunon used for its P-Q curves (not stated).
- PLA HDT is from annealed specimens; an unannealed printed wall may soften lower.

Sources:
- https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc - throttle temperatures, fan curve
- https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008348-DS-8-raspberry-pi-5-product-brief.pdf - Pi 5 operating temperature
- https://www.raspberrypi.com/news/introducing-raspberry-pi-5/ - about 12 W peak
- https://www.raspberrypi.com/documentation/computers/os.html - vcgencmd meanings
- https://pip-assets.raspberrypi.com/categories/993-raspberry-pi-active-cooler/documents/RP-008188-DS-2-raspberry-pi-active-cooler-product-brief.pdf - Active Cooler airflow
- https://wiki.bambulab.com/filament-acc/abs-asa-pc/bambu_pla_basic_technical_data_sheet.pdf - PLA Basic HDT
- https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf - PETG Basic HDT
- https://wiki.bambulab.com/en/general/filament-guide-material-table - PLA about 50 C guidance
- https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF - LRS-50 efficiency and derating
- https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF - GST60A derating
- https://www.sameskydevices.com/blog/understanding-airflow-fundamentals-for-proper-dc-fan-selection - airflow formula, operating point
- http://web.archive.org/web/20250825231620/https://noctua.at/en/nf-a4x10-5v/specification - NF-A4x10 5V airflow
- https://www.delta-fan.com/AFB0412VHB.html - AFB0412VHB airflow
- https://www.sunon.com/en/MANAGE/Docs/WEBCONT/Files/824/DC%20Fan_20260210(255-A).pdf - P-Q curves
