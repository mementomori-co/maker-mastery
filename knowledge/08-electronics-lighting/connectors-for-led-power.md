# Connectors for low-voltage LED power: JST VH/EL/VL/VYH/XH, 4-pin DIN, DC barrel jacks, lever splices
Applies to: any build (printer-independent) · 5 V to 24 V DC LED and fan wiring
Verified: 2026-10-04

## Facts

### JST wire-to-board and wire-to-wire families
- JST VH: 10 A AC/DC with AWG #16 on the standard header, 7 A with AWG #18 on the shrouded header; 250 V AC/DC; -40 to +105 °C; contact resistance 10 mΩ max initial, 20 mΩ max after test; PC board thickness 1.6 mm. JST cautions against paralleling contacts to carry more than the rated current. - [JST VH catalogue](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf); [JST VH series page](https://www.jst-mfg.com/product/index.php?series=262)
- VH's AWG #22 to #16 range is split across contacts: SVH-21T-P1.1 takes #22 to #18 (insulation OD 1.7 to 2.2 mm); SVH-41T-P1.1 takes #20 to #16. VH does not take AWG #14. - [JST VH catalogue](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf)
- JST EL (4.5 mm pitch, wire-to-wire): 10 A AC/DC, AWG #26 to #16 (0.13 to 1.25 mm2); no #14. - [JST EL catalogue](https://www.jst-mfg.com/product/pdf/eng/eEL.pdf)
- JST VL (6.2 mm pitch) takes AWG #22 to #12 (0.3 to 3.5 mm2); 600 V AC/DC; -25 to +90 °C including temperature rise; 2, 3, 4, 6, 8 or 12 circuits. The #14 contact is SVF-61T-P2.0 (insulation OD 1.9 to 3.4 mm). Rating with AWG #14, all circuits loaded: 15 A (2 circuits), 14 A (3), 13 A (4), 12 A (6), 11 A (8), 10 A (12). The current catalogue is eVL-WB.pdf; the older eVL.pdf URL returns 404. - [JST VL series page](https://www.jst-mfg.com/product/index.php?series=264&lang=en); [JST VL-WB catalogue](https://www.jst-mfg.com/product/pdf/eng/eVL-WB.pdf)
- JST VYH (6.5 mm pitch): 15 A AC/DC (2 circuits, AWG #14) down to 2 A (6 circuits, AWG #26); 300 V AC/DC; AWG #26 to #14 (0.13 to 2 mm2); -25 to +85 °C; 2, 3, 4 or 6 circuits. - [JST VYH series page](https://www.jst-mfg.com/product/index.php?series=270&lang=en); [JST VYH catalogue](https://www.jst-mfg.com/product/pdf/eng/eVYH.pdf)
- JST XH: 3 A AC/DC with AWG #22; 250 V AC/DC; -25 to +85 °C including temperature rise; SXH-001T-P0.6 contact for AWG #28 to #22 (0.08 to 0.33 mm2), insulation OD 0.9 to 1.9 mm. - [JST XH catalogue](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf)

### JST VH part-number gotchas (same catalogue)
- Standard N-type housings run VHR-2N to VHR-11N without gaps, but retainer-mountable housings exist only as VHRR-2N, -3N, -5N, -7N, -8N and -9N, and retainers only as VHS-2V, -3V, -5V, -7V, -8V, -9V: there is no 4-circuit retainer version. - [JST VH catalogue](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf)
- The M-type housing column shows VHR-2M to VHR-7M and VHR-9M, with no VHR-8M. - [JST VH catalogue](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf)
- Headers: top entry B2P-VH to B10P-VH (and a PBT-base B2P-VH-B to B11P-VH-B series); shrouded B2P-VH-FB-B to B10P-VH-FB-B; side entry B2PS-VH to B10PS-VH; side entry with stopper is a separate S2P-VH to S7P-VH series. The 2-circuit retainer-mountable housing works only with the standard header, not the shrouded one. - [JST VH catalogue](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf)

### 4-pin DIN power connector (Kycon KPJX-PM-4S / KPPX-4P)
- KPJX-PM-4S jack: 7.5 A max per pin at 48 V DC, contact resistance 30 mΩ max, UL94 V-0, -40 to 75 °C, 4 pins; rev C2 01/08/26. The rating is per pin; the sheet gives no combined rating for paralleled pins. - [Kycon KPJX-PM-4S drawing](https://www.kycon.com/Pub_Eng_Draw/KPJX-PM-4S.pdf)
- KPPX-4P plug: 7.5 A max per pin at 48 V DC; ABS body UL94 HB, nylon insert UL94 V-2; 18 AWG recommended for power wires; -40 to +85 °C; rev A17 05/29/25. The series catalogue suggests #18 for power and #24 for signal wires. - [Kycon KPPX-4P drawing](https://www.kycon.com/Pub_Eng_Draw/KPPX-4P.pdf); [Kycon KPJX-PM catalogue](https://www.kycon.com/Catalog_PDF/KPJX-PM.pdf)
- Mean Well's GST60A plug table names the R7B 4-pin DIN option as a KPPX-4P equivalent with pinout 1 +V, 2 -V, 3 -V, 4 +V. - [Mean Well GST60A datasheet](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF) (pp. 4-5)

### DC barrel jacks
- Same Sky panel-mount jacks: PJ-005A 2.0 mm pin, 24 Vdc, 5 A, -40 to 70 °C, nut and washer included; PJ-067A 2.0 mm pin, 5 A, -25 to 70 °C, metal bushing; PJ-063AH (2.0 mm) and PJ-063BH (2.5 mm) 8.0 A at 24 Vdc, 30 mΩ, UL94 V-0, -25 to 85 °C (no ambient condition stated for the 8 A). PJ-202A is a through-hole right-angle jack rated 2.5 A. - [PJ-005A](https://www.sameskydevices.com/product/resource/pj-005a.pdf), [PJ-067A](https://www.sameskydevices.com/product/resource/pj-067a.pdf), [PJ-063AH](https://www.sameskydevices.com/product/resource/pj-063ah.pdf), [PJ-063BH](https://www.sameskydevices.com/product/resource/pj-063bh.pdf), [PJ-202A](https://www.sameskydevices.com/product/resource/pj-202a.pdf)
- Same Sky's 26-entry panel-mount catalogue has centre pins of 1.0, 1.4, 1.65, 2.0 (14 parts) and 2.5 mm (9 parts) only; no 2.1 mm panel-mount jack. Its marketing page mentions 2.1 mm, but the datasheets say 2.0 mm. - [Same Sky DC power jacks](https://www.sameskydevices.com/catalog/interconnect/dc-power-connectors/dc-power-jacks); [Same Sky panel-mount page](https://www.sameskydevices.com/panel-mount-dc-power-jacks)
- Switchcraft 722A (panel) and 722AC (in-line, solder, locking): 2.0 mm pin, 24 V, 5 A; mate with the S760 family. The 722AC page lists contact resistance 0.01 Ω without saying per contact or per pair, and warns the parts carry current only and must not be connected or disconnected under load. A 2010 copy of the 722A sheet gave 12 V; the current page gives 24 V. - [Switchcraft 722A](https://www.switchcraft.com/dc-power-jack-0-080-2-0mm-pin-solder-lugs-termination/722a/); [Switchcraft 722AC](https://www.switchcraft.com/cable-mount-in-line-dc-power-jack-2-0mm-pin-5-5mm-bushing-w-o-flex-relief/722ac/); [722AC drawing](https://www.switchcraft.com/assets/1/24/712AC-732AC%20712ACF-732ACF%20712ACFL-732ACFL_CD.PDF?6875); [2010 722A copy](https://datasheet.octopart.com/722A-Switchcraft-datasheet-9793928.pdf)
- Kycon KLDHCX-0202 (PCB mount): 2.0 / 2.5 mm pin, 5 A, 24 V RMS, UL file E140125. Adam Tech ADC (2009 sheet): standard series 12 V DC / 1 A, ADCH high-current 5 A, pins 1.00 / 1.30 / 2.00 / 2.35 / 2.50 mm; no 2.1 mm. - [Kycon KLDHCX-0202](https://www.kycon.com/Catalog_PDF/KLDHCX-0202-x-LT.pdf); [Adam Tech ADC-H-028-1](https://cdn.sparkfun.com/datasheets/Prototyping/ADC-H-028-1.pdf)
- Mean Well's standard GST18 to GST60 plug is P1J (2.1 x 5.5 x 11 mm) and the GST90 to GST120 plug is P1M (2.5 x 5.5 x 11 mm); adapters P1M-P1J and P1J-R7B exist. The 722AC family mates Mean Well's optional lock-style plugs, not the standard P1J. - [Mean Well DC plug sheet, distributor host](https://files.trcelectronics.com/datasheets/MW-DC-PLUG.PDF); [GST60A datasheet](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF)

### Lever splice connector (WAGO 221-412)
- cULus Listed to UL 486C (certificate E69654), 600 V / 20 A in the UL column; separately listed to UL 467 (E201573). The EN 60664 rating of 450 V / 32 A is a different scheme and not the UL rating. Wire 0.2 to 4 mm2 / 24 to 12 AWG solid, stranded or fine-stranded; strip 11 mm; polycarbonate housing UL94 V2; +85 °C ambient, 105 °C continuous (T85). - [WAGO 221-412 datasheet, distributor host](https://assets.cef.co.uk/downloads/pdg/wago_221-412_datasheet/wago_221-412_datasheet.pdf)

## In practice
- Match the contact part number to the wire gauge before crimping; a series' headline range is not one contact.
- For AWG #14, VH and EL are out; use VL (SVF-61T-P2.0) or VYH, and read the per-circuit-count rating, not the headline figure.
- Treat 4-pin DIN ratings as per pin. Do not double the rating by paralleling pins.
- A 2.1 mm plug on a 2.0 mm pin jack can seat loosely; no 2.1 mm panel-mount jack was found anywhere checked. Test the fit on real parts, or use the matching in-line or adapter part instead.
- Never make or break a barrel or DIN power connection under load unless the maker rates it for that.

## Not verified / open questions
- Molex Mini-Fit Jr. with AWG #14: the current Molex spec could not be fetched; a 2014 distributor copy suggests 16 to 24 AWG only (not filed as fact).
- XT30 current rating: the maker's page shows it only in an image; do not use a figure from memory.
- Phoenix Contact MKDS 1.5/3.5 rating not obtained (page blocked). WAGO 236 is a spring (cage-clamp) block, not a screw terminal.
- Whether the Same Sky "24 Vdc" rating tolerates a 24 V supply running at its +3 % tolerance (about 24.7 V) was not checked.
- Switchcraft 722A panel hole size (.313 in, panel up to .125 in) is confirmed only in the 2010 copy.
- Mean Well adapter drawings (P1J-R7B, P1M-P1J) are hosted only by a third party (meanwell.com copies returned 404) and their pin text could not be decoded.

Sources:
- https://www.jst-mfg.com/product/pdf/eng/eVH.pdf - JST VH ratings, contacts, part numbers
- https://www.jst-mfg.com/product/index.php?series=262 - JST VH series page
- https://www.jst-mfg.com/product/pdf/eng/eEL.pdf - JST EL ratings
- https://www.jst-mfg.com/product/index.php?series=264&lang=en - JST VL series page
- https://www.jst-mfg.com/product/pdf/eng/eVL-WB.pdf - JST VL per-circuit ratings, #14 contact
- https://www.jst-mfg.com/product/index.php?series=270&lang=en - JST VYH series page
- https://www.jst-mfg.com/product/pdf/eng/eVYH.pdf - JST VYH catalogue
- https://www.jst-mfg.com/product/pdf/eng/eXH.pdf - JST XH ratings
- https://www.kycon.com/Pub_Eng_Draw/KPJX-PM-4S.pdf - 4-pin DIN jack
- https://www.kycon.com/Pub_Eng_Draw/KPPX-4P.pdf - 4-pin DIN plug
- https://www.kycon.com/Catalog_PDF/KPJX-PM.pdf - series wire-gauge suggestion
- https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF - R7B pinout, P1J plug
- https://files.trcelectronics.com/datasheets/MW-DC-PLUG.PDF - Mean Well plug families and adapters (distributor host)
- https://www.sameskydevices.com/product/resource/pj-005a.pdf - PJ-005A
- https://www.sameskydevices.com/product/resource/pj-067a.pdf - PJ-067A
- https://www.sameskydevices.com/product/resource/pj-063ah.pdf - PJ-063AH
- https://www.sameskydevices.com/product/resource/pj-063bh.pdf - PJ-063BH
- https://www.sameskydevices.com/product/resource/pj-202a.pdf - PJ-202A
- https://www.sameskydevices.com/catalog/interconnect/dc-power-connectors/dc-power-jacks - no 2.1 mm panel jack
- https://www.sameskydevices.com/panel-mount-dc-power-jacks - marketing page disagreeing with datasheets
- https://www.switchcraft.com/dc-power-jack-0-080-2-0mm-pin-solder-lugs-termination/722a/ - 722A
- https://www.switchcraft.com/cable-mount-in-line-dc-power-jack-2-0mm-pin-5-5mm-bushing-w-o-flex-relief/722ac/ - 722AC
- https://www.switchcraft.com/assets/1/24/712AC-732AC%20712ACF-732ACF%20712ACFL-732ACFL_CD.PDF?6875 - 722AC drawing
- https://datasheet.octopart.com/722A-Switchcraft-datasheet-9793928.pdf - 2010 722A copy
- https://www.kycon.com/Catalog_PDF/KLDHCX-0202-x-LT.pdf - Kycon PCB jack
- https://cdn.sparkfun.com/datasheets/Prototyping/ADC-H-028-1.pdf - Adam Tech ADC
- https://assets.cef.co.uk/downloads/pdg/wago_221-412_datasheet/wago_221-412_datasheet.pdf - WAGO 221-412
- https://www.tti.com/content/dam/ttiinc/manufacturers/molex/doc/Molex-Mini-Fit-Jr-Connectors-Datasheet-Specifications.pdf - 2014 distributor copy, Mini-Fit Jr. (not filed as fact)
