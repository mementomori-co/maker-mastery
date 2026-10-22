# Translucent vs transparent: definitions, optics, Bambu's clarity recipe, published transmission numbers
Applies to: both (wording and recipe are printer-independent; Bambu's example clarity 3MFs are X1C-only, no H2C version exists) · Bambu Studio 02.08.02.61
Verified: 2026-10-06

See also: [bambu-petg-family.md](bambu-petg-family.md), [bambu-pla-family.md](bambu-pla-family.md), [pla-vs-petg.md](pla-vs-petg.md), [third-party-filament-brands-tds.md](third-party-filament-brands-tds.md) (clarity numbers by brand).

## Facts

### Definitions
- ASTM D1003-21 covers luminous transmittance and haze of essentially transparent plastics, and says material with haze above 30 % is considered diffusing (tested instead under Practice E2387). The public abstract never uses the word "translucent". In standards terms: transparent = high transmittance with low haze; above 30 % haze = diffusing. — [ASTM D1003-21](https://www.astm.org/d1003-21.html)
- Bambu describes PLA Translucent as having a frosted, light-diffusing finish, and PETG Translucent as more see-through, ranging from tinted translucent to tinted transparent depending on parameters. Bambu says transparency varies with size, thickness, structure and print settings (speed, nozzle temperature, infill). — [PLA Translucent store page](https://us.store.bambulab.com/products/pla-translucent), [PETG Translucent store page](https://us.store.bambulab.com/products/petg-translucent), [PLA Translucent TDS V3.0](https://store.bblcdn.com/s7/default/729a8bf233e9474db25c8d5be1e64a00/Bambu_PLA_Translucent_Technical_Data_Sheet.pdf)
- Bambu explains why PETG is clearer: PLA is semi-crystalline and its internal grains scatter light, while PETG is amorphous, so PETG is generally more transparent. It also notes that complex shapes are hard to make highly transparent even with good settings. — [Bambu wiki: printing tips for translucent PLA/PETG](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)
- Bambu publishes no transmittance or haze figure for any filament. The PETG Translucent store page makes light-transmission claims with no number, and its TDS V1.0 has no optical row. — [PETG Translucent store page](https://us.store.bambulab.com/products/petg-translucent), [PETG Translucent TDS V1.0](https://store.bblcdn.com/s1/default/338c9cd853fd44d9b6ed354a49048e72/Bambu_PETG_Translucent_Technical_Data_Sheet.pdf)

### Naming in Bambu Studio
- No preset name and no `filament_type` in the system profiles contains "transparent". PETG Translucent colour 32101 is "Clear" (#00000000) in English (translated as "Transparent" in French and Spanish). The only English colour named "Transparent" is PC 60103. A description string pointing to Bambu's transparent-PETG wiki tips sits in the PETG Basic, PETG Matte and PETG Translucent `@base` presets and also in `SUNLU PETG @base`. — [filaments_color_codes.json](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/filaments_color_codes.json), [BBL filament folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament)
- The old wiki URL named in that description (`printing-tips-for-transparent-petg`) returned 404; the live page is the one linked here. — [Bambu wiki](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)

### Why prints come out translucent
- Prusa: trapped bubbles scatter light so most printed objects end up translucent rather than transparent, and a print is never completely transparent. — [Prusa blog: 3D printed lens and other transparent objects](https://blog.prusa3d.com/3d-printed-lens-and-other-transparent-objects_31231/)
- Taulman (archived): stacked oval threads tend to give a result that is not transparent and somewhat white. — [Taulman t-glase features, archived](https://web.archive.org/web/20191210212427/http://taulman3d.com/t-glase-features.html)
- Bambu: a larger nozzle means fewer lines and fewer seams between lines, which improves light transmittance; drying prevents moisture bubbles and voids that reduce transparency. — [Bambu wiki](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)

### Published transmission numbers and their status
| Maker / product | Number | Basis | Status |
|---|---|---|---|
| Polymaker PolyLite PETG | 90 % light transmission | GB/T 2410; no thickness, colour or printed-vs-moulded condition | Stands as a material figure — [TDS V5.4](https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyLite_PETG_TDS_EN_V5.4.pdf?v=1731954068), [Polymaker wiki](https://wiki.polymaker.com/polymaker-products/more-about-our-products/documents/technical-data-sheets/petg-pet/polylite-tm-petg) |
| Formfutura HDglass | 90 % transmittance; haze < 1.0 % | ASTM D1003; no thickness; TDS v4 (2016) | Stands as a material figure — [TDS](https://www.formfutura.com/web/content/256561?download=true), [product page](https://www.formfutura.com/hdglass) |
| Taulman t-glase | 92 % | no standard, no thickness; archived page only | Weak — [archived page](https://web.archive.org/web/20191224173057/http://taulman3d.com/t-glase-options.html) |
| Polymaker Panchroma Translucent PLA | "Transmission Distance" 8 (Cyan) to 21 (Natural) | millimetres of plastic light can pass through; not a percentage | Not comparable; no PETG value published — [Polymaker TD page](https://wiki.polymaker.com/polymaker-products/more-about-our-products/hex-codes-and-transmission-distances), [PolyLite Translucent PETG](https://shop.polymaker.com/products/polylite-translucent-petg) |
| Bambu (any line), eSUN, Extrudr, Prusament | none | words only, or no optical row on the TDS | None — [eSUN TDS](https://www.esun3d.com/media/esun/catalog/certification/product/PETG/eSUN_PETG_Filament_TDS_1.pdf), [Extrudr TDS](https://s3.extrudr.com/extrudr-media/datasheets/tds/tds-en/petg-bundle-TDS-en.pdf), [Prusament TDS 2022](https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf), [Prusament TDS 2023](https://prusament.com/wp-content/uploads/2023/07/PETG_V0_ENG.pdf) |
| Fiberlogy Easy PET-G | none | page says transparent and opaque versions exist; no figure | None — [product page](https://fiberlogy.com/en/filaments/petg-en/easy-petg-en/) |

- None of the published numbers states specimen thickness or whether it was moulded or printed, so none predicts a printed part. A LulzBot-branded t-glase sheet (dated 4-6-18 in its footer, 3 mm filament) suggests larger layer heights and a larger (0.50 mm) nozzle for more translucence. — [DigiKey-hosted t-glase sheet](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/751/T-Glase_Web.pdf)
- PolyLite Translucent PETG settings per Polymaker: 230-260 °C, bed 70-80 °C, 30-50 mm/s, fan 20 %; dry at 65 °C for 6 h only if it has absorbed moisture. — [Polymaker shop](https://shop.polymaker.com/products/polylite-translucent-petg)

### Bambu's clarity recipe (wiki "Printing Tips for Translucent PLA/PETG")
- Steps, paraphrased: dry the filament; use a 0.8 mm nozzle (recommended); use high temperature; raise the flow ratio; turn all fans off (Bambu warns this raises PLA warping risk); sand the surface after printing. — [Bambu wiki](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)
- With a 0.4 mm nozzle: 0.1 mm layers and 0.5 mm line width; 1 wall loop; no top or bottom shells; 100 % sparse infill at 0° or 90°; all speeds 20 mm/s. — [Bambu wiki](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)
- The example 3MFs are X1C only (Bambu says to transfer the settings for other printers). PETG 0.4 mm: based on `0.20mm Standard @BBL X1C`, 0.1 mm layers, 1 wall, no shells, 100 % aligned rectilinear infill at 0°, 20 mm/s, flow ratio 1.01, 270 °C, all fans 0, no spiral mode, no ironing, aligned seam; line widths 0.5 mm except top surface 0.42 mm; the filament preset derives from PETG Basic, not PETG Translucent. — [0.4 mm PETG 3MF](https://wiki.bambulab.com/filament-acc/filament/petg_-_transparent_parameters_-_0.4_mm_nozzle.3mf)
- PETG 0.8 mm 3MF: `0.40mm Standard @BBL X1C 0.8 nozzle`, PETG Basic-derived filament, 0.2 mm layers, 0.82 mm lines, 1 wall, no shells, 100 % aligned rectilinear, 20 mm/s, flow 1.01, 270 °C, fans 0. — [0.8 mm PETG 3MF](https://wiki.bambulab.com/filament-acc/filament/petg_-_transparent_parameters_-_0.8_mm_nozzle.3mf)
- PLA 0.4 mm 3MF: Generic PLA-derived, 0.1 mm layers, 0.5 mm lines (top surface 0.42), 1 wall, no shells, 100 % aligned rectilinear, 20 mm/s, flow 1.01, 230 °C, fans 0. — [0.4 mm PLA 3MF](https://wiki.bambulab.com/knowledge-sharing/transparent-petg/pla_-_transparent_parameters_-_0.4_mm_nozzle_.3mf)
- The recipe credits Rygar1432 ("How To Print Glass", Printables) for some parameters. — [Bambu wiki](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)
- Bambu gives no advice on vase mode, ironing or annealing for clarity; its 3MFs have spiral mode and ironing off, and the PETG TDS advise against annealing for mechanical reasons. Single-shell (vase-like) printing for clarity comes from Polymaker; Prusa found annealing for clarity warped the part. — [Polymaker: how to print transparent models](https://polymaker.com/how-to-print-transparent-models/), [Prusa blog](https://blog.prusa3d.com/3d-printed-lens-and-other-transparent-objects_31231/)
- Prusa's recipe for comparison: 100 % rectilinear infill, 0.05 mm layers, flow 112 %, infill/perimeter overlap 5 %, speed cut to 20 %, temperature 5 °C lower so the fan can stay off, sand to 1500 grit, then lacquer or polishing compound. — [Prusa blog](https://blog.prusa3d.com/3d-printed-lens-and-other-transparent-objects_31231/)
- Taulman's large-thread recipe (archived): 1.2 mm nozzle, 260 °C, 1.8 mm set line width, 12 mm/s, 1.6 mm layers. — [archived page](https://web.archive.org/web/20191224173057/http://taulman3d.com/t-glase-options.html)

## In practice
- A transparent part passes light with little scatter (haze under about 30 %): you see through it and an LED behind it shows as a point. A translucent part scatters light: the LED spreads into a glow and hides what is behind it.
- By Bambu's own wording, PLA Translucent is a diffuser (frosted); PETG Translucent is more see-through and moves toward transparent as the clarity settings are applied. Neither has a measured transmission or haze number.
- Settings decide the look more than the spool. Toward transparent: the clarity recipe above. Toward diffusing: a stock 0.20 mm process with several walls and normal infill, where line seams scatter light. — [Bambu wiki](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)
- PETG Translucent colours on the store: Gray (32100), Clear (32101), Pink (32200), Orange (32300), Olive (32500), Teal (32501), Light Blue (32600), Purple (32700), Brown (32800). There is no white or frosted variant, so for an even white glow use geometry (thicker diffuser, more LED distance) or another diffusing material. — [PETG Translucent store page](https://us.store.bambulab.com/products/petg-translucent)
- For heat near LEDs, compare HDT: PETG Translucent sits well above PLA Translucent (see [hdt-vicat-table.md](hdt-vicat-table.md)).
- For a see-through part, no Bambu line is sold as transparent. The only published haze number is Formfutura HDglass; Polymaker PolyLite PETG publishes 90 % transmission. Start from a Generic PETG preset plus the clarity recipe, and judge on a printed coupon.
- Diffusion and clarity for your part must come from a printed, lit test coupon on your own printer: no maker publishes printed-part transmission or haze with a thickness basis.

## Not verified / open questions
- Thickness and printed-versus-moulded basis of every published transmission number: not stated by any maker.
- The ASTM D1003 haze angle definition is behind a paywall; only the public abstract was read.
- Whether Bambu's recipe gives clarity on PETG Translucent (its 3MFs use PETG Basic): not stated by Bambu.
- The recipe has no H2C example; transferring it to the H2C is untested.

Sources:
- https://www.astm.org/d1003-21.html — D1003-21 scope, "diffusing" above 30 % haze
- https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg — Bambu recipe, PLA vs PETG reasoning, 3MF list, credits
- https://wiki.bambulab.com/filament-acc/filament/petg_-_transparent_parameters_-_0.4_mm_nozzle.3mf — 0.4 mm PETG 3MF
- https://wiki.bambulab.com/filament-acc/filament/petg_-_transparent_parameters_-_0.8_mm_nozzle.3mf — 0.8 mm PETG 3MF
- https://wiki.bambulab.com/knowledge-sharing/transparent-petg/pla_-_transparent_parameters_-_0.4_mm_nozzle_.3mf — 0.4 mm PLA 3MF
- https://us.store.bambulab.com/products/pla-translucent — PLA Translucent wording
- https://us.store.bambulab.com/products/petg-translucent — PETG Translucent wording and colours
- https://store.bblcdn.com/s7/default/729a8bf233e9474db25c8d5be1e64a00/Bambu_PLA_Translucent_Technical_Data_Sheet.pdf — PLA Translucent TDS V3.0
- https://store.bblcdn.com/s1/default/338c9cd853fd44d9b6ed354a49048e72/Bambu_PETG_Translucent_Technical_Data_Sheet.pdf — PETG Translucent TDS V1.0, no optical row
- https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/resources/profiles/BBL/filament/filaments_color_codes.json — Clear 32101 and Transparent naming
- https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyLite_PETG_TDS_EN_V5.4.pdf?v=1731954068 — PolyLite PETG 90 % GB/T 2410
- https://wiki.polymaker.com/polymaker-products/more-about-our-products/documents/technical-data-sheets/petg-pet/polylite-tm-petg — same row on the wiki
- https://wiki.polymaker.com/polymaker-products/more-about-our-products/hex-codes-and-transmission-distances — Transmission Distance definition
- https://shop.polymaker.com/products/polylite-translucent-petg — settings
- https://polymaker.com/how-to-print-transparent-models/ — single-shell guidance
- https://www.formfutura.com/hdglass — HDglass product page
- https://www.formfutura.com/web/content/256561?download=true — HDglass TDS v4
- https://web.archive.org/web/20191224173057/http://taulman3d.com/t-glase-options.html — t-glase 92 %, large-thread recipe
- https://web.archive.org/web/20191210212427/http://taulman3d.com/t-glase-features.html — t-glase wording
- https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/751/T-Glase_Web.pdf — LulzBot t-glase sheet
- https://blog.prusa3d.com/3d-printed-lens-and-other-transparent-objects_31231/ — bubbles, recipe, annealing warps
- https://www.esun3d.com/media/esun/catalog/certification/product/PETG/eSUN_PETG_Filament_TDS_1.pdf — eSUN, no number
- https://s3.extrudr.com/extrudr-media/datasheets/tds/tds-en/petg-bundle-TDS-en.pdf — Extrudr, no number
- https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf — no optical row
- https://prusament.com/wp-content/uploads/2023/07/PETG_V0_ENG.pdf — no optical row
- https://fiberlogy.com/en/filaments/petg-en/easy-petg-en/ — Fiberlogy wording, no figure
