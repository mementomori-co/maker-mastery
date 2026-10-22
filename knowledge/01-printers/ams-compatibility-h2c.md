# AMS compatibility on the H2C (first-gen AMS, lower/left inlet)
Applies to: H2C · H2C User Manual V1.0 2026.01 · firmware up to 01.02.00.00 (20260601)
Verified: 2026-10-05

**Answer line:** first-gen AMS supported on the H2C: yes. Supported on the lower (left) inlet: not stated by any official page.

## Facts
- The first-gen AMS is plug-and-play with the H2C and supports multi-color printing but not drying (manual section 2.9 NOTE, printed p.36). - [H2C User Manual V1.0](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf)
- The AMS lite is not compatible with the H2C (different loading mechanism and buffer structure; manual section 2.9 NOTE). The wiki says the AMS lite is only for A-series printers. - [H2C User Manual V1.0](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf), [AMS multi-model guide](https://wiki.bambulab.com/en/ams/manual/multi-model-AMS-compatibility-guide)
- Inlet to hotend: upper inlet = right hotend, lower inlet = left hotend (manual section 2.4.1 TIPS; section 1.2 item 8 "Chamber Filament Inlet (Hotend - Left)"). - [H2C User Manual V1.0](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf)
- Bambu recommends 2 AMS units on the right hotend and 1 on the left (manual section 2.9, AMS type not stated). Every left-inlet example uses an AMS HT (section 2.9.2 Step 3; the H2C FAQ describes two AMS 2 Pro feeding the right induction hotends and an AMS HT feeding the left). - [H2C User Manual V1.0](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf), [H2C FAQ](https://bambulab.com/en-us/h2c/faq)
- The AMS Setup left/right flow (section 2.4.1) is worded for the AMS 2 Pro only; it says nothing about a first-gen AMS. - [H2C User Manual V1.0](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf)
- Unit limits name only the AMS 2 Pro and AMS HT: up to 4 AMS 2 Pro + 8 AMS HT at once, 24 slots total (manual Ch.6 NOTE, section 2.9.2 TIPS; wiki H2-series guide). How a first-gen AMS counts against this limit is not stated. - [H2C User Manual V1.0](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf), [AMS multi-model guide](https://wiki.bambulab.com/en/ams/manual/multi-model-AMS-compatibility-guide)
- Cabling is 6-pin Bambu Bus. For an AMS 2 Pro or AMS HT use the included new-version 6-pin cable (step height 2.5 mm); the older cable has a 1.1 mm step and "may cause unstable communication" with an AMS 2 Pro/HT. The first-gen AMS is compatible with the new-version cable. - [AMS multi-model guide](https://wiki.bambulab.com/en/ams/manual/multi-model-AMS-compatibility-guide)
- The AMS connects to the printer's 6-pin Bambu Bus port (section 1.2 item 6); the 4-pin port is for expansion accessories (item 10). - [H2C User Manual V1.0](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf)
- The filament buffer is built into the H2D/H2C; no AMS Hub is needed (the Hub is listed only for X1/P1 multi-AMS). 1 AMS + an external spool, or 2 AMS units, connect directly to the buffer's two inlet ports; 2 AMS + a spool, or 3 or more AMS units, need the H2-series 4-in-1 PTFE Adapter. - [AMS multi-model guide](https://wiki.bambulab.com/en/ams/manual/multi-model-AMS-compatibility-guide)
- PTFE: the tube shipped with the printer is 900 mm; when an AMS 2 Pro / AMS HT sits on top of the printer it may be shortened to no less than 600 mm (generic guidance, not first-gen specific). Manual section 2.9.2 also uses the shortest tube (185 mm) from the accessory box. - [H2C connect-AMS wiki](https://wiki.bambulab.com/en/h2c/how-to-connect-ams), [H2C User Manual V1.0](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf)
- Drying needs an AMS 2 Pro or AMS HT on the 6-pin cable; offline drying mode is not supported. - [AMS multi-model guide](https://wiki.bambulab.com/en/ams/manual/multi-model-AMS-compatibility-guide)
- Left-hotend filament limits: the manual says use the right hotend for specific TPU types and the left hotend for PPS/PPA-CF/PET-CF; TPU 85A is not supported on the left hotend (manual section 8.2 CAUTION, clogging risk). - [H2C User Manual V1.0](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf)
- Correction to the manual's "TPU on the right": firmware 01.02.00.00 (20260601) added left-nozzle TPU printing for TPU of hardness 90A or higher. TPU 85A stays right-hotend only. - [H2C firmware release history](https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history)
- The H2C firmware release history (01.01.00.00 to 01.02.00.00) never mentions the first-gen AMS. - [H2C firmware release history](https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history)
- The wiki FAQ on printing with AMS and AMS 2 Pro at the same time answers yes for X1/P1/H2D/H2S; the H2C is not listed. The A1 section of the multi-model guide explicitly allows mixing AMS, AMS 2 Pro and AMS HT (A1 firmware 01.07.00.00 or later). - [AMS 2 Pro / AMS HT FAQ](https://wiki.bambulab.com/en/ams/manual/ams-2-pro-ams-ht-faq), [AMS multi-model guide](https://wiki.bambulab.com/en/ams/manual/multi-model-AMS-compatibility-guide)
- The H2C wiki multi-AMS guide covers only the AMS 2 Pro and AMS HT and says multiple AMS units can connect to the right hotend. - [H2C connect-AMS wiki](https://wiki.bambulab.com/en/h2c/how-to-connect-ams)
- Without a Filament Track Switch each nozzle is locked to one AMS: left nozzle only the left AMS, right nozzle only the right AMS. The switch guide is written for 2 x AMS 2 Pro; it needs H2C firmware 01.01.50.00 beta or later and Bambu Studio 2.5.3.60 or later. - [Filament Track Switch guide](https://wiki.bambulab.com/en/general/manual/filament-track-switch-h2)
- The H2D store FAQ (H2D only; embedded page data, rendering not confirmed) says the first-gen AMS is fully plug-and-play with the H2D and cannot dry. It says nothing about the H2C. - [H2C store page](https://us.store.bambulab.com/products/h2c)
- Community (not official), one forum thread, no staff post, nobody reports first-hand first-gen AMS use on the left inlet: one user runs a first-gen AMS + AMS 2 Pro on the right nozzle and an AMS HT on the left and finds first-gen load time negligible; another notes that with the Track Switch the first-gen AMS retracts all the way back; another sees no difference mixing generations except that the first-gen AMS cannot dry. - [Bambu forum, AMS1 on H2C](https://forum.bambulab.com/t/ams1-on-h2c/213122) (community)

## In practice
Checklist before putting a first-gen AMS on the lower (left) inlet:
1. Cable: new-version 6-pin cable (2.5 mm step, from an AMS 2 Pro or AMS HT) on every link, into the printer's 6-pin port, not the 4-pin port.
2. Firmware: no documented minimum; update to the newest, then confirm on the touchscreen that the first-gen AMS is detected and assigned to the left hotend (AMS Setup is documented for AMS 2 Pro only). Verify on your own printer.
3. Drying: the first-gen AMS cannot dry on the H2C; dry its filament elsewhere.
4. Filament types on the left hotend: TPU 85A not supported; TPU 90A or harder only on firmware 01.02.00.00 or later; PPS-CF, PPA-CF, PET-CF belong on the left. Whether the first-gen AMS itself can feed a given material (TPU included) was not checked.
5. Tubing: PTFE from the AMS to the lower coupler, 900 mm cut down to no less than 600 mm; one AMS per inlet needs no 4-in-1 adapter; without a Track Switch the left nozzle uses only the left AMS's filaments.

## Not verified / open questions
- Official first-gen AMS support on the lower/left inlet specifically: not stated either way (manual V1.0, wiki multi-model guide, connect-AMS wiki, AMS FAQ, Track Switch guide, firmware history, store page and H2C FAQ all searched).
- How AMS Setup (manual section 2.4.1) handles a first-gen AMS: documented for the AMS 2 Pro only.
- A minimum H2C firmware for the first-gen AMS: not in the release history.
- How a first-gen AMS counts against the "4 AMS 2 Pro + 8 AMS HT" limit: not stated.
- Whether the first-gen AMS can feed a given material (TPU included): not checked.
- A search-engine snippet claiming the H2C works with the original AMS in combination with AMS 2 Pro and AMS HT does not appear on the H2C FAQ page; treat it as unsourced.

Sources:
- https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf - H2C User Manual V1.0 2026.01: first-gen AMS plug-and-play, no AMS lite, inlet mapping, 6-pin port, unit limits, TPU 85A
- https://wiki.bambulab.com/en/ams/manual/multi-model-AMS-compatibility-guide - cable generations, buffer, 4-in-1 adapter, drying, H2-series limits
- https://wiki.bambulab.com/en/ams/manual/ams-2-pro-ams-ht-faq - mixing-generations FAQ omits the H2C
- https://wiki.bambulab.com/en/h2c/how-to-connect-ams - PTFE 900/600 mm; guide covers AMS 2 Pro and AMS HT only
- https://wiki.bambulab.com/en/h2c/manual/h2c-firmware-release-history - left-nozzle TPU 90A+ from 01.02.00.00; no first-gen AMS mention
- https://wiki.bambulab.com/en/general/manual/filament-track-switch-h2 - nozzle locked to its AMS without the switch
- https://us.store.bambulab.com/products/h2c - H2D first-gen AMS FAQ (H2D only)
- https://bambulab.com/en-us/h2c/faq - left hotend fed by AMS HT; no first-gen AMS mention
- https://forum.bambulab.com/t/ams1-on-h2c/213122 - community reports only
