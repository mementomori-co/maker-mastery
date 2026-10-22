# Electrical safety and listing for maker builds

Applies to: both · n/a (electrical code, listing and component-rating facts, not slicer settings)
Verified: 2026-10-04

Scope: low-voltage DC builds (for example a 5-24 V LED or single-board-computer enclosure powered by an external listed power supply). Nothing here covers wiring mains voltage yourself; if a build needs mains wiring inside it, use a listed, enclosed power supply and get qualified help. Part numbers below are examples used to show how to read ratings, not recommendations.

## Facts

### What a listing (NRTL) mark means
- An NRTL mark means a Nationally Recognized Testing Laboratory tested and certified the product to one or more product-safety standards under OSHA's NRTL program. — [OSHA NRTL program](https://www.osha.gov/nationally-recognized-testing-laboratory-program)
- 29 CFR 1910.303(b)(2): listed or labelled equipment must be installed and used per the instructions in its listing or labelling. This is a US workplace rule, not a residential code. — [29 CFR 1910.303](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.303)
- 29 CFR 1910.305(g)(1)(iv)(B),(C): flexible cords may not be run through holes in walls, ceilings or floors, or through doorways and windows, unless (g)(1)(ii) specifically permits it. 1910.305(g)(2)(iii): cords must be connected with strain relief so pull is not transmitted to joints or terminal screws. Workplace rules. — [29 CFR 1910.305](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.305)
- OSHA's electrical overview only asks whether you are working energised, or de-energised but not locked out; it does not itself state a lockout rule. — [OSHA Electrical](https://www.osha.gov/electrical)

