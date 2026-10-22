# WS2812B power: per-LED current and supply-voltage limits
Applies to: any build (printer-independent) · WS2812B addressable RGB LED (WorldSemi datasheet in general circulation)
Verified: 2026-10-03

## Facts
- The WorldSemi WS2812B datasheet (cover dated Mar-2017) lists an operating current of 16 mA for each of the red, green and blue dies. "48 mA per LED" is the sum of the three channels, not a single datasheet figure, and the sheet gives no test condition (VDD, temperature) for it and no separate IC quiescent current. - [WS2812B datasheet, Triopak host](https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf)
- Absolute maximum supply voltage VDD is +3.5 to +5.3 V. The electrical characteristics are measured at TA -20 to +70 °C and VDD 4.5 to 5.5 V, a range wider than the absolute maximum; this is a contradiction inside the datasheet itself. Logic thresholds: VIH = 0.7 x VDD, VIL = 0.3 x VDD. - [WS2812B datasheet, Adafruit host](https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf); [Triopak host](https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf)
- The older 2013 copy of the datasheet contains only one current figure, the logic input leakage current of +/-1 µA; it gives no mA figure for the LED or the IC. In that copy the VIL row is mislabelled as a hysteresis row. - [WS2812B datasheet, Adafruit host](https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf)
- Adafruit's NeoPixel guide (covers the whole NeoPixel family, not only WS2812B) states each pixel draws up to 60 mA at full-brightness white, and gives 20 mA per pixel (one third of that) as a budgeting rule of thumb for typical content. This is vendor guidance, not a datasheet value, and it is higher than the datasheet's 3 x 16 mA. - [Adafruit NeoPixel Uberguide: Powering NeoPixels](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels) (vendor guide)

## In practice
- To size a power supply, budget 60 mA per pixel (Adafruit's full-white figure); it is more conservative than the datasheet's 48 mA sum. Use 20 mA per pixel only for typical animated content with a brightness limiter in place (see [wled-abl-current-limiting-and-json-api.md](wled-abl-current-limiting-and-json-api.md)).
- Keep the 5 V rail between 4.5 and 5.3 V so it sits inside both the characterisation range and the absolute maximum. Do not rely on 5.5 V just because the characterisation table lists it.
- Worked example: 120 pixels x 60 mA = 7.2 A at full white, before any margin for the supply's derating.

## Not verified / open questions
- The 5.3 V absolute maximum vs 5.5 V characterisation range contradiction is unresolved in the source document; treat 5.3 V as the limit.
- Other die revisions, batches and clone parts sold as "WS2812B" may carry different figures; only the 2013 and 2017 WorldSemi copies were checked.

Sources:
- https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf - 2017 WS2812B datasheet: per-channel operating current, VDD limits, VIH/VIL
- https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf - 2013 WS2812B datasheet: VDD limits, mislabelled VIL row, leakage current only
- https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels - Adafruit 60 mA max / 20 mA rule of thumb (vendor guide)
