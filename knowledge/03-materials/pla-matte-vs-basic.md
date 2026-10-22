# Bambu PLA Matte vs PLA Basic (and how 3-value preset arrays work)
Applies to: H2C presets (0.4 mm nozzle); TDS rows apply to the filament on any printer · Bambu Studio 02.08.02.61, profile bundle BBL 02.08.00.05
Verified: 2026-10-05 (array-variant section 2026-10-16)

Preset values below were read from the Bambu Studio system profiles. The same files are public in the Bambu Studio repository at tag v02.08.02.61 (bundle version 02.08.00.05): [BBL filament folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament). Values resolve through `inherits` (H2C preset -> `@base` -> `fdm_filament_pla` -> `fdm_filament_common`) plus the `include` template `fdm_filament_template_direct_dual_e3d`.

## Facts

### Colour catalogue (example: Bone White vs Desert Tan)
- PLA Matte Bone White is colour code 11103, short code W3, hex #CBC6B8; PLA Matte Desert Tan is 11401, short code Y3, hex #E8DBB7. The two are easy to confuse by eye. — [filaments_color_codes.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/filaments_color_codes.json), [Bambu PLA Matte hex code PDF](https://cdn.shopify.com/s/files/1/0584/7236/6216/files/Bambu_PLA_Matte_Hex_Code.pdf?v=1745547424)
- Store variant names carry the colour code, for example "PLA Matte - Bone White (11103)" and "PLA Matte - Desert Tan (11401)". — [Bambu US store, PLA Matte](https://us.store.bambulab.com/products/pla-matte)
- A 3MF project stores only the slot hex colour and preset name, not a colour name. When the AMS colour differs, Studio maps to the same type and closest colour, and Bambu asks you to check the mapping popup. That statement is on an X1 manual page; H2C behaviour is not verified. — [Bambu wiki, X1 multi-color printing](https://wiki.bambulab.com/en/x1/manual/multi-color-printing)

### Installed presets: `Bambu PLA Matte @BBL H2C` vs `Bambu PLA Basic @BBL H2C`
- Identical on H2C: nozzle 220 °C (initial layer too), recommended range 190-240 °C, Textured PEI 55 °C, Cool Plate 35 °C, engineering and hot plate 55 °C, SuperTack 40 °C, `temperature_vitrification` 45 °C, retraction length [0.4, 0.8, 0.4] mm, `filament_max_volumetric_speed` [25, 40, 25] mm³/s, Z-hop type Spiral Lift, wipe on, aux fan 75 %, `fan_min_speed` 60 %. — [Bambu PLA Matte @BBL H2C.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Matte%20%40BBL%20H2C.json), [Bambu PLA Basic @BBL H2C.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20%40BBL%20H2C.json), [fdm_filament_pla.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_pla.json)
- Keys that differ (Matte / Basic): `fan_max_speed` 100 / 80 %; `filament_density` 1.32 / 1.26 g/cm³; `filament_flow_ratio` 1.00 / 0.99; `filament_scarf_height` 5 % / 10 %; `impact_strength_z` 6.6 / 13.8 kJ/m²; `filament_id` GFA01 / GFA00; and the circle-compensation coefficients (`counter_coef_*`, `hole_coef_*`, `*_limit_*`). — same files as above
- `filament_scarf_seam_type` resolves to "none" for both, so the scarf-height difference only matters if you turn a scarf seam on. `required_nozzle_HRC` is 3 for both (no hardened-steel check). — [Bambu PLA Matte @base.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Matte%20%40base.json), [fdm_filament_common.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_common.json)
- AMS drying keys are the same for both: `filament_dev_ams_drying_temperature` 45 °C and `filament_dev_ams_drying_time` 12 h. — [Bambu PLA Matte @BBL H2C.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Matte%20%40BBL%20H2C.json)
- Preset densities (1.32 and 1.26 g/cm³) differ from the TDS values (1.31 and 1.24 g/cm³). `filament_density` is used for weight and cost statistics only. — [Matte TDS V3.0](https://store.bblcdn.com/s7/default/5b061f2feeac4ba88f355a33248bbda7/Bambu_PLA_Matte_Technical_Data_Sheet.pdf), [Basic TDS V3.0](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf), [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)

### What the 3 values in an H2C preset array mean
- H2C filament presets include `fdm_filament_template_direct_dual_e3d`, which sets `filament_extruder_variant` to Direct Drive Standard, Direct Drive High Flow and Direct Drive E3D High Flow. So a 3-value array is indexed by hotend flow variant, not by left/right extruder. For PLA Matte and Basic: Standard 25 mm³/s and 0.4 mm retraction; High Flow 40 mm³/s and 0.8 mm; E3D High Flow 25 mm³/s and 0.4 mm. — [fdm_filament_template_direct_dual_e3d.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/fdm_filament_template_direct_dual_e3d.json), [Print.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Print.cpp), [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- Studio picks the entry whose variant string matches the extruder type plus nozzle volume type. The preset loader applies the parent first, then the `include` template, then the file's own keys. — [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), [PresetBundle.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PresetBundle.cpp)
- For comparison, `Generic PLA @BBL H2C 0.4 nozzle` uses 12 mm³/s and 0.4 mm retraction on all three entries, density 1.24 g/cm³, flow ratio 0.99 and `temperature_vitrification` 45 °C. — [Generic PLA @BBL H2C 0.4 nozzle.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/Generic%20PLA%20%40BBL%20H2C%200.4%20nozzle.json)

### TDS values (both Technical Data Sheet V3.0)
- Printing, same for both: nozzle 190-230 °C; Cool Plate, High Temperature Plate or Textured PEI with glue; bed 35-45 °C; chamber 25-45 °C; maximum overhang 55°; maximum bridge 30 mm; retraction 0.6-1.0 mm. The H2C presets use 55 °C on Textured PEI, above the TDS 35-45 °C. — [Matte TDS V3.0](https://store.bblcdn.com/s7/default/5b061f2feeac4ba88f355a33248bbda7/Bambu_PLA_Matte_Technical_Data_Sheet.pdf), [Basic TDS V3.0](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf)
- Thermal, Matte vs Basic: Vicat 63 vs 57 °C; HDT 52 vs 54 °C at 1.8 MPa; HDT 58 vs 57 °C at 0.45 MPa; Tg (DSC, 10 °C/min) 61 vs 60 °C. — same TDS
- Density (ISO 1183): Matte 1.31 g/cm³, Basic 1.24 g/cm³. — same TDS
- Z-direction strength (specimens 220 °C nozzle, 35 °C bed, 200 mm/s, 100 % infill, annealed and dried 55 °C for 8 h): tensile Z Matte 22 ± 4 MPa vs Basic 31 ± 3 MPa; impact Z (ISO 179) Matte 6.6 ± 1.1 vs Basic 13.8 ± 0.9 kJ/m². The 7.9 kJ/m² figure sometimes quoted for Basic is its X-Y notched impact, not Z. — same TDS
- The filament guide gives PLA (including Basic and Matte) a nozzle range of 190-240 °C (±10 °C) and bed by plate: Cool Plate 35-45 °C; Engineering, Smooth PEI, High Temperature and Textured PEI 45-65 °C (glue required on Engineering Plate). — [Bambu filament guide material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- Speed figures for PLA Matte are marketing with mixed conditions: the store gives up to 270 mm/s (0.4 mm nozzle, 0.4 mm line, 0.2 mm layer) and elsewhere 250-300 mm/s; the TDS says under 300 mm/s. Claims of fewer visible layer lines and easier support removal carry no test condition. — [Bambu US store, PLA Matte](https://us.store.bambulab.com/products/pla-matte), [Matte TDS V3.0](https://store.bblcdn.com/s7/default/5b061f2feeac4ba88f355a33248bbda7/Bambu_PLA_Matte_Technical_Data_Sheet.pdf)

### Drying
- TDS (both): forced-air oven 50 °C for 8 h; X1-series heatbed 60-70 °C for 12 h; print and store below 20 % RH with desiccant. — [Matte TDS V3.0](https://store.bblcdn.com/s7/default/5b061f2feeac4ba88f355a33248bbda7/Bambu_PLA_Matte_Technical_Data_Sheet.pdf), [Basic TDS V3.0](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf)
- AMS 2 Pro and AMS HT: 45 °C for 12 h (drying guide, filament guide and preset keys agree). Static drying mode is not suitable for PLA. — [Bambu wiki: dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)
- Unresolved: the filament guide gives generic PLA an oven value of 55 °C for 8 h, while the TDS V3.0 and the drying guide say 50 °C for 8 h. — [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table), [dry filament](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament)

### AMS, nozzle and bonding class
- The store lists PLA Matte as compatible with all AMS series, printers, plates and nozzles. The guide's "PLA" class covers PLA Basic and PLA Matte and needs no hardened-steel nozzle. — [Bambu US store, PLA Matte](https://us.store.bambulab.com/products/pla-matte), [material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- PLA Matte is in the low-temperature class, the same as PLA Basic, so the two can be fused in one print. The PLA/PETG mutual-support guide lists PLA Matte as not supported, so no Matte-to-PETG support pairing is claimed. — [H2D/H2C filament config limit](https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit), [H2D PLA and PETG mutual support](https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support)

## In practice
- If you want Bone White, the slot colour is #CBC6B8. #E8DBB7 is Desert Tan.
- Matte and Basic share temperatures and speeds on the H2C. The real preset differences are fan maximum (100 vs 80 %), flow ratio (1.00 vs 0.99), density and the circle-compensation coefficients.
- If both are on one plate, Basic is about twice as tough in Z impact (13.8 vs 6.6 kJ/m²). Put load-bearing or snap features in Basic.
- Check whether your 0.4 mm hotend is Standard or High Flow before trusting the 3-value array entry in a preset.
- AMS 2 Pro drying: 45 °C for 12 h. For an oven, state which source you follow (50 °C or 55 °C for 8 h).

## Not verified / open questions
- The 50 vs 55 °C oven-drying disagreement between official Bambu sources is unresolved.
- Whether the H2C mapping popup shows an explicit colour-mismatch warning is not verified (the closest-colour behaviour is from an X1 page).
- No Bambu statement found on seam visibility or abrasion for PLA Matte.
- Marketing claims (smoother layer lines, easier support removal) have no test conditions.
- Keys not listed were not checked for `include`-template overrides.

Sources:
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament — Bambu Studio system filament presets, tag v02.08.02.61 (bundle 02.08.00.05)
- https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/filaments_color_codes.json — colour codes and hex values
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp — key meanings, variant index lookup
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Print.cpp — `filament_extruder_variant` selection
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PresetBundle.cpp — parent, include, own-keys order
- https://cdn.shopify.com/s/files/1/0584/7236/6216/files/Bambu_PLA_Matte_Hex_Code.pdf?v=1745547424 — official PLA Matte hex table
- https://us.store.bambulab.com/products/pla-matte — variant names, AMS compatibility, speed claims
- https://store.bblcdn.com/s7/default/5b061f2feeac4ba88f355a33248bbda7/Bambu_PLA_Matte_Technical_Data_Sheet.pdf — PLA Matte TDS V3.0
- https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf — PLA Basic TDS V3.0
- https://wiki.bambulab.com/en/general/filament-guide-material-table — PLA temperatures, PLA class definition, 55 °C oven value
- https://wiki.bambulab.com/en/filament-acc/filament/dry-filament — drying guide, static-drying exclusion
- https://wiki.bambulab.com/en/x1/manual/multi-color-printing — closest-colour mapping (X1 page)
- https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit — temperature classes
- https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support — mutual-support scope
