# Microcontroller GPIO and power limits: Arduino UNO R4 WiFi, Pico 2 (RP2350), ESP32

Applies to: any build (general electronics, printer-independent) · Arduino UNO R4 WiFi (RA4M1 + ESP32-S3), Raspberry Pi Pico 2 (RP2350), ESP32 (original) and ESP32-WROOM-32E/32UE module
Verified: 2026-10-04

## Facts

### Arduino UNO R4 WiFi
- The GPIOs on the RA4M1 microcontroller can safely handle up to 8 mA; the datasheet warns never to connect higher-current loads directly. - [Arduino UNO R4 WiFi datasheet (ABX00087)](https://docs.arduino.cc/resources/datasheets/ABX00087-datasheet.pdf)
- The RA4M1 runs at a fixed 5 V and the ESP32-S3 module at 3.3 V; the two talk through a TXB0108DQSR logic-level translator. - [ABX00087 datasheet](https://docs.arduino.cc/resources/datasheets/ABX00087-datasheet.pdf)
- The CAN pins are contradictory within the same datasheet: the pinout table puts CANRX0 on digital pin 13 (SPI clock) and CANTX0 on digital pin 10 (SPI chip select), while the feature list says "1x CAN (pin D4, D5, external transceiver is required)". - [ABX00087 datasheet](https://docs.arduino.cc/resources/datasheets/ABX00087-datasheet.pdf)
- Input voltage through VIN or the barrel jack: 6 to 24 V (table: min 6, typ 7.0, max 24 V). - [UNO R4 WiFi product page](https://docs.arduino.cc/hardware/uno-r4-wifi), [ABX00087 datasheet](https://docs.arduino.cc/resources/datasheets/ABX00087-datasheet.pdf)

### Raspberry Pi Pico 2 (RP2350)
- The Pico 2 exposes 26 multi-function GPIO, three usable as ADC; its GPIO is powered from the on-board 3.3 V rail and is fixed at 3.3 V. GPIO0-22 are digital only; GPIO26-28 can be digital or ADC. - [Pico 2 datasheet](https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf)
- The RP2350 chip itself has 30 GPIO (four ADC-capable) and supports 1.8-3.3 V IO, but the Pico 2 fixes IO at 3.3 V and exposes only 26 pins. - [Pico 2 datasheet](https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf)
- RP2350 has 3 PIO blocks with 12 state machines in total (RP2040: 2 blocks, 8 state machines). - [Pico 2 datasheet](https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf)
- The Pico 2 datasheet gives no per-pin GPIO current; its only milliamp figures are the 3V3 regulator load limit ("less than 300 mA") and an ADC reference filter figure. Per-pin drive is in the separate RP2350 datasheet (not checked here). - [Pico 2 datasheet](https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf)

### ESP32 (original): DC characteristics
- Table 5-3 (3.3 V, 25 C): VIH = 0.75 x VDD to VDD + 0.3 V; VOH = 0.8 x VDD. Maximum source current at VOH >= 2.64 V with maximum drive strength: 40 mA on VDD3P3_CPU and VDD3P3_RTC domain pins, 20 mA on VDD_SDIO domain pins; maximum sink current 28 mA. Per-pin source current on one domain falls from about 40 mA to about 29 mA as more pins on that domain source current at once. Original ESP32 only, not ESP32-S3. - [ESP32 Series Datasheet v5.3](https://documentation.espressif.com/esp32_datasheet_en.pdf)

### ESP32 (original): pin traps
- Strapping pins and their defaults (Table 3-1): GPIO0 pull-up, GPIO2 pull-down, MTDI (GPIO12) pull-down, MTDO (GPIO15) pull-up, GPIO5 pull-up (Table 2-1 maps MTDI and MTDO). Avoid anything that could hold them in the wrong state at boot. - [ESP32 Series Datasheet v5.3](https://documentation.espressif.com/esp32_datasheet_en.pdf)
- The section 2.6 advice not to use GPIO16/17 applies only to chips with in-package flash/PSRAM (for example ESP32-U4WDH, ESP32-D0WDRH2-V3) or modules with off-package PSRAM (WROVER-type), per Tables 2-5 and 2-6. On a plain ESP32-D0WD-V3 without PSRAM they are ordinary GPIO. Name the exact chip or module before ruling them in or out. - [ESP32 Series Datasheet v5.3](https://documentation.espressif.com/esp32_datasheet_en.pdf)
- Table 2-1: GPIO18 = GPIO18, HS1_DATA7, VSPICLK; GPIO19 = GPIO19, U0CTS, VSPIQ, EMAC_TXD0. GPIO19 is taken on any board wired for RMII Ethernet. Neither is a strapping or flash/PSRAM pin. - [ESP32 Series Datasheet v5.3](https://documentation.espressif.com/esp32_datasheet_en.pdf)

### ESP32 module supply and Wi-Fi transmit current
- ESP32-WROOM-32E/32UE Table 14: current delivered by the external supply, minimum 0.5 A (no typ./max. given); VDD33 3.0 V min, 3.3 V typ., 3.6 V max. This is a module-level floor, separate from the chip's per-pin limits. - [ESP32-WROOM-32E/32UE datasheet v2.1](https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf)
- ESP32 Table 5-4: transmit 802.11b, DSSS 1 Mbps, +19.5 dBm, 240 mA typical. Section 5.4 states the condition: 3.3 V supply, 25 C, measured at the RF port, transmitters at 50 % duty cycle. - [ESP32 Series Datasheet v5.3](https://documentation.espressif.com/esp32_datasheet_en.pdf)

## In practice
- Never exceed 8 mA on a UNO R4 WiFi GPIO; use a transistor or driver for LEDs beyond an indicator, and for relays.
- Treat the UNO R4 WiFi CAN pins as unresolved: check the RA4M1 pin mux or the Arduino core variant file before wiring.
- Never drive 5 V logic into a Pico 2 pin.
- On an ESP32, budget below the 40 mA / 20 mA ceilings when several pins on one domain source current together.
- Size an ESP32-WROOM-32E supply for at least 0.5 A. For a peak budget add the 240 mA transmit figure, remembering it was measured at 50 % duty cycle, so it is not a steady-state draw.
- Before picking an ESP32 pin, check three lists: strapping pins (0, 2, 5, 12, 15), flash/PSRAM pins (6-11 always; 16/17 on certain chips and modules), and input-only pins (34-39 on the classic ESP32). On a plain WROOM-type board GPIO18/19 clear all three, with GPIO19 lost only if the board wires Ethernet.
- For level shifting a 3.3 V board to WS2812B data, see [level-shifting-3v3-to-ws2812b.md](../08-electronics-lighting/level-shifting-3v3-to-ws2812b.md).

## Not verified / open questions
- Which UNO R4 WiFi pins carry CAN (digital pins 4/5 per the feature list, or 10/13 per the pinout table).
- ESP32-S3 per-pin current limits were not checked; only the original ESP32 table was.
- The input-only status of GPIO34-39 is stated from common ESP32 documentation and was not re-checked against the v5.3 datasheet for this note (not verified).

Sources:
- https://docs.arduino.cc/resources/datasheets/ABX00087-datasheet.pdf - UNO R4 WiFi GPIO limit, voltage domains, CAN contradiction, VIN range
- https://docs.arduino.cc/hardware/uno-r4-wifi - UNO R4 WiFi VIN range
- https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf - Pico 2 / RP2350 GPIO count and voltage, PIO, absence of a per-pin current spec
- https://documentation.espressif.com/esp32_datasheet_en.pdf - ESP32 Tables 2-1, 2-5, 2-6, 3-1, 5-3, 5-4 and section 5.4
- https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf - module supply-current floor and VDD33 range
