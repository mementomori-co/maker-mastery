# Blender render helpers for Claude Code (EL4CTEO blender-skills, RobLe3 cc-blender-skill, mcp-for-blender)

Applies to: render tooling on Windows - Blender 5.2 LTS; repository state as read at the date below
Verified: 2026-10-20

## Facts

### EL4CTEO/blender-skills (MIT, community, AI-co-authored)
- At check the repo was 6 days old (created 2026-10-14, last push 2026-10-19), with 323 stars and 0 open issues; the latest release was 1.1.0 (time-of-day and weather skills), and commits carry Claude co-author trailers. - [GitHub API](https://api.github.com/repos/EL4CTEO/blender-skills), [CHANGELOG](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/CHANGELOG.md)
- It states Blender 5.2 LTS or newer as the minimum. CI runs only on Ubuntu with Blender 5.2.2; there is no Windows job. - [README](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/README.md), [blender-core SKILL.md](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-core/SKILL.md)
- 22 skill folders; 20 have a `scripts/` folder, each with a synced `_bpyx.py` copy; `tests/` holds 22 .py files (20 `test_*.py` plus `fixtures.py` and `run_all.py`). - [repo tree](https://api.github.com/repos/EL4CTEO/blender-skills/git/trees/HEAD?recursive=1)
- Headless route without MCP: `blender -b in.blend --factory-startup --python-exit-code 1 -P x.py -- args`, with results printed as `@@JSON@@` lines. - [blender-core SKILL.md](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-core/SKILL.md)
- `run_in_blender.py` finds Blender via `$BLENDER_EXE`, then PATH, then standard install folders (on Windows: Program Files, per-user Programs, Steam), runs it with captured output, and prints the `@@JSON@@` lines or the last 15 log lines; `--user-prefs` drops `--factory-startup`. - [run_in_blender.py](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-core/scripts/run_in_blender.py)
- `render_batch.py` presets: preview 64 samples, adaptive threshold 0.05, 50 % size; final 512 / 0.01; product 1024 / 0.005 with a transparent background. GPU backends are tried in the order OPTIX, CUDA, HIP, METAL, ONEAPI; the OptiX denoiser is used only on an OPTIX device, else OpenImageDenoise; it sets `media_type` before `file_format` (a 5.0+ requirement) and reports `files` and `sec_per_image`; no network imports. - [render_batch.py](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-rendering/scripts/render_batch.py)
- `turntable.py` (lighting-lookdev) builds Disk key/fill/rim lights at azimuth -45/50/160 deg and elevation 35/15/40 deg, an 85 mm lens and an 18 % grey bevelled backdrop at roughness 0.8. Everything it makes is prefixed `LD_` in collection `LD_Lookdev`, and a re-run deletes every object whose name starts with `LD_`, including one of yours with that prefix. - [turntable.py](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-lighting-lookdev/scripts/turntable.py)
- Author guidance (recommendations, not measurements): key 45 deg to the side and 30-40 deg up, fill opposite at 1/3 power, rim behind; soft area lights about the object's size; Khronos PBR Neutral view for products; 85-135 mm lenses; f/2.8-5.6 at real scale. - [lighting-lookdev SKILL.md](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-lighting-lookdev/SKILL.md), [rendering SKILL.md](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-rendering/SKILL.md)
- A static grep of the source tarball (80 .py files, not run) found no network or telemetry code in skill scripts; `subprocess` only in `run_in_blender.py` and two test/tool files; `exec(compile(...))` only in one test; the only download is a Blender `curl` in CI; no `allowed-tools` lines. This is a static read, not a security audit. - [tarball](https://codeload.github.com/EL4CTEO/blender-skills/tar.gz/refs/heads/main)
- Install: `/plugin marketplace add EL4CTEO/blender-skills` then `/plugin install blender-agent-skills@blender-agent-skills`, or `install\install.ps1`, which defaults to your user-level `.claude\skills` and `.agents\skills` folders and force-deletes same-named target folders (`Remove-Item -Recurse -Force`). - [README](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/README.md), [install.ps1](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/install/install.ps1)

### RobLe3/cc-blender-skill (MIT, community)
- Created 2026-04-27, last push 2026-10-12, 110 stars, 0 issues, v1.4.0 at check. - [GitHub API](https://api.github.com/repos/RobLe3/cc-blender-skill)
- 30 skills under `plugin/skills/`, all driven through a configured Blender MCP (no Python wrapper, no custom MCP); no `blender -b` route found. Tested on Blender 5.1.1 only; newer versions are marked as needing community testing. It has 33 `allowed-tools` lines, 17 name-based `nodes['Principled BSDF']` lookups (name lookups break on localised node names) and an OpenImageDenoise default. - [README](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/README.md), [blender-rendering SKILL.md](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-rendering/SKILL.md), [mcp-backends.md](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/references/mcp-backends.md), [blender-version-compat.md](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/references/blender-version-compat.md)

### mcp-for-blender (formerly blender-mcp; community)
- PyPI `blender-mcp` 2.0.0 is a rename shim that depends on `mcp-for-blender>=2.0.0`; the repo `ahujasid/mcp-for-blender` is MIT, README at version 2.2.2 when read. - [PyPI](https://pypi.org/pypi/blender-mcp/json), [README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md)
- Nine tools: `execute_blender_code`, `look`, `get_scene_info`, `generate_3d`, `search_assets`, `import_asset`, `get_addon_status`, `disable_telemetry`, `record_trajectory_feedback`. Prerequisites: Blender 3.0+, Python 3.10+, uv. - [README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md)
- It works only with a GUI Blender; the server source says commands never execute when Blender runs headless. The add-on starts its server when Blender opens. - [server.py](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/src/blender_mcp/server.py), [README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md)
- Per the 2.2.2 README, a minimal anonymous usage record (install and session IDs, tool name, success, duration, versions, OS, timestamp) is collected by default; prompts, code, screenshots and scene data are not collected without opt-in. Set `DISABLE_TELEMETRY=true` (also accepted: `BLENDER_MCP_DISABLE_TELEMETRY`, `MCP_DISABLE_TELEMETRY`) to turn it off. The README says the data may be used to train AI models. - [README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md), [telemetry.py](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/src/blender_mcp/telemetry.py)
- By default the AI can run any Python inside Blender; `BLENDER_MCP_SAFE_MODE=1` checks and blocks risky code. The README tells you to save your work, and the add-on's socket server has no authentication or encryption. - [README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md)
- Update with `uvx mcp-for-blender@latest update`; releases before 2.1.7 lack `update`, and uvx may run a cached older copy. - [README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md)

## In practice
- For unattended renders, the EL4CTEO route (`run_in_blender.py` plus `render_batch.py`) is the only one of the three that runs headless; the two MCP routes need Blender open with the add-on.
- Read any of these scripts at the exact commit you install and do a test render on your own OS and Blender build before relying on them; CI covers Linux only.
- If you configure mcp-for-blender, pin its version and set `DISABLE_TELEMETRY` in the server's `env` block.
- Look shader nodes up by type, not by name, in your own scripts.

## Not verified / open questions
- Whether a telemetry record is actually sent depends on the installed version; no traffic was captured.
- Whether EL4CTEO's scripts work on Windows, and whether OptiX is selected under `--factory-startup`, is untested (the downloaded code was read, not run).
- Repo stats (stars, dates, versions) were true at the check date and will drift.

Sources:
- https://api.github.com/repos/EL4CTEO/blender-skills - licence, dates, stars, issues
- https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/CHANGELOG.md - release dates
- https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/README.md - minimum Blender, install commands
- https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-core/SKILL.md - headless route
- https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-core/scripts/run_in_blender.py - Blender discovery and command line
- https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-rendering/scripts/render_batch.py - presets, GPU and denoiser logic
- https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-rendering/SKILL.md - PBR Neutral guidance
- https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-lighting-lookdev/scripts/turntable.py - light rig values, `LD_` deletion
- https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-lighting-lookdev/SKILL.md - product lighting guidance
- https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/install/install.ps1 - install defaults and force-delete
- https://api.github.com/repos/EL4CTEO/blender-skills/git/trees/HEAD?recursive=1 - file counts
- https://codeload.github.com/EL4CTEO/blender-skills/tar.gz/refs/heads/main - static grep
- https://api.github.com/repos/RobLe3/cc-blender-skill - licence, dates, stars
- https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/README.md - contents and tested version
- https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-rendering/SKILL.md - denoiser default
- https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/references/mcp-backends.md - MCP-only design
- https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/references/blender-version-compat.md - Blender 5.1.1 tested
- https://pypi.org/pypi/blender-mcp/json - rename shim
- https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md - tools, telemetry, safe mode, update
- https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/src/blender_mcp/server.py - headless commands never execute
- https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/src/blender_mcp/telemetry.py - telemetry code and opt-out variables
