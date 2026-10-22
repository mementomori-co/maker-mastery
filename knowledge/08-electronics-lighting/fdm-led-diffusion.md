# FDM LED diffusion: making a printed PLA or PETG panel glow evenly
Applies to: any Bambu Lab printer for the material and optics facts; slicer default from the Bambu Studio system process profile `0.20mm Standard @BBL H2C` (BBL profile chain)
Verified: 2026-10-20

Evidence grades: "vendor" = seller or maker guidance; "patent" = a patent's own statement, not test data; "peer-reviewed" = journal paper. No source here measures uniformity or line visibility of a printed FDM panel next to LEDs.

## Facts

### Bambu's own wording
- The Bambu store describes PLA Translucent as a frosted material that diffuses light well, and PETG Translucent as more see-through with a crystal-clear finish. No transmittance or haze figure is given. - [Bambu PLA Translucent store page](https://us.store.bambulab.com/products/pla-translucent) (vendor)
- The PLA Translucent TDS V3.0 says its frosted finish diffuses light; neither the PLA nor the PETG Translucent TDS gives a transmittance or haze figure. - [PLA Translucent TDS V3.0](https://store.bblcdn.com/s7/default/729a8bf233e9474db25c8d5be1e64a00/Bambu_PLA_Translucent_Technical_Data_Sheet.pdf); [PETG Translucent TDS V1.0](https://store.bblcdn.com/s1/default/338c9cd853fd44d9b6ed354a49048e72/Bambu_PETG_Translucent_Technical_Data_Sheet.pdf)
- Bambu notes PETG Translucent transparency varies with part size, thickness, structure and print parameters (speed, nozzle temperature, infill density). - [Bambu PETG Translucent store page](https://us.store.bambulab.com/products/petg-translucent) (vendor)

### Distance, thickness and colour (guidance, not measurement)
- Adafruit says the diffuser material matters, but its distance from the LEDs matters even more; its demo moves material from flush to about 8 inches with no ratio or lux given. It also says diffusion depends on the material's irregularities, thickness and distance. - [Adafruit: Make It Glow](https://learn.adafruit.com/make-it-glow-neopixel-and-led-diffusion-tips-tricks?view=all) (vendor)
- For printed diffusers Adafruit recommends a light-coloured filament (white, natural or transparent), with no thickness, infill or orientation given. - [Adafruit: NeoPixel arcade button, 3D printing](https://learn.adafruit.com/neopixel-arcade-button/3d-printing) (vendor)
- An LED channel vendor's rule of thumb for opal covers is channel depth at least equal to LED pitch, but its own table gives at least 16 mm at 60 LEDs/m (about 16.6 mm pitch), 12 mm at 120/m (about 8.3 mm) and 10 mm at 180/m (about 5.5 mm), so the table does not follow the rule exactly. Depth is from the channel floor, not the LED-to-cover gap. Cover transmittance on the same page: clear about 90 to 95 %, opal about 70 to 75 %, smoke about 30 to 45 %, with no thickness or method. Aluminium channel with PC/PMMA cover, not printed parts. - [SignLite LED channel guide](https://www.signliteled.com/led-channel-guide/) (vendor)
- A Magna patent's background text says diffusers typically work best at a distance equal to the LED pitch, and that a 1:1 ratio gives acceptable uniformity (max/min variation under 15 %). No material, method or test is reported, and the invention itself claims a ratio below 1:1. - [US11598504B2](https://patents.google.com/patent/US11598504B2/en) (patent statement)

### Peer-reviewed PLA and PETG optics (trends)
- Wang & Zhou 2023 (milky white vs colourless PLA, 0.4 mm nozzle, 210 °C, 100 % fill): white PLA has lower transmittance and higher haze than colourless; thicker walls (0.8, 1.6, 2.4 mm) lower transmittance and raise haze only a little; layer height (0.1 to 0.3 mm) had little effect by the authors' account (no statistical test). The paper reports the same specimen three ways, so only trends are usable. - [Wang & Zhou 2023, BioResources 18(1)](https://bioresources.cnr.ncsu.edu/wp-content/uploads/2023/01/BioRes_18_1_1545_Wang_Zhou_Design_Applicat_PLA_3D_Printing_Lamp_22210.pdf) (peer-reviewed)
- Wang et al. 2023 (PETG): printed PETG scatters light through irregular refraction at the fill pattern and defects such as bonding-neck gaps and moisture bubbles; fill lines parallel to the long edge of the wall avoid irregular refraction (cited from earlier work); best transmission in the tested ranges at 0.2 mm layer, 110 % extrusion, 40 mm/s (1 mm specimens). This is clarity, not diffusion. - [Wang et al. 2023, BioResources 19(1)](https://bioresources.cnr.ncsu.edu/wp-content/uploads/2023/11/BioRes_19_1_500_Wang_J_Effect_Slicing_Param_Light_FDM_3D_Printed_PETG_23056.pdf) (peer-reviewed)
- Orientation study (transparent PLA, 1 mm, 0.30 mm layer, 210 °C, ten prints each, integrating sphere with a 36 W 6000 K LED lamp): flat 194.2 lx, landscape 240.8 lx, portrait 246.0 lx, against 300 lx with no sample; best settings portrait, 0.30 mm, 240 °C, fan 100 %, extrusion 0.75, 40 mm/s, reported as 88 % efficiency vs 65 % default. Total transmitted light, not uniformity. - [Polymers 16(20) 2862](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11511128/fullTextXML) (peer-reviewed)
- A DTU conference paper measured extinction and scattering coefficients of PLA filaments by layer thickness (abstract only read). - [DTU Orbit, Pranovich et al. 2021](https://orbit.dtu.dk/en/publications/optical-properties-and-appearance-of-fused-deposition-modelling-f/)

### Bambu clarity recipe (aims at transparency, not diffusion)
- The Bambu wiki recommends a 0.8 mm nozzle to reduce line seams, zero top and bottom shell layers, and rectilinear infill in one direction. Its 0.4 mm recipe: 0.1 mm layer, 0.5 mm line width, 1 wall, no shells, 100 % infill at 0 or 90°, 20 mm/s, fans off, raised flow; example presets are X1C only. It also suggests sanding to raise transmittance. - [Bambu wiki: Printing tips for translucent PLA/PETG](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)
- Bambu Studio's code default for `top_surface_pattern` is rectilinear, but the BBL system profile chain (`fdm_process_common.json`) sets top `monotonicline` (Monotonic line), bottom `monotonic` (Monotonic) and `infill_direction` 45. - [BambuStudio PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp); [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json)
- A third-party vendor claims its PETG Translucent reaches up to 90 % transmittance with optimised settings, and suggests more wall loops for a softer, diffused look (no thickness or method). - [Snapmaker PETG Translucent](https://us.snapmaker.com/products/petg-translucent-filament-1kg) (vendor)

## In practice
- Clear or translucent PETG is the wrong class for a diffuser: every source aims it at see-through. Test white or natural PLA, thicker walls and a larger LED-to-panel gap first.
- The clarity recipe (one wall, no shells, aligned infill, fans off) is the opposite of what a diffuser needs; aligned lines pass light cleanly and show their structure.
- No source gives a gap for printed parts. Print a small lit test coupon at two or three gaps and wall thicknesses and judge it with your actual LEDs.
- The BBL system profiles print top surfaces as Monotonic line and bottoms as Monotonic (config keys `top_surface_pattern`, `bottom_surface_pattern`); do not assume the code default (rectilinear) applies. The UI path to these settings is not given here (label not verified).

## Not verified / open questions
- A community blog test with white PLA: LEDs clearly visible under 1 mm, smoother at about 5 mm, pixels hidden at about 10 mm (LED pitch not stated). - [newscrewdriver.com 2019](https://newscrewdriver.com/2019/07/18/glow-flow-led-diffusion-test-3d-printed-sheet/) (community, unverifiable)
- Forum advice (thin walls, no infill in the light path, consistent line direction, white PLA for RGB, smooth vs textured plate) and reports that white PETG diffuses better than translucent PETG. - [Bambu forum: LED diffuser using transparent PC](https://forum.bambulab.com/t/led-diffuser-using-transparent-pc/185469); [Bambu forum: Translucent PETG translucency](https://forum.bambulab.com/t/translucent-petg-translucency/259232) (community, unverifiable)
- A frosted look from a textured plate plus fuzzy skin on white PLA. - [bone.id.au 2026](https://bone.id.au/blog/2026/02/07/3d-printing-led-diffusers/) (community, unverifiable)
- No official or peer-reviewed measurement of line visibility or uniformity for a printed panel at a stated LED pitch and gap was found.

Sources:
- https://us.store.bambulab.com/products/pla-translucent - PLA vs PETG Translucent wording
- https://us.store.bambulab.com/products/petg-translucent - PETG transparency varies
- https://store.bblcdn.com/s7/default/729a8bf233e9474db25c8d5be1e64a00/Bambu_PLA_Translucent_Technical_Data_Sheet.pdf - PLA Translucent TDS
- https://store.bblcdn.com/s1/default/338c9cd853fd44d9b6ed354a49048e72/Bambu_PETG_Translucent_Technical_Data_Sheet.pdf - PETG Translucent TDS
- https://learn.adafruit.com/make-it-glow-neopixel-and-led-diffusion-tips-tricks?view=all - distance matters
- https://learn.adafruit.com/neopixel-arcade-button/3d-printing - light-coloured filament
- https://www.signliteled.com/led-channel-guide/ - channel depth, cover transmittance
- https://patents.google.com/patent/US11598504B2/en - 1:1 pitch background text
- https://bioresources.cnr.ncsu.edu/wp-content/uploads/2023/01/BioRes_18_1_1545_Wang_Zhou_Design_Applicat_PLA_3D_Printing_Lamp_22210.pdf - PLA trends
- https://bioresources.cnr.ncsu.edu/wp-content/uploads/2023/11/BioRes_19_1_500_Wang_J_Effect_Slicing_Param_Light_FDM_3D_Printed_PETG_23056.pdf - PETG scattering, slicing optimum
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11511128/fullTextXML - PLA orientation vs illuminance
- https://orbit.dtu.dk/en/publications/optical-properties-and-appearance-of-fused-deposition-modelling-f/ - PLA optical coefficients (abstract)
- https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg - Bambu clarity recipe
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp - top_surface_pattern code default
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json - system profile surface patterns
- https://us.snapmaker.com/products/petg-translucent-filament-1kg - vendor claim
- https://newscrewdriver.com/2019/07/18/glow-flow-led-diffusion-test-3d-printed-sheet/ - community test (unverifiable)
- https://forum.bambulab.com/t/led-diffuser-using-transparent-pc/185469 - community advice (unverifiable)
- https://forum.bambulab.com/t/translucent-petg-translucency/259232 - community reports (unverifiable)
- https://bone.id.au/blog/2026/02/07/3d-printing-led-diffusers/ - community method (unverifiable)
