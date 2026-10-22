# Third-party notices

This file lists every third-party component this repository uses, includes or adapts, with its licence. Keep it up to date: whenever you add a dependency, adapt someone else's code or include someone else's text, add a row here in the same pull request.

Unofficial community project. Not affiliated with or endorsed by Anthropic or Bambu Lab. Claude and Bambu Lab are trademarks of their owners.

## Code adapted into this repository

### `tools/check_skill.py` (adapted, MIT)

- Upstream: addyosmani/agent-skills, https://github.com/addyosmani/agent-skills (commit 9d0c60d406b454a78ccc0a175b19932047aa4dac, `scripts/lib/skill-lint.js`).
- What was adapted: the idea and rule set of the skill linter (frontmatter keys, a "Use when" description, required sections,
  a "Rationalization | Reality" table, a Verification checklist). `tools/check_skill.py` is a Python re-implementation with
  extra rules for agent files; no JavaScript was copied.
- Copyright (c) 2025 Addy Osmani. The licence text below is also kept at the end of `tools/check_skill.py`.

```text
MIT License

Copyright (c) 2025 Addy Osmani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### OpenSpec `maker` schema (copied and changed, MIT)

- Upstream: Fission-AI/OpenSpec, https://github.com/Fission-AI/OpenSpec (commit 2500d6da971336167548b53731a35b2127df35ac).
- Licence: MIT License, "Copyright (c) 2024 OpenSpec Contributors" (checked in the upstream `LICENSE` file at that commit:
  https://github.com/Fission-AI/OpenSpec/blob/2500d6da971336167548b53731a35b2127df35ac/LICENSE).
- Files copied from OpenSpec `schemas/spec-driven/`: `templates/project/openspec/schemas/maker/schema.yaml` (changed; the
  changes are listed in that folder's `README.md`) and the four templates in `templates/project/openspec/schemas/maker/templates/`:
  `proposal.md`, `spec.md`, `design.md` and `tasks.md` (unchanged).
- The full licence text is kept beside them in
  [templates/project/openspec/schemas/maker/LICENSE-openspec.txt](templates/project/openspec/schemas/maker/LICENSE-openspec.txt).
- `assessment.md` and `constitution-check.md` in the same folder are new files written for this project (see spec-kit below).

### spec-kit concepts (MIT)

- Upstream: github/spec-kit, https://github.com/github/spec-kit (commit e1fa857a7f536b22760d48c1aa9ace41df0fd1dc).
- Licence: MIT License, "Copyright GitHub, Inc." (checked in the upstream `LICENSE` file at that commit:
  https://github.com/github/spec-kit/blob/e1fa857a7f536b22760d48c1aa9ace41df0fd1dc/LICENSE).
- What was reused: the assessment funnel and the Constitution Check / Complexity Tracking gate, as concepts rewritten in
  this project's words, and the scorecard criterion names, which are spec-kit's. They appear in
  `templates/project/openspec/schemas/maker/templates/assessment.md`, `constitution-check.md` and the schema
  [README](templates/project/openspec/schemas/maker/README.md). No spec-kit code is included, and spec-kit is not installed.

## Python dependencies (installed by you, not vendored)

No third-party Python code is copied into this repository. These packages are installed from PyPI into the project's `.venv` by `tools/setup.ps1` (`pip install -r requirements.txt`, and `requirements-optional.txt` only when you ask for it) and keep their own licences. Each licence below was read from the package's PyPI JSON record for the pinned version (`https://pypi.org/pypi/<name>/<version>/json`): the `license_expression` field where the package sets one, otherwise the `License ::` classifier and the `license` field. Packages that these depend on in turn are installed by pip and carry their own licences; they are not listed here, except the three below that this repository's code imports directly.

### Required (`requirements.txt`)

