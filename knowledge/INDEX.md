# Knowledge library index

Verified notes for makers: 3D printing on Bambu Lab printers, CAD and modeling, electronics, rendering, and the AI agents
that help with all of it. Every note follows the same format: a title, `Applies to:` and `Verified:` header lines,
`## Facts` (each fact ends with a public source link), `## In practice`, `## Not verified / open questions`, and a
`Sources:` list. Anything without a public source is marked "not verified".

Version 1.0.0 ships 16 categories. Each category has its own `index.md` with a one-line summary per note.

## 3D printing

| Category | What it covers |
| --- | --- |
| [01-printers](01-printers/index.md) | Printer hardware facts for the Bambu Lab H2C and P1S: architecture, hotends and nozzles, AMS compatibility, cooling and filament changes. |
| [02-bambu-studio](02-bambu-studio/index.md) | Bambu Studio settings by exact UI label and config key, CLI slicing, filament grouping and purge, supports, and the checks the GUI does that the CLI does not. |
| [03-materials](03-materials/index.md) | Filament families from vendor TDS and wiki pages: PLA, PETG, ABS/ASA/PC, PA/TPU/CF, heat deflection, drying and translucency. |
| [04-design-for-fdm](04-design-for-fdm/index.md) | Designing parts that print well: orientation, overhangs, bridges, walls and clearances. |
| [12-failure-diagnosis](12-failure-diagnosis/index.md) | When a print fails: Bambu HMS error codes, hotend clogs and swaps, and a symptom-cause-fix table. |
| [40-bambu-ecosystem](40-bambu-ecosystem/index.md) | How Bambu Lab printers connect, update and take add-ons: connection modes, Bambu Connect, Farm Manager, firmware and the H2 laser kits. |

## CAD and modeling

| Category | What it covers |
| --- | --- |
| [05-cad-hard-surface](05-cad-hard-surface/index.md) | Parametric and code-based CAD for printable parts: Fusion 360 workflow and export, its Personal Use licence limits, and a Python code-CAD toolchain. |
| [06-organic-modeling](06-organic-modeling/index.md) | Sculpting organic shapes in Blender and turning them into watertight, printable meshes. |
| [26-ai-to-3d](26-ai-to-3d/index.md) | AI 3D generation services and local models, what their licences let you do with the output, and repairing AI meshes for FDM. |

## Engineering and electronics

| Category | What it covers |
| --- | --- |
| [07-engineering](07-engineering/index.md) | Mechanical design for printed parts: heat-set inserts, snap-fits and living hinges, keyed joints, physical stability, drilling polycarbonate sheet and enclosure thermal budgets. |
| [08-electronics-lighting](08-electronics-lighting/index.md) | LED lighting builds: WS2812B and analog RGB strips, power injection, supplies, level shifting, WLED limits, fuses, wire gauge, connectors, glands, enclosures and FDM light diffusion. |
| [39-raspberry-pi-and-microcontrollers](39-raspberry-pi-and-microcontrollers/index.md) | Raspberry Pi 5, Pico 2, Arduino UNO R4 WiFi and ESP32: power budgets, GPIO limits, power-on pin states, relay switching and the DS18B20 temperature sensor. |

## Rendering

| Category | What it covers |
| --- | --- |
| [24-surfacing-and-rendering](24-surfacing-and-rendering/index.md) | Blender look development for printed parts: retopology and UVs, materials, product lighting, colour management and headless rendering. |

## AI and agents

| Category | What it covers |
| --- | --- |
| [41-mcp](41-mcp/index.md) | The Model Context Protocol: what the current spec requires, and how to configure and write MCP servers for Claude Code in Python. |
| [42-agent-engineering](42-agent-engineering/index.md) | How Claude Code's hooks, permissions, settings, skills, sub-agents, plugins and headless mode behave, from the official docs. |

## Safety

| Category | What it covers |
| --- | --- |
| [44-safety](44-safety/index.md) | Conservative safety notes: printer fumes and filtration, low-voltage electrical safety and listings, casting-bench ventilation, wood dust and machine guarding. |

## Roadmap

- v1.1: full library. The remaining categories, including game design and game development, finishing, business and more, are released after they pass the same privacy and source review.
