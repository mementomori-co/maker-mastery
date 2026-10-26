# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Ollama mode** (`docs/12-ollama-mode.md`): run Claude Code, and so Maker Mastery's rulebook, agents, skills, hooks and
  tools, on a local model on your GPU or an Ollama Cloud model. The guide covers setup, the environment variables
  (including the `opus` / `sonnet` alias variables the agents need and the 200k context fix), the VS Code and terminal
  routes, how to confirm and how to switch back. It also says what does not work yet (web search for the research
  pipeline) and that Anthropic does not support this route. Every fact links its Ollama or Claude Code source.
- `tools/ollama_check.py`: checks the Ollama server on this PC (server, model, tool calling, context window,
  `/v1/messages`) and prints the settings to paste. Talks to `localhost` only: proxies are ignored and redirects are not
  followed. Exit 0 on OK or WARN, 2 on FAIL. Unit tests in
  `tools/tests/test_ollama_check.py` use a fake local server; `tools/selftest.py` lists them.
- Knowledge note `knowledge/42-agent-engineering/claude-code-on-ollama.md`.
- README and FAQ: Ollama mode in the Guides table and the cost and data answers.

## [1.0.1] - 2026-10-22

Documentation only. No code, tool, test or brand image changed, and the v1.0.0 release asset `maker-mastery-v1.0.0.zip` is unchanged.

### Added

- `docs/02-install.md`: new section **0. Create your Anthropic account**. It covers:
  - which accounts can use Claude Code (Pro, Max, Team, Enterprise or Console; not the free plan);
  - creating a Claude or Console account, click by click;
  - phone verification;
  - the first sign-in from the VS Code extension.

  Every fact comes from Anthropic's own pages, listed in the guide's Sources. The section is also added to the Contents and the Summary table.
- One-line pointers to that section in the README Quick Start (new step 0) and in `docs/04-first-run.md` step 7.

### Fixed

- `RELEASE_NOTES_v1.0.0.md`:
  - the Checksums line now carries the SHA-256 of `maker-mastery-v1.0.0.zip`;
  - the crest line names the master (parent) crest as the main logo, as the README shows it.

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

[Unreleased]: https://github.com/mementomori-co/maker-mastery/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/mementomori-co/maker-mastery/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/mementomori-co/maker-mastery/releases/tag/v1.0.0
