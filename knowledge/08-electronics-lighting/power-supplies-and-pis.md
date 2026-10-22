# Power-limited sources (PIS) and fuse-bound arithmetic for low-voltage LED circuits
Applies to: any build (printer-independent) · IEC 62368-1 Ed. 2 wording as seen in a test report form; Mean Well GST60A24, Traco TMDC 40, Littelfuse 0251/0451 data
Verified: 2026-10-05

## Facts

### What "resistive PIS" means in the readable sources
- A community conference slide summarises a resistive potential ignition source as a point where more than 100 W can be dissipated in the first 30 s, or more than 15 W afterwards; and an arcing PIS as above 50 V peak with a (Vpeak x Irms) product above 15, both conditions together. - [IEEE PSES slide deck, 2012](https://ewh.ieee.org/r6/ocs/pses/1202_portland.pdf) (community)
- A CB test report form for IEC 62368-1 Ed. 2 (2014) words it differently: a resistive PIS dissipates more than 15 W measured after 30 s of normal operation, or under a single fault exceeds 100 W measured immediately after the fault (where electronic circuits, regulators or PTC devices are used) or 15 W measured 30 s after the fault. So the 100 W figure applies only to those circuit types and is measured right after the fault. - [onsemi FPF2895 UL test report, table 6.2.3.2](https://www.onsemi.cn/pub/collateral/fpf2895%20ul%20test%20report.pdf) (a test report form, not the standard)

### Supply data used in the worked examples
- Mean Well GST60A24 (spec sheet 2026-04-03): 24 V, 2.5 A, 60 W; tolerance +/-3.0 %; over-voltage protection trips between 25.2 and 32.4 V; overload 105 to 150 % of rated power. The spec sheet itself carries no ES/PS/LPS text; Mean Well publishes that in a separate table (GST60A listed as PS2, meets LPS). - [GST60A datasheet](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF); [Mean Well ES/PS/LPS table](https://www.meanwell.com/Upload/PDF/62368%20ES%20PS%20LPS%2061558%20OVC%2060335.pdf)
- Traco TMDC 40-2411 (datasheet rev. September 4, 2026; values at nominal input, resistive full load, 25 °C): 9 to 36 VDC in, 5.1 VDC 8 A out, 90 % typ.; set accuracy +/-2 % max; current limit 150 % typ. (12 A); over-voltage protection 120 % typ. of nominal (6.12 V, a typical value, not a guaranteed ceiling); output classed PS3 per IEC 62368-1; input current at 24 V typ. 90 mA no load, 1868 mA full load (about 91 % efficiency); no part-load efficiency given. - [TMDC 40 datasheet](https://www.tracopower.com/sites/default/files/products/datasheets/tmdc40_datasheet.pdf)
- Fuse data (see [fuses-and-holders-dc.md](fuses-and-holders-dc.md)): PICO II 0251 opens within 1 s at 200 %; its re-rating curve, as drawn, reads 101.47 % at 20 °C (100.54 % if normalised to 25 °C = 100 %). Nano2 0451.200 cold resistance 0.8372 Ω. - [Littelfuse 251 datasheet](https://www.littelfuse.com/assetdocs/fuse-251-datasheet?assetguid=f47a0bb7-8ede-4679-9646-7114c3787688); [251/253 datasheet, Rexel host](https://rexel-cdn.com/products/littelfusefuse251253datasheet.pdf?i=2A0248F5-797E-4B9C-B780-FA5A032DED3E); [Littelfuse 451/453 datasheet](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1)

## In practice
Method (computed, not from a standard): the most power a fused branch can deliver before the fuse is guaranteed to open quickly is about P = 2 x In x re-rating x Uoc, where In is the fuse rating, the 2 is the 200 % opening point, the re-rating is read at the coldest expected ambient, and Uoc is the highest open-circuit voltage the supply can reach.
- Worked example 1, an example 24 V, 2.5 A brick: Uoc from tolerance is 24 x 1.03 = 24.72 V; at the over-voltage trip ceiling it is 32.4 V. Overload up to 150 % means 90 W can flow before the brick limits, and 2.5 A x 32.4 V = 81.0 W.
- Worked example 2, a 0.200 A PICO II on that brick: 2 x 0.2 x 1.0147 x 24.72 = 10.03 W, and 13.15 W at 32.4 V (both under 15 W). A 0.250 A fuse at 32.4 V gives 16.44 W (over 15 W).
- Worked example 3, a 2 A PICO II at 24.72 V: 99.41 W normalised but 100.33 W as drawn, so it cannot be claimed to stay at or below 100 W.
- Worked example 4, a 1 A PICO II on a 5.1 V converter: with Uoc 5.28 V it is about 10.7 W; at the 6.12 V typical over-voltage point about 12.4 W. A 2 A fuse at 6.12 V gives about 24.6 W (normalised) to 24.8 W (as drawn), so check the fuse rating before quoting a small-watt bound.
- State which re-rating convention you used (normalised or as drawn); as drawn is about 0.9 % higher and is the conservative one.
- These numbers are design aids. A product that must comply needs the current edition of the standard and, normally, a test lab.

## Not verified / open questions
- IEC 62368-1 Ed. 3 (2018) and Ed. 4 (2023) PIS wording was not checked (paywalled); the slide vs Ed. 2 form difference is unresolved.
- NEC Article 725 and UL 60950-1 power limits are not covered here.
- The 5.28 V Uoc for the converter adds 0.5 % and 1 % terms (input and load variation) to the 2 % set accuracy; those terms come from the same datasheet's variation rows but were not separately fact-checked for this use.
- The converter's over-voltage point is typical, not guaranteed, so its worst case is not known.

Sources:
- https://ewh.ieee.org/r6/ocs/pses/1202_portland.pdf - community slide: resistive and arcing PIS limits
- https://www.onsemi.cn/pub/collateral/fpf2895%20ul%20test%20report.pdf - IEC 62368-1 Ed. 2 test report form wording
- https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF - GST60A24 rating, tolerance, OVP, overload
- https://www.meanwell.com/Upload/PDF/62368%20ES%20PS%20LPS%2061558%20OVC%2060335.pdf - Mean Well ES/PS/LPS table
- https://www.tracopower.com/sites/default/files/products/datasheets/tmdc40_datasheet.pdf - TMDC 40 output, accuracy, current limit, OVP, PS3, input current
- https://www.littelfuse.com/assetdocs/fuse-251-datasheet?assetguid=f47a0bb7-8ede-4679-9646-7114c3787688 - PICO II ratings
- https://rexel-cdn.com/products/littelfusefuse251253datasheet.pdf?i=2A0248F5-797E-4B9C-B780-FA5A032DED3E - PICO II re-rating curve
- https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1 - Nano2 0451.200 data
