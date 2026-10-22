---
name: pi-power-budget
description: Use when a Raspberry Pi 5 build (screen, LEDs, fans, USB devices, encoders) needs a per-rail power budget with datasheet-sourced currents and a PSU choice. Runs the systems-engineer in a fresh context and writes systems\power-budget.md in the project folder you name.
argument-hint: "<project folder> | <loads: board, screen, LED count and type, fans, USB devices>"
context: fork
agent: systems-engineer
---
## Overview
Budget: $ARGUMENTS (project folder and the load list). Output: `<project folder>\systems\power-budget.md` (see `templates\project\` for the folder layout) with one row per load, a sum per rail, the chosen margin (labelled design decision), the PSU, and a check step for the real Pi.

## When to use
Before buying or wiring a supply for any Pi 5 build (a display piece with a screen, a bartop, a lit sign). Not for LED data wiring, injection points or level shifting (electronics-engineer), not for ESP32 pin maps (ask systems-engineer for `pin-map.md`), not for mains work (safety-officer gate, NEEDS MAKER).

## Steps
1. Read `lessons\` and the notes in `knowledge\08-electronics-lighting\` and `knowledge\44-safety\`. If a load's exact part is not named, ask: NEEDS MAKER (never assume a part).
2. Pi 5 rules: fetch https://www.raspberrypi.com/documentation/computers/raspberry-pi.html and quote the recommended supply (voltage, current) and the USB current limit that applies when a smaller supply is used, each with its condition.
3. Per load: fetch the datasheet or product page; record voltage, current (typical and peak), the condition (brightness, resolution, full white, idle), the URL and the page date. LED strips: per-LED current from the LED datasheet at the stated colour and brightness; count of LEDs and count of segments stated as separate numbers; hand injection and gauge to electronics-engineer by naming it in the file.
4. Sum per rail (5 V, 12 V, USB-powered). State the margin as "design decision: <value>, because <reason>", not as a sourced fact. Pick the PSU and quote its rated output with URL.
5. Check step for you: after wiring, run `vcgencmd get_throttled` on the Pi under load and paste the result; the meaning of the value is read from the Raspberry Pi documentation page fetched this run. Steps are written as device menu paths or a line to paste, never "open a terminal" without saying which one and how.
6. Facts fetched go to `research\inbox\raspberry-pi\<question-slug>.md` for `/verify`. Return the budget path, inbox paths, NEEDS MAKER list, one next step.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "The Pi 5 needs 5 V 5 A, done." | The USB limit changes with the supply; quote both rules with their conditions from the page fetched this run. |
| "WS2812B is 60 mA per LED." | Only at a stated colour and brightness for a stated part. Datasheet URL and condition. |
| "Add 20 % headroom, standard practice." | Fine as a choice; label it design decision, not fact. |
| "Two 1 m strips, so about 288 LEDs." | LED count, segment count and injection points are separate numbers; count each. |

## Red flags
- A current without voltage, condition and URL.
- Margin presented as a sourced figure.
- A PSU chosen before the per-rail sum exists.
- Mains wiring described as a step instead of NEEDS MAKER.

## Verification
- [ ] `<project folder>\systems\power-budget.md` exists.
- [ ] Every load row: V, A (typ and peak), condition, datasheet URL fetched this run, page date.
- [ ] Pi 5 supply and USB-limit quotes present with conditions.
- [ ] Margin labelled "design decision"; PSU rating quoted with URL.
- [ ] `vcgencmd get_throttled` check step written; inbox paths returned.
