# Orientation and plate finish: how a part sits on the plate and what the plate does to its faces

Applies to: H2C | P1S | both · Bambu Studio 2.8.02.61 · Textured PEI and Smooth PEI plates
Verified: 2026-10-04

This note is mostly a method. It pulls together facts from the overhang, support and plate sources below; it adds no measured result of its own.

## Facts
- In Bambu Studio, `support_threshold_angle` (Process > Support > Threshold angle) is measured from horizontal: support is generated for overhangs whose slope is below the threshold. The code default is 30 degrees. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support); [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- The H2C `0.20mm Standard` preset inherits 30 degrees; the `0.16mm High Quality` preset uses 25 degrees. -- [BBL process profiles, v02.08.02.61](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process)
- A useful way to compute overhangs in code: take the angle between each face normal and straight down (-Z). A face that is not on the plate is an overhang when its slope from horizontal is below the threshold angle. This is the same convention the wiki uses ("slope angle" from the bed). -- [Bambu wiki, overhang](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang)
- Textured PEI gives the bottom face of a part a textured finish and usually holds without adhesive. -- [Bambu wiki, plates](https://wiki.bambulab.com/en/filament-acc/acc/plates)
- On Textured PEI, PC, PA, ABS and ASA may need a layer of glue stick. -- [Bambu wiki, plates](https://wiki.bambulab.com/en/filament-acc/acc/plates)
- Bambu recommends waiting until the bed is at 35 C or lower before removing prints from Textured PEI. -- [Bambu wiki, plates](https://wiki.bambulab.com/en/filament-acc/acc/plates)
- Clean PEI plates with a sponge, dishwashing detergent and warm water; never use acetone. -- [Bambu wiki, PEI plate clean guide](https://wiki.bambulab.com/en/filament-acc/acc/pei-plate-clean-guide); [Bambu wiki, filament guide material table](https://wiki.bambulab.com/en/general/filament-guide-material-table)
- On Smooth PEI, only PLA prints without glue; every other filament needs glue so the PEI sheet does not tear. -- [Bambu wiki, plates](https://wiki.bambulab.com/en/filament-acc/acc/plates)
- Elephant foot is the first layer (sometimes the first few) printing wider than the layers above. The fix is Process > Quality > Precision > Elephant foot compensation (key `elefant_foot_compensation`). The right value differs between plate types. -- [Bambu wiki, elephant foot](https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot)
- Bambu Studio refuses to slice when the selected filament has a bed temperature of 0 for the selected plate type ("does not support filament" error, raised in `Print::validate()`). -- [Print.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Print.cpp) L1669-1689; details in [gui-checks.md](../02-bambu-studio/gui-checks.md)
- Bridge and support settings, such as Max bridge length, only take effect once Process > Support > Enable support is on. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support); details in [support-settings.md](../02-bambu-studio/support-settings.md)

## In practice
1. Choose orientation by measurement, not by eye. For each candidate orientation, compute in code: overhang area (mm2 and %), plate-contact area, number of first-layer islands, and the widest unsupported span. Pick the one with the least overhang and the most plate contact that still puts the right face down.
2. Put hidden or functional faces on the plate and keep visible faces up or vertical. If a visible face must face down, choose the plate for the finish you want (textured or glossy) or plan post-finishing.
3. Check the assembly path together with orientation: a part that prints well but cannot be slid or dropped into its mating part is still a failure. Check both before slicing.
4. After slicing, confirm that the support length in the G-code is zero for an orientation meant to be self-supporting, and that the plate type matches the filament. Verify on your own printer.
5. Seam placement is a separate visible-face decision: see [seam-painting.md](../02-bambu-studio/seam-painting.md) and [quality-tab-settings.md](../02-bambu-studio/quality-tab-settings.md).

## Not verified / open questions
- No public side-by-side comparison of Textured vs Smooth PEI finish on the same part was found. Print your own comparison.
- How layer direction affects strength under load is not covered here; see the [07-engineering](../07-engineering/index.md) category.
- The Elephant foot compensation UI path comes from the wiki, which names no Bambu Studio version (label not verified in 2.8.02.61).

Sources:
- https://wiki.bambulab.com/en/software/bambu-studio/support -- threshold angle, enable support
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang -- overhang angle convention
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- `support_threshold_angle` default
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Print.cpp -- bed-type vs filament check
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process -- H2C preset threshold values
- https://wiki.bambulab.com/en/filament-acc/acc/plates -- plate finish, adhesion, glue, removal temperature
- https://wiki.bambulab.com/en/filament-acc/acc/pei-plate-clean-guide -- PEI cleaning
- https://wiki.bambulab.com/en/general/filament-guide-material-table -- no acetone
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot -- elephant foot cause and setting
