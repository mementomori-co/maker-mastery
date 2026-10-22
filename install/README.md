# install - prerequisite installers and checks

Scripts that install and check the apps Maker Mastery needs (Git, VS Code, Python 3.12, the Claude Code extension for
VS Code, Bambu Studio, plus optional apps). The Claude Code command line is optional, because the VS Code extension
works on its own; when the scripts offer it, they first print Anthropic's native installer as the recommended route
(it updates itself; the winget and Homebrew packages do not). The full guide, with every manual method and the
official source of each package id, is [docs/02-install.md](../docs/02-install.md).

None of these scripts has been run as a real install: the Windows script was run as a dry run only, and the macOS and
Linux install scripts only had a syntax check (`check.sh` was also run in Git Bash on Windows; see the table).

| File | What it does | Tested |
|---|---|---|
| `windows.ps1` | Installs with winget, one app at a time, asking y/N. `-DryRun` prints the commands and installs nothing. | dry run on Windows 11 (Windows PowerShell 5.1) |
| `check.ps1` | Read-only PASS/FAIL table with versions, last line `RESULT: PASS` or `RESULT: FAIL`. | run on Windows 11 |
| `apps.json` | The Windows app list: winget id, scope, required or optional, check, and the source URL of each id. | read by both scripts above |
| `macos.sh` | Installs with Homebrew, asking y/N. Never installs Homebrew itself. `--dry-run` installs nothing. | syntax check only; not run on a Mac |
| `linux.sh` | Ubuntu: apt for archive packages, Anthropic's installer for Claude Code; prints vendor steps for the rest. `--dry-run`. | syntax check only; not run on Linux |
| `check.sh` | Read-only PASS/FAIL table for macOS or Linux. Python passes only if `python3.12` can import `ensurepip` and `venv`. | syntax check, and run in Git Bash on Windows 11 (it reports FAIL for Python 3.12 and Bambu Studio there, as expected); not run on macOS or Linux |
| `lib.sh`, `common.ps1` | Shared helpers and the macOS/Linux app list (sourced by the scripts, not run directly). | |

Run them from the project folder:

```powershell
powershell -ExecutionPolicy Bypass -File install\windows.ps1 -DryRun   # see what it would do
powershell -ExecutionPolicy Bypass -File install\windows.ps1           # install, y/N per app
powershell -ExecutionPolicy Bypass -File install\check.ps1             # check
```

```bash
bash install/macos.sh --dry-run     # or install/linux.sh --dry-run on Ubuntu
bash install/check.sh
```

Rules the scripts follow:

- Nothing installs without your y for that app. No `--silent`. On Windows, `--accept-package-agreements` and
  `--accept-source-agreements` are added only after your y (they answer winget's license questions for you).
- Use a normal PowerShell window. User-scope apps need no administrator; machine-scope apps (Bambu Studio, OrcaSlicer,
  Blender) make Windows show an administrator prompt during their install. See
  [Windows: normal or administrator?](../docs/02-install.md#windows-normal-or-administrator).
- Apps already installed are skipped, so you can run a script again at any time.
- Every run appends to `install/install.log`, which is git-ignored and stays on your machine.
- The project's own setup (`tools\setup.ps1`) is tested on Windows 11 only. On macOS and Linux these scripts install
  prerequisites; running the project there is planned for v1.1.
