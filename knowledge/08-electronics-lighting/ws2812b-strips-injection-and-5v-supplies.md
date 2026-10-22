# WS2812B-family strips: strip specs, power injection and 5 V supplies
Applies to: any build (printer-independent) · WS2812B / WS2815 / SK6812 addressable strips, Mean Well LRS-50-5 / LRS-100-5 and GST60A05 5 V supplies
Verified: 2026-10-04

## Facts

### Strip specs (one vendor's store pages; marketing figures)
- BTF-Lighting sells its 5 V WS2812B strip at 30, 60, 96, 100 and 144 LEDs/m, with stated maximum power at 5 V input of 6, 11, 17, 18 and 25 W/m respectively; no brightness or colour condition is given. Every LED is a cut point, with no cut pitch in mm. FPC width is stated (12 mm) only for 74 and 96 LEDs/m rows. - [BTF-Lighting WS2812B page](https://www.btf-lighting.com/products/ws2812b-rgb-addressable-led-strip-dc5v) (vendor, undated)
- Computed from those W/m figures at 5 V: 30/m about 1.2 A/m (40 mA per LED), 60/m about 2.2 A/m (36.7 mA), 96/m about 3.4 A/m (35.4 mA), 100/m about 3.6 A/m (36.0 mA), 144/m about 5.0 A/m (34.7 mA). These derive from a marketing figure, not a datasheet maximum. - computed from the [BTF-Lighting WS2812B page](https://www.btf-lighting.com/products/ws2812b-rgb-addressable-led-strip-dc5v)
- The WS2812B datasheet calls its 3 x 16 mA an operating current, not a stated maximum, so "48 mA per LED" is not a datasheet worst case. - [WS2812B datasheet, Triopak host](https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf)
- The vendor's 12 V WS2815 strip has a backup data line (the chain keeps running past one dead pixel) and is sold at 30, 60, 100 and 144 LEDs/m; the page gives no mA or W/m figure. - [BTF-Lighting WS2815 page](https://www.btf-lighting.com/products/ws2815-rgb-addressable-led-strip-dc12v) (vendor)
- The vendor's 5 V SK6812 RGBW strip lists the same W/m figures as the 3-channel RGB strip (6 W/m at 30/m, 11 at 60/m, 25 at 144/m) although it has a fourth (white) channel; treat as a marketing figure, not a measured RGBW worst case. - [BTF-Lighting SK6812 RGBW page](https://www.btf-lighting.com/products/5v-sk6812-rgbw-addressable-led-strip) (vendor)

### Power injection (Adafruit NeoPixel guide, vendor guidance for the NeoPixel family)
- Aim for 1 m or less of strip between any pixel and a power feed, for colour consistency (not a hard electrical limit). Feed at the head, tail, middle or several points, laid out "as branches of a tree rather than one continuous line." - [Adafruit: Powering NeoPixels](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels)
- Fit a 500 to 1000 µF capacitor rated 6.3 V or higher across + and - at the strip before connecting power, to absorb transients from brightness changes. - [Adafruit: Powering NeoPixels](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels)
- Put a 300 to 500 Ω resistor in the data line at the end nearest the first pixel. Avoid connecting a strip to a live circuit; if you must, connect ground first, then +5 V, then data, and disconnect in reverse. - [Adafruit: Best Practices](https://learn.adafruit.com/adafruit-neopixel-uberguide/best-practices)

### 5 V supplies: Mean Well LRS-50-5 and LRS-100-5 (datasheets dated 2025-04-07)
- LRS-50-5: 5 V, 10 A rated (0 to 10 A), 50 W, output adjustable 4.5 to 5.5 V. Case 99 x 82 x 30 mm (+/-1 mm), 0.21 kg, free-air convection cooling. Terminal order: 1 AC/L, 2 AC/N, 3 FG, 4 -V, 5 +V. - [LRS-50 datasheet](https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF)
- LRS-100-5: 5 V, 18 A rated (0 to 18 A), 90 W, adjustable 4.5 to 5.5 V; case 129 x 97 x 30 mm, 0.33 kg; efficiency typ. 86 % at 230 VAC input, rated load, 25 °C. - [LRS-100 datasheet](https://www.meanwell.com/Upload/PDF/LRS-100/LRS-100-SPEC.PDF)
- Both list working temperature -30 to +70 °C with a pointer to the derating curve: full current applies only in the curve's full-load region. Both list UL 62368-1 among their safety standards, but some marks on the sheets carry a "12/24 V only" style caveat, so which marks cover the 5 V model is not clear from the text. - [LRS-50 datasheet](https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF); [LRS-100 datasheet](https://www.meanwell.com/Upload/PDF/LRS-100/LRS-100-SPEC.PDF)
- The LRS-50 spec sheet gives no wire size or torque. Mean Well's enclosed-type manual groups the LRS family under a terminal screw "M3.5, 8-10" with no unit on that row (the next table in the manual uses kgf-cm, so kgf-cm is an inference). - [Mean Well Enclosed Type manual](https://www.meanwell.com/Upload/PDF/Enclosed_Type_EN.pdf)
- The same manual's generic wire table (all enclosed families): AWG 18 / 16 / 14 / 12 / 10 / 8 (0.75 / 1.00 / 1.5 / 2.5 / 4 / 6 mm2) for rated current up to 6 A / 6-10 A / 10-16 A / 16-25 A / 25-32 A / 32-40 A, with each wire derated to 80 % when 5 or more wires connect to the unit. The manual also says every strand of a stranded wire must enter the terminal. - [Mean Well Enclosed Type manual](https://www.meanwell.com/Upload/PDF/Enclosed_Type_EN.pdf)

### 5 V supplies: Mean Well GST60A05 desktop adapter (spec sheet 2026-04-03)
- Despite the family name, the 5 V model is rated 6 A / 30 W, not 60 W. Class I with a built-in IEC 320-C14 inlet; case 125 x 50 x 31.5 mm (+/-1 mm), 0.305 kg; 5 to 9 V models use a UL2464 16 AWG output cord, 1000 +/-50 mm, with the P1J plug (2.1 x 5.5 x 11 mm, centre positive). - [GST60A datasheet](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF)
- Voltage tolerance by output: 5 / 7.5 / 9 V +/-5.0 %; 12 to 24 V +/-3.0 %; 48 V +/-2.5 %. Line regulation +/-1.0 % on every model. The sheet's tolerance figure already includes set-up tolerance, line and load regulation (do not stack them again). Conditions: 230 VAC input, rated load, 25 °C, 70 % RH; output measured at the plug terminal at 50 % load. Temperature coefficient +/-0.03 %/°C over 0 to 50 °C. - [GST60A datasheet](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF)
- The "7.5 A max." printed in the plug table belongs to Mean Well's separately sold quick-adapter accessory, not to the supply's output or the moulded P1J plug. - [GST60A datasheet](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF) (pp. 4-5)

## In practice
- Size a strip from the vendor's W/m figure for that exact product. Where no figure is published (WS2815, SK6812 RGBW), use 60 mA per pixel (see [ws2812b-power.md](ws2812b-power.md)).
- Fit the reservoir capacitor and data resistor on every run, keep each pixel within about 1 m of a feed, and wire feeds tree-style.
- The LRS trim pot (4.5 to 5.5 V) can offset cable drop, but stay at or below 5.3 V at the first pixel (WS2812B absolute maximum).
- Per Mean Well's wire table, an LRS-50-5 at its full 10 A calls for AWG 14 at its terminals (the 10-16 A row), not AWG 16 or 18.
- Worked voltage-drop budget for an example 5 V, 3 A run: start from the supply tolerance (+/-5 % on a GST60A05 = 4.75 V worst case), then subtract each series drop: cord (I x R for both conductors, see [wire-gauge-ampacity.md](wire-gauge-ampacity.md)), each connector contact (JST VH 10 mΩ max initial, two contacts per pair: 3 A x 0.02 Ω = 0.06 V), and any fuse's cold resistance (see [fuses-and-holders-dc.md](fuses-and-holders-dc.md)). If the far pixel lands below 4.5 V, add an injection point or move the supply.
- Connector and wire choices for these currents are in [connectors-for-led-power.md](connectors-for-led-power.md); cable glands are in [cable-glands-and-strain-relief.md](cable-glands-and-strain-relief.md).

## Not verified / open questions
- Whether the BTF page says anything about voltage drop or injection distance in its images (only the text was searched).
- WS2815 and SK6812 chip datasheets: WorldSemi's download links were dead when checked, so no chip current or voltage is verified for them. - [WorldSemi RGBIC page](https://www.world-semi.com/products-rgbic-led.html)
- Mean Well's DC-plug guide (https://www.meanwell.com/upload/pdf/DC_plug.pdf) is image-only, so plug ratings could not be cross-checked there.
- The LRS terminal torque unit (kgf-cm) is inferred, not stated on the LRS row.
- Using a microcontroller's PIO or another driver instead of a level shifter was not checked.

Sources:
- https://www.btf-lighting.com/products/ws2812b-rgb-addressable-led-strip-dc5v - WS2812B strip densities, W/m, cut points
- https://www.btf-lighting.com/products/ws2815-rgb-addressable-led-strip-dc12v - WS2815 12 V strip
- https://www.btf-lighting.com/products/5v-sk6812-rgbw-addressable-led-strip - SK6812 RGBW W/m
- https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf - "operating current" wording
- https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels - injection distance, capacitor
- https://learn.adafruit.com/adafruit-neopixel-uberguide/best-practices - data resistor, connection order
- https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF - LRS-50-5 ratings, case, terminals
- https://www.meanwell.com/Upload/PDF/LRS-100/LRS-100-SPEC.PDF - LRS-100-5 ratings, case, efficiency
- https://www.meanwell.com/Upload/PDF/Enclosed_Type_EN.pdf - terminal screw, wire table, stranded-wire rule
- https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF - GST60A05 rating, cord, plug, tolerance definitions
- https://www.world-semi.com/products-rgbic-led.html - dead datasheet links for WS2815/SK6812
