# Pi GPIO power-on state, and switching a load with a PhotoMOS or SSR

Applies to: any build (printer-independent) · Raspberry Pi 5 (RP1 GPIO), Panasonic AQV252G PhotoMOS relay, Crydom DC60S3 SSR
Verified: 2026-10-04

## Facts

### Pi GPIO at power-on
- All GPIO pins revert to general-purpose inputs on power-on reset, and the default pull states are applied; most GPIOs have a default pull. So a pin is an input, not a driven output, until software configures it. - [Raspberry Pi documentation: GPIO pads, power-on states](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- RP1 (the Pi 5's I/O chip) PADS_BANK0, Table 21: OD (output disable, which overrides peripheral output enable) resets to 1 (disabled); IE (input enable) resets to 0 (disabled); PUE and PDE (pull-up and pull-down enable) reset to values that vary per pin. - [RP1 Peripherals datasheet](https://datasheets.raspberrypi.com/rp1/rp1-peripherals.pdf) (build date 2023-11-07)

### Switching parts
- Panasonic AQV252G PhotoMOS: continuous load current 2.5 A; load voltage 60 V (recommended maximum 48 V); ON resistance maximum 0.12 Ohm; LED operate current maximum 3.0 mA; LED turn-off current minimum 0.2 mA; recommended LED drive current 5-30 mA; UL Recognized (File E191218). - [Panasonic AQV252G product page](https://industry.panasonic.com/global/en/products/control/relay/photomos/number/aqv252g)
- Crydom DC60S3 SSR: minimum turn-on voltage 3.5 VDC; must-turn-off voltage 1 VDC; maximum on-state drop at rated current 1 V (3 A part); minimum load current 20 mA; UL Approved. - [Crydom DC60S3 datasheet (third-party host)](https://www.uscomponent.com/datasheet/dc60s3.pdf) (Rev. 060216)

## In practice
- A 3.3 V GPIO cannot reliably drive the DC60S3: its 3.5 VDC minimum turn-on is above 3.3 V. Use a 5 V-side driver or another part.
- The AQV252G can be driven straight from a Pi pin: its LED needs at most 3.0 mA to operate, inside the RP1 pad drive strengths (see [level-shifting-3v3-to-ws2812b.md](../08-electronics-lighting/level-shifting-3v3-to-ws2812b.md)). Add a series resistor to set the LED current. Note that the 3.0 mA operate figure sits below the 5-30 mA recommended drive range; aim inside the recommended range if the pad strength allows.
- During boot the pin is output-disabled until Linux configures it. If the load must have a known default state before that, set it with an external pull resistor, not with an assumption about the Pi's boot-time pin state.
- Keep the AQV252G load within 2.5 A and 48 V (recommended); it is a small-load relay, not a mains part.

## Not verified / open questions
- Whether a newer RP1 datasheet build changes the PADS_BANK0 reset values.
- The per-pin default pull of whichever GPIO you choose (PUE/PDE vary per pin); check the RP1 table for that pin.
- The DC60S3's full load-voltage and surge ratings were not re-checked.

Sources:
- https://www.raspberrypi.com/documentation/computers/raspberry-pi.html - GPIO power-on reset behaviour
- https://datasheets.raspberrypi.com/rp1/rp1-peripherals.pdf - RP1 PADS_BANK0 reset values
- https://industry.panasonic.com/global/en/products/control/relay/photomos/number/aqv252g - AQV252G ratings
- https://www.uscomponent.com/datasheet/dc60s3.pdf - DC60S3 turn-on/turn-off voltage, on-state drop, minimum load
