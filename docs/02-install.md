# 02 - Install the free tools

You install five things, in this order: Git, VS Code, the Claude Code extension, Python 3.12 and Bambu Studio. Each part
ends with a "check it worked" command. Next: [03 - Get the project](03-get-the-project.md).

About the labels on this page: a button or menu name in **bold** is quoted from the official page linked in that part.
A label marked "(label not verified)" was not found in the official docs; your screen may word it slightly differently.

## Before you start

- A Windows 11 PC with an internet connection and permission to install programs.
- An Anthropic account that can use Claude Code: "any paid Claude subscription (Pro, Max, Team, or Enterprise) or a
  Claude Console account works" ([Claude Code VS Code docs](https://code.claude.com/docs/en/vs-code)).
- A Bambu Lab printer is optional. Without one, everything except printing still works.

### How to open PowerShell for the checks

Until VS Code is installed, run the check commands in Windows PowerShell:

1. Click the Start button, type `PowerShell`, and click **Windows PowerShell** (label not verified).
2. You should see a dark window with a prompt such as `PS C:\...>`. Type the command and press Enter.
3. After you install something new, **close this window and open a new one**. A window that was already open does not
   see programs added to the PATH after it started.

## 1. Git

Git downloads and updates projects from GitHub. You need it for the `git clone` route in guide 03, and it is useful
later. (If you will only use Download ZIP, you can skip Git.)

1. Open https://git-scm.com/install/windows in your browser.
2. Click **Click here to download**, or under the standalone installers click **Git for Windows/x64 Setup**.
   You should see a file named like `Git-<version>-64-bit.exe` in your Downloads folder.
3. Double-click the file. If Windows asks "Do you want to allow this app to make changes to your device?"
   (label not verified), click **Yes** (label not verified).
4. Keep the default choice on every page and click **Next** (label not verified) until **Install** (label not verified),
   then **Finish** (label not verified).

Check it worked (in a new PowerShell window):

```powershell
git --version
```

You should see a line like `git version 2.x.y.windows.1`. If you see "git is not recognized", close every PowerShell
window, open a new one and try again; if it still fails, run the installer again and keep the default PATH choice.

Alternative (one line, the official page lists it): `winget install --id Git.Git -e --source winget`. The page notes that
this winget package is not maintained by the Git for Windows project.

## 2. VS Code

VS Code is the editor where you will use Claude Code. Official guide: https://code.visualstudio.com/docs/setup/windows

1. Open https://code.visualstudio.com/download and click the Windows download. The official guide says "The User setup is
   the recommended installation for most people"; it needs no administrator rights.
2. Run the downloaded `VSCodeUserSetup-x64-<version>.exe` (file name not verified).
3. Accept the agreement and keep the defaults. The installer adds VS Code to your PATH (the guide says Setup adds
   VS Code to `%PATH%`). Click **Install** (label not verified), then **Finish** (label not verified).
4. VS Code opens with a Welcome tab.

Check it worked (in a new PowerShell window):

```powershell
code --version
```

You should see a version number (three numbers with dots) on the first line and two more lines. The extension needs VS Code **1.94.0 or later**
([Claude Code VS Code docs](https://code.claude.com/docs/en/vs-code)). If `code` is not recognized, open a new
PowerShell window; if it still fails, open VS Code from the Start menu, it works the same.

## 3. The Claude Code extension

Official guide: https://code.claude.com/docs/en/vs-code

1. In VS Code, press `Ctrl+Shift+X` to open the Extensions view.
2. Search for "Claude Code" and click **Install** on the extension published by Anthropic.
   You should see the Spark icon appear in the Activity Bar (the narrow bar on the far left).
3. If the extension does not appear, run **Developer: Reload Window** from the Command Palette (`Ctrl+Shift+P`), as the
   official guide suggests.
4. You sign in later, in guide 04, after the project setup has run. The official guide says that the first time you open
   the panel, "a sign-in screen appears"; you click **Sign in** and finish in your browser.

Check it worked: press `Ctrl+Shift+P`, type `Claude Code`. You should see Claude Code commands such as
**Open in New Tab**. If none appear, reload the window (step 3) or restart VS Code.

Note: the extension carries its own copy of Claude Code for the panel. Typing `claude` in a terminal needs the separate
command-line install, which this project does not require.

## 4. Python 3.12

The tools run on Python 3.12. The setup script makes a private Python environment for this project from it.
Official docs: https://docs.python.org/3.12/using/windows.html

1. Open https://www.python.org/downloads/windows/ and find **Python 3.12.10** (the last 3.12 release with a Windows
   installer on that page). Click its **Windows installer (64-bit)** link.
   Direct page: https://www.python.org/downloads/release/python-31210/
2. Run the downloaded `python-3.12.10-amd64.exe`.
3. On the first screen, **tick the PATH checkbox at the bottom before you click anything else.** The 3.12 docs call it
   "Add Python to PATH"; on the installer screen it reads **Add python.exe to PATH** (label not verified).
4. Click **Install Now**. This also installs the `py` launcher, which the setup script looks for first.
5. At the end, if you see **Disable path length limit** (label not verified), click it. It lifts Windows' 260-character
   path limit; the Python docs describe this setting under "Removing the MAX_PATH Limitation".
6. Click **Close** (label not verified).

Check it worked (in a new PowerShell window):

```powershell
py -3.12 --version
py --list
python --version
```

You should see `Python 3.12.10` from the first line, a list that includes 3.12 from the second, and `Python 3.12.10`
from the third. If `py` is not recognized, the launcher was not installed: run the installer again, choose
**Customize installation** and keep the launcher ticked. If only `python` fails, the PATH box was not ticked; the setup
script still works through `py`, but you can run the installer again, choose to modify (label not verified) and add it.

Newer Python versions (3.13, 3.14) may work but were not tested with this project. Python 3.14 brings a new
"Python install manager"; the guide above uses the classic 3.12 installer, which the docs mark as deprecated from 3.14 on.

## 5. Bambu Studio

Bambu Studio is Bambu Lab's slicer. The tools call it to slice; you use it to look at the result and to print.
Official guide: https://wiki.bambulab.com/en/software/bambu-studio/studio-quick-start

1. Open https://bambulab.com/download (the download link on the wiki's quick-start page) and download Bambu Studio for
   Windows.
2. Run the installer and keep the default install folder. The tools expect
   `C:\Program Files\Bambu Studio\bambu-studio.exe`; if you choose another folder, write it in `config\paths.yaml` later
   (guide 04).
3. Start Bambu Studio. The wiki's setup wizard asks you to **Select Login Region**, then **Printer Selection** (pick your
   printers and nozzles), then **Filament Selection**, then offers the **Install Bambu Network Plug-in** step. Logging in
   is optional for this project.

Check it worked:

```powershell
Test-Path "C:\Program Files\Bambu Studio\bambu-studio.exe"
```

You should see `True`. If you see `False`, Bambu Studio is installed somewhere else: find `bambu-studio.exe` in File
Explorer and note the full path for guide 04.

## Done

You now have Git, VS Code with Claude Code, Python 3.12 and Bambu Studio. Next: [03 - Get the project](03-get-the-project.md).

If anything here failed, see [09 - Troubleshooting](09-troubleshooting.md).
