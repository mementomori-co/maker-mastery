# H2 laser modules: kits, compatibility, software path and laser safety

Applies to: H2-series printers (H2C, H2D, H2S) · Bambu Suite · firmware "latest" (the sources give no version number)
Verified: 2026-10-04

## Facts

### Compatibility and kits
- Laser modules work only on the H2 Laser version; an existing H2 printer needs the Laser Upgrade Kit, sold as "For H2D/H2C" or "For H2S". The H2S takes the 10 W laser only; H2D/H2C take 10 W and 40 W. - [Bambu Lab Laser Upgrade Kit store page](https://us.store.bambulab.com/products/laser-upgrade-kit)
- Prices when checked (US store, a sale banner was showing): H2D/H2C kit USD 698.00 on the type selector (the page does not say which wattage; no 40 W kit price was shown); H2S kit USD 638.00. - [Laser Upgrade Kit store page](https://us.store.bambulab.com/products/laser-upgrade-kit)

### Kit contents
- H2D/H2C 10 W kit: 21 numbered items, including 2x sealing sticker, a cable organizer and the 10 W module. The 40 W kit has the same 21 items with a 40 W module. - [Laser Upgrade Kit store page](https://us.store.bambulab.com/products/laser-upgrade-kit)
- H2S 10 W kit: 16 items; only a front safety window, no sealing sticker, no cable organizer. Module-only SKUs: module, laser lens, user manual. - [Laser Upgrade Kit store page](https://us.store.bambulab.com/products/laser-upgrade-kit)

### 10 W vs 40 W (store FAQ, basswood)
- Maximum cutting thickness 6 mm vs 15 mm; maximum engraving speed 400 vs 1000 mm/s; working area 310 x 270 mm with 280 mm height vs 310 x 250 mm with 265 mm height. - [Laser Upgrade Kit store page](https://us.store.bambulab.com/products/laser-upgrade-kit)
- The wiki's 10 W spec table gives 5 mm maximum cutting thickness (basswood plywood), against the store's 6 mm. - [wiki: H2 laser safety document](https://wiki.bambulab.com/en/h2/laser-safety-document)

### Safety class and interlocks
- The laser module is Class 4; the printer system with the module is Class 1 (store and wiki tables agree, the wiki for the 10 W module). The wiki says Class 1 holds only when the printer's protection is complete and working. - [Laser Upgrade Kit store page](https://us.store.bambulab.com/products/laser-upgrade-kit), [wiki: H2 laser safety document](https://wiki.bambulab.com/en/h2/laser-safety-document)
- The module runs in a closed casing with interlocks and stops if the front door, top glass cover or safety window is opened. - [wiki: H2 laser safety document](https://wiki.bambulab.com/en/h2/laser-safety-document)
- Further protections: flame sensor, vision and temperature detection trigger a buzzer; drop or communication loss shuts the laser off; opening the door shuts it off immediately. The text names the H2D but sits in the shared `/en/h2/` pages. - [wiki: H2 laser FAQ](https://wiki.bambulab.com/en/h2/manual/laser-faq)
- The 10 W spec table lists flame detection, temperature detection, door sensor and module installation detection as supported. - [wiki: H2 laser safety document](https://wiki.bambulab.com/en/h2/laser-safety-document)

### Ventilation
- Install and secure the smoke exhaust system (pipe adapter, pipe and related parts); if smoke or an unusual odour appears, check it at once. All exhaust must be filtered by an air purifier or discharged outdoors. - [wiki: H2 laser safety document](https://wiki.bambulab.com/en/h2/laser-safety-document), [wiki: H2 laser important info](https://wiki.bambulab.com/en/h2/manual/imp-info-laser)
- Smoke Purifier: USD 599.00 when checked; filters 99 % of particles down to 0.3 um plus VOCs; compatible with H2 Laser and R1; ships with a 2 m pipe, a clamp and primary, medium and high-efficiency filters. - [Bambu Lab Smoke Purifier store page](https://us.store.bambulab.com/products/smoke-purifier)

### Materials
- Do not engrave or cut materials that can release harmful gases, such as PVC, or materials of unknown composition. - [wiki: H2 laser safety document](https://wiki.bambulab.com/en/h2/laser-safety-document)
- Heat transfer vinyl, PVC adhesive sticker and PVC sheet are marked not processable by laser engrave or cut; PVC sheet may be blade-cut only up to 0.3 mm, with heavy blade wear. The list is "for reference only". - [wiki: processable materials list](https://wiki.bambulab.com/en/h2/laser/processable-materials-list)

### Standards and labels
- The wiki defines the Laser Safety Officer (LSO) and deputy (DLSO), and cites EN 60825-1:2014+A11:2021, IEC 60825-1:2014, ANSI Z136.1-2022 and GB 7247.1-2012. - [wiki: H2 laser safety document](https://wiki.bambulab.com/en/h2/laser-safety-document)
- The compliance section publishes Class 4 label text for the 10 W module: 10 W maximum output, 455 nm and 850 nm wavelengths, and a 21 CFR 1040.10/1040.11 compliance statement citing Laser Notice No. 56. Where the label sits on the printer is still "(To be updated)"; no 40 W label text is published. - [wiki: H2 laser safety document](https://wiki.bambulab.com/en/h2/laser-safety-document)
- 21 CFR 1040.10(b): a Class I product does not permit access during operation to radiation above the Table I limits; a Class IV product permits access above the Table III-B limits. - [eCFR 21 CFR 1040.10](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-J/part-1040/section-1040.10)
- OSHA: some lasers can damage the eye and skin, and the eye is almost always more vulnerable than skin. OSHA's standards page names ANSI Z136.1 and the Laser Institute of America as the Z136 secretariat. - [OSHA laser hazards](https://www.osha.gov/laser-hazards), [OSHA laser standards](https://www.osha.gov/laser-hazards/standards), [Laser Institute of America](https://www.lia.org/)

### Software path
- Setup needs Bambu Suite and the latest firmware: bind the printer in Bambu Handy by QR code, then log in to Bambu Suite on the computer. - [wiki: H2 laser setup](https://wiki.bambulab.com/en/h2/manual/laser-setup)
- Bambu Suite 2D processing types: Laser line, Laser fill, Laser cut, Laser image, Basic cut, Drawing line, Drawing fill, Print then cut. Importing a bitmap limits you to "Laser image" and "Print then cut". - [wiki: 2D processing types](https://wiki.bambulab.com/en/software/bambu-suite/manual/2d-processing-type-intro)

## In practice
- An H2C takes the "For H2D/H2C" kit in 10 W or 40 W; 40 W cuts thicker and engraves faster in a slightly smaller envelope.
- Class 1 depends on the enclosure, door, top glass, windows and interlocks being intact. Never defeat them.
- Set up exhaust (outdoors, or a purifier) before the first laser job; treat smoke or odour as a stop signal.
- Never laser PVC, vinyl or PVC stickers.
- Laser jobs run in Bambu Suite, not Bambu Studio. As with prints, the maker starts every laser job; the AI does not.
- For general fume guidance see [printer-fumes-and-filtration.md](../44-safety/printer-fumes-and-filtration.md).

## Not verified / open questions
- Whether H2 firmware blocks Developer Mode while laser or cutting functions are in use: not verified (no public source).
- 10 W basswood cutting thickness: 5 mm (wiki) vs 6 mm (store); treat it as 5-6 mm.
- Store prices change; the wattage behind the USD 698 price is not stated.

Sources:
- https://us.store.bambulab.com/products/laser-upgrade-kit - compatibility, contents, prices, 10 W vs 40 W, safety class
- https://us.store.bambulab.com/products/smoke-purifier - Smoke Purifier spec and price
- https://wiki.bambulab.com/en/h2/laser-safety-document - safety class, interlocks, ventilation, LSO, standards, label text, 10 W table
- https://wiki.bambulab.com/en/h2/manual/laser-faq - detection and shut-off protections
- https://wiki.bambulab.com/en/h2/manual/imp-info-laser - exhaust guidance
- https://wiki.bambulab.com/en/h2/laser/processable-materials-list - PVC and vinyl restrictions
- https://wiki.bambulab.com/en/h2/manual/laser-setup - setup flow
- https://wiki.bambulab.com/en/software/bambu-suite/manual/2d-processing-type-intro - processing types
- https://www.ecfr.gov/current/title-21/chapter-I/subchapter-J/part-1040/section-1040.10 - Class I and Class IV definitions
- https://www.osha.gov/laser-hazards - eye and skin hazard
- https://www.osha.gov/laser-hazards/standards - ANSI Z136.1, LIA
- https://www.lia.org/ - LIA as Z136 secretariat
