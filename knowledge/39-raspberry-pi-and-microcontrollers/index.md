# 39 Raspberry Pi and microcontrollers - index

Power, pin and sensor facts for Raspberry Pi 5, Pico 2, Arduino UNO R4 WiFi and ESP32 builds, from vendor datasheets and the Raspberry Pi documentation. Every note lists public sources; measure real current draw before you finalise a budget.

- [pi5-power-budget.md](pi5-power-budget.md) - Pi 5 supply and USB current budget (5 A, 1.6 A vs 600 mA), board, GPIO and HDMI draw, peak and off-state power, throttle temperatures and fan curve, Active Cooler, PCIe FFC power, `get_throttled` bits, example 5 V supplies.
- [microcontroller-gpio-and-power-limits.md](microcontroller-gpio-and-power-limits.md) - UNO R4 WiFi 8 mA GPIO limit and CAN pin contradiction, Pico 2 / RP2350 GPIO and PIO, ESP32 per-pin current, strapping and flash/PSRAM pin traps, WROOM-32E supply floor and Wi-Fi transmit current.
- [pi-gpio-power-on-state-and-relay-switching.md](pi-gpio-power-on-state-and-relay-switching.md) - Pi GPIO state at power-on (RP1 reset values), and why a PhotoMOS (AQV252G) can be driven from a 3.3 V pin while a DC60S3 SSR cannot.
- [ds18b20-1-wire-temperature-sensor.md](ds18b20-1-wire-temperature-sensor.md) - DS18B20 range, accuracy band, supply and pull-up, Pi `w1-gpio-pi5` overlay and `w1_therm` sysfs read format.

Related: LED power, level shifting and supplies in [08-electronics-lighting](../08-electronics-lighting/index.md); electrical safety in [44-safety](../44-safety/index.md).
