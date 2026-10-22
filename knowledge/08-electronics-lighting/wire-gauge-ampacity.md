# Wire gauge ampacity (AWG): chassis wiring vs power transmission
Applies to: any build (printer-independent) · copper hookup and harness wire, 10 to 22 AWG
Verified: 2026-10-04

## Facts
- PowerStream's AWG table has two different current columns. "Maximum amps for chassis wiring": 16 AWG 22 A, 18 AWG 16 A, 20 AWG 11 A, 22 AWG 7 A; the page says this column is for a single wire in air, not in a bundle. "Maximum amps for power transmission": 16 AWG 3.7 A, 18 AWG 2.3 A, 20 AWG 1.5 A, 22 AWG 0.92 A; it uses a 700 circular mils per amp rule that the page itself calls very conservative. The page does not label the second column "bundled" or "continuous". The page calls the whole table a rule of thumb and says installations that must meet the National Electrical Code must follow NEC guidelines. - [powerstream.com/Wire_Size.htm](https://www.powerstream.com/Wire_Size.htm) (community/vendor page, dated 2023-04-18)
- Heavier rows from the same table (same conditions: chassis = single wire in free air; power transmission = 700 cmil/A; no conductor temperature stated for resistance): 10 AWG 3.276 Ω/km, 55 A chassis, 15 A transmission; 12 AWG 5.209 Ω/km, 41 A, 9.3 A; 14 AWG 8.282 Ω/km, 32 A, 5.9 A; 16 AWG 13.17 Ω/km; 18 AWG 20.94 Ω/km. - [powerstream.com/Wire_Size.htm](https://www.powerstream.com/Wire_Size.htm)

## In practice
- For wires bundled inside an enclosure harness, plan against the lower "power transmission" column. That is a margin-of-safety choice made here, not a label the page applies to bundles. The chassis column assumes open air and overstates what a bundle can carry.
- Use the resistance column for voltage-drop budgets: drop = I x R x round-trip length. Example: 2 A over 1 m of 18 AWG pair (2 m of conductor) = 2 x 0.02094 x 2 = 0.084 V (resistance at the page's unstated temperature; copper resistance rises with temperature).
- This is not a standard. For anything safety-critical or mains-connected, check the applicable code table (for example NEC Table 310.16) or the cable maker's own rating before finalising.

## Not verified / open questions
- No UL or NEC table was checked against these numbers; treat them as planning figures only.

Sources:
- https://www.powerstream.com/Wire_Size.htm - AWG chassis vs power-transmission ampacity and resistance per length, with the page's own conditions (community)