| Package | Pinned | Used for | Licence (from PyPI) | PyPI page |
|---|---|---|---|---|
| numpy | 2.5.3 | arrays for every geometry and G-code check | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 (license_expression) | https://pypi.org/project/numpy/ |
| scipy | 1.18.1 | KD-trees, clustering and statistics (`tools/support_gap_readback.py`, `tools/interface_coverage.py`, `tools/render_critic.py` and others) | BSD License (classifier; the `license` field holds the BSD licence text) | https://pypi.org/project/scipy/ |
| trimesh | 5.1.1 | loading STL meshes, sections, mass properties | MIT License (classifier and `license` field) | https://pypi.org/project/trimesh/ |
| shapely | 2.1.2 | 2D polygons: prime-tower footprints, support polygons | BSD License (classifier; `license` field "BSD 3-Clause") | https://pypi.org/project/shapely/ |
| manifold3d | 3.5.4 | robust mesh booleans (code-CAD; the calibration-cube fallback) | Apache Software License (classifier) | https://pypi.org/project/manifold3d/ |
| rtree | 1.4.1 | spatial index for trimesh nearest-point queries (`tools/overhang_gate.py`) | MIT (license_expression) | https://pypi.org/project/rtree/ |
| networkx | 3.7 | graph support for trimesh section polygons (`tools/stability_check.py`) | BSD-3-Clause (license_expression) | https://pypi.org/project/networkx/ |
| PyYAML | 6.0.2 | reading `config/paths.yaml` (`tools/mm_config.py`) | MIT License (classifier; `license` field "MIT") | https://pypi.org/project/PyYAML/ |
| mcp | 2.3.0 | the optional read-only audit MCP server (`tools/mcp/mm_audit_server.py`) | MIT License (classifier; `license` field "MIT") | https://pypi.org/project/mcp/ |

### Transitive, but imported directly (installed by `mcp`, not pinned by this repository)

`tools/mcp/mm_audit_server.py` imports these three packages itself (`import anyio.to_thread`, `from pydantic import ...`,
`from mcp_types import ToolAnnotations`). They are not in `requirements.txt`: pip installs them because `mcp` 2.3.0
requires them (`anyio>=4.9`, `pydantic>=2.12.0`, `mcp-types==2.3.0` in the `mcp` 2.3.0 metadata). The versions below are
the ones pip resolved when this file was checked; yours may be newer within those ranges.

| Package | Version checked | Imported as | Licence (from PyPI) | PyPI page |
|---|---|---|---|---|
| anyio | 4.15.1 | `anyio` | MIT (license_expression) | https://pypi.org/project/anyio/ |
| pydantic | 2.13.5 | `pydantic` | MIT (license_expression) | https://pypi.org/project/pydantic/ |
| mcp-types | 2.3.0 | `mcp_types` | MIT License (classifier; `license` field "MIT") | https://pypi.org/project/mcp-types/ |

`mcp_types` is not a module inside `mcp`: it is a separate PyPI distribution, `mcp-types`, from the same repository
(https://github.com/modelcontextprotocol/python-sdk), and `mcp` 2.3.0 pins it to the exact same version.

### Optional (`requirements-optional.txt`)

| Package | Pinned | Used for | Licence (from PyPI) | PyPI page |
|---|---|---|---|---|
| open3d | 0.20.0 | image reading and writing for `tools/render_critic.py` | MIT License (classifier; `license` field "MIT") | https://pypi.org/project/open3d/ |

Only packages named in `requirements.txt` and `requirements-optional.txt` are direct dependencies. If these tables and the requirements files disagree, the requirements files win and these tables must be fixed. A PyPI licence field is the publisher's own statement; read each project's licence file before you redistribute the package.

## Bambu Studio (not included)

Bambu Studio is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0): https://github.com/bambulab/BambuStudio (licence file: https://github.com/bambulab/BambuStudio/blob/master/LICENSE).

- No Bambu Studio code, binaries or system profile JSON files are included in this repository.
- The tools call the copy of Bambu Studio that you installed yourself, through its command line.
- Slicer settings are referred to by their user-interface label and configuration key only, with a link to the public source.

## Contributor Covenant

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) is the Contributor Covenant, version 2.1, from https://www.contributor-covenant.org/version/2/1/code_of_conduct/ . Only the contact method was filled in. The attribution section inside the file is kept as published.

Licence: Creative Commons Attribution 4.0 International (CC BY 4.0, https://creativecommons.org/licenses/by/4.0/). That is
the licence in the Contributor Covenant repository's `LICENSE.md` from January 2022, when version 2.1 was current
(https://github.com/EthicalSource/contributor_covenant/blob/91532d80ea5f39b6685aff4892bc6854bf2f6d6f/LICENSE.md). The
repository's current `LICENSE.md` names the Hippocratic License 3.0 instead, and the newer version 3.0 of the Covenant
states CC BY-SA 4.0 on its own page; neither of those applies to the version 2.1 text used here. Changes made: the contact
method was filled in.

## Fonts (used to make the brand images, not shipped)

The brand images in `assets/brand/` were rendered with Oswald (SIL Open Font License 1.1, https://github.com/googlefonts/OswaldFont) and IBM Plex Mono (SIL Open Font License 1.1, https://github.com/IBM/plex). The font files are **not** included in this repository. The SVG banners contain the text as vector outlines and reference no font files.

## Brand assets

The crests, logos and the Memento Mori name are not third-party material and are not open-licensed. See [NOTICE.md](NOTICE.md).
