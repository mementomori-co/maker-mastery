# Symptom, cause, fix (warping, stringing, under-extrusion, layer shift, spaghetti, AMS feed, Textured PEI)

Applies to: H2C | P1S | both · Bambu Studio 2.x (UI labels below come from wiki pages that name no Studio version) · firmware not named by the source pages
Verified: 2026-10-03

## Facts

### Warping, bed adhesion, structural collapse
- Bambu groups these failures as corner warping, bed adhesion failure and structural collapse. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing)
- Causes listed: thermal shrinkage (edges cool faster than the centre and pull the corners up); skin oil on the plate, which Bambu calls the most common cause; the wrong plate type selected in the slicer; Z offset too high; the nozzle knocking over a tall thin part at speed; crossing infill patterns (Grid, Triangles); loose belts. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing)
- First fix before changing slicer settings: clean the plate, run auto bed leveling, confirm the nozzle is installed correctly; Bambu says these steps fix about 80% of warping and adhesion failures. An advanced fourth step adjusts first-layer settings. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing)
- PLA corner lift on Textured PEI: raise the bed 5-10 °C toward 55-65 °C (PLA only; no PETG target is given), add an 8-10 mm brim, set "No cooling for first X layers" to 3 in the filament Cooling settings, or paint brim ears. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing)

### First layer not sticking
- Because Textured PEI is grainy, the printer lowers the nozzle by 0.04 mm after leveling. If you print on Textured PEI but slice for a different plate, the first layer is too high. — [source](https://wiki.bambulab.com/en/knowledge-sharing/first-layer-not-sticking)
- Other causes: an unwashed plate and skipped bed leveling. Fix: select the plate type that matches the plate installed, and clean the plate. — [source](https://wiki.bambulab.com/en/knowledge-sharing/first-layer-not-sticking)

### Stringing and oozing
- Six causes: damp filament, retraction, travel speed, nozzle temperature, path planning, nozzle too large. Fixes: dry the filament and store it sealed with desiccant; raise retraction length or speed (Bambu generally keeps length at 2 mm or less); enable "Avoid crossing wall". — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/stringing-oozing)
- The 0.5-0.7 flow-ratio advice on that page is only for low-density foaming filament such as PLA Aero; do not apply it to normal PLA or PETG. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/stringing-oozing)

### Filament building up on the nozzle
- Buildup can grow into a blob that fails the print. Causes: damp filament, flow too high, speed and temperature mismatched, a nozzle-wiper problem, many travel moves. Bambu says it happens mostly with PETG-type filaments. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/filament-sticks-to-nozzle)
- Fix: heat the nozzle, then remove the buildup carefully. For PETG-type filaments a flow ratio of 0.93-0.96 works well, and Bambu's PETG Basic and PETG-CF profiles default to 0.95. Retraction 1.2-1.6 mm at 40-60 mm/s (no nozzle size or printer named for these values). — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/filament-sticks-to-nozzle)
- Dry PETG before printing and store it in an AMS or sealed box with desiccant below 20% RH. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/filament-sticks-to-nozzle)

### Layer shift
- A layer shift is a position or height error that misaligns one or more layers. Causes: a damaged toolhead cable chain (X1/P1/P2/H2 series); tubes or cables obstructing the toolhead (A series); high-viscosity filament such as PETG Basic letting the nozzle hit the part; Ludicrous speed mode; filament piled up in the purge chute. — [source](https://wiki.bambulab.com/en/knowledge-sharing/layer-shifts)
- Fix: check that X and Y move freely with nothing in the way. Auto-recovery from step loss addresses the speed-related cause: on H2 series it is on the printer under Settings > Print Options; for P1 series it is enabled in Bambu Studio. Paths are firmware-dependent. — [source](https://wiki.bambulab.com/en/knowledge-sharing/layer-shifts)

### Under-extrusion
- Global or localised. Causes: too much extrusion resistance (for example a spool that cannot turn or tangled filament), too little extrusion volume, a wrong pressure-advance value. Fix the spool or tangle first and reprint. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/under-extrusion)
- Raising the flow ratio is offered as a fix, but for genuine Bambu filament the page recommends keeping the default flow ratio. A wrong pressure advance calls for flow calibration; the method shown is for P1P and X1 series. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/under-extrusion)

### Elephant foot
- The bottom layer(s) end up wider than the layers above, because the heated bed keeps them soft and the weight above presses them out. Setting: Process > Quality > Precision > Elephant foot compensation (label not verified against your Studio version). Values differ between plate types and are not interchangeable. — [source](https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot)

