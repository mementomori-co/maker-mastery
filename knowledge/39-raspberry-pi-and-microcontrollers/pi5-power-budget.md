# Raspberry Pi 5 power and thermal budget

Applies to: Raspberry Pi 5 (printer-independent) · firmware and bootloader as documented by Raspberry Pi at the time of checking
Verified: 2026-10-03

## Facts

### Supply and USB budget
- Recommended supply for a Pi 5: 5.0 A. Typical bare-board active current is 800 mA (a typical figure, not a maximum). The official recommendation is the 27 W USB-C Power Supply. - [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html), [power-supplies.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc)
- Downstream USB budget: 1.6 A total when the supply is recognised as 5 A at 5 V over USB-PD; otherwise 600 mA. The fan connector draws from the same limit. - [power-supplies.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc), [frequency-management.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)
- With a detected 5 A supply the docs describe 5 W extra for downstream USB and 5 W extra onboard budget, shared between the USB ports and the fan header. Without a 5 A PDO, USB stays at 600 mA and USB boot is disabled unless the power button is pressed. - [usb-bus-on-raspberry-pi.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/usb-bus-on-raspberry-pi.adoc), [USB Power Delivery on Raspberry Pi 5 white paper](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf)
- `usb_max_current_enable` (read with `vcgencmd get_config`): 0 means the low USB limit was set at boot, non-zero means the 1.6 A limit is on. The high limit turns on automatically only if the PSU claims 5 A over USB-PD, or if `usb_max_current_enable=1` is set in `config.txt`. A 5 V feed through the GPIO header or pogo pins does not claim 5 A. - [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html), [configuration reference](https://www.raspberrypi.com/documentation/computers/configuration.html)
- Official 27 W USB-C PSU: 5.1 V at 5.0 A; PD profiles 9 V/3 A, 12 V/2.25 A, 15 V/1.8 A, all capped at 27 W; input 100-240 VAC; 1.2 m 17 AWG cable; in production until at least January 2035. - [Raspberry Pi 27W USB-C Power Supply](https://www.raspberrypi.com/products/27w-power-supply/)

### Board draw
- Peak power under the most intensive workloads is about 12 W (Pi 4: about 8 W). This is a 2023 launch-article figure, not a datasheet spec. - [Introducing Raspberry Pi 5](https://www.raspberrypi.com/news/introducing-raspberry-pi-5/)
- Off-state power is 1-1.4 W by default; `POWER_OFF_ON_HALT=1` in the bootloader EEPROM config brings it to about 0.01 W. - [power-supplies.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc)
- There is no official Pi 5 row in the Boot/Idle/Video/Stress/Halt power table (it covers Pi 1B+ to 4B). - [power-supplies.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc)
- GPIO: 50 mA combined across all pins, 16 mA per pin. HDMI: 50 mA. These are generic across Pi models. USB HID devices (keyboard, mouse) draw 100-1000 mA each. - [power-supplies.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc)
- PCIe FFC connector (16-way, 0.5 mm pitch): 5 V on pins 1 and 2 at 500 mA each, 1 A / about 5 W total. It carries PCIe Gen 2.0 x1; the Pi 5 is not certified for Gen 3.0. - [RP-008298-DS](https://pip.raspberrypi.com/documents/RP-008298-DS), [pcie.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/pcie.adoc)

### Temperature and cooling
- The product brief gives an operating temperature of 0 C to 70 C and never says "ambient"; it is not stated whether this means air around the board. - [Raspberry Pi 5 product brief](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008348-DS-8-raspberry-pi-5-product-brief.pdf)
- Arm cores throttle progressively between 80 C and 85 C; at 85 C or above both Arm cores and GPU throttle, on all models. The limit can be lowered in config, not raised. The 60 C soft limit (`temp_soft_limit`) is documented for Pi 3A+/3B+ only, and Pi 4 has "no soft limit defined". - [frequency-management.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc), [overclocking.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/config_txt/overclocking.adoc)
- Default Pi 5 fan curve: off below 50 C; 30 % at 50 C; 50 % at 60 C; 70 % at 67.5 C; 100 % at 75 C; 5 C hysteresis on the way down. Configurable with `fan_tempN`, `fan_tempN_hyst` and `fan_tempN_speed`. - [frequency-management.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)
- A heatsink is not needed to prevent damage (throttling protects the SoC), but a heatsink or fan reduces throttling. Official options: the Active Cooler and the Case for Raspberry Pi 5. - [frequency-management.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)
- Fan connector (4-pin JST-SH, 1 mm pitch): pin 1 +5 V, pin 2 PWM, pin 3 GND, pin 4 tach. - [frequency-management.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)
- Active Cooler: 5 V via the fan header, PWM with tach, 1.09 CFM maximum airflow, 8000 RPM +/-15 % maximum, MTTF 379,000 h at 25 C. The brief warns against heat from any external source and gives no numeric ambient range. - [Active Cooler product brief](https://pip.raspberrypi.com/documents/RP-008188-DS-active-cooler-product-brief.pdf)
- `vcgencmd get_throttled` bits: 0x1 undervoltage now; 0x2 Arm frequency capped; 0x4 throttled now; 0x8 soft temperature limit active; 0x10000, 0x20000, 0x40000, 0x80000 the same four events "has occurred". - [Raspberry Pi OS documentation](https://www.raspberrypi.com/documentation/computers/os.html)

### Example external 5 V supplies
- Mean Well GST60A05-P1J (desktop brick): 5 V, 6 A, 30 W max, +/-5.0 % tolerance, hiccup overload protection at 105-150 % (auto-recovery), IEC320-C14 inlet, Class I; figures at 230 VAC, rated load, 25 C, with derating curves. - [Mean Well GST60A spec](https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF)
- Mean Well LRS-50-5 (enclosed): 5 V, 10 A, 50 W, adjustable 4.5-5.5 V, +/-2.0 % tolerance. - [Mean Well LRS-50 spec](https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF)

### USB button encoders
- The Ultimarc I-PAC 4 and Brook Universal Fighting Board product pages publish no current-draw figure. - [Ultimarc I-PAC 4](https://www.ultimarc.com/control-interfaces/i-pacs/i-pac4-board/), [Brook UFB](https://www.brookaccessory.com/detail/06960737/)

## In practice
- Know which supply feeds the Pi. The official 27 W supply (or any supply that negotiates 5 A over USB-PD) gives 1.6 A downstream USB; any other path caps USB at 600 mA and disables USB boot unless you force `usb_max_current_enable=1`.
- Budget the board's own draw (about 800 mA active, about 12 W peak) separately from the USB pool. There is no official idle figure; use 1-1.4 W (or about 0.01 W with `POWER_OFF_ON_HALT=1`) for the off state.
- Do not design enclosure air to 70 C. Design to the documented SoC thresholds (80 C progressive, 85 C hard) and do not carry over the Pi 3's 60 C soft limit. For enclosure heat maths see [enclosure-thermal-budget.md](../07-engineering/enclosure-thermal-budget.md).
- Budget a PCIe HAT or M.2 adapter separately: 1 A at 5 V, Gen 2.0 x1.
- Of the two example bricks, GST60A05-P1J is the lower-headroom external option; LRS-50-5 gives more headroom if LEDs or a screen share the 5 V rail. For LED power and wire sizing see [ws2812b-power.md](../08-electronics-lighting/ws2812b-power.md) and [wire-gauge-ampacity.md](../08-electronics-lighting/wire-gauge-ampacity.md).
- Measure USB encoder draw (bench meter, or the USB descriptor's `bMaxPower`) instead of guessing.
- Check `vcgencmd get_throttled` after a stress run; any undervoltage bit means the supply or cable is short.

## Not verified / open questions
- A 60 C / 1.4-1.2 GHz soft limit is sometimes quoted for the Pi 5; no official source documents it for the Pi 5.
- The exact text `vcgencmd get_config usb_max_current_enable` prints is not documented; read it on the device.
- Display boards that power the Pi through GPIO pogo pins (for example the 52Pi EP-0188) do not state which path feeds the Pi; if it is the pogo pins, the Pi sees no 5 A PD claim and USB falls back to 600 mA. That vendor's wiki text and images also disagree on brightness. - [52Pi EP-0188 wiki](https://wiki.52pi.com/index.php?title=EP-0188)

Sources:
- https://www.raspberrypi.com/documentation/computers/raspberry-pi.html - PSU recommendation, USB budget, GPIO/HDMI draw, `usb_max_current_enable`
- https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc - power figures, off-state power, absence of a Pi 5 idle row
- https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc - throttle temperatures, fan curve, fan pinout, cooling options
- https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/config_txt/overclocking.adoc - soft limit is Pi 3A+/3B+ only
- https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/usb-bus-on-raspberry-pi.adoc - 600 mA / 1.6 A USB figures
- https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/pcie.adoc - PCIe Gen 2.0 x1
- https://www.raspberrypi.com/documentation/computers/os.html - `get_throttled` bits
- https://www.raspberrypi.com/documentation/computers/configuration.html - `usb_max_current_enable`
- https://www.raspberrypi.com/products/27w-power-supply/ - official 27 W PSU
- https://www.raspberrypi.com/news/introducing-raspberry-pi-5/ - about 12 W peak
- https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008348-DS-8-raspberry-pi-5-product-brief.pdf - operating temperature
- https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf - 5 W / 5 W budget, USB boot fallback
- https://pip.raspberrypi.com/documents/RP-008188-DS-active-cooler-product-brief.pdf - Active Cooler spec
- https://pip.raspberrypi.com/documents/RP-008298-DS - PCIe FFC power pins
- https://www.meanwell.com/Upload/PDF/GST60A/GST60A-SPEC.PDF - GST60A05-P1J
- https://www.meanwell.com/Upload/PDF/LRS-50/LRS-50-SPEC.PDF - LRS-50-5
- https://www.ultimarc.com/control-interfaces/i-pacs/i-pac4-board/ - no published current
- https://www.brookaccessory.com/detail/06960737/ - no published current
- https://wiki.52pi.com/index.php?title=EP-0188 - pogo-pin power path question
