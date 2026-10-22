# Heat-set threaded inserts (M2-M5): hole, depth, boss and install temperature

Applies to: any FDM printer (design-stage fact, not slicer-dependent) - PLA and PETG
Verified: 2026-10-03

## Facts

### Caveat that applies to every manufacturer row below
- SPIROL, PEM and Tappex write their hole tables for moulded or drilled holes in moulded plastic, not for FDM. SPIROL prefers moulded holes over drilled ones, and PEM's minimum-wall figure was tested in ABS and polycarbonate coupons. None of the three mentions FDM, PLA or PETG. Treat every hole and wall number below as a nominal moulded-hole starting point, not a CAD value. - [SPIROL design guide](https://www.spirol.com/assets/files/ins-threaded-inserts-design-guide-us.pdf), [PEM SI data](https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/sidata.pdf)
- Printed holes come out smaller than CAD: CNC Kitchen measured holes about 0.25 mm under the CAD diameter on one printer (Prusa CORE One L) with one PLA. That figure belongs to that printer and filament; measure your own. - [CNC Kitchen, "Are our heat-set insert datasheets wrong?"](https://www.cnckitchen.com/blog/are-our-heat-set-insert-datasheets-wrong)

### SPIROL Series 19/29: recommended hole diameter (moulded or drilled with standard core pins)
- M2 (2-56): 3.20 mm, tolerance +0.08 mm. M2.5 and M3 (4-40, shared row): 3.99 mm. M3.5 (6-32): 4.78 mm. M4 (8-32): 5.61 mm. M5 (10-24/10-32): 6.40 mm. - [SPIROL design guide](https://www.spirol.com/assets/files/ins-threaded-inserts-design-guide-us.pdf) pp. 8-9
- Minimum hole depth = insert length + 2 thread pitches (self-tapping inserts use 1.2 x insert length instead). - [SPIROL design guide](https://www.spirol.com/assets/files/ins-threaded-inserts-design-guide-us.pdf) p. 5, [SPIROL white paper](https://www.spirol.com/assets/files/ins-wp-how-to-design-the-proper-hole-for-heat-ultrasonic-inserts-us.pdf)
- Boss diameter is generally 2-3 x the insert diameter, with the multiple falling as the insert gets bigger. SPIROL gives no numeric minimum wall, only "enough to avoid bulging" during installation. - [SPIROL design guide](https://www.spirol.com/assets/files/ins-threaded-inserts-design-guide-us.pdf) p. 5
- SPIROL heated-tip rule (for its own installation machines, a tuning start point, not a PLA/PETG setpoint): start 28 C above the plastic's initial softening temperature (83 C above for filled plastics); tip pressure 0.03-0.10 MPa (5-15 PSI). - [SPIROL design guide](https://www.spirol.com/assets/files/ins-threaded-inserts-design-guide-us.pdf) p. 15

### PEM IUTB (metric): hole diameter and minimum depth (depth depends on insert length A)
- M2 x 0.4: hole 3.23 mm; min depth 3.94 mm (A = 3.18 mm) or 4.76 mm (A = 4 mm). - [PEM SI data](https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/sidata.pdf) SI-6
- M2.5 x 0.45: hole 4.01 mm; min depth 6.5 mm (A = 5.74 mm). - [PEM SI data](https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/sidata.pdf) SI-6
- M3 x 0.5: hole 4.01 mm; min depth 4.19 mm (A = 3.43 mm) or 6.5 mm (A = 5.74 mm). - [PEM SI data](https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/sidata.pdf) SI-6
- M4 x 0.7: hole 5.67 mm; min depth 5.46 mm (A = 4.7 mm) or 8.91 mm (A = 8.15 mm). - [PEM SI data](https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/sidata.pdf) SI-6
- M5 x 0.8: hole 6.43 mm; min depth 6.48 mm (A = 5.72 mm) or 10.28 mm (A = 9.52 mm). - [PEM SI data](https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/sidata.pdf) SI-6
- General boss rule: boss diameter = 2 x insert diameter; PEM notes thinner walls can be used at a performance cost. - [PEM SI data](https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/sidata.pdf) SI-25
- The microPEM MSIB M2 is a smaller, different insert (outer diameter 3.2 mm vs 3.73 mm for IUTB M2): hole 2.85 mm, min depth 3.77 mm (A = 3 mm) or 4.77 mm (A = 4 mm), minimum boss wall 1.6 mm, tested in ABS/PC. Do not apply that 1.6 mm wall to IUTB-size holes. - [PEM SI data](https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/sidata.pdf) SI-9

### Tappex Multisert Unheaded: hole range C and part sizes
- Tappex calls its hole values suggestions for a range of materials and says they are not meant for production tooling. The insert is a cold press fit in flexible materials, and can also be installed with heat or ultrasonics for better performance. Brochure content is dated 2012; confirm it is current. - [Tappex brochure](https://www.tappex.co.uk/wp-content/uploads/2017/04/Tappex-Brochure-2016.pdf) p. 15
- Hole C: M2 3.0-3.3 mm; M2.5 and M3 3.7-4.0 mm; M4 5.4-5.9 mm; M5 6.0-6.5 mm. Long-part lengths X: M2 6.0 mm, M2.5/M3 7.4 mm, M4 10.9 mm, M5 12.2 mm (full head and wall dimensions in the brochure table). - [Tappex brochure](https://www.tappex.co.uk/wp-content/uploads/2017/04/Tappex-Brochure-2016.pdf) p. 15

### FDM-specific data (community, M3 lead-free inserts only)
- CNC Kitchen (one printer, one PLA) found a 4.2 mm CAD hole the best M3 compromise: the insert pre-seats without a burr underneath at about 90 % of maximum pull strength. The 4.0 mm nominal on the packaging is a reasonable start, and the usable range was 3.6-4.6 mm depending on burr vs strength. - [CNC Kitchen, "Are our heat-set insert datasheets wrong?"](https://www.cnckitchen.com/blog/are-our-heat-set-insert-datasheets-wrong)
- CNC Kitchen rule of thumb: set the soldering iron 10-20 C above the filament's print temperature, about 225 C for PLA, 245 C for PETG, 265 C for ABS. No manufacturer above states a PLA/PETG install temperature; this is community guidance tied to print temperature. - [CNC Kitchen, "Tips and tricks for heat-set inserts"](https://www.cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts)
- CNC Kitchen blind-hole rule: about 1 mm deeper than the insert. SPIROL's rule (length + 2 pitches) gives +1.0 mm for M3 and +1.6 mm for M5, so it adds margin as size grows. - [CNC Kitchen, "Tips and tricks for heat-set inserts"](https://www.cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts), [SPIROL design guide](https://www.spirol.com/assets/files/ins-threaded-inserts-design-guide-us.pdf)
- CNC Kitchen's M3 pull tests used a 240 C iron with insert-specific tips in PLA. That is the test setting, not a general recommendation. - [CNC Kitchen, "Are our heat-set insert datasheets wrong?"](https://www.cnckitchen.com/blog/are-our-heat-set-insert-datasheets-wrong)

## In practice
- Start a printed M3 hole slightly larger than the moulded nominal (SPIROL 3.99 mm, PEM 4.01 mm), for example 4.2 mm, then print a small coupon with a few hole sizes and test-fit before committing a boss design.
- Use SPIROL's depth rule (insert length + 2 thread pitches) as the default; it scales with size, unlike a flat +1 mm.
- Start the iron about 10-20 C above print temperature and confirm by a pull or torque test on your own coupon.
- Do not mix PEM microPEM MSIB figures with IUTB figures; they are different inserts.

## Not verified / open questions
- No manufacturer source states an installation temperature for PLA or PETG.
- The 0.25 mm undersize is from one community test; your printer, nozzle and filament will differ.
- Whether the Tappex brochure is still the current catalogue was not confirmed.
- McMaster-Carr install guidance could not be read (pages returned only script menus), so it is not cited.

Sources:
- https://www.spirol.com/assets/files/ins-threaded-inserts-design-guide-us.pdf - hole table, depth rule, boss rule, heated-tip rule
- https://www.spirol.com/assets/files/ins-wp-how-to-design-the-proper-hole-for-heat-ultrasonic-inserts-us.pdf - depth rule wording
- https://www.pemnet.com/wp-content/uploads/sites/2/2022/06/sidata.pdf - IUTB and MSIB hole/depth tables, boss rule
- https://www.tappex.co.uk/wp-content/uploads/2017/04/Tappex-Brochure-2016.pdf - Multisert hole range and sizes
- https://www.cnckitchen.com/blog/are-our-heat-set-insert-datasheets-wrong - printed-hole undersize, 4.2 mm M3 result, 240 C test setting (community)
- https://www.cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts - iron temperature and blind-hole rules of thumb (community)
