# 09 - Troubleshooting

The 15 problems you are most likely to meet, each with what you see and the fix. Run every command in the VS Code
terminal (**Terminal > New Terminal**) from the project folder unless the fix says otherwise. Next: [10 - FAQ](10-faq.md).

If your problem is not here, ask Claude in the panel: paste the exact error and say which step you were on.

## Contents

1. [Running scripts is disabled on this system](#1-running-scripts-is-disabled-on-this-system)
2. [Python 3.12 or newer was not found](#2-python-312-or-newer-was-not-found)
3. [`python` opens the Microsoft Store or is not recognized](#3-python-opens-the-microsoft-store-or-is-not-recognized)
4. [A hook error when Claude Code starts](#4-a-hook-error-when-claude-code-starts)
5. [PyYAML is missing](#5-pyyaml-is-missing)
6. [Bambu Studio is installed somewhere else](#6-bambu-studio-is-installed-somewhere-else)
7. [The audit's load check C7 fails](#7-the-audits-load-check-c7-fails)
8. [The note checker blocks: missing Verified date](#8-the-note-checker-blocks-missing-verified-date)
9. [Long paths: pip or a tool cannot find a file](#9-long-paths-pip-or-a-tool-cannot-find-a-file)
10. [The project is inside OneDrive](#10-the-project-is-inside-onedrive)
11. [pip install failed](#11-pip-install-failed)
12. [The Claude Code panel or Spark icon is missing](#12-the-claude-code-panel-or-spark-icon-is-missing)
13. [Not logged in](#13-not-logged-in)
14. [Claude's command was blocked by guard_paths](#14-claudes-command-was-blocked-by-guard_paths)
15. [C8 warns that a filament profile was not found](#15-c8-warns-that-a-filament-profile-was-not-found)

## 1. Running scripts is disabled on this system

**You see:** `.\tools\setup.ps1 cannot be loaded because running scripts is disabled on this system` or a message about
the file not being digitally signed.

**Why:** Windows PowerShell's default policy on Windows clients does not run script files, and files from a downloaded
ZIP are marked as coming from the internet
([about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)).

**Fix:** run the script through a one-off process with the policy bypassed for that process only:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\setup.ps1
```

Nothing about your PC's policy changes; the setting ends with that process. Do not change the machine-wide policy for
this project.

If the message says the file `is not digitally signed`, your policy is **RemoteSigned** and the script still carries
the "downloaded from the internet" mark from the ZIP. Besides the line above, you can read `tools\setup.ps1` and then
remove that mark once with `Unblock-File .\tools\setup.ps1`
([Unblock-File](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/unblock-file)).

## 2. Python 3.12 or newer was not found

**You see:** `Python 3.12 or newer was not found.` from the setup script.

**Fix:**

1. Run `py --list`. If 3.12 is not in the list, install it ([02 - Install, section 3](02-install.md#3-python-312)).
2. Close the VS Code terminal (trash-can icon) and open a new one with **Terminal > New Terminal**. A terminal opened
   before the install does not see the new PATH. If that is not enough, close and reopen VS Code.
3. Run the setup line again.

## 3. `python` opens the Microsoft Store or is not recognized

**You see:** typing `python` opens the Microsoft Store, prints a message that starts `Python was not found; run without
arguments to install from the Microsoft Store` (exact wording not verified), or says `python is not recognized`.

**Why:** the PATH box was not ticked in the installer, and Windows offers its Store shortcut instead.

**Fix:** you do not need a bare `python` for this project: the setup script uses `py -3.12`, and every command in the
guides uses `.venv\Scripts\python.exe`. If you want it anyway, run the Python installer again, choose to modify the
installation (label not verified) and tick the PATH option, or turn off the Store shortcut: open **Manage app execution
aliases** from Start and switch the **App Installer** Python entries to Off
([Microsoft Learn, Python on Windows FAQ](https://learn.microsoft.com/en-us/windows/dev-environment/python)); in
Settings that page is under **Settings > Apps > Advanced app settings > App execution aliases** (label not verified).

## 4. A hook error when Claude Code starts

**You see:** in the Claude Code panel, an error mentioning a hook, `SessionStart`, `PreToolUse`, or
`.venv/Scripts/python.exe` not found. Or every file edit and shell command Claude tries is blocked, with an error that
contains `failed; blocking because onFailure is "block"`.

**Why:** the hooks in `.claude\settings.json` run the project's own Python, `.venv\Scripts\python.exe`. Before setup, it
does not exist. The folder guard (`PreToolUse`) is set to fail closed (`"onFailure": "block"`), so on Claude Code
v2.1.295 or later it blocks every write and shell command until the venv exists; Claude cannot run setup for you then.
On an older Claude Code the guard cannot start and nothing is guarded. The quoted error text is from the
[hooks reference](https://code.claude.com/docs/en/hooks); the exact wording on your screen is not verified.

**Fix:**

1. Close the Claude Code panel.
2. Run the setup ([04 - First run](04-first-run.md), step 4) and wait for `Setup finished`.
3. Check: `Test-Path .venv\Scripts\python.exe` should print `True`.
4. Run **Developer: Reload Window** from the Command Palette (`Ctrl+Shift+P`) and open the panel again.

> **Warning: a Settings Error that names `.claude\settings.json`.** If a Settings Error names `.claude\settings.json`,
> choose **Exit** and update Claude Code ([check your version](02-install.md#check-your-claude-code-version); this
> project needs v2.1.295 or later). Never "continue without the broken settings": that drops the deny rules (including
> the no-print rules) and the guard hook for the whole session.
>
> Per the settings docs, a Settings Error means a file has invalid JSON or a value the schema rejects, and the dialog
> offers to fix the file with Claude's help, exit, or "continue without the broken settings"
> ([Settings, "Fix a broken settings file"](https://code.claude.com/docs/en/settings#fix-a-broken-settings-file)). The
> same section says a `-p` (print, headless) run shows no dialog: Claude Code skips the broken file silently and
> carries on with the rest. After such a run, `claude doctor` shows what it dropped, and in an interactive session
> `/status` lists the affected files (same section). So never run `claude -p` in this folder before you have confirmed
> that `.claude\settings.json` loads without an error.

## 5. PyYAML is missing

**You see:** `config line N is not 'key: value': ... (install PyYAML for full YAML)`, or `No module named 'yaml'`.

**Why:** `tools\mm_config.py` uses PyYAML when it is installed and otherwise reads only the simple `key: value` form of
`config\paths.example.yaml`. A multi-line list or other YAML features in your `config\paths.yaml` need PyYAML.

**Fix:** install the requirements into the project environment (this is what setup does):

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt -c constraints.txt
```

Or keep your `config\paths.yaml` in the simple one-line form the example uses.

## 6. Bambu Studio is installed somewhere else

**You see:** `Bambu Studio was not found at: C:\Program Files\Bambu Studio\bambu-studio.exe` from setup, or
`bambu-studio.exe not found at '...': set bambu_studio_exe in config\paths.yaml or pass --exe` from `slice_cli.py`.
Or, after you pasted a path: `ERROR: config\paths.yaml cannot be read (..., line N): ...` from `tools\mm_config.py`, or
a hook message `config\paths.yaml cannot be read; fix it (see docs\09) before Claude can write files`.

**Why the paste fails:** File Explorer's **Copy as path** (label not verified) gives `"E:\Apps\Bambu Studio\bambu-studio.exe"`:
backslashes inside double quotes. YAML treats a backslash inside double quotes as the start of an escape, so `\A` is an
error and `\b` silently becomes a control character. The tools refuse such a value with the message above, and the
folder guard blocks Claude's writes until the file is fixed (it still lets you or Claude edit `config\paths.yaml`).

**Fix:**

1. Find `bambu-studio.exe` in File Explorer and copy its path.
2. Open `config\paths.yaml` in VS Code and set `bambu_studio_exe` to that path. Change every `\` to `/` and keep the
   double quotes, or keep the backslashes and use single quotes instead:

   ```yaml
   # Before (Copy as path; does not work):
   bambu_studio_exe: "E:\Apps\Bambu Studio\bambu-studio.exe"
   # After, forward slashes:
   bambu_studio_exe: "E:/Apps/Bambu Studio/bambu-studio.exe"
   # After, single quotes:
   bambu_studio_exe: 'E:\Apps\Bambu Studio\bambu-studio.exe'
   ```

   Save. The same rule applies to every path in the file (`blender_exe`, `allowed_roots`, `protected_roots` and others).
3. Check: `.venv\Scripts\python.exe tools\mm_config.py`. It should print no `ERROR`, and the `bambu_studio_exe` line
   should no longer say `[does not exist]`.

## 7. The audit's load check C7 fails

**You see:** `[FAIL] C7: L1: ... has no valid 'Verified: YYYY-MM-DD' (MISSING) - undated load = unknown load` and more C7
FAIL lines, `VERDICT: FAIL`.

**Why:** this is on purpose. `knowledge\00-gear-inventory\current-load.md` ships as an empty template: every slot says
EMPTY and the date is the placeholder. Until you record what is physically loaded, no print file can pass.

**Fix:** fill the file ([04 - First run](04-first-run.md), step 6): a real date in the `Verified:` line (from
`Get-Date -Format yyyy-MM-dd`), only your printers' rows, and each loaded spool in bold, for example
`**Bambu PLA Basic, Black**`. Then run the audit again. If C7 still fails, read the C7 lines: they say which row or
filament does not match (wrong side on a dual-nozzle printer, wrong colour, wrong plate).

## 8. The note checker blocks: missing Verified date

**You see:** after Claude writes a file under `knowledge\`, a message such as
`FAIL knowledge\00-gear-inventory\printers.md - missing 'Verified: YYYY-MM-DD'`, or `missing 'Applies to:' line`,
`missing 'Sources:' section`, `fact bullet without URL / local path / 'measured' / 'not verified' ...`.

**Why:** a hook runs `tools\check_note.py` after every write under `knowledge\`. It requires an `Applies to:` line, a
`Verified:` line with a real date in digits (the placeholder `YYYY-MM-DD` does not count), a `Sources:` section with a
URL, and a source on each fact bullet (its own URL, the word "measured", a "not verified" label, a link to another
note, or "same source" under a bullet with a URL in the same subsection). The file was written; the hook tells Claude
what to fix.

**Fix:** ask Claude to fix the note, or add the lines yourself. For your own gear files, the source line can be
`- my own look at the printer, measured`. Check by hand with `.venv\Scripts\python.exe tools\check_note.py <file>`.

## 9. Long paths: pip or a tool cannot find a file

**You see:** pip errors such as `OSError: [Errno 2] No such file or directory` with a very long path, or
`Could not install packages due to an OSError`.

**Why:** Windows limits classic paths to 260 characters unless long paths are enabled
([Python docs, "Removing the MAX_PATH Limitation"](https://docs.python.org/3.12/using/windows.html)).

**Fix (either):**

- Move the project to a short path such as `C:\Projects\maker-mastery` (guide 03), delete the `.venv` folder in File
  Explorer, and run setup again.
- Or enable long paths: run the Python installer again and use **Disable path length limit** (label not verified), or
  follow the Python docs page above. That change needs administrator rights.

## 10. The project is inside OneDrive

**You see:** the project's path contains a `OneDrive` folder, or File Explorer shows cloud or tick
icons beside the project's files; setup is very slow, or tools report a file in use.

**Why:** `.venv` holds thousands of files and the tools write into `work\`; a sync client uploads and may lock them (from
general experience, not verified against a Microsoft page).

**Fix:** move the project to a local folder outside OneDrive, such as `C:\Projects\maker-mastery`: close VS Code, move
the folder in File Explorer, delete the `.venv` folder inside it (a venv does not survive a move), reopen the folder in
VS Code and run setup again.

## 11. pip install failed

**You see:** `pip install failed (see the lines above).` from setup.

**Fix:**

1. Read the last red lines above it. `Could not find a version that satisfies the requirement` usually means your Python
   is not 3.12 (the pinned packages were tested on 3.12): run `py --list` and install 3.12.
2. Connection errors: check your internet connection or proxy and run setup again; it reuses `.venv` and continues.
3. Path errors: see problem 9.

## 12. The Claude Code panel or Spark icon is missing

**Fix, in order** (from the [Claude Code VS Code docs](https://code.claude.com/docs/en/vs-code)):

1. The Spark icon in the **Editor Toolbar** only appears when a file is open: click any file first. The Spark icon in
   the **Activity Bar** and **✻ Claude Code** in the **Status Bar** are always there.
2. Check the extension is installed: `Ctrl+Shift+X`, search "Claude Code".
3. Run **Developer: Reload Window** from the Command Palette.
4. Check workspace trust: the extension does not work in Restricted Mode. Trust the folder (the banner at the top
   offers **Manage**; then choose **Trust**).
5. Check your VS Code version is 1.94.0 or later: **Help > About** (label not verified).

## 13. Not logged in

**You see:** **Not logged in · Please run /login** in the panel.

**Fix:** the extension should reopen the sign-in screen; click **Sign in** and finish in the browser. If it does not
appear, run **Developer: Reload Window**. You need a paid Claude plan or a Claude Console account
([Claude Code VS Code docs](https://code.claude.com/docs/en/vs-code)).

## 14. Claude's command was blocked by guard_paths

**You see:** in the panel, `BLOCKED by tools\hooks\guard_paths.py: ...`.

**Why and fix, by message:**

- `... resolves under the protected root ...`: the target is in a folder listed under `protected_roots` in
  `config\paths.yaml`. That is the guard working. Copy the file into the project and work on the copy, or remove the
  folder from `protected_roots` yourself if you really want Claude to write there.
- `bare 'python' resolves through PATH ...` (or `py`, `pip`): the guard makes Claude use the project's environment. Tell Claude:
  "use .venv\Scripts\python.exe". It should retry with the full path.
- `... the command names a protected root ... is not a read-only verb`: a shell command named a protected folder and
  could write there. `find`, `sort`, `uniq`, `tree`, `xxd`, `rg`, `ForEach-Object` and `Where-Object` are only allowed
  when they do not name the protected folder, and a `{ }` script block is never allowed next to it. Ask Claude to read
  with `cat`, `ls`, `grep`, `Get-Content` or `Get-ChildItem`, or to copy the files into the project first.

**What the guard is, and is not:** a hook that blocks Claude's file tools and common shell writes into protected
folders. It is a safety net, not a sandbox: a command that builds the path at run time, or an MCP server's own write
tools, can get around it. For strong isolation use Windows folder permissions, a separate Windows user or a VM.

**Watch edits to `config\paths.yaml`:** emptying `protected_roots` there switches the protection off. Claude is allowed
to edit that file (so a broken config can be fixed), so read its diff before you accept a Claude edit to it.

## 15. C8 warns that a filament profile was not found

**You see:** `[WARN] C8: filament 1 profile '...' not found in the installed profiles (checked system BBL, user presets,
install folder) - compatibility unproven`.

**Why:** the audit looks for Bambu Studio's profiles in `%APPDATA%\BambuStudio\system` and next to the installed
program. If Bambu Studio has never been started, or is installed somewhere else, they are not found.

**Fix:**

1. Start Bambu Studio once and finish its setup wizard, so it writes its profiles.
2. Check `bambu_studio_exe` in `config\paths.yaml` (problem 6).
3. If the profiles are in another folder, set `bambu_profiles_dir` in `config\paths.yaml` to the folder that contains
   `BBL`.
4. Run `.venv\Scripts\python.exe tools\mm_config.py` and read the `bambu profile roots` line.

Next: [10 - FAQ](10-faq.md).
