# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-22 - First Light

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
- **229 automated tests in 15 test files** (`tools/tests/`), run by `tools/selftest.py`; no test needs Bambu Studio, Blender or the internet.
- **20 lessons** in `lessons/`: general post-mortems, each with the rule it created.
- Beginner guides `docs/01-what-this-is.md` to `docs/11-autonomous-mode.md`, and sample outputs of every tool in `docs/tool-sample-outputs.md`.
- Install guide for Windows 11, macOS (Apple silicon and Intel) and Ubuntu with every method per app (direct download, winget, Homebrew, apt, the vendor's own installer), each command and package id from its official source (`docs/02-install.md`).
- Install scripts `install/windows.ps1`, `install/macos.sh` and `install/linux.sh` (y/N per app, dry-run mode, idempotent, log file) and read-only check scripts `install/check.ps1` and `install/check.sh`. The Claude Code command line is optional; the scripts recommend Anthropic's native installer for it.
- Recommended VS Code extensions in `.vscode/extensions.json`, with IDs and reasons in `docs/04-first-run.md`.
- Autonomy guide `docs/11-autonomous-mode.md`: permission modes, allow/ask/deny rules, the skip-all-permissions flag, parallel and background subagents, the two-brain workflow.
- Owner profile template `templates/OWNER_PROFILE.md`, read first by `CLAUDE.md`.
- `constraints.txt` with the exact package versions of a tested fresh install, used by `tools/setup.ps1`.
- Hardened folder guard `tools/hooks/guard_paths.py` (junctions, symlinks, 8.3 names, `\\?\` and share paths, fail closed on an unreadable config), set to block the call when it cannot run (`"onFailure": "block"`, Claude Code v2.1.295 or later).
- Maintainer guide `docs/PUBLISHING.md` (publishing the repository and the release) and the release notes `RELEASE_NOTES_v1.0.0.md`.
- Print-quality gate and pre-print checklist: nothing is called ready until a second, independent check has passed.
- Slicing and audit helpers for the Bambu Studio command line, 3MF and G-code checks.
- Machine settings in one place: `config/paths.example.yaml`, read by `tools/mm_config.py`.
- Privacy scan (`tools/privacy_scan.py`) and metadata stripper (`tools/strip_metadata.py`) to run before sharing anything.
- Calibration-cube example.
- Brand assets in `assets/brand/` (crest, dark and light banners, social preview, the four-crest Memento Mori family strip in dark and light, small crest icons, and `org-avatar-500.png` for a GitHub organization); not open-licensed, see `NOTICE.md`.
- Legal and community files: MIT `LICENSE`, `NOTICE.md`, `THIRD_PARTY_NOTICES.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `CONTRIBUTING.md`.

[Unreleased]: https://github.com/mementomori-co/maker-mastery/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/mementomori-co/maker-mastery/releases/tag/v1.0.0