### Spaghetti
- Bambu names first-layer, mid-print, warping, support-collapse and nozzle-scraping spaghetti. Fixes: clean the plate; Z hop type Normal (printer settings > Extruder); Brim type Outer brim only with 5-8 mm width (Others tab); initial layer speed at most 30 mm/s and initial layer infill speed at most 60 mm/s. Labels not verified against your Studio version. — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/spaghetti)
- The spaghetti page says to add support for overhangs "greater than 45°", while Bambu's overhang page words the same line as "smaller than 45°"; the two pages measure the angle from different references. State which page and reference you use when citing either. Overhang detail lives in [04-design-for-fdm](../04-design-for-fdm/index.md). — [source](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/spaghetti)

### Spaghetti detection (camera feature; scope differs by printer)
- The X1C page describes a USB camera in the chamber corner; that page is X1C-only. The H2D/H2C page describes a live chamber camera plus a nozzle camera that detects nozzle clumping, printing in air and spaghetti. — [source](https://wiki.bambulab.com/en/knowledge-sharing/Spaghetti_detection), [source](https://wiki.bambulab.com/en/h2/manual/intelligent-detection)
- On H2D/H2C the method matches the X1 series (an AI detector flags spaghetti when enough consistent candidates appear); black or dark filament raises false positives. It must be enabled in the print options, has low/medium/high sensitivity, needs the chamber light on, and is not active when slicing with third-party software or using G-code from another model. — [source](https://wiki.bambulab.com/en/h2/manual/intelligent-detection)

### AMS 2 Pro loading and unloading failures
- Sections cover pre-loading anomalies, loading failure and unloading failure; the worked example is a P2S, so tube routing on other printers may differ. Causes: feeder-unit sensor or motor fault, internal hub sensor fault, worn filament, dirty hub knurled teeth, bent PTFE tube, abnormal extrusion. — [source](https://wiki.bambulab.com/en/ams-2-pro/troubleshooting/loading-unloading-failure)
- First fixes: check the feeder unit for a worn or grooved magnet or a clog (per the feeder cleaning guide); pull the filament from the failing slot, cut off any worn section and reload. — [source](https://wiki.bambulab.com/en/ams-2-pro/troubleshooting/loading-unloading-failure)

### Textured PEI plate
- Wear at the spot where the nozzle-wipe move dips 1-2 mm into the plate is normal; wear inside the print area can affect prints. Adhesion causes: dust, sweat or oil on the plate, bed temperature, contact area, first-layer settings. — [source](https://wiki.bambulab.com/en/general/textured-PEI-plate-not-working-as-expected)
- Fixes: clean the plate per Bambu's PEI cleaning guide; raise bed temperature slightly, but too hot with PLA or PETG can cause nozzle clogs and elephant foot. Suggested first-layer start: 0.5 mm line width and 0.25 mm layer height (no nozzle size stated). — [source](https://wiki.bambulab.com/en/general/textured-PEI-plate-not-working-as-expected)

## In practice
- For warping, adhesion and spaghetti alike, start with the same three checks: clean plate, correct plate type in the slicer, bed leveling.
- For PETG nozzle buildup, start from Bambu's 0.95 default flow ratio before tuning inside 0.93-0.96.
- For under-extrusion on genuine Bambu filament, check spool rotation, tangles and pressure advance before touching flow ratio.
- Spaghetti detection on H2C is documented on the H2D/H2C page (two cameras); no official page confirms it on the P1S.

## Not verified / open questions
- None of the wiki pages names a Bambu Studio version, so the quoted UI labels may differ on your build.
- No PETG bed-temperature target for Textured PEI was found (the 55-65 °C advice is PLA-only).
- Whether spaghetti detection exists on the P1S: no official page found.
- Whether the AMS 2 Pro loading procedure (written for P2S) applies unchanged to other printers.
- The nozzle size behind the 0.5 mm / 0.25 mm Textured PEI starting point is not stated (0.4 mm assumed, not confirmed).

Sources:
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing - warping causes and fixes
- https://wiki.bambulab.com/en/knowledge-sharing/first-layer-not-sticking - 0.04 mm Textured PEI offset, plate-type mismatch
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/stringing-oozing - stringing causes and fixes
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/filament-sticks-to-nozzle - nozzle buildup, PETG flow and storage
- https://wiki.bambulab.com/en/knowledge-sharing/layer-shifts - layer shift causes and auto-recovery
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/under-extrusion - under-extrusion causes, flow-ratio caveat
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot - elephant foot and compensation setting
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/spaghetti - spaghetti failure modes and fixes
- https://wiki.bambulab.com/en/knowledge-sharing/Spaghetti_detection - X1C spaghetti detection
- https://wiki.bambulab.com/en/h2/manual/intelligent-detection - H2D/H2C intelligent detection
- https://wiki.bambulab.com/en/ams-2-pro/troubleshooting/loading-unloading-failure - AMS 2 Pro loading failures
- https://wiki.bambulab.com/en/general/textured-PEI-plate-not-working-as-expected - Textured PEI troubleshooting
