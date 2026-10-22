# WLED: first setup, brightness limiter (ABL), multi-output ESP32 and the JSON API off switch
Applies to: any build (printer-independent) · WLED firmware v0.15.0, v0.15.4 and v16.0.1 (LED Settings page `wled00/data/settings_leds.htm`); original (classic) ESP32
Verified: 2026-10-04

## Facts

### First setup
- WLED is flashed from the browser with the official web installer at https://install.wled.me, which needs a board with at least 4 MB flash. The docs recommend an ESP32 over an ESP8266 for new projects and say ESP8266 support is ending. - [WLED docs: Getting started](https://kno.wled.ge/basics/getting-started/)
- After flashing, a stock build opens its own access point `WLED-AP` with password `wled1234`; the docs tell you to change that password at once because it is the same on every device. A custom build can rename the AP. - [WLED docs: Getting started](https://kno.wled.ge/basics/getting-started/)
- While connected to the AP, the UI is at `wled.me` or `4.3.2.1`. Both stop working once the device joins your Wi-Fi; then use its mDNS name or its DHCP address. - [WLED docs: Getting started](https://kno.wled.ge/basics/getting-started/)

### Automatic brightness limiter and current limits
- LED Settings has the checkbox "Enable automatic brightness limiter" (`name="ABL"`) in v0.15.0, v0.15.4 and v16.0.1. The docs describe it as lowering overall brightness so supply current stays below a set level, and say analog (PWM) and virtual LEDs cannot use it. - [WLED docs: Settings](https://kno.wled.ge/features/settings/); [settings_leds.htm v16.0.1](https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/settings_leds.htm)
- "Maximum PSU Current" (`name="MA"`) accepts 250 to 65000 mA. The firmware default is 850 mA (`ABL_MILLIAMPS_DEFAULT 850` in `wled00/const.h` in v0.15.4 and v16.0.1, with no `platformio.ini` override), not the 3000 mA the docs page states. The docs advise staying below about 1 A when LEDs are powered from the ESP board's 5 V pin. - [WLED docs: Settings](https://kno.wled.ge/features/settings/); [const.h v0.15.4](https://raw.githubusercontent.com/wled/WLED/v0.15.4/wled00/const.h); [const.h v16.0.1](https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/const.h)
- "Use per-output limiter" (`name="PPL"`) splits the budget into one limit per LED output; the docs recommend it for multiple outputs. When ticked, each output shows its own "PSU:" mA field (`name="MA<n>"`, 250 to 65000, initial value 250), the global field is hidden and is filled with the sum of the per-output values. The docs page does not mention the per-output field, but the firmware UI has it. - [WLED docs: Settings](https://kno.wled.ge/features/settings/); [settings_leds.htm v16.0.1](https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/settings_leds.htm)
- "mA/LED" defaults to the option "55mA (typ. 5V WS281x)"; "Custom" allows 1 to 255 mA per LED. - [settings_leds.htm v16.0.1](https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/settings_leds.htm)
- Per-output ABL arrived in the 0.15.0-a0 build cycle (changelog line "Per port Auto Brightness Limiter (ABL)"); the v0.15.0 release (2024-12-10) lists it. - [CHANGELOG.md](https://raw.githubusercontent.com/wled/WLED/main/CHANGELOG.md); [v0.15.0 release](https://github.com/wled/WLED/releases/tag/v0.15.0)

### Multi-output on a classic ESP32
- The getting-started guide recommends GPIO16 for an ESP32 data line and lists GPIOs 4, 13 and 16 to 33 as usable. - [WLED docs: Getting started](https://kno.wled.ge/basics/getting-started/)
- The multi-strip page says pin choice does not matter on an ESP32 except that input-only pins cannot be used; on a classic ESP32 those are 34 to 39. - [WLED docs: Multiple strips](https://kno.wled.ge/features/multi-strip/)
- The compatible-hardware page lists the SN74AHCT125 as the recommended level shifter. - [WLED docs: Compatible hardware](https://kno.wled.ge/basics/compatible-hardware/)
- Per-output labels in v16.0.1: `Color Order:`, `Start:`, `Length:`, `GPIO:`, `Use per-output limiter:`, and `Make a segment for each output:` (under "Show Advanced Settings"). The per-output `PSU:` field shows only when the limiter is ticked, and its minimum is forced to 0 for non-digital (analog) outputs. - [settings_leds.htm v16.0.1](https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/settings_leds.htm)
- The LED type name for plain RGB strips is "WS281x RGB", defined in firmware source, not the settings page. - [bus_manager.cpp v16.0.1](https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/bus_manager.cpp)
- Menu path: `Config` is a tab label in `index.htm`; `settings.htm` (title "WLED Settings") holds the `LED & Hardware` and `Pin Info` links; "LED Settings" is the page title of `settings_leds.htm`. - [index.htm](https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/index.htm), [settings.htm](https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/settings.htm), [settings_leds.htm](https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/settings_leds.htm) (all v16.0.1)

### JSON API
- `/json/state` field `bri` takes 0 to 255. The docs recommend using 1 to 255 and `on: false` to switch off, and say the state response never reports `bri` as 0. POSTing to `/json/state` or `/json` updates values. - [WLED docs: JSON API](https://kno.wled.ge/interfaces/json-api/)
- `{"on": "t"}` toggles the current state, so sent to a light that is already off it turns it on. With `on` false, `bri` keeps reporting the last brightness. - [WLED docs: JSON API](https://kno.wled.ge/interfaces/json-api/)

## In practice
- Path in the UI: Config > LED & Hardware (page "LED Settings") > Enable automatic brightness limiter, then Maximum PSU Current, or Use per-output limiter and each output's PSU: field.
- Always set the current limit yourself. A stock build boots at 850 mA, not 3000 mA, and each per-output field starts at 250 mA, not a computed share.
- Worked example: an example 5 V, 10 A supply feeding two outputs; set each output's PSU: field to its share with margin (for example 4000 mA and 4000 mA) so the sum stays under the supply's derated rating.
- GPIO18 and GPIO19 are a valid two-output pair on a classic ESP32: inside the 16 to 33 range, not input-only, not strapping pins (0, 2, 5, 12, 15) and not flash/PSRAM pins. Avoid GPIO19 on boards with wired Ethernet (it is an EMAC data pin), and check your exact module before trusting GPIO16, which is used by PSRAM on WROVER-type modules.
- Turn lights off with `{"on": false}`; never send `"t"` as an off command.
- After updating past v16.0.1, re-check ABL behaviour: the nightly changelog mentions an ABL rework.

## Not verified / open questions
- ABL changes after v16.0.1 (nightly entry "new ABL #4798") were seen but not read.
- The docs page has no version banner; its 3000 mA default was checked only against v0.15.0, v0.15.4 and v16.0.1 source.
- The GPIO19 Ethernet and GPIO16 PSRAM pin notes come from the Espressif module documentation, not from WLED; they were not re-checked for this note (not verified).

Sources:
- https://kno.wled.ge/basics/getting-started/ - web installer, AP defaults, UI address, recommended pins
- https://kno.wled.ge/features/settings/ - ABL toggle, Maximum PSU Current (3000 mA docs default), per-output limiter
- https://kno.wled.ge/interfaces/json-api/ - bri range, on/off and toggle behaviour
- https://kno.wled.ge/features/multi-strip/ - ESP32 pin rule, input-only pins 34 to 39
- https://kno.wled.ge/basics/compatible-hardware/ - SN74AHCT125 recommended level shifter
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/settings_leds.htm - field names, labels, per-output PSU field
- https://raw.githubusercontent.com/wled/WLED/v0.15.4/wled00/data/settings_leds.htm - same fields at v0.15.4
- https://raw.githubusercontent.com/wled/WLED/v0.15.0/wled00/data/settings_leds.htm - same fields at v0.15.0
- https://raw.githubusercontent.com/wled/WLED/v0.15.4/wled00/const.h - ABL_MILLIAMPS_DEFAULT 850
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/const.h - same default at v16.0.1
- https://raw.githubusercontent.com/wled/WLED/main/CHANGELOG.md - per-port ABL changelog placement
- https://github.com/wled/WLED/releases/tag/v0.15.0 - v0.15.0 release notes
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/bus_manager.cpp - "WS281x RGB" type name
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/settings.htm - LED & Hardware and Pin Info links
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/wled00/data/index.htm - Config tab label
