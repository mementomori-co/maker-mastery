# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - First Light (unreleased)

Release name: **v1.0.0 — First Light**. Release asset: `maker-mastery-v1.0.0.zip`.

### Added

- A Claude Code operating system for makers, with 3D printing on Bambu Lab printers as the flagship example.
- Core operating rules for Claude Code, led by the headline rule: no AI ever starts, sends, uploads or queues a print. The maker always presses Print in Bambu Studio.
- Verified knowledge library: **94 notes in 16 domains**, every fact linked to its public source:
  - 01 printers (7 notes), 02 Bambu Studio (19), 03 materials (11), 04 design for FDM (3), 12 failure diagnosis (3), 40 Bambu ecosystem (4)
  - 05 CAD, hard surface (3), 06 organic modeling (1), 26 AI to 3D (2), 24 surfacing and rendering (5)
  - 07 engineering (6), 08 electronics and lighting (13), 39 Raspberry Pi and microcontrollers (4)
  - 41 MCP (2), 42 agent engineering (7), 44 safety (4)
  - plus 00 gear inventory as a fill-in template (2 files), and the full domain map as an empty learning tracker in `CURRICULUM.md`.
- **22 agents, 30 skills and 5 commands** for Claude Code in `.claude/`: research, fact-checking, filing knowledge, CAD and sculpting, design-for-FDM review, slicer questions, materials, electronics, safety sheets and the print-quality gate.
- **27 tool files**: 21 Python tools in `tools/`, 3 Claude Code hook scripts in `tools/hooks/`, 2 MCP scripts in `tools/mcp/`, and the `tools/setup.ps1` setup script.
- **210 automated tests in 15 test files** (`tools/tests/`), run by `tools/selftest.py`; no test needs Bambu Studio, Blender or the internet.
- **20 lessons** in `lessons/`: general post-mortems, each with the rule it created.
- Beginner guides `docs/01-what-this-is.md` to `docs/10-faq.md`, and sample outputs of every tool in `docs/tool-sample-outputs.md`.
- Print-quality gate and pre-print checklist: nothing is called ready until a second, independent check has passed.
- Slicing and audit helpers for the Bambu Studio command line, 3MF and G-code checks.
- Machine settings in one place: `config/paths.example.yaml`, read by `tools/mm_config.py`.
- Privacy scan (`tools/privacy_scan.py`) and metadata stripper (`tools/strip_metadata.py`) to run before sharing anything.
- Calibration-cube example.
- Brand assets in `assets/brand/` (crest, dark and light banners, social preview); not open-licensed, see `NOTICE.md`.
- Legal and community files: MIT `LICENSE`, `NOTICE.md`, `THIRD_PARTY_NOTICES.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `CONTRIBUTING.md`.

[Unreleased]: https://github.com/<owner>/maker-mastery/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/<owner>/maker-mastery/releases/tag/v1.0.0
