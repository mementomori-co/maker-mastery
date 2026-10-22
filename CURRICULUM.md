# Curriculum - your learning tracker

This is your own progress tracker across the maker domains of this project. It ships empty: every box is unticked.

How to use it:

- Tick a topic (`[x]`) only when a verified note on it is filed in `knowledge\` (every fact sourced, `tools\check_note.py`
  passes). Write the note's file name after the topic when you tick it.
- Tick **Mastered** only when you can show a real result for the domain: a printed and measured part, a passed gate, a
  finished build, not only notes.
- In this project the `librarian` agent ticks topics when it files verified notes (`/file`, `/research-topic`);
  `/curriculum` only reads this file, reports where you stand and suggests the next three topics.
- Numbers are stable. Domains marked "notes ship in v1.0" already have a knowledge folder and notes to read; the others
  are planned for v1.1 and start empty. Numbers missing from the list are not part of this project.
- Add, rename or remove topics freely: this file is yours.

## A - Making (00-13)

### 00 Your gear (template)
- [ ] Printers recorded in `knowledge\00-gear-inventory\printers.md` · [ ] Dated `current-load.md` (every slot, spool,
  nozzle and plate) · [ ] Owned spools and nozzles listed · [ ] Calibrated presets per printer and filament recorded ·
  [ ] Mastered

### 01 Printers (notes ship in v1.0)
- [ ] Printer architecture (extruders, inlets, printable areas) · [ ] AMS and feeding limits · [ ] Hotends, nozzles and
  swaps · [ ] Cooling and enclosure settings · [ ] Mastered

### 02 Bambu Studio (notes ship in v1.0)
- [ ] Filament grouping and purge · [ ] Support settings · [ ] Quality, Strength, Speed and Others tabs · [ ] CLI slicing
  and `result.json` · [ ] GUI-only checks replicated in code · [ ] Mastered

### 03 Materials (notes ship in v1.0)
- [ ] PLA vs PETG, bonding and drying · [ ] Heat deflection table with loads · [ ] ABS/ASA/PC, PA, TPU and fibre-filled
  families · [ ] Third-party filaments from their data sheets · [ ] Mastered

### 04 Design for FDM (notes ship in v1.0)
- [ ] Orientation and plate finish · [ ] Self-supporting geometry (overhangs, bridges) · [ ] Splitting and joining ·
  [ ] Measured clearances from a coupon · [ ] Mastered

### 05 CAD, hard surface (notes ship in v1.0)
- [ ] Code-CAD toolchain and check suite · [ ] Parametric CAD workflow and export · [ ] Source beside every STL ·
  [ ] Mastered

### 06 Organic modeling (notes ship in v1.0)
- [ ] Sculpt to remesh to watertight to minimum wall · [ ] Splitting organic shells at natural boundaries · [ ] Mastered

### 07 Engineering (notes ship in v1.0)
- [ ] Heat-set inserts and screw bosses · [ ] Snap-fits, hinges and mechanisms · [ ] Keyed joints and connectors ·
  [ ] Physical stability · [ ] Enclosure thermal budget · [ ] Prediction versus measured result · [ ] Mastered

### 08 Electronics and lighting (notes ship in v1.0)
- [ ] Addressable LED power and injection · [ ] Level shifting · [ ] Diffusion vs hotspotting (measured) · [ ] LED
  controller current limiting · [ ] Fuses, wire gauge, connectors and strain relief · [ ] Mastered

### 09 Finishing
- [ ] Sanding, priming and painting FDM · [ ] Weathering · [ ] Silicone molds and resin casting, with safety ·
  [ ] Mastered

### 10 Workflows
- [ ] Build-to-print pipeline tied to the tools · [ ] Knowledge pipeline runbook · [ ] Mastered

### 11 Calibration and testing
- [ ] Flow, pressure advance and max volumetric speed per filament · [ ] Clearance ladder results · [ ] Mastered

### 12 Failure diagnosis (notes ship in v1.0)
- [ ] Printer error code index · [ ] Symptom, cause and fix table · [ ] Clogs and hotend swaps · [ ] Mastered

### 13 Project ops
- [ ] 3MF structure · [ ] Naming and versioning · [ ] Project folder layout · [ ] Mastered

## B - Creative (14, 17)

### 14 Creative mindset
- [ ] Ideation and constraint-breaking methods · [ ] Critique loop · [ ] "Not done before" log · [ ] Mastered

### 17 Creative direction
- [ ] Concept art process · [ ] Moodboards · [ ] Colour theory · [ ] Typography · [ ] Composition · [ ] Mastered

## C - Business (18, 20-22)

### 18 Selling 3D prints
- [ ] Product design for sale · [ ] Costing and pricing · [ ] Batch production · [ ] Packaging and QC ·
  [ ] Selling channels · [ ] Mastered

### 20 Woodworking
- [ ] Joinery · [ ] Finishing · [ ] Tools and jigs · [ ] Design for wood · [ ] Hybrid wood and print · [ ] Mastered

### 21 MakerWorld
- [ ] Publishing rules · [ ] Licences and commercial use · [ ] Print profiles · [ ] Monetisation · [ ] What sells ·
  [ ] Mastered

### 22 IP and licensing
- [ ] Trademarks · [ ] Copyright and fan art · [ ] Licensing in and out (Creative Commons) · [ ] Mastered

## D - 3D and design (24-27)

### 24 Surfacing and rendering (notes ship in v1.0)
- [ ] Retopology · [ ] UVs · [ ] Texturing and materials · [ ] Rendering and lighting · [ ] Headless rendering ·
  [ ] Mastered

### 25 Reference sheets
- [ ] Turnarounds · [ ] Orthographic sheets · [ ] Model sheets · [ ] Mastered

### 26 AI to 3D (notes ship in v1.0)
- [ ] Generation services and their licences · [ ] Local models · [ ] Cleaning AI meshes for printing · [ ] Mastered

### 27 Scanning and photogrammetry
- [ ] Capture · [ ] Reconstruction · [ ] Cleanup to printable · [ ] Mastered

## E - Games and pre-production (28-32)

### 28 Game design
- [ ] Mechanics and systems · [ ] Level design · [ ] Narrative · [ ] Game design document · [ ] Mastered

### 29 Game development
- [ ] Engine choice and setup · [ ] Game art pipeline · [ ] Characters, rigging and animation · [ ] Mastered

### 30 Visual pre-production
- [ ] Storyboards · [ ] Animatics · [ ] Shot planning · [ ] Character and environment design · [ ] Mastered

### 31 Retro arcade
- [ ] Emulation and legality · [ ] Emulation front-ends on a Raspberry Pi · [ ] Cabinet design · [ ] Controls ·
  [ ] Mastered

### 32 Audio and sound
- [ ] Sound design · [ ] Music licensing · [ ] Mastered

## F - Media (33-35, 37)

### 33 Animation and motion
- [ ] Motion graphics · [ ] 3D animation · [ ] Mastered

### 34 Video editing
- [ ] Editing workflow · [ ] Export and delivery · [ ] Mastered

### 35 AI image and video
- [ ] Tools and commercial terms · [ ] Prompting and consistency · [ ] Mastered

### 37 Photography
- [ ] Product photography and lighting · [ ] Mastered

## G - Tech (39-43)

### 39 Raspberry Pi and microcontrollers (notes ship in v1.0)
- [ ] Raspberry Pi power, GPIO and thermal · [ ] ESP32 and Arduino limits · [ ] Wiring and power · [ ] Sensors ·
  [ ] Mastered

### 40 Bambu ecosystem (notes ship in v1.0)
- [ ] Connection modes and apps · [ ] Firmware policy · [ ] Laser and cutter modules · [ ] LAN mode · [ ] Mastered

### 41 MCP (notes ship in v1.0)
- [ ] Using and configuring MCP servers in Claude Code · [ ] Building servers · [ ] Security · [ ] Mastered

### 42 Agent engineering (notes ship in v1.0)
- [ ] Subagents, skills and hooks · [ ] Permissions and settings · [ ] Pipelines and verification · [ ] Mastered

### 43 Data and backups
- [ ] Asset management and naming · [ ] Version control for creative files · [ ] Backups · [ ] Mastered

## H - Safety (44)

### 44 Safety (notes ship in v1.0)
- [ ] Laser · [ ] Resin and solvents · [ ] Wood dust and machine guarding · [ ] Electrical · [ ] Printer fumes ·
  [ ] Mastered
