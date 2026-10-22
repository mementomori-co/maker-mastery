# 11 - Autonomous mode: fewer approvals, still safe

How to let Claude Code and its agents work for long stretches with few "May I?" prompts, without giving up the things
only you should decide. Back to the start: [01 - What this is](01-what-this-is.md). Related:
[06 - Print safety](06-print-safety.md), [08 - Make it yours](08-customize.md).

Every mode name, flag, setting key and UI label below is quoted from the official Claude Code documentation or the
official Claude Help Center, linked next to it. Claude Code changes often: if your screen shows something different,
the linked page wins. Anything the docs do not state is marked "(not verified)".

> **Read this first.** Fewer approvals means Claude acts before you look. Three things never change, whatever mode you
> pick: **no AI ever starts, sends, uploads or queues a print**; the owner-only list in your owner profile stays yours;
> and secrets never go in this repository. See the [Safety box](#7-safety-box) at the end.

## Contents
1. [Permission modes](#1-permission-modes)
2. [Allow, ask and deny rules](#2-allow-ask-and-deny-rules)
3. [The "skip all permissions" flag](#3-the-skip-all-permissions-flag)
4. [Subagents, parallel work and background tasks](#4-subagents-parallel-work-and-background-tasks)
5. [The two-brain workflow](#5-the-two-brain-workflow)
6. [A safe setup, step by step](#6-a-safe-setup-step-by-step)
7. [Safety box](#7-safety-box)
8. [Sources](#8-sources)

---

## 1. Permission modes

A permission mode decides which actions Claude may take without asking you first. Source for this whole section:
[Choose a permission mode](https://code.claude.com/docs/en/permission-modes).

| Mode (config value) | Label in VS Code | What runs without asking | Use it for |
|---|---|---|---|
| `default` | **Manual** | Reads only | Reviewing every action yourself, unfamiliar or sensitive work |
| `acceptEdits` | **Edit automatically** | Reads, file edits, and common filesystem commands (`mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`) inside your working folder | Iterating while you review changes afterwards |
| `plan` | **Plan** | Reads; Claude proposes a plan and edits nothing until you approve it | Exploring before changing anything |
| `auto` | **Auto** | Everything, with a second model (the "classifier") reviewing actions in the background | Long tasks, fewer prompts |
| `dontAsk` | (not in the VS Code mode indicator) | Only pre-approved tools and reads; anything that would prompt is denied | Locked-down scripts and CI |
| `bypassPermissions` | **Bypass permissions** (hidden unless enabled) | Everything | Throwaway containers and VMs only (see [section 3](#3-the-skip-all-permissions-flag)) |

What the docs add, in plain words:

- **Manual** is the mode's name in the UI; its config value is `default`, and `manual` is accepted as an alias.
- **Auto mode reduces prompts but "does not guarantee safety"** (quoted from the docs). The classifier blocks actions
  that go beyond your request, target unrecognised infrastructure, or look driven by hostile content Claude read.
  Explicit `ask` rules still prompt you.
- **In `acceptEdits`**, paths outside your working folder still prompt, and so do writes to protected paths such as
  `.git`, `.claude` and `.vscode` (the docs list them under "Protected paths").
- **Critical-path removals** (`rm` or `rmdir` aimed at a drive root, your home folder, your working folder or its
  parents) are never auto-approved by any mode. In auto mode inside the VS Code chat panel they are denied immediately
  and Claude is told to leave the removal to you. The docs warn that this check "can miss some commands".
- **`Remove-Item` in PowerShell** gets its own checks: system paths and bare wildcards such as `*` or `folder\*` are
  denied in every mode.
- **Which mode is the default** depends on your Claude Code version and plan: the docs say newer versions start
  terminal and VS Code sessions in auto mode. Check the mode indicator before you send your first prompt.

### Switch modes in VS Code
- **During a conversation:** click the mode indicator at the bottom of the prompt box and pick **Manual**,
  **Edit automatically**, **Plan**, **Auto** or **Bypass permissions**. **Auto** appears only when auto mode is
  available to your account and model.
- **As the default for new conversations:** File > Preferences > Settings, search `claudeCode.initialPermissionMode`,
  and set `default`, `manual`, `acceptEdits`, `plan` or `bypassPermissions`. The setting does not accept `auto`. To start
  in Auto, leave it unset and pick **Auto** from the mode indicator once; the extension remembers it.
- **The project file does not set the VS Code mode:** the extension "never reads a project's `.claude/settings.json` or
  `.claude/settings.local.json` for the starting permission mode" (quoted from the docs). This repository's settings
  therefore cannot switch you into a looser mode.
- Sources: [permission-modes, "Switch permission modes"](https://code.claude.com/docs/en/permission-modes) and
  [VS Code, "Extension settings"](https://code.claude.com/docs/en/vs-code).

### Switch modes in the CLI (terminal)
- **During a session:** press `Shift+Tab` to cycle modes. The status bar shows the current one, for example
  `accept edits on` or `plan mode on`.
- **At start-up:** `claude --permission-mode plan` (also `default`, `acceptEdits`, `auto`, `dontAsk`,
  `bypassPermissions`). The same flag works with `-p` for one-shot runs
  ([CLI reference](https://code.claude.com/docs/en/cli-reference), [headless](https://code.claude.com/docs/en/headless)).
- **As a default:** set `permissions.defaultMode` in a settings file. The docs say `auto` and `bypassPermissions` do not
  take effect from a project's `.claude/settings.json` or `.claude/settings.local.json`; put them in your user file
  `~/.claude/settings.json` (on Windows `%USERPROFILE%\.claude\settings.json`) if you really want them.

**Recommendation for this project:** use **Auto** or **Edit automatically** for normal work, **Plan** before anything
big, and **Manual** whenever a task touches folders outside the project.

---

## 2. Allow, ask and deny rules

Rules sit on top of the mode. Source: [Configure permissions](https://code.claude.com/docs/en/permissions).

### How rules work
- **Allow** runs a matching tool without asking. **Ask** always prompts. **Deny** blocks it.
- **Order:** "Rules are evaluated in order: deny, then ask, then allow" (quoted). A broad deny beats a narrower allow;
  an allow can never carve an exception out of a deny.
- **Across files:** a deny in any settings file blocks an allow in any other. Lists such as `permissions.allow` from
  several files are merged, not replaced ([Settings](https://code.claude.com/docs/en/settings)).
- **Deny rules work in every mode, including `bypassPermissions`**
  ([permission-modes](https://code.claude.com/docs/en/permission-modes), "Available modes").
- **Rules are enforced by Claude Code, not by the model.** Text in `CLAUDE.md` or your owner profile shapes what Claude
  tries to do; only rules, modes and hooks change what Claude Code allows (permissions page, note under "Manage
  permissions").
- **See and edit rules:** in VS Code, open the command menu (type `/`) and select **Permissions** under Customize, or
  type `/permissions` in the CLI ([VS Code](https://code.claude.com/docs/en/vs-code), "Use the prompt box").

### Rule syntax in one table

| Rule | Matches | Notes from the docs |
|---|---|---|
| `Bash(npm run *)` | any command starting `npm run` | `*` matches any text, spaces included |
| `PowerShell(Remove-Item *)` | `Remove-Item` and its common aliases | case-insensitive; aliases are canonicalised |
| `Read(./.env)` | reading `.env` in the current folder | a `Read` deny also blocks Edit and Write on that path |
| `Edit(//e/FinishedPrints/**)` | edits anywhere under `E:\FinishedPrints` | `//` means an absolute path; Windows paths become `/e/...` |
| `WebFetch(domain:wiki.bambulab.com)` | fetches from that site | |
| `mcp__mm-audit__*` | every tool of the `mm-audit` MCP server | allow rules need the literal `mcp__<server>__` prefix |
| `Agent(Explore)` | the Explore subagent | use in `deny` to switch an agent off |

Watch out for these, all from the permissions page:
- `Edit(/docs/**)` with **one** leading slash is relative to the project, not the drive. Use `//` for absolute paths.
- `Write(...)` path rules are accepted but **never match**. Write path rules as `Edit(...)`.
- Rules written with parentheses for an MCP tool are skipped when the settings file loads.
- **On Windows with Git Bash installed, any `Bash` deny rule also switches off the PowerShell tool**, silently, unless
  you also add a `PowerShell(...)` rule or set `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`
  ([Tools reference](https://code.claude.com/docs/en/tools-reference), "Bash deny rules also turn off the PowerShell
  tool"). The deletion example below pairs every Bash rule with a PowerShell rule for that reason.

### What this repository ships
Read the files yourself: [`.claude/settings.json`](../.claude/settings.json) and its explanation
[`.claude/settings.notes.md`](../.claude/settings.notes.md).

- **Allow:** nothing. The shipped file has no `allow` list, so every approval is yours or your mode's.
- **Ask:** nothing extra.
- **Deny, always:**
  - any MCP tool, on any server, whose name contains `print` or `queue`;
  - any `upload_gcode` or `send_gcode` tool;
  - `upload` and `start` tools on any server whose name contains `bambu` or `printer`;
  - reading `.env` and `.env.*` in the project folder (`Read(./.env)`, `Read(./.env.*)`).
- **Hooks:** a `PreToolUse` guard on Write, Edit, MultiEdit, NotebookEdit, Bash and PowerShell
  ([`tools/hooks/guard_paths.py`](../tools/hooks/guard_paths.py)) that blocks the call if it cannot run
  (`"onFailure": "block"`, Claude Code v2.1.295 or later), a `SessionStart` hook that prints the lessons, a
  `PostToolUse` note checker and a `SubagentStop` run logger.

### What the guard hook blocks (and what it does not)
[`tools/hooks/guard_paths.py`](../tools/hooks/guard_paths.py) runs before every file write and shell command. It blocks a
call by exiting with code 2, which the [hooks reference](https://code.claude.com/docs/en/hooks) defines as "Blocks the
tool call" for `PreToolUse`.

It blocks:
- **Writes into protected roots:** any file-tool write under a folder listed in `protected_roots` in
  `config\paths.yaml`, or in the `MM_PROTECTED` environment variable (semicolon-separated).
- **Shell commands that name a protected root** with anything but a read-only verb: no `rm`, `mv`, `Remove-Item`,
  `Set-Content`, redirect (`>`), `cd` into the root, or copy *into* it. Copying *out of* it and reading it are allowed.
- **Tricks around the path:** it follows junctions and symlinks, expands 8.3 short names and maps `\\?\` and
  `\\host\D$\` spellings back to the drive letter.
- **A bare `python`, `py` or `pip`** run from inside the project. Use `.venv\Scripts\python.exe`.
- **Broken config, fail closed:** if `config\paths.yaml` exists but cannot be read, every file write and every shell
  command that is not purely read-only is blocked, except editing `config\paths.yaml` itself so you can fix it.

It does **not** block:
- **Anything, until you add folders.** `protected_roots` is empty in `config\paths.example.yaml`. Add your important
  folders (finished prints, photos, other projects): see [08 - Make it yours](08-customize.md).
- **Paths it cannot see in the command text,** such as a path built inside a Python script or read from a file.
- **Anything, on an old Claude Code, if it cannot start.** It runs with `.venv\Scripts\python.exe`. The shipped
  settings set `"onFailure": "block"` on this hook only. The hooks reference says that with it, a hook that "fails to
  start", crashes (exit code other than 0 or 2) or times out blocks a `PreToolUse` call, and that the field "Requires
  Claude Code v2.1.295 or later" ([hooks, "Block the action when a hook fails"](https://code.claude.com/docs/en/hooks)).
  So on v2.1.295 or later, a missing venv means every file write and shell command is **blocked** until you run
  `tools\setup.ps1` yourself in the VS Code terminal. On an older version the guard stays fail-open (a hook that cannot
  start is a "non-blocking error" and the call goes ahead), and what an older version does with the unknown field is
  (not verified). The panel uses the copy of Claude Code inside the VS Code extension, so update the extension. Details:
  [.claude/settings.notes.md](../.claude/settings.notes.md).
- **Deletions outside the protected roots.** Be honest with yourself here: **no shipped deny rule stops Claude from
  deleting files outside this repository.** Your mode's prompts and Claude Code's built-in critical-path checks are all
  that stand in the way until you add rules.

### Add deletion rules safely
Deleting files is on the owner-only list, so the simplest safe rule is: Claude never deletes, you do. Put this in
`.claude\settings.local.json` (your personal, git-ignored file; see the next section):

```json
{
  "permissions": {
    "deny": [
      "Bash(rm *)",
      "Bash(rmdir *)",
      "PowerShell(Remove-Item *)",
      "Edit(//e/FinishedPrints/**)"
    ]
  }
}
```

- `Bash(rm *)` also matches a bare `rm` and `FOO=bar rm -rf tmp/`: the docs say a deny rule matches past any leading
  variable assignment.
- `PowerShell(Remove-Item *)` keeps the PowerShell tool switched on next to the Bash rules (see the warning above). The
  docs say common aliases are canonicalised; whether every alias (`del`, `erase`, `rd`, `ri`, `rm`, `rmdir`) and
  `cmd /c del` is covered by this one rule is (not verified).
- Replace `//e/FinishedPrints/**` with your own folder (`E:\FinishedPrints` is written `//e/FinishedPrints/**`). Add one
  line per folder Claude must never change. Add the same folders to `protected_roots` so the guard hook covers shell
  commands too.
- After saving, open **Permissions** (command menu `/` > Customize) and check the rules are listed.

**The limits, in the docs' own words.** A Bash rule "isn't a security boundary around the program"
([permissions, "What a Bash rule doesn't match"](https://code.claude.com/docs/en/permissions)). `Bash(rm *)` stops
`rm -rf build/` but not `/bin/rm -rf build/` or `bash -c 'rm -rf build/'`, and no rule sees files that a Python or Node
script deletes by itself. "Outside the repository" cannot be written as a command pattern at all. For enforcement that
does not depend on command text, the docs point to the sandbox, which runs on macOS, Linux and WSL2 but not on native
Windows ([Sandboxing](https://code.claude.com/docs/en/sandboxing)). On a Windows PC, your real safety nets are: rules
and the guard hook as speed bumps, Manual mode for risky tasks, and a backup of anything you cannot lose.

### Add your own allow rules
Use `.claude\settings.local.json` in the project folder:
- It is your personal file for this one project and overrides the shared `.claude\settings.json`
  ([Settings, "Keep personal settings out of a repository"](https://code.claude.com/docs/en/settings)).
- This repository's [.gitignore](../.gitignore) lists `.claude/settings.local.json`, so it is never committed.
- On Windows it stays next to `.claude\settings.json` (same page, "Where Claude Code keeps the local file").
- Its allow rules apply without the workspace-trust step while the file is untracked
  ([permissions, "When your local settings file needs trust"](https://code.claude.com/docs/en/permissions)).

**Easiest way:** when a prompt offers **Yes, and don't ask again**, pick it. For Bash commands and web domains,
Claude Code saves the exact rule into `.claude\settings.local.json` for you
([permissions, "Permission system"](https://code.claude.com/docs/en/permissions)). File-edit approvals last only until
the session ends.

**By hand**, for example to let research and the read-only audit server run without prompts:

```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:wiki.bambulab.com)",
      "WebFetch(domain:code.claude.com)",
      "mcp__mm-audit__*",
      "Bash(git add *)",
      "PowerShell(git add *)"
    ]
  }
}
```

One file can hold both `allow` and `deny` lists; merge the two examples into one `permissions` object.

Rules of thumb from the docs:
- Put the `*` **after** the subcommand: `Bash(git log *)` allows only `git log`, while `Bash(git *)` allows every git
  command, `git push` included.
- Never allow `Bash`, `PowerShell` or `Bash(python *)` as a whole: that approves every command, deletions included.
- Do not allow anything that prints, uploads, installs, signs in, spends or sends. Those stay owner-only.

---

## 3. The "skip all permissions" flag

The official names are the CLI flag `--dangerously-skip-permissions`, which the CLI reference calls "Equivalent to
`--permission-mode bypassPermissions`", and the mode `bypassPermissions`, labelled **Bypass permissions** in VS Code.
Sources: [CLI reference](https://code.claude.com/docs/en/cli-reference) and
[permission-modes, "Skip all checks with bypassPermissions mode"](https://code.claude.com/docs/en/permission-modes).

**What it does:** it turns off permission prompts and safety checks, so tool calls "execute immediately, including
writes to protected paths" (quoted). It turns off the classifier that auto mode uses and offers "no protection against prompt
injection or unintended actions" (quoted).

**Why only in a throwaway VM or container, never on your daily PC:**
- The docs' own warning: use this mode only in isolated containers, VMs or dev containers without internet access,
  "where Claude Code cannot damage your host system."
- The VS Code setting for it, `allowDangerouslySkipPermissions`, is described as "Use it only in sandboxes with no
  internet access" ([VS Code, "Extension settings"](https://code.claude.com/docs/en/vs-code)).
- On your PC, one wrong command, or one web page with hidden instructions, would run with your user rights against your
  files, your accounts and anything your printers' software can reach. The Bash sandbox that could contain it does not
  run on native Windows ([Sandboxing](https://code.claude.com/docs/en/sandboxing)).
- If you want fewer prompts on your own PC, use **Auto** instead; the docs recommend it over bypass for exactly this.

**How it is switched on (so you recognise it):** in the CLI, start with `--dangerously-skip-permissions` or
`--permission-mode bypassPermissions`. In VS Code, the **Allow dangerously skip permissions** toggle in the extension
settings adds **Bypass permissions** to the mode indicator. In the Claude Desktop app's Code tab, the
**Allow bypass permissions mode** toggle does the same on Pro and Max plans. You cannot switch into it from a session
that was started without it enabled. The first interactive start shows a warning dialog you must accept.

**What still applies under it, exactly as the docs say:**

| Protection | Still applies in `bypassPermissions`? | Source |
|---|---|---|
| Deny rules (including this repo's no-print denies) | **Yes.** "Deny rules block in every mode, including `bypassPermissions`." | [permission-modes, "Available modes"](https://code.claude.com/docs/en/permission-modes) |
| Allow rules | No effect: "Allow rules have no effect in `bypassPermissions`." | same |
| Explicit `ask` rules | Yes, they still prompt | same, "Actions no mode auto-approves" |
| Recognised `rm`/`rmdir` critical-path removals | Yes, they still prompt (two-minute countdown in a terminal) | same, "Critical-path removals in each permission mode" |
| `Remove-Item` denies on system paths and bare wildcards | Yes | same, "Remove-Item in PowerShell" |
| Protected paths (`.git`, `.claude`, `.vscode` ...) | **No**, writes are allowed | same, "Protected paths" |
| The guard hook (`PreToolUse`, exit code 2) | (not verified): no page states it in one sentence. The hooks reference lists `"bypassPermissions"` as a value hooks receive in `permission_mode`, which implies hooks still run, and the permissions page says a hook that exits with code 2 "stops the tool call before permission rules are evaluated". Test it in your VM before relying on it. | [hooks](https://code.claude.com/docs/en/hooks), [permissions](https://code.claude.com/docs/en/permissions) |
| The rules in `CLAUDE.md` and your owner profile | They are instructions to the model, not enforcement; nothing stops a confused or manipulated model from ignoring them | [permissions, "Manage permissions"](https://code.claude.com/docs/en/permissions) |

If you never want bypass to be possible, set `permissions.disableBypassPermissionsMode` to `"disable"` in your user file
`~/.claude/settings.json`; the docs say it "works from any scope" and a user can lock themselves out of bypass mode
([permissions, "Managed settings"](https://code.claude.com/docs/en/permissions)).

---

## 4. Subagents, parallel work and background tasks

Source for this section: [Create custom subagents](https://code.claude.com/docs/en/sub-agents), plus
[VS Code](https://code.claude.com/docs/en/vs-code) and [Interactive mode](https://code.claude.com/docs/en/interactive-mode).

### Parallel subagents
A subagent is a separate Claude with its own context, tools and instructions. Ask for independent jobs in one prompt and
Claude runs them side by side, for example:

```text
Research PETG drying temperature, PLA bed adhesion on textured PEI and TPU retraction in parallel using separate researcher subagents.
```

- Only parallelise work that does not depend on another job's result.
- The docs warn that many subagents returning long reports "can consume significant context", and each spends its own
  tokens.
- By default, at most 20 subagents run at once in a session (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` changes it).

### Background tasks
- With nothing configured, a subagent Claude starts from your main conversation **runs in the background** while you keep
  working; its result arrives later as a completion notification.
- When a background subagent needs a permission, the prompt appears **in your main session** and names the subagent.
  Approve it, or press Esc to deny that one call without stopping the subagent.
- **Subagents use the main conversation's mode.** If the main conversation is in `bypassPermissions`, `acceptEdits` or
  auto mode, the subagent runs in that same mode and its own `permissionMode` setting is ignored.
- Long shell commands can also run in the background: ask Claude to, press `Ctrl+B` in the terminal, or click
  **Run in background** under the tool call in VS Code.

### How to check on them
- **VS Code:** when subagents exist, an agent count such as **2 agents** appears at the bottom of the prompt box; its dot
  shows whether one is working or waiting for your permission. Click it to open the **agent map**: each subagent's status,
  elapsed time and tokens, its prompt and tool calls, its read-only transcript, and a stop button. Type `/tasks` in the
  prompt box to open the same map when no count is showing (for example for a background shell command). A blue dot on
  a conversation tab's spark icon means a permission request is waiting.
- **CLI:** type `/tasks` to list running shells and subagents, press `Enter` on one to open it.
  `Ctrl+X Ctrl+K` (pressed twice within 3 seconds) stops all background subagents.
  `claude agents` opens the agent view for parallel background *sessions* (a separate feature).
- **This project:** the `SubagentStop` hook appends one line per finished subagent to `work\agent-runs.log`
  (git-ignored), so a subagent that ended silently still leaves a trace.

### This repository's agents
The agents live in [`.claude/agents/`](../.claude/agents/), the project scope the docs describe; Claude Code finds them
automatically when you open this folder. Three ways to use one:
1. **Name it:** "Use the dfm-engineer subagent to review `parts\bracket.stl`." Claude decides whether to delegate.
2. **@-mention it:** type `@` and pick it from the list, or type `@agent-print-qa`. This makes sure that agent runs. The
   docs describe the typeahead in general terms; that the VS Code panel shows agents in it is (not verified).
3. **Use a slash command or skill** that runs the pipeline for you, for example `/research-topic <topic>`
   (researcher -> fact-checker -> librarian) or `/preprint-check <file.3mf>` (print-qa). Type `/` in the panel to list
   them. The pipelines are described in [CLAUDE.md](../CLAUDE.md), "Agent army".

Some agents are locked down by design: `print-qa` cannot write files, and no agent has a tool that can print.

---

## 5. The two-brain workflow

An optional way to work for long stretches: two Claudes, one deciding and one building, sharing plain files.

| Role | Runs in | Does | Never does |
|---|---|---|---|
| **Director** | Claude Desktop app (chat) | Reads the builder's reports, checks the evidence, decides technical questions you delegated, writes the next instructions | Owner-only actions; it cannot press Print or approve one |
| **Builder** | Claude Code in VS Code, this project | Reads `plan\handoff\`, builds, runs the gates, appends a report to `plan\handoff\TO_CHAT.md` | Owner-only actions; anything marked `NEEDS_DECISION` waits |
| **You** | Your chair | Carry messages if needed, answer owner-only questions, press Print | Delegate owner-only decisions to either Claude |

### Set it up
1. Follow [templates/handoff/README.md](../templates/handoff/README.md): create `plan\handoff\`, copy
   [templates/handoff/TO_CHAT.template.md](../templates/handoff/TO_CHAT.template.md) to `plan\handoff\TO_CHAT.md`, and
   write at its top which decisions the director may make. `plan/` is git-ignored, so your plans stay on your PC.
2. Add the one-line handoff rule from that README to the end of `CLAUDE.md`.
3. Give the director a reply file. A simple convention: the director writes decisions to `plan\handoff\FROM_CHAT.md`
   (append only, newest at the bottom), and you tell the builder "Read plan\handoff\FROM_CHAT.md and continue." This
   file name is a suggestion of this guide; the project ships no template for it.

### How the director reads and writes the files
- **Manual routine (works everywhere):** copy the newest report from `TO_CHAT.md` into the director chat, then paste its
  reply into `FROM_CHAT.md` or straight into the Claude Code panel.
- **Claude Desktop with folder access:** the Claude Help Center says the desktop app "is the full Cowork experience, where
  Claude can also use your local files and browser", and that Claude "reaches only the folders you've connected, through
  the desktop app, and only while it's open"
  ([Use Claude Cowork on web, desktop, and mobile](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)).
  Connect only the `plan\handoff\` folder, never the whole project or your drive. The same article says that on Pro
  and Max plans new Cowork sessions run in the cloud and fetch copies of the files they need. The exact steps to connect
  a folder are (not verified) in this guide; follow the app.

### Scheduled check-ins (official features only)
These exist, per the official docs. Each starts a new run; none of them can approve an owner-only action.

| Feature | Where | What it is good for | Limits from the docs |
|---|---|---|---|
| **Local scheduled task** | Claude Desktop, **Code** tab > **Scheduled** > **New task**, with **Only on this computer** turned on | A builder check-in on your PC, for example hourly: "Read plan\handoff\FROM_CHAT.md, continue approved steps, append a report to TO_CHAT.md" | Runs only while the app is open and the PC is awake; a Manual-mode run stalls on any permission until you answer it in that run's session; needs Claude Desktop 1.1.5368 or later ([Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)) |
| **Cowork scheduled task** | Claude Desktop (or web/mobile), **Scheduled** in the left sidebar | A director check-in: summarise the latest report, list decisions | Runs remotely; it can reach your local files only while the desktop app is open ([Schedule recurring tasks in Claude Cowork](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)) |
| **`/loop`** | Inside an open Claude Code session | Polling during one sitting, for example `/loop 30m check plan\handoff\FROM_CHAT.md for new decisions` | Only while that session is open and idle; recurring loops expire after 7 days ([Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)) |
| **Cloud scheduled task** | claude.ai / Desktop | Work that needs no local files | Runs on a fresh clone in the cloud, so it cannot see your git-ignored `plan\` folder ([scheduled-tasks comparison table](https://code.claude.com/docs/en/scheduled-tasks)) |

Whether a scheduled run inside the VS Code extension is possible is (not verified); the scheduling options above are
the documented ones. A scheduled builder run uses the permission mode you pick for the task, so the rules in
[section 2](#2-allow-ask-and-deny-rules) matter even more there.

### The honest limits
- **Files are the reliable channel.** The two Claudes never talk to each other directly; they read and write files you
  can open, diff and keep.
- **UI automation is fragile.** Scripts that click or type into the Claude windows break when an update moves a button.
  Do not build on them.
- **A person still does every owner-only action.** Neither the director nor a schedule can press Print, buy, install,
  sign in, type a password, delete, publish or send a message. The builder prepares up to that step, marks it
  `NEEDS_DECISION` in `TO_CHAT.md`, and keeps working on whatever is not blocked.
- **Times in reports come from the PC clock,** never a guess (the rule in the handoff README).

---

## 6. A safe setup, step by step

1. Run `tools\setup.ps1` yourself in the VS Code terminal first, so the hooks have their Python
   ([04 - First run](04-first-run.md)). Until then the guard blocks Claude's file writes and shell commands.
2. Add your important folders to `protected_roots` in `config\paths.yaml` ([08 - Make it yours](08-customize.md)).
3. Create `.claude\settings.local.json` with the deletion deny rules from [section 2](#add-deletion-rules-safely), plus
   any allow rules you want.
4. Make your owner profile: copy [templates/OWNER_PROFILE.md](../templates/OWNER_PROFILE.md) to `OWNER_PROFILE.md` in
   the project root and fill it in (see that file, and
   [08 - Make it yours](08-customize.md#make-it-address-you-your-way-owner_profile)).
5. In VS Code, pick **Auto** (or **Edit automatically**) from the mode indicator. Leave **Bypass permissions** off.
6. Give Claude the whole job in one prompt, ask for parallel subagents where the parts are independent, and watch the
   agent map.
7. Read the report at the end: what changed, files to review, Known flaws, and the numbered owner-only questions.

---

## 7. Safety box

> **No AI ever starts, sends, uploads or queues a print.** No mode, flag, rule, schedule or second Claude changes this.
> Claude prepares and checks the files; you read the pre-print checklist and press Print in Bambu Studio yourself.
> See [06 - Print safety](06-print-safety.md).

**Owner-only, always a person's yes in the current session:**
1. Prints: starting, sending, uploading or queuing any print job.
2. Purchases and any spending.
3. Installs of software, packages, extensions or MCP servers.
4. Sign-ins and account sign-ups.
5. Passwords, API keys, tokens and access codes.
6. Deletions of files or folders.
7. Publishing: public repositories, releases, listings, posts.
8. Sending messages: email, chat, comments, forum posts, issues.

**Never store secrets in the repository.** No passwords, API keys, tokens, printer access codes or serial numbers in any
file here, including `OWNER_PROFILE.md`, `config\paths.yaml`, notes and handoff files. Keep them in your password
manager. The shipped rules deny reading `.env` files, but a deny rule cannot protect a secret you pasted into a note.

**Your owner profile** sets your name, tone, reply format and owner-only list. Customise it from
[templates/OWNER_PROFILE.md](../templates/OWNER_PROFILE.md): see that file. You can add items to the owner-only list;
you cannot remove the no-AI-print rule.

---

## 8. Sources

Official Claude Code documentation (each page fetched and read for this guide):
- https://code.claude.com/docs/en/permission-modes - modes, VS Code labels, protected and critical paths, bypass behaviour
- https://code.claude.com/docs/en/permissions - rule syntax, precedence, Bash and PowerShell rule limits, local settings and trust
- https://code.claude.com/docs/en/settings - settings files, precedence, `settings.local.json`
- https://code.claude.com/docs/en/hooks - exit code 2, non-blocking failures, `onFailure`, `permission_mode` values
- https://code.claude.com/docs/en/sub-agents - subagent scope, invocation, background subagents, `/tasks`, limits
- https://code.claude.com/docs/en/vs-code - mode indicator, `initialPermissionMode`, `allowDangerouslySkipPermissions`, agent map
- https://code.claude.com/docs/en/cli-reference - `--permission-mode`, `--dangerously-skip-permissions`, `claude agents`
- https://code.claude.com/docs/en/headless - non-interactive `-p` runs
- https://code.claude.com/docs/en/interactive-mode - `Ctrl+B`, `/tasks`, `Ctrl+X Ctrl+K`
- https://code.claude.com/docs/en/tools-reference - PowerShell tool, Bash deny rules turning PowerShell off
- https://code.claude.com/docs/en/sandboxing - sandbox platforms (not native Windows)
- https://code.claude.com/docs/en/scheduled-tasks - `/loop` and the scheduling comparison
- https://code.claude.com/docs/en/desktop-scheduled-tasks - Claude Desktop local scheduled tasks

Official Claude Help Center:
- https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile - Desktop local file access, cloud sessions
- https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork - Cowork scheduled tasks

This project's own files: [.claude/settings.json](../.claude/settings.json),
[.claude/settings.notes.md](../.claude/settings.notes.md), [tools/hooks/guard_paths.py](../tools/hooks/guard_paths.py),
[templates/handoff/README.md](../templates/handoff/README.md), [templates/OWNER_PROFILE.md](../templates/OWNER_PROFILE.md).
