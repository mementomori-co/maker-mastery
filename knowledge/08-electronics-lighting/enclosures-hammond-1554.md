# Hammond 1554 polycarbonate boxes (1554HL2GY, 1554JL2GY): key drawing dimensions and gland capacity
Applies to: any build (printer-independent) · Hammond 1554 series moulded enclosures as a bought housing for a fuse or driver board
Verified: 2026-10-05

## Facts
- 1554HL2GY: outside 180.00 x 120.00 mm, box plus lid 45.55 mm tall; inside 173.09 x 113.09 x 39.45 mm. The straight inner end wall between the corner bosses is 75.10 mm. Lid 3.00 mm and floor 3.10 mm are dimensioned; the side wall is not. - [1554HL2GY drawing](https://www.hammfg.com/files/parts/pdf/1554HL2GY.pdf)
- The polycarbonate version is UL 508A approved, material UL94 5VA at 3 mm, UL file E65324, Type 4 / 4X / 6 / 6P; the rating applies at that thickness and to the polycarbonate version only. - [1554HL2GY drawing](https://www.hammfg.com/files/parts/pdf/1554HL2GY.pdf)
- 1554JL2GY: inside length 153.09 mm, body 30.05 mm tall, boss height 6.00 mm in section A-A, straight end wall 45.10 mm. Steel inner panel 1554JPL: 147.32 x 77.47 x 1.63 mm. - [1554JL2GY drawing](https://www.hammfg.com/files/parts/pdf/1554JL2GY.pdf); [1554JPL drawing](https://www.hammfg.com/files/parts/pdf/1554JPL.pdf)
- Inner panel for the HL (1554HPL): 167.13 x 106.68 x 1.63 mm, six 3.73 mm holes, four of them on 132.00 x 84.00 mm. - [1554HPL drawing](https://www.hammfg.com/files/parts/pdf/1554HPL.pdf)
- Both drawings show a ribbed boss in the middle of each end wall that accepts a #6 self-tapping screw (on the HL the two are 160.00 mm apart). Accessories named on the JL drawing: M3 x 8 mm panel screws (1591MM100), #6 x 1/4 in self-tapping screws (1598ATS100), M4 cover screws (SC576-50). - [1554HL2GY drawing](https://www.hammfg.com/files/parts/pdf/1554HL2GY.pdf); [1554JL2GY drawing](https://www.hammfg.com/files/parts/pdf/1554JL2GY.pdf)
- The series sheet lists the HL at 180 x 120 x 46 mm with panel 1554HPL, and says vertical card guides for 1.5 mm boards are moulded into all but the smallest sizes. - [Hammond 1554 series PDF](https://www.hammfg.com/electronics/small-case/plastic/1554.pdf)
- HL inside-box text (single read, not cross-checked): 4 x 4.30 mm mounting holes on 167.10 x 87.00 mm; M3 brass inserts on 132.00 x 84.00 mm. - [1554HL2GY drawing](https://www.hammfg.com/files/parts/pdf/1554HL2GY.pdf)

## In practice
- Gland capacity is arithmetic on the straight wall length. Worked example with Lapp M16 locknuts (20.9 mm across corners, 3 mm thick; see [cable-glands-and-strain-relief.md](cable-glands-and-strain-relief.md)): the JL's 45.10 mm wall takes 2 x 20.9 = 41.8 mm (3.3 mm slack, no wrench room); the HL's 75.10 mm wall takes 3 x 20.9 = 62.7 mm (12.4 mm slack, pitch up to about 27 mm), while 4 (83.6 mm) do not fit.
- The middle #6 boss sits where a centre gland would go; check its stand-off on the real box (or trim it) before drilling.
- With the JL steel panel fitted, the space above the panel (about 19.4 mm, using a floor thickness scaled from the drawing) is less than an M16 locknut's 20.9 mm, so plan glands there only without the panel.
- The side-wall thickness is not on the drawing; (180.00 - 173.09) / 2 = 3.455 mm is arithmetic, not a measurement. Measure with calipers before relying on it for a drill or gland thread length.
- For drilling vent holes in polycarbonate, see [drilling-polycarbonate-sheet.md](../07-engineering/drilling-polycarbonate-sheet.md).

## Not verified / open questions
- Undimensioned features scaled from the drawing (#6 boss diameter about 7 mm, stand-off about 3.1 to 3.7 mm, M3 boss about 8 mm, JL floor about 3.0 mm, corner-pocket floor) need the Hammond STEP model or a real box.
- Wrench access for 19 mm locknuts at tight spacing was not checked.
- Whether a card guide interferes with the HPL panel outline was not checked.

Sources:
- https://www.hammfg.com/files/parts/pdf/1554HL2GY.pdf - HL dimensions, 5VA at 3 mm, UL file, end wall, bosses
- https://www.hammfg.com/files/parts/pdf/1554JL2GY.pdf - JL dimensions, accessories
- https://www.hammfg.com/files/parts/pdf/1554HPL.pdf - HL inner panel
- https://www.hammfg.com/files/parts/pdf/1554JPL.pdf - JL inner panel
- https://www.hammfg.com/electronics/small-case/plastic/1554.pdf - series sizes, card guides
- https://products.lappgroup.com/fileadmin/documents/technische_doku/datenblaetter/skindicht/DB52103000EN.pdf - M16 locknut footprint used in the arithmetic
