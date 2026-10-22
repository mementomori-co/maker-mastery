# 04 - First run

You open the project in VS Code, run the setup script once, check your config, write down your gear, and then open
Claude Code for your first prompt. Next: [05 - Daily workflow](05-daily-workflow.md).

> [!IMPORTANT]
> **Run the setup script (step 3) before you open the Claude Code panel (step 6).** The project's hooks run with the
> project's own Python in `.venv\`, which the setup script creates. Before setup, every hook fails to start, and the
> folder guard is not active.

This guide assumes the project is in `C:\Projects\maker-mastery` (guide 03). If yours is elsewhere, use your folder.

## Step 1. Open the folder in VS Code

1. Start VS Code.
2. Click **File > Open Folder...** ([VS Code docs](https://code.visualstudio.com/docs/editing/workspaces/workspaces)).
3. Select `C:\Projects\maker-mastery` and click **Select Folder** (label not verified).
4. VS Code asks whether you trust the authors of the files in this folder. Click **Yes, I trust the authors**
   (label not verified). If you choose **No, I don't trust the authors**, VS Code opens in Restricted Mode, and the Claude
   Code extension "doesn't work in Restricted Mode"
   ([Claude Code VS Code docs](https://code.claude.com/docs/en/vs-code)).

You should see the Explorer on the left with `.claude`, `assets`, `config`, `docs`, `examples`, `knowledge`, `lessons`,
`templates`, `tools`, `CLAUDE.md` and `README.md`. If you see only one folder such as `maker-mastery-main`, you opened
the folder above the project: repeat step 2 and pick the inner folder.

Trusting the folder lets its scripts run. If you want to know what will run, read `tools\setup.ps1` and the three hook
scripts in `tools\hooks\` and `tools\check_note.py` first; they are short and commented.

## Step 2. Open the terminal

1. Click **Terminal > New Terminal** ([VS Code terminal docs](https://code.visualstudio.com/docs/terminal/basics)).
2. A panel opens at the bottom. You should see a prompt like `PS C:\Projects\maker-mastery>`. The `PS` means PowerShell.

If the prompt does not start with `PS` (for example it shows `C:\Projects\maker-mastery>` or a `$`), you have another
shell. Click the small arrow next to the **+** in the terminal panel and choose **PowerShell** (label not verified), or
type `powershell` and press Enter.

## Step 3. Run the setup script

Paste this line into the terminal and press Enter:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\setup.ps1
```

**Why this line, and why it is safe.** Windows PowerShell does not run script files under its default policy on Windows
clients, and files from a downloaded ZIP are marked as coming from the internet. This line starts one new PowerShell
process with the policy set to **Bypass** for that process only, runs `setup.ps1` in it, and exits. Nothing is saved:
Microsoft's docs say a policy set for a session "is stored only in memory and is lost when the session is closed"
([about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)).
Your PC's policy stays exactly as it was, and only this one script runs, which you can read first.

An equivalent two-line form, which lasts until you close this terminal:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\tools\setup.ps1
```

What you should see, in order:

1. `Maker Mastery setup - repository: C:\Projects\maker-mastery` and the line "No AI ever starts, sends, uploads or
   queues a print."
2. `==> Step 1 of 5: looking for Python 3.12 or newer` and `Found Python 3.12 with: py -3.12`.
3. `==> Step 2 of 5: private Python environment (.venv in this repository)`. The script first creates the empty `.venv`
   folder (offline: it uses only the Python you installed and its built-in pip, and downloads nothing). Then it shows the
   list of packages and asks `Install them now? [y/N]`. Type `y` and press Enter. pip downloads and installs the packages into `.venv` only; this
   takes a while and prints many lines.
4. `==> Step 3 of 5: your config file` and `Copied config\paths.example.yaml to config\paths.yaml.`
5. `==> Step 4 of 5: looking for Bambu Studio (read-only check)` and `Found: C:\Program Files\Bambu Studio\bambu-studio.exe`.
6. `==> Step 5 of 5: self-test`, then one line per tool, for example:

   ```text
   Self-test: 15 test files, Python 3.12.10 at C:\Projects\maker-mastery\.venv\Scripts\python.exe
   Nothing here prints, slices or sends anything.

     PASS    audit_3mf.py - slicer-setting checks C1-C16  (41 checks, 0.6 s)
     PASS    audit_3mf.py - load check against your current-load.md (C7)  (25 checks, 0.4 s)
     (13 more lines, one per tool)

   RESULT: PASS - every tool that could be tested works on this PC.
   ```

7. `Setup finished. Open this folder in VS Code and start Claude Code there.` in green.

The `render_critic.py` line needs the optional open3d package for most of its checks. Without it you should see that
line with most checks skipped, which is normal:

```text
  PASS    render_critic.py - render critique (needs optional open3d)  (12 checks, 11 skipped, 0.7 s)
```

To add open3d, run the setup again with
`powershell -ExecutionPolicy Bypass -File .\tools\setup.ps1 -Optional` and answer `y`. (The sample above was captured
on a PC that had open3d; the skipped line was captured on a Python without it.)

If something else happens:

| You see | Do this |
|---|---|
| `running scripts is disabled on this system` | You ran `.\tools\setup.ps1` on its own. Use the one-line command above. |
| `... setup.ps1 is not digitally signed. The script will not execute on the system.` | Your policy is **RemoteSigned** (Microsoft's default for Windows computers) and the file still carries the "downloaded from the internet" mark from the ZIP. Either use the one-line command above, or read `tools\setup.ps1` and then unblock it once with `Unblock-File .\tools\setup.ps1` and run it again. `Unblock-File` removes that internet mark so a RemoteSigned policy runs the script ([Unblock-File](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/unblock-file), [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)). The Process-scope form above (`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`) works too. |
| I answered `N` | Nothing is wrong. `.venv` exists but has no packages yet, so the script skips the self-test and ends with `Setup paused: run tools\setup.ps1 again and answer y when ready.` Run the one-line command again and answer `y`. |
| `Python 3.12 or newer was not found.` | Install Python 3.12 ([02 - Install](02-install.md), part 4), close the terminal (trash-can icon), open a new one and run the line again. |
| `pip install failed (see the lines above).` | Read the last red lines. Usually the internet connection dropped or a path is too long: see [09 - Troubleshooting](09-troubleshooting.md). Then run the line again; it reuses `.venv`. |
| `Bambu Studio was not found at: ...` | Fine for now. Fix it in step 4. |
| `RESULT: FAIL` | Read the lines under the FAIL; they name the test. See [09 - Troubleshooting](09-troubleshooting.md). Nothing is wrong with your printer. |

## Step 4. Check your config

The setup copied `config\paths.example.yaml` to `config\paths.yaml`. That copy holds every machine-specific path and is
never uploaded by git. Check it:

```powershell
.venv\Scripts\python.exe tools\mm_config.py
```

You should see lines such as `bambu_studio_exe: C:\Program Files\Bambu Studio\bambu-studio.exe` and
`slice_workdir: C:\Projects\maker-mastery\work\slice  [does not exist]`. `[does not exist]` on `slice_workdir` is normal
until your first slice.

If `bambu_studio_exe` says `[does not exist]`:

1. In File Explorer, find `bambu-studio.exe` and copy its full path (Shift + right-click the file, **Copy as path**
   (label not verified)).
2. In VS Code's Explorer, open `config\paths.yaml`.
3. Replace the value after `bambu_studio_exe:` with your path, and change every `\` to `/`. **Copy as path** gives a
   path in double quotes with backslashes, which YAML cannot read (it treats `\b`, `\t` and similar as special
   characters). Before and after:

   ```yaml
   # Before (what Copy as path pastes; does not work):
   bambu_studio_exe: "E:\Apps\Bambu Studio\bambu-studio.exe"
   # After (forward slashes; works):
   bambu_studio_exe: "E:/Apps/Bambu Studio/bambu-studio.exe"
   # Also works (single quotes keep the backslashes as they are):
   bambu_studio_exe: 'E:\Apps\Bambu Studio\bambu-studio.exe'
   ```

4. Save (**File > Save**, label not verified) and run the check command again. If it prints
   `ERROR: config\paths.yaml cannot be read (... line N ...)`, fix that line the same way.

If `config\paths.yaml` is missing (you skipped setup), create it with
`Copy-Item config\paths.example.yaml config\paths.yaml`.

## Step 5. Write down your gear

Claude answers for your gear only, and never assumes a filament is loaded. Two files hold that:
`knowledge\00-gear-inventory\current-load.md` (what is on the printer today) and `printers.md`, which you create
yourself in the same folder (what you own). Read
[the folder's README](../knowledge/00-gear-inventory/README.md) once.

You can fill them by hand now, or let Claude interview you in step 7. By hand:

1. Get today's date in the right format:

   ```powershell
   Get-Date -Format yyyy-MM-dd
   ```

2. Open `knowledge\00-gear-inventory\current-load.md`. Replace `YYYY-MM-DD` in the `Verified:` line with that date.
3. In the load table, delete the rows of printers you do not own, and for each position write what is really there, in
   the format the file explains: `EMPTY`, or the spool in bold such as `**Bambu PLA Basic, Black**`, and the plate name
   such as `Textured PEI`. Save.

Until this file has a real date and real rows, the 3MF audit's load check (C7) FAILs on purpose, so nothing can be
called ready to print. That is the rule working, not a bug.

If you create `printers.md` yourself, start it with an `Applies to:` line, a `Verified: YYYY-MM-DD` line with a real date,
and end it with a `Sources:` line followed by one line such as `- my own look at the printer, measured`. The note checker
(a hook) reports any knowledge file without these lines.

## Step 6. Open the Claude Code panel and sign in

1. Open any file (for example click `README.md` in the Explorer). Click the **Spark icon** in the **Editor Toolbar** at
   the top right of the editor. Other ways: the Spark icon in the **Activity Bar** on the left, or **✻ Claude Code** in the
   **Status Bar** at the bottom right ([Claude Code VS Code docs](https://code.claude.com/docs/en/vs-code)).
2. The first time, a sign-in screen appears. Click **Sign in** and finish in your browser.
3. You should see the chat panel with a prompt box at the bottom. A **Learn Claude Code** checklist may appear; you can
   dismiss it.

If you see **Not logged in · Please run /login**, run **Developer: Reload Window** from the Command Palette
(`Ctrl+Shift+P`). If the panel shows an error about a hook or `python.exe`, setup did not finish: go back to step 3.

## Step 7. Your first prompts

Click in the prompt box, type or paste a prompt, and press Enter. Claude asks for permission before it edits a file or
runs a command (depending on the permission mode shown under the prompt box); read what it wants to do, then allow it.

A good first prompt:

```text
Read CLAUDE.md and knowledge\00-gear-inventory\README.md. Then ask me what is physically loaded on my printer right
now, one numbered question at a time, and fill knowledge\00-gear-inventory\current-load.md with today's date from the
PC clock. Write only what I answer.
```

You should see Claude summarise the rules, then ask you questions one at a time, then show you the edited file.

Then try the calibration cube:

```text
Walk me through examples\calibration-cube\README.md. Generate the cube, then tell me exactly what to click in Bambu
Studio. Do not print anything; I will press Print myself.
```

Or ask the library something:

```text
Using only knowledge\03-materials, what drying temperature and time do the notes give for PETG, and from which source?
```

Type `/` in the prompt box to see the skills and commands, for example `/preprint-check` and `/research-topic`.

Optional: the read-only audit MCP server (`mm-audit`) lets Claude call the audits as tools. It is off by default; see
[`.mcp.json.example.md`](../.mcp.json.example.md) to turn it on.

Next: [05 - Daily workflow](05-daily-workflow.md).
