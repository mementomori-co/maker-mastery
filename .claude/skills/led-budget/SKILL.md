---
name: led-budget
description: Use when an LED, wiring or power question needs numbers (current per LED, PSU size, injection points, wire gauge, level shifting, capacitors). Runs the electronics-engineer in a fresh context and returns the budget with datasheet URLs; the lead saves it beside the build.
argument-hint: "<LED type, count or length, controller, supply>"
context: fork
agent: electronics-engineer
---
## Overview
Input: $ARGUMENTS: strip type and density, length or count, controller (for example Raspberry Pi or ESP32), supply. Output: the budget in the reply (electronics-engineer has no Write tool).

## When to use
Any lighting or low-voltage wiring plan; before `/pi-power-budget` when the LED rail dominates.

## Steps
1. Read `knowledge\08-electronics-lighting\` (for example the WS2812B power note: the WorldSemi datasheet gives a per-channel current; the often-quoted 60 mA per LED is a community rule of thumb) and cite.
2. Compute LED count, worst-case and realistic current, PSU with a stated margin, injection points, wire gauge with a resistance source, series resistor, bulk capacitor; level shifting with VIH math and a named part with its datasheet URL.
3. Label every value: datasheet / official / community / computed.
4. Return the table and the wiring list.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "60 mA per LED, everyone uses it." | Check the datasheet's per-channel figure; 60 mA is a community rule. Say which you used. |
| "3.3 V drives WS2812B fine." | VIH is 0.7 x VDD, which is 3.5 V at 5 V supply; use a level shifter. |

## Red flags
- A PSU size without the margin stated.
- Feeding LEDs from a single-board computer's 5 V header.

## Verification
- [ ] Every number labelled by source class with a URL.
- [ ] Level shifter named with datasheet.
