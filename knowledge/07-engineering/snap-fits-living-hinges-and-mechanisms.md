# Snap fits, living hinges and mechanisms: design-guide rules and equations (with the FDM caveat)

Applies to: any FDM printer (design-stage fact) - Bambu PLA Basic and PETG Basic inputs from TDS V3.0 - Bambu Studio 02.08.02.61
Verified: 2026-10-04

## Facts

### Scope caveat
- The four classic guides below (BASF, Bayer/Covestro, DuPont, LyondellBasell) are injection-moulding guides; a text search found no mention of FDM, 3D printing, PLA or PETG in any of them. Every rule here needs a printed test coupon before it carries load. - [BASF manual](https://web.archive.org/web/20151030052517id_/http://www2.basf.us//PLASTICSWEB/displayanyfile?id=0901a5e1801499d5), [Bayer/Covestro guide](https://fab.cba.mit.edu/classes/S62.12/people/vernelle.noel/Plastic_Snap_fit_design.pdf), [DuPont Module I](https://web.archive.org/web/20111111182616id_/http://plastics.dupont.com:80/plastics/pdflit/americas/general/H76838.pdf), [LyondellBasell guide](https://web.archive.org/web/20240606131904id_/https://www.lyondellbasell.com/globalassets/documents/polymers-technical-literature/a-guide-to-polyolefin-injection-molding.pdf)

### BASF Snap-Fit Design Manual (2007; vendor URLs are gone, read via the Internet Archive)
- Cantilever snaps are the usual choice for engineering plastics; cylindrical snaps suit unfilled, high-elongation plastics; U- and L-shaped cantilevers are used when a straight beam cannot be kept under the allowable strain. - [BASF manual](https://web.archive.org/web/20151030052517id_/http://www2.basf.us//PLASTICSWEB/displayanyfile?id=0901a5e1801499d5) p. 7
- A gentle entrance angle eases assembly; a steep retraction angle resists disassembly. BASF gives no single recommended value; its worked example uses 30 deg. - same source pp. 8, 15
- Assembly deflection equals the overhang depth; beam force P = kY (k = stiffness, Y = deflection). - same source pp. 8-9
- Stiffness and strain by beam shape (E flexural modulus, b width, t thickness, L length): uniform k = (Eb/4)(t/L)^3, strain = 1.50 Yt/L^2; thickness tapered to t/2 k = (Eb/6.528)(t/L)^3, strain = 0.92 Yt/L^2; width tapered to b/4 k = (Eb/5.136)(t/L)^3, strain = 1.17 Yt/L^2. Read from the PDF text layer. - same source p. 9
- Plain cantilever formulas underestimate strain because they ignore wall deformation at the root; they hold only when L/t is above about 10. Below that, apply BASF's Q (deflection magnification) factor from its L/t chart. - same source p. 11
- Corrected equations: strain = 1.5 tY/(L^2 Q); P = b t^2 E strain/(6L); mating force W = P(mu + tan a)/(1 - mu tan a), with mu the friction coefficient and a the lead angle (use the return angle for separation). - same source p. 14
- Worked example (PBT, t 3 mm, L 15 mm, b 6 mm, E 4830 MPa, mu 0.3, a 30 deg, allowable strain 2.5 %): L/t 5.0 gives Q 2.07, Ymax 2.59 mm, P 72.45 N, W 76.9 N. BASF advises choosing a smaller real deflection for safety. - same source p. 15
- Allowable-strain table: the table numbers in the body text are swapped; Table IV-I is allowable strain and Table IV-II is friction (confirmed by page layout and BASF's own example). Most allowable strains are 70 % of tensile yield strain (for example PC 4 %, acetal 7 %, PET 1.5 %). - same source pp. 14-15
- Hygroscopic plastics: check both dry-as-moulded and 50 % RH property values. - same source p. 9
- Root fillet: a sharp corner at the beam root is the most common snap-fit failure cause; keep root radius / wall thickness at 0.5 or more. Larger gains little. - same source p. 20
- A 90 deg return angle lets the snap relax in tension rather than bending after assembly. - same source p. 20
- Fatigue design (S-N curve) matters only when hundreds or thousands of cycles are expected. - same source p. 21

### Bayer/Covestro "Snap-Fit Joints for Plastics" (2005; read via an MIT Fab Lab mirror)
- Four snap types: cantilever, U-shaped, torsion, annular. - [Bayer/Covestro guide](https://fab.cba.mit.edu/classes/S62.12/people/vernelle.noel/Plastic_Snap_fit_design.pdf) p. 4
- Tapering the arm (thickness to half at the hook, or width to a quarter) allows more than 60 % more deflection than a constant arm of the same material; a constant arm sized for equal strain uses 17 % more material. - same source pp. 2, 8, 12
- Root radius should never be below 0.381 mm (0.015 in), per Bayer's internal testing; very large radii make the root too thick, so choose a compromise. - same source p. 8
- Permissible strain: partially crystalline plastics can go almost to yield; amorphous plastics to about 70 % of yield strain. Snap-joint permissible strain is roughly half the elongation at break. For frequent re-assembly use about 60 % of the single-use deflection. - same source pp. 11-12
- Friction coefficients (plastic on steel): PP 0.25-0.30, POM 0.20-0.35, PA 0.30-0.40, PC 0.45-0.55, ABS 0.50-0.65, PBT 0.35-0.40; same-material pairs are generally higher. No PLA or PETG row. - same source pp. 14-15
- Above the proportional limit use the strain-dependent secant modulus instead of the elastic modulus. - same source p. 7
- Torsion snaps: shear strain about 1.35 x tensile strain (Poisson's ratio about 0.35). Annular snaps: undercut limited by strain x diameter; self-releasing above a clearance of 1.8 sqrt(d t); tests rarely exceed 3 x the cantilever mating force although theory predicts 4 x. - same source pp. 18-22

### DuPont "General Design Principles", Module I (2000; read via the Internet Archive)
- Cylindrical snaps are generally stronger than cantilever lugs but need more assembly force. - [DuPont Module I](https://web.archive.org/web/20111111182616id_/http://plastics.dupont.com:80/plastics/pdflit/americas/general/H76838.pdf) PDF p. 76
- Cylindrical snap: a 45 deg return bevel suits most uses; 90 deg makes a permanent joint; a 30 deg lead-in eases entry; the undercut should be circular, and rectangular snaps are said not to work well. - same source PDF p. 77
- Cantilever lug: aim for constant stress along the beam (taper or rib); stress S = FLc/I, deflection y = FL^3/3EI. - same source PDF pp. 79-80
- Allowable strain per material, used once vs used often (for example Delrin 100: 8 % vs 2-4 %; Hytrel: 20 % vs 10 %). - same source PDF p. 79
- Module I has no living-hinge section. - same source

### LyondellBasell polyolefin moulding guide (PP living hinges; 2015, read via the Internet Archive)
- Normal hinge thickness 0.2-0.38 mm (0.008-0.015 in); thicker for a load-carrying hinge. - [LyondellBasell guide](https://web.archive.org/web/20240606131904id_/https://www.lyondellbasell.com/globalassets/documents/polymers-technical-literature/a-guide-to-polyolefin-injection-molding.pdf) p. 33
- Well designed and moulded hinges have lasted more than a million cycles. - same source
- Provide a shallow relief at the hinge so material does not bunch up when closed; run flow straight across the hinge and keep weld lines out of it. - same source
- Flex the hinge several times right after moulding; homopolymer PP hinges best, then random copolymer, then impact copolymer (delamination risk). All of this is moulded PP, not FDM. - same source

### Bambu PLA Basic and PETG Basic: inputs for the beam equations (TDS V3.0)
- PLA Basic (specimens annealed and dried 55 C for 8 h, 100 % infill): bending modulus X-Y 2750 MPa, Z 2370 MPa; elongation at break X-Y 12.2 %, Z 7.5 %. - [Bambu PLA Basic TDS](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf) pp. 3-4
- PETG Basic (printed, not annealed; 255 C nozzle, 100 % infill; Bambu advises against annealing PETG Basic): bending modulus X-Y 1950 MPa, Z 1740 MPa; elongation at break X-Y 9.5 %, Z 5.2 %. - [Bambu PETG Basic TDS](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf) pp. 3-4
- Both sheets say the values come from Bambu's standard samples and are for design reference and comparison only. - same two TDS, p. 5

### Bambu Studio tolerance tools
- XY Hole Compensation changes only hole size (diameter grows by twice the entered value), XY Contour Compensation changes the outer contour; both are filament-specific and apply to closed paths only. Over-compensation can show as layer separation at the hole. - [Bambu wiki: XY hole/contour compensation](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation)
- Auto Circle Holes-contour Compensation handles only full horizontal circles up to 50 mm, only with some Bambu filaments; dry filament fits looser than moist; positive offset = looser; tune in 0.02 mm steps. - [Bambu wiki: Auto Circle compensation](https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation)
- The Cut tool wiki lists Plug, Dowel and Snap connectors; the source at tag v02.08.02.61 also has Thread. Snap defaults in code: gap proportion 0.3, bulge proportion 0.15. See [keyed-joints-and-connectors.md](keyed-joints-and-connectors.md). - [Bambu wiki: Cut tool](https://wiki.bambulab.com/en/software/bambu-studio/cut-tool), [GLGizmoAdvancedCut.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp), [Model.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.hpp)

### Other-vendor data point (Prusa)
- Prusa suggests at least 0.3 mm clearance as a first try for moving parts, and orienting structural parts for strength because FFF prints are anisotropic. Prusa printers, not Bambu. - [Prusa: Modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)

## In practice
- For short printed snap arms (L/t below about 10) use BASF's Q-corrected equations; the plain P = kY formula underestimates strain.
- Use the TDS bending modulus as E and about half the elongation at break as the permissible-strain ceiling (Bayer rule), then prove it with a coupon. Orient arms so they bend in the X-Y plane; Z values are lower.
- Root fillet at least 0.5 x wall thickness and never below about 0.4 mm; lead-in about 30 deg; return 90 deg for permanent joints, 45 deg for releasable cylindrical snaps.
- Start moving-part clearance at about 0.3 mm and tune with XY Hole / Contour or Auto Circle compensation rather than editing CAD blind.
- PP living-hinge numbers (0.2-0.38 mm) are moulding rules; a printed hinge needs its own coupon and a flexible filament.

## Not verified / open questions
- BASF's beam-coefficient figure was checked against the PDF text layer only, not the rendered figure.
- No Bambu wiki page on snap, hinge or clearance design was found (URL-slug search only).
- Which of two connector-default structs in `Model.hpp` the GUI reads was not traced.
- None of the moulding-guide numbers has been confirmed on a printed part.

Sources:
- https://web.archive.org/web/20151030052517id_/http://www2.basf.us//PLASTICSWEB/displayanyfile?id=0901a5e1801499d5 - BASF Snap-Fit Design Manual
- https://fab.cba.mit.edu/classes/S62.12/people/vernelle.noel/Plastic_Snap_fit_design.pdf - Bayer/Covestro Snap-Fit Joints for Plastics
- https://web.archive.org/web/20111111182616id_/http://plastics.dupont.com:80/plastics/pdflit/americas/general/H76838.pdf - DuPont General Design Principles, Module I
- https://web.archive.org/web/20240606131904id_/https://www.lyondellbasell.com/globalassets/documents/polymers-technical-literature/a-guide-to-polyolefin-injection-molding.pdf - LyondellBasell PP living hinges
- https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf - PLA Basic TDS V3.0
- https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf - PETG Basic TDS V3.0
- https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation - XY hole/contour compensation
- https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation - Auto Circle compensation
- https://wiki.bambulab.com/en/software/bambu-studio/cut-tool - Cut tool connectors
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp - Thread connector in code
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.hpp - connector defaults
- https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135 - 0.3 mm clearance, anisotropy (other vendor)
