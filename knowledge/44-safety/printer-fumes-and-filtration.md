# Printer fumes and filtration

Applies to: both · Bambu Studio n/a (hardware and SDS facts, not slicer settings)
Verified: 2026-10-04

## Facts

### What the filament SDSs say (paraphrased; read the current SDS yourself)
- Bambu PLA Basic SDS (No. SDS20250724A00, 24 Jul 2025): Section 6 advises avoiding inhalation of aerosol or gas and ensuring adequate ventilation; Section 8 says respiratory protective equipment is not necessary "under normal use conditions" (a phrase the SDS does not define); Sections 9/10 give no data for decomposition temperature or hazardous decomposition products. A later revision may change the wording. — [PLA Basic SDS](https://store.bblcdn.com/s7/default/6e47ce4e48b54b20b3afd3be7539ac27/SDS20250724A00_Bambu_PLA_Basic.pdf)
- Bambu PETG HF (SDS20250724G02, 24 Jul 2025) and Bambu ASA (SDS20251127B01, 27 Nov 2025) SDSs carry the same three positions: ventilate, no respirator needed under normal use, no decomposition data. — [PETG HF SDS](https://store.bblcdn.com/s7/default/859e223a3eeb4aea96dab858e497152b/SDS20250724G02_Bambu_PETG_HF.pdf), [ASA SDS](https://store.bblcdn.com/s7/default/10a896db93e04636a9f70b841867e7e6/SDS20251127B01_Bambu_ASA.pdf)
- Bambu PETG-CF SDS (SDS20260701G50, 1 Jul 2026) has the same text plus a fibre note: tiny fibre debris from use, post-processing or broken surfaces can puncture or irritate skin, so wear gloves when loading, cutting, sanding or post-processing. — [PETG-CF SDS](https://store.bblcdn.com/s7/default/b8ed09c39c5545b19882c05c37b19c96/SDS20260701G50_Bambu_PETG_CF.pdf)

### Store safety notices
- Bambu's US store pages for PLA Basic, PETG HF, PETG-CF and ASA all tell you to print in a well-ventilated area or install effective air filtration or exhaust. — [PLA Basic](https://us.store.bambulab.com/products/pla-basic-filament), [PETG HF](https://us.store.bambulab.com/products/petg-hf), [PETG-CF](https://us.store.bambulab.com/products/petg-cf), [ASA](https://us.store.bambulab.com/products/asa-filament)
- The ASA page's FAQ warns that pungent odours may be released while printing and that the printer should be in a well-ventilated area. — [ASA product page](https://us.store.bambulab.com/products/asa-filament)

### H2C and P1S filtration hardware (marketing copy, no efficiency figure)
- The H2C product page describes a three-stage filter: G3 pre-filter, H12 HEPA filter and coconut-shell activated carbon, said to reduce odours and harmful particles from engineering materials. No efficiency percentage is given. — [bambulab.com/en-us/h2c](https://bambulab.com/en-us/h2c)
- The P1S store FAQ says the P1S has an activated carbon filter for odour-prone filaments such as ABS. No efficiency figure is given. — [P1S store page](https://us.store.bambulab.com/products/p1s)

### Filter replacement intervals
- H2 series air filter (the wiki says the steps are the same for H2S and H2C; H2D is pictured): replace after 1440 hours of printing time (or 60 days) when only the printing function is used. This is the chamber VOC filter; the page does not give separate intervals for the G3 or HEPA stages. — [H2 replace air filter](https://wiki.bambulab.com/en/h2/maintenance/replace-air-filter), [H2 air filter product](https://us.store.bambulab.com/products/air-filter-h2-series)
- X1 series / P1S activated carbon filter: working life 1440 hours (60 days) of cumulative printing time. — [activated carbon filter](https://us.store.bambulab.com/products/activated-carbon-air-filter)

### Standards and independent emission research
- UL 2904 (Edition 2, ANSI-approved 26 May 2023) is a test method for particle and VOC emissions from operating 3D printers in classroom, office and residential scenarios. Neither the H2C nor the P1S page claims UL 2904 testing. — [UL 2904](https://www.shopulstandards.com/ProductDetail.aspx?productId=UL2904)
- Azimi et al., Environ. Sci. Technol. 50(3):1260-1268, 2016 (DOI 10.1021/acs.est.5b04983): five desktop printers (none from Bambu) with up to nine filaments in a test chamber gave median ultrafine-particle emission rates of roughly 10^8 to 10^11 particles per minute, varying mainly by filament and less by bed temperature. These numbers do not carry over to other printers. — [Crossref record](https://api.crossref.org/works/10.1021/acs.est.5b04983), [Europe PMC abstract](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1021/acs.est.5b04983&resultType=core&format=json)
- Same study, same chamber conditions: main VOCs were caprolactam from nylon-based and wood/brick-fill filaments (about 2-180 ug/min), styrene from ABS and HIPS (about 10-110 ug/min) and lactide from PLA (about 4-5 ug/min). The authors urge caution when running many printer/filament combinations in poorly ventilated spaces without combined gas and particle filtration. ASA and PETG were not named in the abstract. — [Europe PMC abstract](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1021/acs.est.5b04983&resultType=core&format=json)
- Chemical Insights (UL Research Institutes): dedicated ventilation (a ventilated enclosure with local exhaust vented outdoors) is credited with 99.7% particle and 69.5% TVOC reduction; filtration systems are separately credited with reducing maximum particle concentration by 95% or more. A separate figure of up to one trillion particles per hour carries no ventilation condition. The underlying studies are not cited inline. — [chemicalinsights.ul.org/3d-printing](https://chemicalinsights.ul.org/3d-printing/)

## In practice
- Treat "not necessary under normal use conditions" on an SDS as a floor, not a ventilation plan; the same maker's store pages tell you to ventilate or filter.
- The H2C and P1S filters recirculate air inside the room. Expect at best filtration-level reduction (95% or more of peak particle concentration per Chemical Insights), not the higher figures that need an enclosure exhausted outdoors.
- Print in a ventilated room, keep people and pets out of long ABS/ASA/nylon runs where you can, and wear gloves when handling carbon- or glass-fibre filament.
- Replace the chamber filter at 1440 hours of printing; whether the H2C's pre-filter and HEPA stages have their own intervals is still open.
- No peer-reviewed emission numbers exist for the H2C or P1S; do not quote Azimi et al. as their numbers.

## Not verified / open questions
- Separate replacement intervals for the H2C's G3 pre-filter and H12 HEPA stages: not found.
- EPA's and NIOSH's 3D-printing pages were not checked.

Sources:
- https://store.bblcdn.com/s7/default/6e47ce4e48b54b20b3afd3be7539ac27/SDS20250724A00_Bambu_PLA_Basic.pdf - PLA Basic SDS
- https://store.bblcdn.com/s7/default/859e223a3eeb4aea96dab858e497152b/SDS20250724G02_Bambu_PETG_HF.pdf - PETG HF SDS
- https://store.bblcdn.com/s7/default/10a896db93e04636a9f70b841867e7e6/SDS20251127B01_Bambu_ASA.pdf - ASA SDS
- https://store.bblcdn.com/s7/default/b8ed09c39c5545b19882c05c37b19c96/SDS20260701G50_Bambu_PETG_CF.pdf - PETG-CF SDS with fibre/glove note
- https://us.store.bambulab.com/products/pla-basic-filament - ventilation notice
- https://us.store.bambulab.com/products/petg-hf - ventilation notice
- https://us.store.bambulab.com/products/petg-cf - ventilation notice
- https://us.store.bambulab.com/products/asa-filament - ventilation notice and odour FAQ
- https://bambulab.com/en-us/h2c - H2C three-stage filtration description
- https://us.store.bambulab.com/products/p1s - P1S activated carbon filter
- https://www.shopulstandards.com/ProductDetail.aspx?productId=UL2904 - UL 2904 scope and edition
- https://api.crossref.org/works/10.1021/acs.est.5b04983 - Azimi et al. 2016 citation
- https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1021/acs.est.5b04983&resultType=core&format=json - Azimi et al. 2016 abstract
- https://chemicalinsights.ul.org/3d-printing/ - ventilation vs filtration figures
- https://wiki.bambulab.com/en/h2/maintenance/replace-air-filter - H2 series filter interval
- https://us.store.bambulab.com/products/air-filter-h2-series - H2 series filter product
- https://us.store.bambulab.com/products/activated-carbon-air-filter - X1/P1S carbon filter working life
