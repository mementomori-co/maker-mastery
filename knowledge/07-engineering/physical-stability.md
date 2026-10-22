# Physical stability of printed display pieces (tip angle, push force, printed mass, centre of mass)

Applies to: any printer (physics); Bambu Studio behaviour read at tag v02.08.02.61, presets checked for `0.20mm Standard @BBL H2C` and Bambu PLA Basic
Verified: 2026-10-05

## Facts

### The rule and two derived formulas
- A body stays upright while its centre of gravity is above its base of support; once the centre of gravity passes outside, gravity's torque tips it over. In uniform gravity the centre of gravity equals the centre of mass (CoM). - [OpenStax College Physics 9.3 (LibreTexts)](https://phys.libretexts.org/Bookshelves/College_Physics/College_Physics_1e_(OpenStax)/09:_Statics_and_Torque/9.03:_Stability), [OpenStax University Physics Vol. 1 ch. 12](https://www.theexpertta.com/book-files/OpenStaxUniversityPhysicsVol1/UP1_Ch12.%20Static%20Equilibrium%20and%20Elasticity.pdf)
- The support polygon is the convex hull of the mesh points touching the ground; an object stands when its CoM projects (along gravity) inside that polygon. The paper notes printed models often fail to stand. No source gives a tolerance for "touching". - [Make It Stand, SIGGRAPH 2013](https://igl.ethz.ch/projects/make-it-stand/make-it-stand-siggraph-2013-prevost-et-al.pdf)
- Static tip angle: theta_tip = atan(d / h_CoM), with d the horizontal distance from the CoM to the nearest support-polygon edge and h_CoM the CoM height. For a uniform block (d = w/2, h_CoM = h/2) this is atan(w/h), matching the RAEng table (w 20, h 12 gives 59.04 deg; w 12, h 20 gives 30.96 deg). Derived from the tipping rule; static only (on a tilting board the piece slides first if the static friction coefficient is below d/h_CoM). - [RAEng: forces, centre of gravity and stability](https://raeng.org.uk/media/phckgici/5-forces-centre-of-gravity-reactions-and-stability.pdf) p. 4 and Table 2 p. 9
- Horizontal push to tip: P_tip = m g d / h_push, pushing perpendicular to the tipping edge at height h_push. It contains no CoM height. Sliding happens first if the static friction coefficient is below d / h_push. Quasi-static only. - [Engineering Statics 9.2](https://engineeringstatics.org/Chapter_09-slipping-vs--tipping.html), [Mechanics Map: slipping vs tipping](http://mechanicsmap.psu.edu/websites/7_friction/7-2_slipping_vs_tipping/slippingvstipping.html)
- "Low and wide" holds for tilt angle (a lower CoM and a wider base tolerate more tilt) but not as a blanket rule for push force: mass added high and centred raises P_tip because m rises and d is unchanged. State the claim per metric. - derived from [RAEng](https://raeng.org.uk/media/phckgici/5-forces-centre-of-gravity-reactions-and-stability.pdf) p. 8 and the formulas above
- For scale only (vehicles, not display pieces): the US NHTSA Static Stability Factor, track width / (2 x CoG height), typically ranges 1.00-1.50 for cars and light trucks, about 45-56 deg as an angle. - [NHTSA DOT HS 812 444](https://crashstats.nhtsa.dot.gov/Api/Public/Publication/812444)
- Make It Stand lets the user choose a target toppling angle and gives no recommended number. - [Make It Stand](https://igl.ethz.ch/projects/make-it-stand/make-it-stand-siggraph-2013-prevost-et-al.pdf)

### Real printed mass
- The CLI's `result.json` reports grams per filament per plate (`total_used_g`, `main_used_g`), with no per-object grams; `main_used_g` includes support. - [BambuStudio.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/BambuStudio.cpp)
- The 3MF's `slice_info.config` has a per-plate weight and per-filament grams split into object and support use, but no per-object grams. - [bbs_3mf.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp)
- Density: the PLA Basic TDS gives 1.24 g/cm3; the `Bambu PLA Basic @base` profile sets `filament_density` 1.26 (its parent `fdm_filament_pla` has 1.24). The tooltip says density is for statistics only. Slicer grams x 1.24/1.26 gives the TDS-density mass. - [PLA Basic TDS](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf), [Bambu PLA Basic @base.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20%40base.json), [fdm_filament_pla.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_pla.json), [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- The Preview shows weight per line type and splits grams into model, flushing and prime tower. - [Bambu wiki: view slicing information](https://wiki.bambulab.com/en/software/bambu-studio/view-slicing-information)
- Infill percentage is not the printed volume fraction: walls and shells add solid material, honeycomb uses about 25 % more than other patterns, and lightning infill applies density only under top surfaces. - [Bambu wiki: fill patterns](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- A mesh library's centre of mass (for example trimesh `center_mass`) assumes uniform, solid density; it is not the printed CoM when infill is below 100 %. - [trimesh documentation](https://trimesh.org/trimesh.base.html)

### Lowering the CoM
- A Height Range Modifier (right-click the model > Height range Modifier) changes settings over a height range; the wiki example changes speed. Whether it can change sparse infill density was not confirmed; test in the GUI. - [Bambu wiki: modifier](https://wiki.bambulab.com/en/software/bambu-studio/modifier)
- Pause at a layer lets you embed an object such as a magnet or weight. - [Bambu wiki: view slicing information](https://wiki.bambulab.com/en/software/bambu-studio/view-slicing-information)
- For ballast, treat the insert as its own solid, weigh it, and combine CoMs weighted by mass (composite-body method, derived). Steel or tungsten shot densities appear only in a vendor blog (community). - [Creality blog (community)](https://www.creality.com/blog/how-to-add-weight-to-3d-prints)

### Tall, thin parts while printing
- Bambu lists the nozzle knocking a tall, thin model over at high speed as a collapse cause; fixes include cutting speed and acceleration by 20-30 %, adding supports, or laying the part flat. Crossing infill patterns can leave bumps the nozzle clips. - [Bambu wiki: warping, falling off, collapsing](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing)
- Auto brim widens for tall parts with small footprints. - [Bambu wiki: brim](https://wiki.bambulab.com/en/software/bambu-studio/auto-brim)
- Slow down by height (`enable_height_slowdown`, Advanced mode, Process > Speed > Other layers speed (label not verified on screen; read from code)) ramps speed and acceleration linearly between a start and end height. It is off in `0.20mm Standard @BBL H2C`. - [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp), [0.20mm Standard @BBL H2C.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json)
- Minimum layer time (`slow_down_layer_time`): code default 5 s; the PLA base profile sets 4 s. - [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), [fdm_filament_pla.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_pla.json)
- A nozzle strike can cause lost steps; newer Bambu printers have an auto-recovery option (menu path varies by model and firmware). - [Bambu wiki: layer shifts](https://wiki.bambulab.com/en/knowledge-sharing/layer-shifts)
- Bambu Studio has no topple or tall-object warning at this tag; the only "too tall" message is the sequential-print collision check. Searched across the tag's source. - [Print.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Print.cpp), [tag tarball](https://codeload.github.com/bambulab/BambuStudio/tar.gz/refs/tags/v02.08.02.61)
- Tall supports can collapse; the wiki calls Honeycomb a good balance for tall support. - [Bambu wiki: support](https://wiki.bambulab.com/en/software/bambu-studio/support)

## In practice
- Worked example (made-up numbers): a uniform block 40 mm wide and 120 mm tall has d = 20 mm and h_CoM = 60 mm, so theta_tip = atan(20/60) = 18.4 deg. If it weighs 100 g and is pushed at its top edge (h_push = 120 mm), P_tip = 0.1 x 9.81 x 0.020 / 0.120 = 0.16 N.
- A standing check you can script: support polygon = 2D convex hull of vertices within a small band above the lowest point (choose and state the band); CoM from the mesh (uniform density) or better from a shell-plus-infill estimate; per edge, tip angle atan(d_i/h_CoM) and push m g d_i / h_push; the piece stands only if every d_i > 0.
- For a mass you will quote, use slicer grams for the part (minus support grams), corrected to TDS density, not mesh volume.
- Pass thresholds are your call: no source gives a tip angle for display pieces. Pick one, state it, and calibrate it with a tilt test on a flat board.
- Every prediction should name the assembly state it covers (glued, loose, or a piece standing alone) and how it will be scored (tilt angle to first lift-off). A glued assembly and a loose one can behave very differently.
- For a tall piece on a small sole: widen or weight the base, slow the top (Slow down by height or a Height Range Modifier), widen the brim, and report tilt angle and push force as separate numbers.

## Not verified / open questions
- No published pass threshold for display pieces (vehicle figures are not transferable).
- No published shell-plus-core model for printed CoM.
- Static friction of PLA on a tabletop: not found, so the slide-versus-tip comparison cannot be completed from sources.
- Whether a Height Range Modifier can lower sparse infill density.
- Whether Preview "Support" grams equal the support grams in `result.json`: not verified (no public source).
- Furniture tip-over standards (ASTM F2057, CPSC) were not read.

Sources:
- https://phys.libretexts.org/Bookshelves/College_Physics/College_Physics_1e_(OpenStax)/09:_Statics_and_Torque/9.03:_Stability - tipping condition
- https://www.theexpertta.com/book-files/OpenStaxUniversityPhysicsVol1/UP1_Ch12.%20Static%20Equilibrium%20and%20Elasticity.pdf - CG equals CM
- https://igl.ethz.ch/projects/make-it-stand/make-it-stand-siggraph-2013-prevost-et-al.pdf - support polygon, standing condition
- https://raeng.org.uk/media/phckgici/5-forces-centre-of-gravity-reactions-and-stability.pdf - tipping angle table
- https://crashstats.nhtsa.dot.gov/Api/Public/Publication/812444 - NHTSA SSF
- https://engineeringstatics.org/Chapter_09-slipping-vs--tipping.html - slip vs tip
- http://mechanicsmap.psu.edu/websites/7_friction/7-2_slipping_vs_tipping/slippingvstipping.html - tipping as moment balance
- https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf - PLA Basic density
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20%40base.json - preset density 1.26
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_pla.json - density 1.24, layer time 4 s
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/BambuStudio.cpp - result.json fields
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp - slice_info.config
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp - tooltips and keys
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp - GUI location
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json - height slowdown off
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Print.cpp - only "too tall" check
- https://codeload.github.com/bambulab/BambuStudio/tar.gz/refs/tags/v02.08.02.61 - source tree searched
- https://trimesh.org/trimesh.base.html - mesh centre of mass (uniform density)
- https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns - infill material use
- https://wiki.bambulab.com/en/software/bambu-studio/view-slicing-information - Preview weights, pause to embed
- https://wiki.bambulab.com/en/software/bambu-studio/modifier - Height Range Modifier
- https://wiki.bambulab.com/en/software/bambu-studio/auto-brim - brim for tall parts
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing - tall-thin collapse
- https://wiki.bambulab.com/en/knowledge-sharing/layer-shifts - step loss, auto-recovery
- https://wiki.bambulab.com/en/software/bambu-studio/support - tall supports
- https://www.creality.com/blog/how-to-add-weight-to-3d-prints - ballast (community vendor blog)
