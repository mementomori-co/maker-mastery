# DS18B20 1-Wire temperature sensor on a Raspberry Pi (w1-gpio / w1_therm)

Applies to: any build (printer-independent) · DS18B20 datasheet Rev 6 (7/19); Raspberry Pi firmware `w1-gpio` / `w1-gpio-pi5` overlays; current kernel `w1_therm` docs
Verified: 2026-10-04

## Facts
- The DS18B20 measures -55 C to +125 C (-67 F to +257 F). - [DS18B20 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf) (footer "19-7487; Rev 6; 7/19"; also on the [Wayback Machine](https://web.archive.org/web/20260102154622id_/https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf))
- Accuracy is +/-0.5 C over -10 C to +85 C only; outside that band the +/-0.5 C figure does not apply. - [DS18B20 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf)
- It talks over a 1-Wire bus, which needs only one data line plus ground to reach the host processor. - [DS18B20 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf)
- Supply voltage VDD (local power): +3.0 V to +5.5 V. - [DS18B20 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf)
- Pull-up resistor: the wiring figures (Figures 6, 7, 12) show 4.7 kOhm, while the text says "approximately 5k". Use 4.7 kOhm as the practical part; the text value is a rounded description. - [DS18B20 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf)
- The Raspberry Pi firmware overlay `w1-gpio` configures the w1-gpio 1-Wire module; its `gpiopin` parameter defaults to "4", and its `pullup` parameter is now enabled by default and ignored. - [raspberrypi/firmware boot/overlays/README](https://raw.githubusercontent.com/raspberrypi/firmware/master/boot/overlays/README)
- `w1-gpio-pi5` is the Pi 5 version of `w1-gpio`, with the same parameters; use it (not plain `w1-gpio`) on a Pi 5. - [raspberrypi/firmware boot/overlays/README](https://raw.githubusercontent.com/raspberrypi/firmware/master/boot/overlays/README)
- The Linux `w1_therm` driver exposes a `w1_slave` sysfs entry; each open-and-read starts a conversion and returns two ASCII lines, with the temperature in millidegrees Celsius after `t=` on the second line. The DS18B20 family code is `0x28`. The full path `/sys/bus/w1/devices/28-xxxx/w1_slave` is not quoted on that page; it is inferred from the family code and the entry name. - [kernel docs: w1_therm](https://docs.kernel.org/w1/slaves/w1_therm.html)

## In practice
- Wire VDD to 3.3 V or 5 V (both inside +3.0 to +5.5 V), put a 4.7 kOhm pull-up on the data line, and load `dtoverlay=w1-gpio-pi5` in `config.txt` on a Pi 5 (`w1-gpio` on older models).
- Read the sensor through `w1_slave` under `/sys/bus/w1/devices/28-<id>/`; run `ls /sys/bus/w1/devices/` on the real Pi to get the exact folder name before hard-coding a path.
- The +/-0.5 C claim holds only from -10 C to +85 C; do not extend it to a hotter mounting spot.

## Not verified / open questions
- The analog.com product page's revision date for Rev 6 was not checked; only the PDF's own stamp ("Rev 6; 7/19") was read.
- The literal sysfs path is inferred, not quoted; confirm on hardware.

Sources:
- https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf - temperature range, accuracy band, 1-Wire description, VDD range, pull-up figure vs text
- https://web.archive.org/web/20260102154622id_/https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf - archived copy of the same datasheet
- https://raw.githubusercontent.com/raspberrypi/firmware/master/boot/overlays/README - `w1-gpio` and `w1-gpio-pi5` overlays, `gpiopin` default
- https://docs.kernel.org/w1/slaves/w1_therm.html - `w1_slave` behaviour, output format, family code 0x28
