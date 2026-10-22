# 10 - FAQ

Short answers. Each links to the guide with the details. Back to the start: [01 - What this is](01-what-this-is.md).

## The basics

**What is this, in one line?**
A project folder that turns Claude Code in VS Code into a careful maker's assistant: rules, a cited knowledge library,
agents, skills, checking tools and lessons. See [01 - What this is](01-what-this-is.md).

**Do I need to know how to code?**
No. You type requests in plain English in the Claude Code panel and paste a few PowerShell lines from the guides.

**What does it cost?**
The project is free under the MIT License. Claude Code needs an Anthropic account with a paid Claude plan or a Claude
Console account ([Claude Code VS Code docs](https://code.claude.com/docs/en/vs-code)). Git, VS Code, Python and Bambu
Studio are free downloads.

**Does it work on macOS or Linux?**
It was written and tested on Windows 11 only. The setup script, the hooks and every guide assume Windows.

**Do I need a Bambu Lab printer?**
No. The library, agents and most tools help any maker. Slicing (`tools\slice_cli.py`) and the 3MF audit are written for
Bambu Studio and Bambu Lab printers.

**Which printers are covered best?**
The printer notes cover the Bambu Lab H2C and P1S; the slicer, materials and design notes apply more widely, and each fact
says which printer or condition it applies to. Add notes for your model with `/research-topic`.

## Safety and control

**Can Claude start a print?**
No. No tool here can talk to a printer, the settings deny print, upload and start tools from any MCP server, and the
rulebook forbids it. You press Print. See [06 - Print safety](06-print-safety.md).

**Can Claude delete my files or install things?**
The rulebook says nothing is installed or deleted without your explicit yes, and Claude Code asks permission before
commands and edits in its default modes. Folders listed under `protected_roots` in `config\paths.yaml` are blocked for
writes by a hook. See [08 - Customize](08-customize.md#machine-paths).

**Can Claude work for hours without asking me every few minutes?**
Yes, with Auto or Edit automatically mode, your own allow rules and parallel subagents, while prints and the other
owner-only actions stay with you. Deletions outside the project are not blocked by a shipped rule; the guide shows how
to add one. See [11 - Autonomous mode](11-autonomous-mode.md).

**Why did the audit FAIL on a perfectly good file?**
Most often the load check (C7): your `current-load.md` still has the placeholder date or does not list the filament. That
is on purpose. See [09 - Troubleshooting](09-troubleshooting.md#7-the-audits-load-check-c7-fails).

**Is my data sent anywhere?**
The tools run locally and make no network calls. Your prompts and the files Claude reads are sent to Anthropic as part of
using Claude Code. `config\paths.yaml`, `.venv\` and `work\` are ignored by git.

## Knowledge

**How do I know a fact is right?**
Every fact in a note links its public source, the note carries the date it was verified, and anything unchecked is marked
"not verified". New facts pass an independent fact-checker before they are filed. Sources can change: if a page says
something else today, the note is out of date, and `/verify-claim` checks it again.

**Why are some domains marked v1.1?**
Version 1.0 ships 16 domains. The rest of the map, including game design and game development, is released after the
same source and privacy review. Your [CURRICULUM.md](../CURRICULUM.md) already lists every domain.

**Can I add my own notes?**
Yes: `/research-topic <topic>`, or by hand from `templates\note.md`. See [08 - Customize](08-customize.md#adding-knowledge).

## Setup

**Why must setup run before I open Claude Code?**
The hooks run with `.venv\Scripts\python.exe`, which setup creates. See [04 - First run](04-first-run.md).

**Is the execution-policy bypass safe?**
It applies to the one PowerShell process that runs `setup.ps1` and ends with it; your PC's policy is unchanged. Read the
script first if you like. See [04 - First run](04-first-run.md#step-4-run-the-setup-script).

**Does setup install anything globally?**
No. Packages go into `.venv` inside the project folder, after you answer `y`. Python, Git, VS Code and Bambu Studio are
installed by you, from their official pages.

**Can I use a newer Python than 3.12?**
The setup accepts 3.12 or newer, but the pinned package versions were tested on 3.12 only.

**What is the optional MCP server for?**
It lets Claude call three read-only audits as tools instead of scripts. Nothing needs it. See
[.mcp.json.example.md](../.mcp.json.example.md).

**What is the "handoff" I keep reading about?**
An optional workflow where a second Claude chat reviews Claude Code's reports. See
[templates/handoff/README.md](../templates/handoff/README.md).

## Sharing

**Can I share my copy or publish a fork?**
Yes, under the MIT License, but replace the brand assets first and run the privacy scan. See
[08 - Customize](08-customize.md#replacing-the-brand-forks) and [NOTICE.md](../NOTICE.md).

**How do I report a security problem?**
Privately, through GitHub's vulnerability reporting, as described in [SECURITY.md](../SECURITY.md). A route that lets
software start a print counts as a security problem.

**How do I contribute a fix or a note?**
Read [CONTRIBUTING.md](../CONTRIBUTING.md): a public source and an independent fact-check for every fact, and a clean
privacy scan.
