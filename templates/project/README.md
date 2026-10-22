# Starting a project from this template (in VS Code)

Everything here is used by Claude Code inside VS Code. "The brain" (written `<brain>` in the files) is the folder where you
put Memento Mori Maker Mastery: the one that holds its `CLAUDE.md`, `knowledge\`, `lessons\`, `templates\` and `tools\`.

## 1. Copy the folder
1. In Windows Explorer, copy `<brain>\templates\project` to where the new project should live, for example
   `E:\Projects\<project-name>`. Keep the project outside the brain folder.
2. Open that folder in VS Code (File > Open Folder...).
3. Open `CLAUDE.md`. Replace `<brain>` in the three `@<brain>/...` import lines with the full path of your brain folder,
   written with forward slashes (for example `@E:/Projects/maker-brain/CLAUDE.md`), and fill the "Brain" line.
4. Hooks (optional but recommended): copy `.claude\settings.example.json` to `.claude\settings.json` in the same folder and
   replace each `<brain>` with the same forward-slash path. The hooks block writes into your protected folders and check
   knowledge notes. Read `<brain>\.claude\settings.notes.md` for what each hook does.
5. Agents and skills: the brain's agents and skills load only when the brain folder is open. To use them in this project
   too, copy the brain's `.claude\agents\` and `.claude\skills\` folders into this project's `.claude\` folder (or into
   your user folder `%USERPROFILE%\.claude\`, which makes them available in every project). Claude Code reads project
   agents and skills from `.claude\` and personal ones from `~/.claude/` (https://code.claude.com/docs/en/skills).
6. Open the Claude Code panel and give this first prompt: "Fill `## This project` and the constitution footer in CLAUDE.md;
   ask me what is loaded."

## 2. One-time OpenSpec setup (optional; paste into the VS Code terminal: Terminal > New Terminal)
OpenSpec is a separate open-source tool (https://github.com/Fission-AI/OpenSpec, MIT). It needs Node.js; check the
OpenSpec README for the minimum Node.js version. Run these one at a time, in the project folder:

```powershell
npm install -g @fission-ai/openspec@latest
openspec init --tools claude
openspec config set telemetry.enabled false
openspec schema validate maker
```

What each does:
- `npm install -g @fission-ai/openspec@latest` installs the `openspec` command globally (once per machine). This is a
  global install: skip OpenSpec if you do not want it; the rest of the template still works.
- `openspec init --tools claude` generates OpenSpec's Claude Code skills and `/opsx:*` commands. It keeps the existing
  `openspec/config.yaml` and the `maker` schema and only adds its own files.
- `openspec config set telemetry.enabled false` turns off OpenSpec's usage telemetry on this machine.
- `openspec schema validate maker` checks `openspec/schemas/maker/schema.yaml` and its templates. Expected: valid, 0 errors.
  If it reports an error, paste the output to Claude.

After a later OpenSpec upgrade, run `openspec update` in the project folder.
These commands come from the OpenSpec README and CLI docs; the exact output text is not reproduced here (not verified on your machine).

## 3. Daily flow (in the Claude Code panel)
1. `/opsx:explore <idea>`: think out loud; Claude fills `openspec/changes/<name>/assessment.md` (five stages, ends `VERDICT:`).
2. `/opsx:propose <name>`: on `VERDICT: go`, Claude writes the constitution check, proposal, specs, design and tasks. You approve the proposal.
3. `/opsx:apply`: builds parts per `tasks.md`; Claude asks what is loaded before any print file and slices with the CLI.
4. Run `/preprint-check <file.3mf>` (from the brain). Print only after the pre-print checklist passes. You press Print in
   Bambu Studio yourself: no AI ever starts, sends, uploads or queues a print. Measure the part.
5. `/opsx:archive`: after measurement; lessons go to `<brain>\lessons\`, facts via `/research-one` -> `/verify` -> `/file`.

## 4. Git
Each project can have its own repository: VS Code > Source Control > Initialize Repository. The `.gitkeep` files keep the
empty folders. The brain is reached by path, not as a submodule.

## Files to know
- `CLAUDE.md`: constitution, project block, layout, write-back rules.
- `openspec/config.yaml`: schema `maker`, your gear, per-artifact rules.
- `openspec/schemas/maker/README.md`: what was forked from OpenSpec (MIT) and borrowed from spec-kit (MIT).
- `.claude/settings.example.json`: hooks (path guard before every write, knowledge-note check after every write).
