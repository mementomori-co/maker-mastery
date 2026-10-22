# H2C cooling mode and automatic vent (PLA), versus the P1S
Applies to: H2C (P1S rows labelled) · Bambu Studio 02.08.02.61 (profiles at tag v02.08.02.61) · H2C manual V1.0 2026.01
Verified: 2026-10-05

## Facts

### What the H2C does for PLA
- Cooling mode is meant for low-heat-resistance filaments such as PLA/TPU; in this mode the Chamber Heat Circulation Fan stays off and the Filter Switch Flap is positioned downward. - [Bambu wiki, H2 cooling fan system](https://wiki.bambulab.com/en/h2/manual/cooling-fan-system)
- When the Chamber Exhaust Fan runs, the Automatic Top Vent and the Active Chamber Exhaust Grille at the back open automatically to control chamber temperature or airflow. The vent opens only while the exhaust fan runs; in cooling mode, when the fan is off, the grille closes. For PLA the exhaust fan slows to 30 % (PETG 0 %) when the chamber is cool, so for PLA it does not stop at 0 % (inference: the vent then stays open; the page does not say so outright). - [Bambu wiki, H2 cooling fan system](https://wiki.bambulab.com/en/h2/manual/cooling-fan-system)
- The H2 page never names the H2C, but the H2C's own pages confirm the same vent behaviour, and say the printer is in cooling mode whenever chamber heating is not active. Manual p.13 section 1.2.1 describes the Automatic Top Vent and rear exhaust opening to bring in cool air and expel hot air. - [Bambu wiki, H2C intro](https://wiki.bambulab.com/en/h2c/manual/h2c-intro), [H2C manual V1.0 PDF](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf)
- The mode is chosen automatically from the filament: manual section 6.6.1 (p.101) says the printer selects the chamber mode per filament type and Bambu Studio configures it during slicing; you can also switch modes on the printer screen under Air Condition. - [H2C manual V1.0 PDF](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf), [Bambu wiki, H2 cooling fan system](https://wiki.bambulab.com/en/h2/manual/cooling-fan-system)
- What triggers it in the profiles: there is no dedicated cooling-mode or vent key. The H2C machine start G-code template emits `M145 P1` (heating) if `overall_chamber_temperature >= 40`, else `M145 P0` (cooling), turns on the chamber exhaust fan (`M106 P3`), and for `min_vitrification_temperature <= 50` adds an `M142 P1 ...` PLA/TPU "chamber autocooling" line (different parameters for 0.2 and 0.4 nozzles). PLA inputs: `chamber_temperatures` 0 (`fdm_filament_common.json`), `temperature_vitrification` 45 and `textured_plate_temp` 55 (`fdm_filament_pla.json`). `activate_air_filtration` is 0 for PLA and plays no part. - [H2C machine_start_gcode template](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.4%20nozzle%20template%20machine_start_gcode.json), [fdm_filament_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_common.json), [fdm_filament_pla.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_pla.json)
- Machine preset `Bambu Lab H2C 0.4 nozzle.json`: `support_chamber_temp_control` 1, `support_cooling_filter` 1. The H2C PLA Basic preset overrides `filament_start_gcode` to a bare comment, which drops the P1S/X1-style bed-temperature `M106 P3` lines inherited from the `@base` preset. - [Bambu Lab H2C 0.4 nozzle.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.4%20nozzle.json), [Bambu PLA Basic @BBL H2C.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20@BBL%20H2C.json)
- Method to confirm on your own slice: open the exported G-code of an H2C PLA plate and look in the start block for `M145 P0` (cooling mode), the `M106 P3` chamber-fan line and the `M142 P1` autocooling line. Verify on your own printer and slicer version; the template can change between profile releases. - [H2C machine_start_gcode template](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.4%20nozzle%20template%20machine_start_gcode.json)

### Door and top glass: what Bambu actually says
- The filament guide, written for enclosed printers in general (it lists H2 series, X2D, P2S, X1, X1C, P1S), recommends opening the front door and/or removing the upper glass cover for filaments softening below 60 C (PLA, PVA, TPU) when the heatbed is above 45 C; its plate table marks glass removal "Recommended" for PLA on Textured PEI above 45 C. It adds this is more necessary in a hot room and less in a cold one. A recommendation, not a requirement; no H2 exception appears on that page. - [Bambu wiki, filament guide material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- No H2 or H2C page checked repeats or cancels that recommendation for ordinary PLA. Checked: H2 cooling fan system, H2C intro, H2C filament printing guide, H2C clogging troubleshooting, H2C FAQ, H2C manual V1.0 (six sources, not the whole wiki). The H2C filament guide only repeats the 45 C chamber limit for clogging risk. - [H2C filament printing guide](https://wiki.bambulab.com/en/h2c/h2c-filament-printing-guide), [H2C clogging](https://wiki.bambulab.com/en/h2c/troubleshooting/clogging), [H2C FAQ](https://wiki.bambulab.com/en/h2c/manual/h2c-faq)
- The H2C manual V1.0 mentions the top glass or door in three places only: p.89 soft/hard multi-material (TPU) workflow (remove the top glass in cooling mode to keep chamber temperature down); section 9.3 p.133 overhang troubleshooting, as the last step for insufficient cooling (open the front door and top glass); section 8.1.2 p.119: low-temperature filaments (PLA listed) must not be used in a chamber above 45 C. No general "open the door for PLA" instruction. - [H2C manual V1.0 PDF](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf)
- Conclusion for the H2C, PLA on Textured PEI at 55 C: door and glass changes are not required by any H2C-specific Bambu page; the generic filament-guide recommendation still stands on paper. - [Bambu wiki, filament guide material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [H2C manual V1.0 PDF](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf)

### P1S
- Printer-specific recommendation (heat creep page; names X1C/P1S/P1P): PLA on the P1S Textured PEI plate needs a 55 C bed, and printing with the front door open and/or the top cover removed is recommended to keep the chamber cool; closed door only with the Cool Plate at 35 C. - [Bambu wiki, heat creep](https://wiki.bambulab.com/en/filament-acc/filament/heat-creep)
- The P1S has no automatic vent: not stated in words by any Bambu page found; supported by the P1P-to-P1S parts list (Glass Cover Plate, Front Glass Door, Chamber Temperature Regulator Fan; no vent or exhaust grille). - [Bambu wiki, P1P to P1S](https://wiki.bambulab.com/en/p1/manual/p1p-to-p1s)

## In practice
- H2C, PLA: no door or glass change is required by Bambu; the slice puts the printer in cooling mode and the vent opens by itself while the exhaust fan runs. In a hot room the generic guide says opening the door and/or removing the glass is more necessary.
- P1S, PLA at 55 C on Textured PEI: door open and/or top cover removed, or use the Cool Plate at 35 C. Bambu states this for the P1S by name.
- To confirm the mode on any H2C slice, search the G-code for `M145 P0` and the `M106 P3` chamber-fan line.

## Not verified / open questions
- Meaning of the `M142` parameters (R/S/T/U/V/W/O, for example whether S/T/O are chamber temperature thresholds): not verified (no public source); only the comment "chamber autocooling" exists in the template.
- The literal statement "the P1S has no automatic vent": not verified as a sentence; the P1 specs page could not be fetched.
- PLA Matte H2C behaviour is inferred from the profile inheritance, not read from a slice.
- Whether the vent stays open for the whole PLA print (inference from the 30 % minimum fan speed).

Sources:
- https://wiki.bambulab.com/en/h2/manual/cooling-fan-system - cooling mode, vent opens with exhaust fan, PLA 30 % minimum
- https://wiki.bambulab.com/en/h2c/manual/h2c-intro - H2C-specific vent and cooling-mode text
- https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf - H2C manual V1.0: p.13, p.89, p.101, p.119, p.133
- https://wiki.bambulab.com/en/general/filament-guide-material-table - generic enclosed-printer door/glass recommendation
- https://wiki.bambulab.com/en/h2c/h2c-filament-printing-guide - H2C page repeats only the 45 C limit
- https://wiki.bambulab.com/en/h2c/troubleshooting/clogging - H2C page, no door/glass override
- https://wiki.bambulab.com/en/h2c/manual/h2c-faq - H2C page, no door/glass override
- https://wiki.bambulab.com/en/filament-acc/filament/heat-creep - P1S door/top-cover recommendation
- https://wiki.bambulab.com/en/p1/manual/p1p-to-p1s - P1S parts list, no vent
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.4%20nozzle%20template%20machine_start_gcode.json - M145/M106/M142 start G-code
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.4%20nozzle.json - chamber control flags
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_common.json - chamber_temperatures 0
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_pla.json - vitrification 45, Textured PEI 55
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20@BBL%20H2C.json - filament_start_gcode override
