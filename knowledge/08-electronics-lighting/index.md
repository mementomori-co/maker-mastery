# 08 Electronics and lighting - index

LED strips, power supplies, wiring, protection and diffusion for printed builds. Every fact carries a public source; numbers carry their conditions. These notes are planning references, not a substitute for the maker's own datasheet check or for local electrical codes. Anything mains-connected belongs to a qualified person.

## Addressable LEDs and control
- [ws2812b-power.md](ws2812b-power.md) - WS2812B per-channel current (3 x 16 mA), 3.5 to 5.3 V supply limit, Adafruit's 60 mA / 20 mA per-pixel budgeting figures.
- [level-shifting-3v3-to-ws2812b.md](level-shifting-3v3-to-ws2812b.md) - why a 3.3 V Pi 5 or ESP32 pin needs a level shifter for WS2812B; SN74AHCT125 family specs, pin handling, WS2812B timing and the reset-time contradiction.
- [wled-abl-current-limiting-and-json-api.md](wled-abl-current-limiting-and-json-api.md) - WLED first setup, brightness limiter fields and the real 850 mA default, per-output limits, ESP32 pin choice, JSON API off switch.
- [wled-temperature-usermods.md](wled-temperature-usermods.md) - which WLED usermods read a DS18B20, which one acts on a threshold, and why neither does both.

## Strips and power
- [ws2812b-strips-injection-and-5v-supplies.md](ws2812b-strips-injection-and-5v-supplies.md) - strip W/m by density, power-injection practice, Mean Well LRS 5 V supplies and wire table, GST60A05 rating and tolerance, a worked voltage-drop budget.
- [analog-rgb-strips-and-12-24v-supplies.md](analog-rgb-strips-and-12-24v-supplies.md) - 12 V / 24 V bricks (GST60A/90A/120A), DC-DC converters (DDR, RSD, TMDC), mains cords and splitters, analog and COB strips, a 24 V fan.
- [power-supplies-and-pis.md](power-supplies-and-pis.md) - what a power-limited (PIS) circuit means in IEC 62368-1 wording, and worked fuse-bound arithmetic.

## Protection, wiring and enclosures
- [fuses-and-holders-dc.md](fuses-and-holders-dc.md) - small fuses and holders with real DC ratings, blade-fuse temperature derating, opening times.
- [connectors-for-led-power.md](connectors-for-led-power.md) - JST VH/EL/VL/VYH/XH ratings by wire gauge, 4-pin DIN, DC barrel jacks (no 2.1 mm panel jack found), WAGO lever splices.
- [wire-gauge-ampacity.md](wire-gauge-ampacity.md) - AWG chassis vs power-transmission current and resistance (community rule of thumb).
- [cable-glands-and-strain-relief.md](cable-glands-and-strain-relief.md) - gland clamping ranges, cable ODs, passing a C13 plug through a wall, ribbon and trace-width data, strain relief.
- [enclosures-hammond-1554.md](enclosures-hammond-1554.md) - Hammond 1554HL/JL key dimensions, 5VA rating, worked gland-capacity arithmetic.

## Light diffusion
- [fdm-led-diffusion.md](fdm-led-diffusion.md) - why translucent PETG shows through, what helps a printed panel diffuse (colour, thickness, distance), and why the clarity recipe is the wrong tool.
