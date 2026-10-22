# Level shifting 3.3 V GPIO to a WS2812B (5 V) data line
Applies to: any build (printer-independent) · Raspberry Pi 5 (RP1) GPIO, original ESP32 GPIO, TI SN74AHCT125 / SN74HCT245 / SN74AHCT1G125, Adafruit #1787, SparkFun BOB-12009, WS2812B
Verified: 2026-10-04

## Facts

### 3.3 V source side
- RP1 (the Pi 5 I/O chip) GPIO pads have selectable drive strength of 2, 4, 8 or 12 mA. The pads are fault tolerant (very little current flows into a pin held above 3.63 V while IOVDD is 0 V), and VDDIO can be set from 1.8 V to 3.3 V. - [RP1 Peripherals datasheet, release 1.1](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008370-DS-1-rp1-peripherals.pdf)
- The RP1 datasheet (release 1.1) has no numeric VOH/VOL/IOH/IOL electrical-characteristics table; a search of the full PDF for those terms finds only a register field. - [RP1 Peripherals datasheet](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008370-DS-1-rp1-peripherals.pdf)
- Raspberry Pi's GPIO voltage table covers only BCM2835/6/7/RP3A0 and BCM2711 (Pi 4), with no RP1/Pi 5 row. For reference only (not for a Pi 5): BCM2711 VOH is 2.6 V min at IOH 4 mA and VOL is 0.4 V max at IOL -4 mA, at the default 4 mA drive. The same page says an output is high (3.3 V) or low (0 V) and warns "Do not use 5V for 3.3V components." - [gpio-on-raspberry-pi.adoc](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/gpio-on-raspberry-pi.adoc)
- No sentence saying "GPIO has no over-voltage protection" exists anywhere in the official Raspberry Pi computer docs (all 28 included pages searched); the nearest text says the pads are designed for 16 mA and gives no guaranteed maximum safe current. Do not attribute that quote to Raspberry Pi. - [raspberry-pi.adoc and its includes](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi.adoc)
- Original ESP32 (not S2/S3/C3/C6), DC characteristics at 3.3 V and 25 °C: VIH 0.75 x VDD to VDD + 0.3 V; VIL -0.3 V to 0.25 x VDD; VOH at least 0.8 x VDD; VOL at most 0.1 x VDD. IOH is a typical 40 mA on the VDD3P3_CPU and VDD3P3_RTC domains and 20 mA on VDD_SDIO (VDD 3.3 V, VOH >= 2.64 V, max drive), not a guaranteed minimum, and drops to about 29 mA per pin when several pins in one domain source current together. IOL is a typical 28 mA (VOL 0.495 V). - [ESP32 Series Datasheet v5.3](https://documentation.espressif.com/esp32_datasheet_en.pdf)

### Level-shifter ICs (3.3 V in, 5 V out)
- TI SN74AHCT125 (quad buffer), recommended operating conditions: VCC 4.5 to 5.5 V, VIH >= 2 V, VIL <= 0.8 V, IOH -8 mA, IOL 8 mA, TA -40 to 85 °C. At VCC 4.5 V: VOH >= 3.8 V (typ 3.94 V) at IOH -8 mA; VOL <= 0.44 V (typ 0.36 V) at IOL 8 mA. At the light load IOH -50 µA, VOH is typ 4.4 V (not a load-driving figure). Propagation delay at VCC 5 V +/-0.5 V: 1 to 6.5 ns at CL 15 pF, 1 to 8.5 ns at CL 50 pF. No maximum operating frequency is published. Absolute maximums: VCC -0.5 to 7 V; output voltage -0.5 to VCC + 0.5 V; continuous output current +/-25 mA. - [SN74AHCT125 datasheet SCLS264R](https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf)
- TI SN74HCT245 (octal transceiver): VCC 4.5 to 5.5 V, VIH >= 2 V, VIL <= 0.8 V. At VCC 4.5 V and TA 25 °C: VOH min 3.98 V (typ 4.3 V) at IOH -6 mA, VOL max 0.26 V (typ 0.17 V) at IOL 6 mA; the looser 3.84 V / 0.33 V figures are the -40 to 85 °C limits. tpd at CL 50 pF, 25 °C: 16 to 28 ns at 4.5 V, 14 to 25 ns at 5.5 V. No rated fmax. - [SN74HCT245 datasheet SCLS020H](https://www.ti.com/lit/ds/symlink/sn74hct245.pdf)
- TI SN74AHCT1G125 (single buffer): VCC 4.5 to 5.5 V, VIH >= 2 V, VIL <= 0.8 V, IOH -8 mA, IOL 8 mA, TA -40 to 125 °C. At 25 °C the sheet gives only typicals (VOH typ 3.94 V at -8 mA, VOL typ 0.36 V at 8 mA); the 3.8 V min / 0.44 V max apply over the full temperature ranges. Delay 1 to 6.5 ns at 15 pF, 1 to 8.5 ns at 50 pF. TI's application section (not warranted) describes the part as suited to 3.3 V to 5 V up-translation, with load current at most 25 mA per output and 50 mA for the part. - [SN74AHCT1G125 datasheet SCLS378P](https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf)
- Adafruit #1787 (a 74AHCT125-family board) lists supply 4.5 to 5.5 V, output current 8 mA and operating temperature -40 to 125 °C; the 125 °C figure does not match TI's SN74AHCT125 (-40 to 85 °C), and the page does not name the chip maker. - [Adafruit product 1787](https://www.adafruit.com/product/1787) (vendor page)
- SparkFun BOB-12009 (BSS138-based bidirectional converter, 4 channels) shifts 5 V and 3.3 V both ways and also works with 2.8 V and 1.8 V; the product page publishes no propagation delay or maximum frequency. - [SparkFun BOB-12009](https://www.sparkfun.com/sparkfun-logic-level-converter-bi-directional.html) (vendor page)

### SN74AHCT125 pin handling
- All unused inputs must be held at VCC or GND, never left floating; a permanently unused input is tied directly, and a 10 kΩ pull-up or pull-down is suggested only for an input used some of the time. Unused outputs may float and must not be tied to VCC or GND. - [SN74AHCT125 datasheet SCLS264R](https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf) (sections 5.2, 8.1, 8.2.1.2, 8.2.1.3, 8.4.1)
- Each output is disabled when its OE pin is high and passes A to Y when OE is low; to keep outputs high-impedance during power-up or power-down, tie OE to VCC through a pull-up sized to the driver's sink capability. A 0.1 µF bypass capacitor is recommended, often paralleled with 1 µF. - [SN74AHCT125 datasheet SCLS264R](https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf) (sections 3, 8.3)
- 14-pin D/DB/DGV/N/NS/PW pinout: 1 1OE, 2 1A, 3 1Y, 4 2OE, 5 2A, 6 2Y, 7 GND, 8 3Y, 9 3A, 10 3OE, 11 4Y, 12 4A, 13 4OE, 14 VCC (the 20-pin FK package differs). - [SN74AHCT125 datasheet SCLS264R](https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf)

### WS2812B data-line requirements
- Colour order on the wire is GRB, most significant bit first (24 bits: G7..G0, R7..R0, B7..B0); confirmed in two WorldSemi copies. Clones may differ. - [WS2812B datasheet, Adafruit host](https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf); [SparkFun host, V1.0](https://cdn.sparkfun.com/assets/e/6/1/f/4/WS2812B-LED-datasheet.pdf)
- Logic thresholds VIH 0.7 x VDD, VIL 0.3 x VDD (TA -20 to +70 °C, VDD 4.5 to 5.5 V). Absolute maximums: VDD +3.5 to +5.3 V; input voltage VI -0.5 V to VDD + 0.5 V, so at VDD 5 V the data line may swing -0.5 to 5.5 V. These apply to the legacy WS2812B only. - [WS2812B datasheet, Triopak host](https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf); [Adafruit host](https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf)
- Bit timing (Mar-2017 revision): T0H 220 to 380 ns; T1H 750 ns to 1.6 µs; T0L 750 ns to 1.6 µs; T1L 220 to 420 ns; bit period 1.25 µs +/-600 ns. DIN-to-DOUT delay at most 300 ns (CL 15 pF, RL 10 kΩ). - [WS2812B datasheet, Triopak host](https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf)
- The same PDF gives two reset (latch) times: the electrical table says more than 300 µs, the timing diagram says at least 50 µs. This is unresolved in the datasheet. - [WS2812B datasheet, Triopak host](https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf)

## In practice
- Neither the Pi 5 (no published VOH) nor the original ESP32 guarantees a 3.3 V high above the WS2812B's VIH of 3.5 V at VDD 5 V. Treat a level shifter as required for a reliable data line; do not rely on "3.3 V usually works."
- Power the SN74AHCT125 from the same 5 V rail as the LEDs. Its output ceiling (VCC + 0.5 V) then matches the LED's input ceiling (VDD + 0.5 V).
- Single-channel wiring: tie every unused input of the three spare channels (both A and OE) directly to GND or VCC, never floating, and leave their Y outputs open; put 0.1 µF (optionally plus 1 µF) close to pins 14 and 7; drive the used channel's OE low, or pull it up to VCC if the output must stay high-Z at power-up.
- Use the 300 µs reset gap when timing a latch; it satisfies both datasheet figures.
- Shifter delays (single-digit to low-teens ns) are far shorter than the 220 ns minimum bit window, so wiring, grounding and correct VCC matter more than shifter speed.
- Quote the 25 °C figures for a room-temperature build and label the over-temperature min/max as such; mixing them is a common datasheet-reading error.
- The bare TI parts are better documented than either breakout board for a long or high-pixel-count run.

## Not verified / open questions
- BOB-12009 timing figures (4 to 10 ns delay, "about 1 MHz") trace only to an uncited third-party blog, not to SparkFun; not usable.
- No official Pi 5 / RP1 VOH or IOH figure exists in the sources checked; do not substitute the Pi 4 table.
- Other WS2812B revisions and clones may have different thresholds and timing.
- The WS2812B-V6 datasheet PDF (https://www.world-semi.com/downloads/datasheets/en/ws2812b-v6-1.0.pdf) had no extractable text, so its input-voltage limit is not verified.

Sources:
- https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008370-DS-1-rp1-peripherals.pdf - RP1 drive strength, fault tolerance, no VOH/VOL table
- https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/gpio-on-raspberry-pi.adoc - GPIO voltage table stops at BCM2711
- https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi.adoc - official doc tree searched for an over-voltage sentence
- https://documentation.espressif.com/esp32_datasheet_en.pdf - ESP32 DC characteristics and typical IOH/IOL
- https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf - SN74AHCT125 ratings, pin handling, pinout, bypass capacitor
- https://www.ti.com/lit/ds/symlink/sn74hct245.pdf - SN74HCT245 ratings
- https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf - SN74AHCT1G125 ratings and application note
- https://www.adafruit.com/product/1787 - Adafruit level-shifter board specs
- https://www.sparkfun.com/sparkfun-logic-level-converter-bi-directional.html - SparkFun BOB-12009 specs
- https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf - WS2812B thresholds, timing, reset contradiction, absolute maximums
- https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf - second WS2812B copy, GRB order, absolute maximums
- https://cdn.sparkfun.com/assets/e/6/1/f/4/WS2812B-LED-datasheet.pdf - WorldSemi V1.0 copy, GRB cross-check
