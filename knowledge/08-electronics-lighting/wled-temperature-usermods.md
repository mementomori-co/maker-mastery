# WLED temperature usermods: DS18B20 reading, internal-sensor guard, fan control
Applies to: any build (printer-independent) · WLED firmware v16.0.1 (usermod files identical to `main` when checked)
Verified: 2026-10-04

## Facts

### Temperature (Dallas 1-Wire) usermod
- Reads an attached 1-Wire sensor such as a DS18B20. The source recognises five Dallas family codes: DS18S20 (0x10), DS1822 (0x22), DS18B20 (0x28), DS1825 (0x3B), DS28EA00 (0x42). - [Temperature/readme.md](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Temperature/readme.md), [Temperature/Temperature.cpp](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Temperature/Temperature.cpp)
- Default data pin: `TEMPERATURE_PIN 18` on ESP32 and 14 on ESP8266, overridable at compile time; the README says the pin and other parameters can also be changed at runtime on the Usermods settings page. - [UsermodTemperature.h](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Temperature/UsermodTemperature.h), [Temperature/readme.md](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Temperature/readme.md)
- It has no over-temperature action: no threshold variable exists, and its only `applyPreset()` call is commented out. Outputs are the Info page readout, MQTT and Domoticz, plus an LED effect that maps the reading onto a palette (default range 15 to 30 °C). - [Temperature/Temperature.cpp](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Temperature/Temperature.cpp)
- It needs a custom build: add `Temperature` to `custom_usermods` in `platformio_override.ini`. The v16.0.1 release ships only standard binaries (no usermod builds), and no environment in the shipped `platformio.ini` includes `Temperature`. - [Temperature/readme.md](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Temperature/readme.md), [platformio.ini](https://raw.githubusercontent.com/wled/WLED/v16.0.1/platformio.ini), [WLED latest release (API)](https://api.github.com/repos/wled/WLED/releases/latest)
- The docs show the mechanism with an example environment extending `env:esp32dev` and say `custom_usermods` replaced the older `usermods_list.cpp` approach from WLED 16. - [WLED docs: Custom features](https://kno.wled.ge/advanced/custom-features/)

### Internal_Temperature_v2 usermod (the one with a guard action)
- Triggers a configurable "warning" preset when a threshold is crossed. It reads the ESP chip's own die temperature via `temperatureRead()`, not an external DS18B20. - [Internal_Temperature_v2/readme.md](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Internal_Temperature_v2/readme.md), [Internal_Temperature_v2.cpp](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Internal_Temperature_v2/Internal_Temperature_v2.cpp)
- Source defaults: activation threshold 95.0 °C, reset margin 2.0 °C, preset to activate 0 (disabled); on trigger it calls `applyPreset()`. All three are runtime settings. - [Internal_Temperature_v2.cpp](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Internal_Temperature_v2/Internal_Temperature_v2.cpp)
- Its build name in `custom_usermods` is `Internal_Temperature` (not the folder name). One release environment (`waveshare_esp32s3_32MB_hub75`) includes it; the standard `esp32dev` build does not. - [platformio.ini](https://raw.githubusercontent.com/wled/WLED/v16.0.1/platformio.ini)

### PWM_fan usermod
- Depends on the Temperature usermod for its reading and ramps a PWM fan; the README says the fan reaches 100 % when the reading is 3 °C above the threshold. - [PWM_fan/readme.md](https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/PWM_fan/readme.md)

## In practice
- No stock WLED usermod takes an external DS18B20 reading and performs an automatic guard action (preset change, brightness drop, shutdown). Temperature only reports; Internal_Temperature_v2 guards but reads only the ESP die; PWM_fan drives a fan, not the LEDs.
- A simple design that needs no custom firmware: let another computer on the network (for example a Raspberry Pi) read the 1-Wire sensor and send a preset or `{"on": false}` to the WLED JSON API when a threshold is crossed (see [wled-abl-current-limiting-and-json-api.md](wled-abl-current-limiting-and-json-api.md)). This is a design suggestion, not a tested setup.
- If you want the guard inside WLED, you need a custom build with `custom_usermods`, and probably your own code joining the two usermods' logic.
- A firmware guard is a convenience, not a safety device; keep hardware protection (fuses, supply limits, thermal cutoffs) in place regardless.

## Not verified / open questions
- No WLED documentation of a combined build (DS18B20 reading feeding a threshold guard) was found.
- Changes after v16.0.1 were not checked.

Sources:
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Temperature/readme.md - DS18B20 usermod, custom build requirement
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Temperature/Temperature.cpp - family codes, no guard action, LED effect
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Temperature/UsermodTemperature.h - default pins
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/platformio.ini - which environments include which usermods
- https://api.github.com/repos/wled/WLED/releases/latest - release asset list
- https://kno.wled.ge/advanced/custom-features/ - custom_usermods mechanism
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Internal_Temperature_v2/readme.md - guard preset description
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/Internal_Temperature_v2/Internal_Temperature_v2.cpp - threshold defaults, die sensor
- https://raw.githubusercontent.com/wled/WLED/v16.0.1/usermods/PWM_fan/readme.md - fan ramp rule