### NFPA 70 (NEC) access
- NFPA 70 has a free-access reader, but the article text loads only in a JavaScript viewer. The current edition is NFPA 70, 2026. — [NFPA 70 free access](https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70), [NFPA 70 product page](https://www.nfpa.org/product/nfpa-70-code/p0070code)

### Power-supply standards
- UL 1310 (Edition 7; last revised 2022-06-09) covers Class 2 power supplies and battery chargers: output limited to 42.4 V peak AC or 60 V continuous DC, at Class 2 power levels per NFPA 70. — [UL 1310](https://www.shopulstandards.com/ProductDetail.aspx?productId=UL1310)
- UL 62368-1 (Edition 4, 2025-07-31) covers audio/video, ICT and office equipment rated up to 600 V, including external power supplies intended mainly for such equipment. — [UL 62368-1](https://www.shopulstandards.com/ProductDetail.aspx?productId=UL62368-1)

### UL 94 flammability classes
- The standard is "UL 94, Flammability of Plastic Materials for Parts in Devices and Appliances"; UL Solutions' page gives no HB/V-x criteria. — [UL flammability testing](https://www.ul.com/services/flammability-testing)
- 5VA/5VB uses an ignition flame about five times more severe than the V-0/V-1/V-2/HB tests, and specimens may not drip flaming particles. — [UL Solutions combustion tests](https://www.ul.com/services/combustion-fire-tests-plastics)
- A 5VA rating does not by itself mean V-0: test-lab and supplier sources say the material must already be V-0 or V-1 (one says V-0) before 5V testing. The UL 94 text itself was not read. — [Measurlabs](https://measurlabs.com/products/surface-burning-test-for-plastics-with-500-w-flame-test-method-ul-94/), [Plaskolite](https://plaskolite.com/docs/default-source/tec/tec103_tuf_ul94_flame_ratings.pdf), [Entec Polymers](https://s3.amazonaws.com/entecpolymers.com/v3/uploads/Understanding-UL-94-Flammability-Ratings.pdf)
- UL 94 ratings apply only at the tested thickness: specimens are tested per thickness, and a resin passing at 1.5 mm may fail at 0.74 mm. — [RTP](https://www.rtpcompany.com/technical-info/ul-recognition-and-flammability-ratings/ul94-5va-5vb-flammability-standard/), [Protolabs](https://www.protolabs.com/resources/blog/flame-retardant-thermoplastics-and-ul-classifications/), [Entec Polymers](https://s3.amazonaws.com/entecpolymers.com/v3/uploads/Understanding-UL-94-Flammability-Ratings.pdf)
- Bambu PETG Basic's TDS (V3.0) lists flammability as "Flammable" and gives no UL 94 class. — [PETG Basic TDS](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf)
- Raspberry Pi documentation: the PCBs used in Raspberry Pi devices meet UL94-V0, and this applies to the PCBs only. — [Raspberry Pi compliance doc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/raspberry-pi-compliance.adoc)

### Reading enclosure flammability: examples
- Hammond 1591XX series: standard black and gray versions are flame-retardant ABS rated UL94 V-0; transparent blue and economy versions are general-purpose, not flame retardant. Within the flanged-lid parts, the FL suffix (for example 1591XXUFLBK) is the FR part while the similar 1591XXUSFLBK is general-purpose. Per-part drawings repeat the "FRABS UL 94-V0" note. — [1591XX series PDF](https://www.hammfg.com/electronics/small-case/plastic/1591xx.pdf), [1591XXUFLBK drawing](https://www.hammfg.com/files/parts/pdf/1591XXUFLBK.pdf)
- Hammond's own pages can disagree on dimensions: the 1591XXDFLBK part page gives 46 mm height, but its drawing shows 46.50 mm inside height plus 2.00 mm walls (50.50 mm overall). Use the drawing. — [1591XXDFLBK part page](https://www.hammfg.com/part/1591XXDFLBK), [1591XXDFLBK drawing](https://www.hammfg.com/files/parts/pdf/1591XXDFLBK.pdf)
- Hammond 1554/1555 polycarbonate: solid gray is UL94-5VA, clear and smoked lids are UL94 V-0; polycarbonate versions are cUL/UL 508A listed (Hammond file E65324, not checked on UL's database), ABS versions are not UL listed. Drawings state "5VA @ 3mm". — [1554 series PDF](https://www.hammfg.com/electronics/small-case/plastic/1554.pdf), [1554JL2GY drawing](https://www.hammfg.com/files/parts/pdf/1554JL2GY.pdf)
- Hammond 1557: the series sheet and 1557F2GY drawing say 5VA but the part page says V-0, an unresolved conflict. — [1557 series PDF](https://www.hammfg.com/electronics/small-case/plastic/1557.pdf), [1557F2GY part page](https://www.hammfg.com/part/1557F2GY)
- Bud Industries ratings vary by family: PN series UL94-HB; Utilibox (e.g. CU-3295) 5VA, with small Style H parts (e.g. CU-1474-MB) V-0; Plastibox Style M V-0 and Style I 5VA. No rating was found for Plastibox Styles H and J. — [Bud PN series](https://www.budind.com/product/nema-ip-rated-boxes/pn-series-nema-box/ip65-nema-4x-box-pn-1324/), [CU-3295](https://www.budind.com/product/general-use-boxes/utilibox-style-b-series-utility-boxes-2/cu-3295/), [CU-1474-MB](https://www.budind.com/product/general-use-boxes/utilibox-style-h-series-utility-boxes/cu-1474-mb/), [PT-11852-PXX](https://www.budind.com/product/general-use-boxes/plastibox-style-m-series-plastic-electronic-enclosure/pt-11852-pxx/), [PT-11785](https://www.budind.com/product/general-use-boxes/plastibox-style-i-series-plastic-electronic-enclosure/pt-11785/)

### Limited power source (LPS) and power-source class: Mean Well example
- Mean Well publishes LPS and power-source (PS) class in a separate cross-reference table (revised 2024-04-26), not on the model spec sheets (the GST60A and GST90A sheets contain no "LPS" text). In that table GST60A is ES1/PS2/meets LPS, while GST90A and NGE90 are ES1/PS3/do not meet LPS. — [Mean Well ES/PS/LPS table](https://www.meanwell.com/Upload/PDF/62368%20ES%20PS%20LPS%2061558%20OVC%2060335.pdf), [GST60A spec](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF), [GST90A spec](https://www.meanwell.com/Upload/PDF/GST90A/GST90A-SPEC.PDF)
- In the brick families in that table (GC/GS/GST/GA/NGE), every model of 90 W or more is PS3; none is 24 V, PS2 and at least 75 W. NGE100's PS2 ports are USB (18 W max). Among non-brick models, LPS-75-24 (24 V, 3.2 A, 76.8 W, PS2) and HDR-100-24 (DIN rail, 24 V, 3.83 A, 92 W, PS2) qualify. — [Mean Well table](https://www.meanwell.com/Upload/PDF/62368%20ES%20PS%20LPS%2061558%20OVC%2060335.pdf), [NGE100 spec](https://www.meanwell.com/Upload/PDF/NGE100/NGE100-SPEC.PDF), [LPS-75 spec](https://www.meanwell.com/Upload/PDF/LPS-75/LPS-75-SPEC.PDF), [HDR-100 spec](https://www.meanwell.com/Upload/PDF/HDR-100/HDR-100-SPEC.PDF)
- Protection behaviour differs by fault. GST60A24 (24 V, 2.5 A, 60 W): over-voltage trips at 25.2-32.4 V and latches off until re-powered; overload at 105-150% of rated power enters hiccup mode and recovers by itself. GST90A: overload 110-150% hiccup with auto-recovery; over-voltage (105-135%) and over-temperature both latch until re-powered. The official GST90A sheet's extractable text does not name "short circuit" protection; only a distributor page does. — [GST60A spec](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF), [GST90A spec](https://www.meanwell.com/Upload/PDF/GST90A/GST90A-SPEC.PDF), [distributor page (community)](https://www.meanwell.co.uk/power-supplies/external-power-supplies/gst90a-series)
- Worked example from those numbers: a 24 V, 60 W brick can deliver up to 2.5 A x 32.4 V = 81 W before its over-voltage trip, or about 1.5 x 60 W = 90 W at the top of its overload band, and 32.4 V exceeds a 32 V DC fuse or holder rating. Size fuses and wiring for the protection limits, not just the label rating. — arithmetic from the [GST60A spec](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF)
- GST60A and GST90A use an IEC 320-C14 inlet (needs a C13 cord). — [GST60A spec](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF)

### IEC 62368-1 overcurrent device and power-source timing (third-party sources only)
- A magazine reproduction of IEC 62368-1 Annex Q Table Q.2 says overcurrent devices are rated so they open within 120 s at 210% of their rating, and for a DC source above 20 V and up to 60 V the device rating must be at most 100/Uoc amperes. A supplier blog states the same 210%/120 s rule on an IEC 60950-1 basis. Neither is the standard. — [In Compliance Magazine](https://incompliancemag.com/evaluation-of-intelligent-and-non%E2%80%91static-power-sources-a-rational-clarification/), [Bel Fuse LPS overview](https://www.belfuse.com/resource-library/blog/overview-of-limited-power-source-lps-requirements)
- A third-party UL 62368-1 test report notes that PS1 is measured after 3 s and PS2/PS3 after 5 s. One lab report, not the standard. — [test report hosted on eac.gov](https://www.eac.gov/sites/default/files/2024-08/PRVV0001-R1_UL%2062368-1%202019.pdf)

### IEC 62368-1 fire-enclosure openings (as described by UL Solutions)
- Edition 2: top or side openings inside the fire cone may not exceed 5 mm in any dimension or 1 mm in width, otherwise a needle-flame test applies; no limit on their number or spacing. Bottom openings: 3 mm / 1 mm comply outright; up to 6 mm / 2 mm under parts rated at least V-1 or passing the needle-flame test; or fine metal mesh; or (metal enclosures) Table 34. — [UL Solutions Knowledge Hub (archived)](https://web.archive.org/web/20230629144019id_/https://62368-ul-solutions.com/engineers/what-are-the-rules-for-openings-and-spacings-between-openings-per-of-a-fire-enclosure-in-62368-1/)
- Edition 3 reworked these clauses (new figures, a 5 degree projection rule below the ignition source, mesh and Table 34 options removed). UL Solutions' Ed.3 analysis restates only the 3 mm / 1 mm bottom limit and gives no top/side figure. — [UL Solutions Ed.3 analysis](https://collateral-library-production.s3.amazonaws.com/uploads/asset_file/attachment/56784/62368-1_Ed_3_UL_Analysis_2021-10-22.pdf), [Ed.3 test report form (clause titles)](https://docs.particle.io/assets/pdfs/b523-EN62368-test-report.pdf)

### Fuse derating (Littelfuse)
- At 25 °C ambient, run a fuse continuously at no more than 75% of its rating (a 10 A fuse at no more than 7.5 A). Ambient-temperature rerating applies on top of that. Worked example in the guide: Curve A shows 80% at 75 °C, so a 1.5 A load needs 1.5 / (0.75 x 0.80) = 2.5 A. Curve B (blade, cartridge, leaded fuses) has no readable numbers; the guide says to use the part's datasheet. — [Littelfuse Fuseology Design Guide](https://info.littelfuse.com/hubfs/Fuseology%20Design%20Guide.pdf)
- Littelfuse 157 series (0.062-10 A, 125 V): interrupting rating 50 A at 125 V AC/DC and 300 A at 32 V DC for 0.062-8 A parts; the 10 A part is 35 A at 125 V AC / 50 A at 125 V DC / 300 A at 32 V DC. The fuse body should not exceed 80 °C in a 25 °C ambient. — [Littelfuse 157 datasheet](https://www.farnell.com/datasheets/3762043.pdf)
- The 157 datasheet's ambient re-rating curve, read from its vector drawing, gives about 101% at 25 °C, 99.4% at 40 °C and 97.4% at 60 °C, applied in addition to the 25% continuous-operation derating. Example: at 40 °C a 2 A part carries at most 2 x 0.75 x 0.994 = about 1.49 A continuously. — [Littelfuse 157 datasheet](https://www.farnell.com/datasheets/3762043.pdf)

### Cord and connector ratings
- Flexible-cord ampacity at 30 °C ambient (from a distributor blog citing NEC Table 400.5(A)(1), no edition stated): 16 AWG 10 A (3 current-carrying conductors) / 13 A (2); 14 AWG 15 A / 18 A; 4-6 conductors drop to 80%. Community source; not checked against NFPA 70. — [distributor blog (community)](https://www.distributorwire.com/blogs/soow-so-cord-ampacity-chart-nec-400-5)
- JST XH connectors: 3 A AC/DC with AWG 22 wire, 250 V AC/DC, -25 to +85 °C. Thinner accepted wire (down to AWG 30) implies a lower current, though the page states no figure. — [JST XH series](https://www.jst-mfg.com/product/detail_e.php?series=277)

## In practice
- Power low-voltage builds from a listed external supply (UL 1310 Class 2 or UL 62368-1, ideally a PS2/LPS-class model) and follow its listing instructions. Do not open or modify it.
- OSHA 1910.303/305 are workplace rules; they describe good practice (listed equipment, strain relief, no cords through walls or doorways) but are not "the code" for a home build. Check NFPA 70 and your local code.
- Never call a filament or printed part "UL 94 rated" without a class on its datasheet at the thickness you print. A 3D-printed wall is not covered by someone else's moulded rating, and 5VA alone does not prove V-0.
- Read the exact part number and the drawing: in the same enclosure family one suffix can be flame-retardant and the next not, and part pages can disagree with drawings.
- Fuse every supply output near the source, sized for the continuous-load derating and ambient temperature, with a voltage rating at or above the supply's over-voltage trip; size wire for the fuse, not the load.
- Expect different recovery per fault: overload often auto-recovers (hiccup), over-voltage and over-temperature may latch off until power is cycled.
- Use conservative choices whenever a number here is marked community, third-party or unresolved.

## Not verified / open questions
- NEC Class 2 text, UL 94 test criteria, NEC Table 310.16 and Table 400.5(A)(1) primary text: not read (paywalled or JS-only).
- IEC 62368-1 Annex Q Table Q.2 primary text: not found free; the 210%/120 s and 100/Uoc figures are third-party.
- IEC 62368-1 Ed.3 top/side opening limits: not found.
- Hammond 1557 class conflict, Bud Plastibox Styles H and J ratings, and Hammond's UL file number (not checked on UL's database): unresolved.
- Whether the GST90A's page-1 graphic lists short-circuit protection: not checked.
- Generic Littelfuse Curve B values: not readable.

Sources:
- https://www.osha.gov/nationally-recognized-testing-laboratory-program - what an NRTL mark means
- https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.303 - listed equipment installation
- https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.305 - cord routing and strain relief
- https://www.osha.gov/electrical - OSHA electrical overview
- https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70 - NFPA 70 free access
- https://www.nfpa.org/product/nfpa-70-code/p0070code - NFPA 70 current edition
- https://www.shopulstandards.com/ProductDetail.aspx?productId=UL1310 - UL 1310 scope and limits
- https://www.shopulstandards.com/ProductDetail.aspx?productId=UL62368-1 - UL 62368-1 scope
- https://www.ul.com/services/flammability-testing - UL 94 title
- https://www.ul.com/services/combustion-fire-tests-plastics - 5VA vs V tests
- https://measurlabs.com/products/surface-burning-test-for-plastics-with-500-w-flame-test-method-ul-94/ - 5V prerequisite
- https://plaskolite.com/docs/default-source/tec/tec103_tuf_ul94_flame_ratings.pdf - 5V prerequisite
- https://s3.amazonaws.com/entecpolymers.com/v3/uploads/Understanding-UL-94-Flammability-Ratings.pdf - 5V prerequisite, thickness
- https://www.rtpcompany.com/technical-info/ul-recognition-and-flammability-ratings/ul94-5va-5vb-flammability-standard/ - per-thickness testing
- https://www.protolabs.com/resources/blog/flame-retardant-thermoplastics-and-ul-classifications/ - thickness dependence
- https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf - PETG Basic flammability
- https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/raspberry-pi-compliance.adoc - Raspberry Pi PCB UL94-V0
- https://www.hammfg.com/electronics/small-case/plastic/1591xx.pdf - Hammond 1591XX FR vs general purpose
- https://www.hammfg.com/files/parts/pdf/1591XXUFLBK.pdf - 1591XXUFLBK drawing
- https://www.hammfg.com/part/1591XXDFLBK - 1591XXDFLBK part page
- https://www.hammfg.com/files/parts/pdf/1591XXDFLBK.pdf - 1591XXDFLBK drawing
- https://www.hammfg.com/electronics/small-case/plastic/1554.pdf - Hammond 1554 ratings and listing
- https://www.hammfg.com/files/parts/pdf/1554JL2GY.pdf - 5VA at 3 mm note
- https://www.hammfg.com/electronics/small-case/plastic/1557.pdf - 1557 series rating
- https://www.hammfg.com/part/1557F2GY - 1557F2GY part page rating
- https://www.budind.com/product/nema-ip-rated-boxes/pn-series-nema-box/ip65-nema-4x-box-pn-1324/ - Bud PN HB
- https://www.budind.com/product/general-use-boxes/utilibox-style-b-series-utility-boxes-2/cu-3295/ - Bud Utilibox 5VA
- https://www.budind.com/product/general-use-boxes/utilibox-style-h-series-utility-boxes/cu-1474-mb/ - Bud Utilibox Style H V-0
- https://www.budind.com/product/general-use-boxes/plastibox-style-m-series-plastic-electronic-enclosure/pt-11852-pxx/ - Bud Plastibox Style M V-0
- https://www.budind.com/product/general-use-boxes/plastibox-style-i-series-plastic-electronic-enclosure/pt-11785/ - Bud Plastibox Style I 5VA
- https://www.meanwell.com/Upload/PDF/62368%20ES%20PS%20LPS%2061558%20OVC%2060335.pdf - Mean Well ES/PS/LPS table
- https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF - GST60A protections and inlet
- https://www.meanwell.com/Upload/PDF/GST90A/GST90A-SPEC.PDF - GST90A protections
- https://www.meanwell.com/Upload/PDF/NGE100/NGE100-SPEC.PDF - NGE100 ports
- https://www.meanwell.com/Upload/PDF/LPS-75/LPS-75-SPEC.PDF - LPS-75-24
- https://www.meanwell.com/Upload/PDF/HDR-100/HDR-100-SPEC.PDF - HDR-100-24
- https://www.meanwell.co.uk/power-supplies/external-power-supplies/gst90a-series - distributor page (community)
- https://incompliancemag.com/evaluation-of-intelligent-and-non%E2%80%91static-power-sources-a-rational-clarification/ - Table Q.2 reproduction
- https://www.belfuse.com/resource-library/blog/overview-of-limited-power-source-lps-requirements - LPS overview
- https://www.eac.gov/sites/default/files/2024-08/PRVV0001-R1_UL%2062368-1%202019.pdf - PS measurement timing (lab report)
- https://web.archive.org/web/20230629144019id_/https://62368-ul-solutions.com/engineers/what-are-the-rules-for-openings-and-spacings-between-openings-per-of-a-fire-enclosure-in-62368-1/ - Ed.2 opening limits
- https://collateral-library-production.s3.amazonaws.com/uploads/asset_file/attachment/56784/62368-1_Ed_3_UL_Analysis_2021-10-22.pdf - Ed.3 changes
- https://docs.particle.io/assets/pdfs/b523-EN62368-test-report.pdf - Ed.3 clause titles
- https://info.littelfuse.com/hubfs/Fuseology%20Design%20Guide.pdf - fuse derating
- https://www.farnell.com/datasheets/3762043.pdf - Littelfuse 157 series
- https://www.distributorwire.com/blogs/soow-so-cord-ampacity-chart-nec-400-5 - cord ampacity (community)
- https://www.jst-mfg.com/product/detail_e.php?series=277 - JST XH ratings
