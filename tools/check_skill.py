r"""check_skill.py - lint SKILL.md and agent .md files for Claude Code.

Credit: adapted from the skill-lint idea in addyosmani/agent-skills (https://github.com/addyosmani/agent-skills,
commit 9d0c60d406b454a78ccc0a175b19932047aa4dac, scripts/lib/skill-lint.js), MIT License, Copyright (c) 2025 Addy Osmani.
The original license text is reproduced at the end of this file and in THIRD_PARTY_NOTICES.md.

What it does: checks the frontmatter and required sections of each file and prints PASS or FAIL with the reasons.
Inputs: files or folders (folders are searched for *.md, skipping files starting with "_" and _TEMPLATE / _draft folders).
Output: PASS/FAIL per file; exit 0 if all pass, 2 otherwise.
Usage: .venv\Scripts\python.exe tools\check_skill.py <path or dir> [...]
Example: .venv\Scripts\python.exe tools\check_skill.py .claude\skills .claude\agents
Rules for skills (.claude/skills/<name>/SKILL.md):
  S1 frontmatter present; keys within {name, description, argument-hint, context, agent, disable-model-invocation,
     user-invocable, allowed-tools, disallowed-tools, model, effort, paths, hooks, metadata, license, compatibility, shell, arguments, background, when_to_use}
  S2 name == folder name, kebab-case
  S3 description <= 1024 chars and matches /\buse (this )?when\b|\buse (before|after|during)\b/i
  S4 required sections: ## Overview, ## When to use, ## Common rationalizations, ## Red flags, ## Verification
  S5 <= 500 lines (warning only)
Rules for agents (.claude/agents/*.md):
  A1 frontmatter keys within {name, description, tools, disallowedTools, model, permissionMode, skills, memory, maxTurns, background, isolation, effort, hooks, color}
  A2 name == file stem, kebab-case; description <= 2 sentences (<= 320 chars); model in {sonnet, opus, haiku, fable, inherit} or a full id
  A3 body has a "## Common rationalizations" table and a "## Verification" checklist
"""
from __future__ import annotations

import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

SKILL_KEYS = {"name", "description", "argument-hint", "context", "agent", "disable-model-invocation", "user-invocable",
              "allowed-tools", "disallowed-tools", "model", "effort", "paths", "hooks", "metadata", "license",
              "compatibility", "shell", "arguments", "background", "when_to_use"}
AGENT_KEYS = {"name", "description", "tools", "disallowedTools", "model", "permissionMode", "skills", "memory", "maxTurns",
              "background", "isolation", "effort", "hooks", "color"}
SKILL_SECTIONS = ["## Overview", "## When to use", "## Common rationalizations", "## Red flags", "## Verification"]
USE_WHEN = re.compile(r"\buse (this )?when\b|\buse (before|after|during)\b", re.I)
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MODELS = {"sonnet", "opus", "haiku", "fable", "inherit"}


def frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    fm = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[end + 4 :]


def check_skill(path: str) -> list[str]:
    p: list[str] = []
    text = open(path, encoding="utf-8", errors="replace").read()
    fm, body = frontmatter(text)
    if fm is None:
        return ["S1 missing frontmatter"]
    extra = set(fm) - SKILL_KEYS
    if extra:
        p.append(f"S1 unknown frontmatter keys: {sorted(extra)}")
    folder = os.path.basename(os.path.dirname(path))
    name = fm.get("name", "")
    if name != folder or not KEBAB.match(name):
        p.append(f"S2 name '{name}' must equal folder '{folder}' and be kebab-case")
    desc = fm.get("description", "")
    if len(desc) > 1024:
        p.append("S3 description > 1024 chars")
    if not USE_WHEN.search(desc):
        p.append("S3 description must say 'Use when' (or use before/after/during)")
    low = body.lower()
    for s in SKILL_SECTIONS:
        if s.lower() not in low:
            p.append(f"S4 missing section '{s}'")
    if "| rationalization |" not in low:
        p.append("S4 Common rationalizations must be a '| Rationalization | Reality |' table")
    if "- [ ]" not in body:
        p.append("S4 Verification must contain checkboxes")
    if text.count("\n") > 500:
        p.append("S5 WARN: over 500 lines")
    return p


def check_agent(path: str) -> list[str]:
    p: list[str] = []
    text = open(path, encoding="utf-8", errors="replace").read()
    fm, body = frontmatter(text)
    if fm is None:
        return ["A1 missing frontmatter"]
    extra = set(fm) - AGENT_KEYS
    if extra:
        p.append(f"A1 unknown frontmatter keys: {sorted(extra)}")
    stem = os.path.splitext(os.path.basename(path))[0]
    name = fm.get("name", "")
    if name != stem or not KEBAB.match(name):
        p.append(f"A2 name '{name}' must equal file stem '{stem}' and be kebab-case")
    desc = fm.get("description", "")
    if len(desc) > 320 or len(re.findall(r"[.!?](\s|$)", desc)) > 2:
        p.append(f"A2 description must be <= 2 sentences and <= 320 chars (is {len(desc)} chars)")
    model = fm.get("model", "")
    if model and model not in MODELS and not model.startswith("claude-"):
        p.append(f"A2 model '{model}' not in {sorted(MODELS)} or a full id")
    if not model:
        p.append("A2 model: missing (an explicit model choice is required)")
    low = body.lower()
    if "## common rationalizations" not in low or "| rationalization |" not in low:
        p.append("A3 missing '## Common rationalizations' table")
    if "## verification" not in low or "- [ ]" not in body:
        p.append("A3 missing '## Verification' checklist")
    return p


def main(argv: list[str]) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="check_skill.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="SKILL.md / agent .md files, or folders to search for *.md")
    args = ap.parse_args(argv[1:])
    targets: list[str] = []
    for a in args.paths:
        if os.path.isdir(a):
            for root, _, files in os.walk(a):
                for f in files:
                    if f.lower().endswith(".md") and not f.startswith("_") and "_TEMPLATE" not in root and "_draft" not in root:
                        targets.append(os.path.join(root, f))
        else:
            targets.append(a)
    if not targets:
        print(__doc__)
        return 0
    failed = False
    for t in sorted(targets):
        is_skill = os.path.basename(t).upper() == "SKILL.MD"
        probs = check_skill(t) if is_skill else check_agent(t)
        hard = [x for x in probs if "WARN" not in x]
        if hard:
            failed = True
            print(f"FAIL {t}\n  - " + "\n  - ".join(probs))
        else:
            print(f"PASS {t}" + (f"  ({'; '.join(probs)})" if probs else ""))
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

# Original license of the adapted work (addyosmani/agent-skills):
# MIT License
#
# Copyright (c) 2025 Addy Osmani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
