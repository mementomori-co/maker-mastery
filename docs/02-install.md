# 02 - Install the free tools

This page installs everything Maker Mastery needs, on Windows 11, macOS (Apple silicon and Intel) and Ubuntu Linux.
It starts with a summary table, then the quick route (one script per system), then one section per app with every
install method, each one checked against the vendor's own page. Next: [03 - Get the project](03-get-the-project.md).

> **What is tested where.** The project's own setup (`tools\setup.ps1`, the Claude Code hooks, the tools' self-test)
> is tested on **Windows 11** only. The macOS and Linux parts of this page only install the prerequisites; running
> the project itself on macOS or Linux is **not yet supported or tested** (planned for v1.1).

About the labels on this page: a button or menu name in **bold** is quoted from the official page linked in that part.
A label marked "(label not verified)" was not found in the official docs; your screen may word it slightly differently.
Anything else marked "(not verified)" was not confirmed on an official page when this guide was written; treat it as a
hint, not a fact. Package ids and version numbers were read from the official sources for this release; versions move
on, ids normally do not.

## Contents

- [Summary table](#summary-table)
- [Before you start](#before-you-start)
- [Windows: normal or administrator?](#windows-normal-or-administrator)
- [The quick route: install scripts](#the-quick-route-install-scripts)
- First: [0. Create your Anthropic account](#0-create-your-anthropic-account)
- Required: [1. Git](#1-git) - [2. VS Code](#2-vs-code) - [3. Python 3.12](#3-python-312) -
  [5. Claude Code extension for VS Code](#5-claude-code-extension-for-vs-code) - [6. Bambu Studio](#6-bambu-studio)
- Optional: [4. Claude Code command line](#4-claude-code-command-line-optional) -
  [7. Claude Desktop](#7-claude-desktop-optional) - [8. GitHub Desktop](#8-github-desktop-optional) -
  [9. GitHub CLI](#9-github-cli-optional) - [10. OrcaSlicer](#10-orcaslicer-optional) - [11. Blender](#11-blender-optional)
- [Check everything at once](#check-everything-at-once)
- [Sources](#sources)

## Summary table

Legend: ✅ verified on the official source (linked in the app's section) · ⚪ not offered / not applicable ·
"(not verified)" = not confirmed on an official page. "Vendor cmd" = the vendor's own installer command.

Why these apps: the tools in `tools\` run on Python (`requirements.txt`), slice with Bambu Studio
(`tools\slice_cli.py`, `bambu_studio_exe` in `config\paths.yaml`) and can render with Blender
(`tools\stability_check.py --render`, `blender_exe`). Git, VS Code and Claude Code are how you get and use the project.

| App | Need | Windows 11 | macOS Apple silicon | macOS Intel | Ubuntu |
|---|---|---|---|---|---|
| Anthropic account (Pro, Max, Team, Enterprise or Console; [section 0](#0-create-your-anthropic-account)) | required | claude.ai ✅ · platform.claude.com ✅ | same | same | same |
| Git | required | Download ✅ · winget ✅ `Git.Git` | Homebrew ✅ `git` · Xcode tools ✅ | Xcode tools ✅ · Homebrew Tier 3 (see note) | apt ✅ `git` |
| VS Code | required | Download ✅ · winget ✅ `Microsoft.VisualStudioCode` | Download ✅ · Homebrew ✅ cask `visual-studio-code` | Download ✅ · Homebrew Tier 3 | .deb ✅ · apt (Microsoft repo) ✅ `code` |
| Python 3.12 | required | Download ✅ 3.12.10 · winget ✅ `Python.Python.3.12` | Download ✅ 3.12.10 universal2 · Homebrew ✅ `python@3.12` | Download ✅ 3.12.10 universal2 · Homebrew Tier 3 | apt ✅ `python3.12` + `python3.12-venv` (24.04) |
| Claude Code (command line) | optional | Vendor cmd ✅ (recommended) · winget ✅ `Anthropic.ClaudeCode` (no auto-update) · npm ✅ | Vendor cmd ✅ · Homebrew ✅ cask `claude-code` · npm ✅ | Vendor cmd ✅ · npm ✅ · Homebrew Tier 3 | Vendor cmd ✅ · apt (Anthropic repo) ✅ `claude-code` · npm ✅ |
| Claude Code extension | required | VS Code ✅ `anthropic.claude-code` | VS Code ✅ | VS Code ✅ | VS Code ✅ |
| Bambu Studio | required | Download ✅ · winget ✅ `Bambulab.Bambustudio` | Download ✅ · Homebrew ✅ cask `bambu-studio` | Download (Intel not verified) · Homebrew Tier 3 | AppImage ✅ · apt ⚪ |
| Claude Desktop | optional | Download ✅ · winget ✅ `Anthropic.Claude` | Download ✅ · Homebrew ✅ cask `claude` | Download ✅ (universal app) · Homebrew Tier 3 | apt (Anthropic repo, beta) ✅ `claude-desktop` · .deb ✅ |
| GitHub Desktop | optional | Download ✅ · winget ✅ `GitHub.GitHubDesktop` | Download ✅ · Homebrew ✅ cask `github` | Download ✅ · Homebrew Tier 3 | ⚪ (not supported) |
| GitHub CLI | optional | winget ✅ `GitHub.cli` · Download ✅ | Homebrew ✅ `gh` | Homebrew Tier 3 · Download ✅ | apt (GitHub repo) ✅ `gh` |
| OrcaSlicer | optional | Download ✅ · winget ✅ `SoftFever.OrcaSlicer` | Download ✅ universal · Homebrew ✅ cask `orcaslicer` | Download ✅ universal · Homebrew Tier 3 | AppImage / Flatpak ✅ · apt ⚪ |
| Blender | optional | Download ✅ · winget ✅ `BlenderFoundation.Blender` | Download ✅ · Homebrew ✅ cask `blender` | No 5.x download; Homebrew cask gives 4.5 (not tested) | Download ✅ · apt `blender` 4.0 (older than tested) |

Homebrew on Intel Macs: Homebrew lists "Intel x86_64 systems running macOS" as **Tier 3**, which it defines as "not
supported", and says it "has stopped building new bottles for Intel systems"
([Homebrew Support Tiers](https://docs.brew.sh/Support-Tiers)). The names in the Intel column are the same as for Apple
silicon, but on an Intel Mac prefer the direct downloads.

## Before you start

- A computer with an internet connection and permission to install programs.
- An Anthropic account that can use Claude Code. The setup docs say Claude Code "requires a Pro, Max, Team, Enterprise,
  or Console account" and that the free plan does not include it ([Claude Code setup](https://code.claude.com/docs/en/setup)).
- Claude Code's system requirements include macOS 13.0+, Windows 10 1809+, Ubuntu 20.04+ and 4 GB+ RAM
  ([Claude Code setup](https://code.claude.com/docs/en/setup)).
- A Bambu Lab printer is optional. Without one, everything except printing still works.

### How to open a terminal

- **Windows:** click the Start button, type `PowerShell`, and click **Windows PowerShell** (label not verified). You
  should see a dark window with a prompt such as `PS C:\...>`. Type the command and press Enter.
- **macOS:** open **Terminal** from Applications > Utilities (label not verified).
- **Ubuntu:** open **Terminal** from the app grid (label not verified).

After you install something new, **close the terminal window and open a new one**. A window that was already open does
not see programs added to the PATH after it started.

## Windows: normal or administrator?

winget is Windows' built-in package manager. Microsoft says it is available on Windows 11 "as a part of the App
Installer" ([winget overview](https://learn.microsoft.com/en-us/windows/package-manager/winget/)). Check it with
`winget --version`; you should see a version such as `v1.29.380`.

**Use a normal PowerShell window** (not "Run as administrator") unless a step below says otherwise:

- Many installers support two **scopes**: *user* (installs for your Windows account only, no administrator rights) and
  *machine* (installs for every account, needs an administrator). winget's `--scope` option "allows you to specify if
  the installer should target user or machine scope"
  ([winget install](https://learn.microsoft.com/en-us/windows/package-manager/winget/install)).
- When you run winget **without** administrator rights and an app needs them, "Windows will prompt you to elevate"
  (a User Account Control prompt). Click **Yes** there; if you refuse, that app fails to install
  ([winget overview, Administrator considerations](https://learn.microsoft.com/en-us/windows/package-manager/winget/)).
- When you run winget **as administrator**, you see no such prompt; Microsoft advises caution and to "only install
  applications you trust" ([same page](https://learn.microsoft.com/en-us/windows/package-manager/winget/)).
- VS Code's User setup "does not require administrator permissions", and updates are disabled when VS Code runs as
  Administrator from a User setup install ([VS Code on Windows](https://code.visualstudio.com/docs/setup/windows)).
- Scope is not always reliable: Microsoft notes that for EXE-based installers scope behaviour "is not necessarily
  deterministic", and that user-scope packages "may still require UAC"
  ([winget troubleshooting](https://learn.microsoft.com/en-us/windows/package-manager/winget/troubleshooting#scope-for-specific-user-vs-machine-wide)).

What each app's winget package offers (read from its manifest in
[microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs)):

| winget id | Scopes in the manifest | What this guide uses |
|---|---|---|
| `Git.Git` | user, machine | `--scope user` (no administrator) |
| `Microsoft.VisualStudioCode` | user, machine | `--scope user` (no administrator) |
| `Python.Python.3.12` | user, machine | `--scope user` (no administrator) |
| `Anthropic.ClaudeCode` | none listed (portable) | no `--scope`, as in the vendor's command |
| `Bambulab.Bambustudio` | machine (installer), plus a portable zip | `--scope machine`: expect an administrator prompt |
| `Anthropic.Claude` | MSIX package, plus a user-scope EXE | no `--scope` |
| `GitHub.GitHubDesktop` | user (EXE), machine (MSI) | `--scope user` (no administrator) |
| `GitHub.cli` | machine (MSI), plus a portable zip | no `--scope`, as in GitHub's own command |
| `SoftFever.OrcaSlicer` | machine | `--scope machine`: expect an administrator prompt |
| `BlenderFoundation.Blender` | machine | `--scope machine`: expect an administrator prompt |

Two more flags you will see: `--accept-package-agreements` accepts the package's license, and
`--accept-source-agreements` accepts the terms of the winget source; without them winget asks you
([winget install](https://learn.microsoft.com/en-us/windows/package-manager/winget/install)). Add them only when you
have decided to install. This guide never uses `--silent`.

How to open an administrator window, only if you need one: Start > type `PowerShell` > right-click
**Windows PowerShell** > **Run as administrator** (labels not verified).

## The quick route: install scripts

The [install](../install/README.md) folder has one script per system. Each one lists what it will install, asks y/N
for every app, skips apps you already have, and writes a log to `install\install.log` (not committed to git).
Nothing installs without your y. Try a dry run first: it prints every command and installs nothing.

| System | Dry run | Real run | Status |
|---|---|---|---|
| Windows 11 | `powershell -ExecutionPolicy Bypass -File install\windows.ps1 -DryRun` | the same without `-DryRun` | dry run self-tested on Windows 11; never run as a real install |
| macOS | `bash install/macos.sh --dry-run` | the same without `--dry-run` | not run on a Mac (syntax-checked only) |
| Ubuntu | `bash install/linux.sh --dry-run` | the same without `--dry-run` | not run on Linux (syntax-checked only) |

The scripts live in the project folder, so on a brand-new PC you first get the project
([03 - Get the project](03-get-the-project.md), Download ZIP needs no Git). The Windows script reads its list from
`install\apps.json`; the macOS and Linux scripts read theirs from `install/lib.sh`. The macOS script never installs
Homebrew itself: if `brew` is missing it prints Homebrew's official command and stops. The Linux script automates only
the Ubuntu archive packages, Anthropic's Claude Code installer and the VS Code extension; for the rest it prints the
vendor's page.

The Claude Code command line is optional in every script. Before offering it, each script prints Anthropic's native
installer command as the recommended route (see [section 4](#4-claude-code-command-line-optional)); the Windows script
then offers the winget package and the macOS script the Homebrew cask, and both say that those do not auto-update.
The Linux script runs the native installer itself, after your y.

If you prefer to do it by hand, follow the sections below in order.

## 0. Create your Anthropic account

Claude Code needs an Anthropic account with Claude Code access. Do this first: no app on this page can sign you in
without it. Every fact below is from Anthropic's own pages, listed under [Sources](#sources).

### Which account works

Anthropic's setup guide says: "Claude Code requires a Pro, Max, Team, Enterprise, or Console account. The free
claude.ai plan does not include Claude Code access." The VS Code extension guide adds that any of these works "and no
API key is required" ([setup](https://code.claude.com/docs/en/setup#authenticate),
[VS Code](https://code.claude.com/docs/en/vs-code)).

| Account | Who it is for | How you pay | Where you sign up |
|---|---|---|---|
| Claude **Pro** or **Max** subscription | one person | a monthly plan on your Claude account | [claude.ai](https://claude.ai), then choose a plan at [claude.com/pricing](https://claude.com/pricing) |
| Claude for **Teams** or **Enterprise** | a team or company | your organization's plan | your team admin invites you; you log in with that claude.ai account |
| Claude **Console** | API (pay-as-you-go) billing | usage billed by the API | [platform.claude.com](https://platform.claude.com); a separate account from claude.ai |

This page does not list prices: check [claude.com/pricing](https://claude.com/pricing) on the day you subscribe.
A Pro or Max plan's limits "are shared across Claude and Claude Code, meaning all activity in both tools counts
against the same limits" ([Use Claude Code with your Pro or Max plan](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan)).
Amazon Bedrock, Google Cloud's Agent Platform and Microsoft Foundry also work; they are for organizations and are not
covered here ([Authentication](https://code.claude.com/docs/en/authentication)).

### Create a Claude account (Pro or Max)

1. Open [claude.ai](https://claude.ai) in your browser.
2. Choose one:
   - **Continue with Google**: enter your Google email and password in the window that opens, then click **Next**.
   - Enter your email address and click **Continue with email**. Open the email titled "Secure link to log in to
     Claude.ai" and click its link on the same device. On a different device, the email's **Sign in with Claude.ai**
     link gives you a verification code to type on the device where you asked for the email.
   ([Log in to your Claude account](https://support.claude.com/en/articles/13189465-log-in-to-your-claude-account))
3. Verify your phone number when asked. Anthropic requires "phone verification for all new users". The number must be
   able to receive a text message, and "you cannot use VoIP numbers, Google Voice, phone numbers created using apps,
   landlines".
   You must be physically in a supported location
   ([Verify your phone number](https://support.claude.com/en/articles/8287232-verify-your-phone-number),
   [supported countries](https://www.anthropic.com/legal/supported-regions)).
4. Subscribe to Pro or Max from [claude.com/pricing](https://claude.com/pricing). The free plan does not include
   Claude Code. (The exact upgrade button wording on claude.ai: label not verified.)

Pick an email address you will keep: Anthropic's help centre says the email on a Claude account cannot be changed at
the moment ([change email](https://support.claude.com/en/articles/8452276-how-do-i-change-the-email-address-associated-with-my-account)).

### Or: a Claude Console account (API billing)

Go to [platform.claude.com](https://platform.claude.com) and use **Continue with Google** or **Continue with email**
(the email is titled "Secure link to log in to Claude Console"). Anthropic says the Console and claude.ai "are separate
accounts, though you can use the same email address for both"
([Log in to your Console account](https://support.claude.com/en/articles/13371040-log-in-to-your-console-account)).
In a company Console organization, an admin invites you and gives you the **Claude Code** or **Developer** role
([Authentication](https://code.claude.com/docs/en/authentication#claude-console-authentication)).

### Sign in from the VS Code extension the first time

You do this after installing the extension ([section 5](#5-claude-code-extension-for-vs-code)); guide
[04 - First run](04-first-run.md) walks you through it in the project folder.

1. Open the Claude Code panel. The quickest way is to open any file and click the Spark icon in the **Editor Toolbar**
   at the top right of the editor. The Spark icon in the **Activity Bar** (the narrow bar on the far left) opens the
   sessions list instead, where you start a new session.
2. "The first time you open the panel, a sign-in screen appears. Click **Sign in** and complete authorization in your
   browser." Log in there with the account you created above.
3. Back in VS Code, a **Learn Claude Code** checklist appears. Work through it with **Show me**, or close it with the X.

([VS Code guide, Get started](https://code.claude.com/docs/en/vs-code))

- **To switch account or log out**, type `/logout` in the Claude Code prompt, then sign in again
  ([Authentication](https://code.claude.com/docs/en/authentication)).
- **If you have an `ANTHROPIC_API_KEY` environment variable set**, Claude Code asks once whether to use it. Once you
  approve it, it uses that key instead of your subscription and you pay API rates
  ([Use Claude Code with your Pro or Max plan](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan),
  [Authentication](https://code.claude.com/docs/en/authentication)). Remove the variable if you meant to use your plan.

## 1. Git

Git downloads and updates projects from GitHub. You need it for the `git clone` route in guide 03. Claude Code on
Windows also uses Git Bash when Git for Windows is installed; without it, Claude Code uses PowerShell
([Claude Code setup](https://code.claude.com/docs/en/setup)).

### Windows

Direct download ([git-scm.com/install/windows](https://git-scm.com/install/windows)):

1. Open https://git-scm.com/install/windows in your browser.
2. Click **Click here to download**, or under the standalone installers click **Git for Windows/x64 Setup**.
   You should see a file named like `Git-<version>-64-bit.exe` in your Downloads folder (file name not verified).
3. Double-click the file. If Windows asks "Do you want to allow this app to make changes to your device?"
   (label not verified), click **Yes** (label not verified).
4. Keep the default choice on every page and click **Next** (label not verified) until **Install** (label not verified),
   then **Finish** (label not verified).

winget, in a normal window. The official Git page lists `winget install --id Git.Git -e --source winget` and notes that
the winget package "is not maintained by the Git for Windows project". This guide adds `--scope user` so no
administrator is needed:

```powershell
winget install --id Git.Git -e --source winget --scope user
```

Id source: [winget-pkgs manifests/g/Git/Git](https://github.com/microsoft/winget-pkgs/tree/master/manifests/g/Git/Git).

### macOS

The Git site lists Homebrew and Apple's Xcode Command Line Tools ([git-scm.com/install/mac](https://git-scm.com/install/mac)):

```bash
brew install git          # Homebrew formula: https://formulae.brew.sh/formula/git
xcode-select --install    # Apple's Command Line Tools include Git
```

### Ubuntu

From the Ubuntu archive ([git-scm.com/install/linux](https://git-scm.com/install/linux);
[Launchpad: git in Ubuntu 24.04](https://launchpad.net/ubuntu/noble/+package/git), version 2.43):

```bash
sudo apt-get install git
```

### Check it worked

```
git --version
```

You should see a line like `git version 2.x.y` (on Windows it ends in `.windows.1`). If you see "git is not
recognized" or "command not found", open a new terminal window and try again; on Windows, if it still fails, run the
installer again and keep the default PATH choice.

## 2. VS Code

VS Code is the editor where you use Claude Code.

### Windows

Official guide: https://code.visualstudio.com/docs/setup/windows

1. Open https://code.visualstudio.com/download and click the Windows download. The official guide says "The User setup is
   the recommended installation for most people"; it needs no administrator rights.
2. Run the downloaded `VSCodeUserSetup-x64-<version>.exe` (file name not verified).
3. Accept the agreement and keep the defaults. The guide says Setup adds VS Code to your `%PATH%`. Click **Install**
   (label not verified), then **Finish** (label not verified).
4. VS Code opens with a Welcome tab.

winget, in a normal window (user scope is the User setup):

```powershell
winget install --id Microsoft.VisualStudioCode -e --source winget --scope user
```

Id source: [winget-pkgs manifests/m/Microsoft/VisualStudioCode](https://github.com/microsoft/winget-pkgs/tree/master/manifests/m/Microsoft/VisualStudioCode).

### macOS

Official guide: https://code.visualstudio.com/docs/setup/mac. It says "VS Code supports Intel-based Macs and Macs with
Apple silicon".

1. Download VS Code for macOS from https://code.visualstudio.com/download (Universal, Intel chip and Apple silicon builds
   are listed).
2. Open the downloaded `.dmg` file and drag **Visual Studio Code.app** to the **Applications** folder.
3. To get the `code` command: open the Command Palette (Cmd+Shift+P), type `shell command`, and run
   **Shell Command: Install 'code' and optionally 'copilot' commands in PATH**, then choose **No** to add only `code`.
   (The guide says the label is **Shell Command: Install 'code' command in PATH** when AI features are hidden.)

Homebrew (cask [visual-studio-code](https://formulae.brew.sh/cask/visual-studio-code); it also links the `code` command):

```bash
brew install --cask visual-studio-code
```

### Ubuntu

Official guide: https://code.visualstudio.com/docs/setup/linux

1. Download the `.deb` package from https://code.visualstudio.com/download.
2. Install it: `sudo apt install ./<file>.deb`. The guide says the `.deb` "prompts to install the apt repository and
   signing key", so later updates come through apt.

Or add Microsoft's apt repository by hand, exactly as the guide shows (signing key, a
`/etc/apt/sources.list.d/vscode.sources` file, then `sudo apt update && sudo apt install code`). Copy those commands
from https://code.visualstudio.com/docs/setup/linux so you always get the current ones.

### Check it worked

```
code --version
```

You should see a version number (three numbers with dots) on the first line and two more lines. The extension needs
VS Code **1.94.0 or later** per the [Claude Code VS Code docs](https://code.claude.com/docs/en/vs-code); its
Marketplace page says 1.98.0 or higher, so use a current VS Code. If `code` is not recognized, open a new terminal
window; on Windows you can also open VS Code from the Start menu.

## 3. Python 3.12

The tools run on Python 3.12. The project's setup script makes a private Python environment (`.venv`) from it.

### Windows

Official docs: https://docs.python.org/3.12/using/windows.html

1. Open https://www.python.org/downloads/windows/ and find **Python 3.12.10** (the last 3.12 release with a Windows
   installer on that page). Click its **Windows installer (64-bit)** link.
   Direct page: https://www.python.org/downloads/release/python-31210/
2. Run the downloaded `python-3.12.10-amd64.exe`.
3. On the first screen, **tick the PATH checkbox at the bottom before you click anything else.** The 3.12 docs call it
   "Add Python to PATH"; on the installer screen it reads **Add python.exe to PATH** (label not verified).
4. Click **Install Now**. This also installs the `py` launcher, which the setup script looks for first.
5. At the end, if you see **Disable path length limit** (label not verified), click it. It lifts Windows' 260-character
   path limit; the Python docs describe this under "Removing the MAX_PATH Limitation".
6. Click **Close** (label not verified).

winget, in a normal window:

```powershell
winget install --id Python.Python.3.12 -e --source winget --scope user
```

Id source: [winget-pkgs manifests/p/Python/Python/3/12](https://github.com/microsoft/winget-pkgs/tree/master/manifests/p/Python/Python/3/12)
(latest there: 3.12.10). Whether the winget install ticks "Add python.exe to PATH" and installs the `py` launcher is
(not verified); if `py -3.12 --version` fails afterwards, use the direct download above.

**The Microsoft Store shortcut.** If `python --version` prints a message that starts `Python was not found; run without
arguments to install from the Microsoft Store` (exact wording not verified), or opens the Microsoft Store, Windows ran
its built-in Store shortcut instead of a real Python. Microsoft explains the shortcut and how to turn it off: open
**Manage app execution aliases** from Start and switch the **App Installer** Python entries to Off
([Microsoft Learn, Python on Windows FAQ](https://learn.microsoft.com/en-us/windows/dev-environment/python)). In
Settings the same page is **Settings > Apps > Advanced app settings > App execution aliases** (label not verified).
Microsoft also notes that a python.org install with the PATH option takes priority over the shortcut.

Newer Python versions (3.13 and later) may work but were not tested with this project. From 3.14 on, python.org offers
a new "Python install manager"; the steps above use the classic 3.12 installer.

### macOS

1. Open https://www.python.org/downloads/release/python-31210/ and click **macOS 64-bit universal2 installer** (one
   installer for Apple silicon and Intel).
2. Open the downloaded `.pkg` and follow the installer (labels not verified).

Homebrew (formula [python@3.12](https://formulae.brew.sh/formula/python@3.12), currently 3.12.15; the formula says it
installs `python3.12`):

```bash
brew install python@3.12
```

### Ubuntu

Ubuntu 24.04 ("noble") ships Python 3.12 in its archive
([Launchpad: python3.12](https://launchpad.net/ubuntu/noble/+package/python3.12), version 3.12.3;
[python3.12-venv](https://launchpad.net/ubuntu/noble/+package/python3.12-venv) adds the `venv` module the setup needs):

```bash
sudo apt-get install python3.12 python3.12-venv
```

Whether older Ubuntu releases carry `python3.12` in their archive is (not verified); use Ubuntu 24.04.

### Check it worked

Windows:

```powershell
py -3.12 --version
py --list
python --version
```

You should see `Python 3.12.10` from the first line, a list that includes 3.12 from the second, and `Python 3.12.10`
from the third. If `py` is not recognized, the launcher was not installed: run the installer again, choose
**Customize installation** and keep the launcher ticked. If only `python` fails, the PATH box was not ticked; the setup
script still works through `py`.

macOS and Ubuntu:

```bash
python3.12 --version
```

You should see `Python 3.12.x`.

## 4. Claude Code command line (optional)

**Optional.** You do not need this to use the project: the VS Code extension (section 5) works on its own. The
Claude Code VS Code docs say the extension "bundles its own copy of the CLI (command-line interface) for the chat
panel" ([VS Code docs](https://code.claude.com/docs/en/vs-code)). Install the command line only if you also want to
run `claude` in a terminal (for example `claude doctor`, or the CLI commands in
[11 - Autonomous mode](11-autonomous-mode.md)). The check scripts list it as optional, so a missing CLI never makes
them fail. Official guide: https://code.claude.com/docs/en/setup

**Which method:** use Anthropic's native installer below. The setup page marks it **Native Install (Recommended)**, and
native installs "automatically update in the background". The winget package does not: the page says "WinGet
installations do not auto-update", so you would have to upgrade it yourself. The winget option is kept below, labelled
as such, for people who manage everything with winget.

### Native installer (recommended)

```powershell
# Windows PowerShell, normal window (the page says "You do not need to run as Administrator")
irm https://claude.ai/install.ps1 | iex
```

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash
```

The page also gives a Windows CMD variant:
`curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`.

### winget (Windows; works, but does not auto-update)

```powershell
winget install Anthropic.ClaudeCode
```

This is the command on the setup page (id source:
[winget-pkgs manifests/a/Anthropic/ClaudeCode](https://github.com/microsoft/winget-pkgs/tree/master/manifests/a/Anthropic/ClaudeCode)).
The page says "WinGet installations do not auto-update": run `winget upgrade Anthropic.ClaudeCode` from time to time.
The same page describes an opt-in, the `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` environment variable set to `1`, that
makes Claude Code run that upgrade for you; this project has not tested it. `install\windows.ps1` offers this winget
route only after it has shown you the native installer command.

### Homebrew (macOS)

```bash
brew install --cask claude-code
```

Cask [claude-code](https://formulae.brew.sh/cask/claude-code) tracks the stable channel;
[claude-code@latest](https://formulae.brew.sh/cask/claude-code@latest) tracks the latest. Homebrew installs do not
auto-update: run `brew upgrade claude-code`. For that reason the native installer above is the recommended route on a
Mac too; `install/macos.sh` prints it before it offers the Homebrew cask.

### apt (Ubuntu, Anthropic's repository)

Anthropic publishes a signed apt repository. The setup page's **Install with Linux package managers** > apt steps
download the signing key to `/etc/apt/keyrings/claude-code.asc`, check its fingerprint, add the repository and run
`sudo apt install claude-code`. Copy those commands from https://code.claude.com/docs/en/setup so you also get the
fingerprint check.

### npm

`npm install -g @anthropic-ai/claude-code` is also documented; it needs Node.js 22 or later, and the page says not to use
`sudo npm install -g`. This project does not need Node.js, so the native installer is simpler.

### Check it worked

```
claude --version
```

The docs say a working install "prints a version number such as 2.1.211 (Claude Code)". For a fuller check run
`claude doctor`. If `claude` is not found, open a new terminal window; see the setup page's "Fix your PATH" if it still
fails. You sign in later (guide 04). The project needs v2.1.295 or later: see
[Check your Claude Code version](#check-your-claude-code-version).

## 5. Claude Code extension for VS Code

Official guide: https://code.claude.com/docs/en/vs-code · Marketplace id: `anthropic.claude-code`
([Marketplace page](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code), publisher Anthropic).

### Any system, in VS Code

1. Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac) to open the Extensions view.
2. Search for "Claude Code" and click **Install** on the extension published by Anthropic.
   You should see the Spark icon appear in the Activity Bar (the narrow bar on the far left).
3. If the extension does not appear, run **Developer: Reload Window** from the Command Palette (`Ctrl+Shift+P`), as the
   official guide suggests.
4. You sign in later, in guide 04. The official guide says that the first time you open the panel, "a sign-in screen
   appears"; you click **Sign in** and finish in your browser.

### Any system, from a terminal

VS Code's command line installs an extension by id with `--install-extension`
([VS Code command line](https://code.visualstudio.com/docs/configure/command-line)):

```
code --install-extension anthropic.claude-code
```

### Check it worked

```
code --list-extensions --show-versions
```

You should see a line `anthropic.claude-code@<version>`. In VS Code, `Ctrl+Shift+P` then typing `Claude Code` should
list Claude Code commands such as **Open in New Tab**.

### Check your Claude Code version

This project needs **Claude Code v2.1.295 or later**. The guard hook in `.claude\settings.json` uses
`"onFailure": "block"`, and the hooks reference marks that field "Requires Claude Code v2.1.295 or later"
([hooks reference](https://code.claude.com/docs/en/hooks), "Command hook fields").

- **The VS Code extension (the one that counts for the panel):** per the VS Code docs, the extension's version number
  is the Claude Code version it bundles, and the Extensions view shows it
  ([VS Code docs](https://code.claude.com/docs/en/vs-code)). Open the Extensions view (`Ctrl+Shift+X`), click
  **Claude Code** (publisher Anthropic) and read the version, or run `code --list-extensions --show-versions` and read
  the `anthropic.claude-code@<version>` line. It must be 2.1.295 or higher. If it is lower, update the extension in the
  Extensions view.
- **The command line (optional, section 4):** run `claude --version`, which "prints a version number" per the
  [setup page](https://code.claude.com/docs/en/setup) ("Verify your installation"). The command line is a separate copy
  and can be older than the extension; update it with `claude update` (or `winget upgrade Anthropic.ClaudeCode` /
  `brew upgrade claude-code` if you installed it that way).

## 6. Bambu Studio

Bambu Studio is Bambu Lab's slicer. The tools call it to slice; you use it to look at the result and to print.
Official download page: https://bambulab.com/en/download/studio ("Windows 10 (64-bit) or above", "macOS 10.15 or
above"; the Linux version comes from GitHub). Quick start: https://wiki.bambulab.com/en/software/bambu-studio/studio-quick-start

### Windows

1. Open https://bambulab.com/en/download/studio and click the **Bambu Studio (Win)** download.
2. Run the installer and keep the default install folder. The tools expect
   `C:\Program Files\Bambu Studio\bambu-studio.exe`; if you choose another folder, write it in `config\paths.yaml` later
   (guide 04). Whether the direct installer shows an administrator prompt is (not verified).
3. Start Bambu Studio. The wiki's setup wizard asks you to **Select Login Region**, then **Printer Selection**, then
   **Filament Selection**, then offers the **Install Bambu Network Plug-in** step. Logging in is optional for this project.

winget (expect an administrator prompt: the manifest's installer is machine scope, with default folder
`%ProgramFiles%\Bambu Studio`):

```powershell
winget install --id Bambulab.Bambustudio -e --source winget --scope machine
```

Id source: [winget-pkgs manifests/b/Bambulab/Bambustudio](https://github.com/microsoft/winget-pkgs/tree/master/manifests/b/Bambulab/Bambustudio).

### macOS

1. On https://bambulab.com/en/download/studio click **Bambu Studio (Mac)**.
2. Open the `.dmg` and drag Bambu Studio to Applications (labels not verified). Whether the single macOS download runs
   natively on Intel Macs is (not verified).

Homebrew (cask [bambu-studio](https://formulae.brew.sh/cask/bambu-studio); it installs `BambuStudio.app`):

```bash
brew install --cask bambu-studio
```

### Ubuntu

Bambu Lab publishes Linux builds as AppImages on GitHub, one for Ubuntu 22.04 and one for 24.04:
https://github.com/bambulab/BambuStudio/releases/latest. There is no apt package. Download the AppImage that matches
your Ubuntu, make it executable (`chmod +x <file>.AppImage`) and run it (these two steps are general AppImage practice,
not verified on Bambu Lab's page). Then set `bambu_studio_exe` in `config/paths.yaml` to that file.

### Check it worked

Windows:

```powershell
Test-Path "C:\Program Files\Bambu Studio\bambu-studio.exe"
```

You should see `True`. If you see `False`, Bambu Studio is installed somewhere else: find `bambu-studio.exe` in File
Explorer and note the full path for guide 04.

macOS: `ls -d /Applications/BambuStudio.app` should print that path.

## 7. Claude Desktop (optional)

The Claude desktop app. This project does not need it; you can use it as a second window next to Claude Code.
Official pages: https://claude.com/download and
[Install Claude Desktop](https://support.claude.com/en/articles/10065433-installing-claude-desktop) (macOS 13+,
Windows 10+, Linux beta on Ubuntu 22.04+ or Debian 12+).

- **Windows or macOS, direct:** on https://claude.com/download click **Download** next to Windows (or macOS), open the
  file, then launch Claude from the Start menu or Applications and sign in.
- **winget:** `winget install --id Anthropic.Claude -e --source winget`
  (id source: [winget-pkgs manifests/a/Anthropic/Claude](https://github.com/microsoft/winget-pkgs/tree/master/manifests/a/Anthropic/Claude)).
- **Homebrew:** `brew install --cask claude` ([cask claude](https://formulae.brew.sh/cask/claude); requires macOS 13;
  its download is a universal app).
- **Ubuntu (beta):** Anthropic's help page gives an apt repository (`claude-desktop` package) and a `.deb`; copy the
  commands from that page, which also shows the key fingerprint to check.

Check it worked: Windows `Get-AppxPackage -Name Claude` (shows a `Version` line) or
`winget list --id Anthropic.Claude --exact`; macOS `ls -d /Applications/Claude.app`; Ubuntu `command -v claude-desktop`.

## 8. GitHub Desktop (optional)

A point-and-click Git app. Official: https://desktop.github.com/download/ and
[Installing GitHub Desktop](https://docs.github.com/en/desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop)
(macOS 12.0 or later, Windows 10 64-bit or later; "Linux is not yet supported").

- **Direct:** on https://desktop.github.com/download/ click **Download for Windows (64bit)**, **Download for Apple
  silicon** or **Download for Intel chip**.
- **winget:** `winget install --id GitHub.GitHubDesktop -e --source winget --scope user`
  (id source: [winget-pkgs manifests/g/GitHub/GitHubDesktop](https://github.com/microsoft/winget-pkgs/tree/master/manifests/g/GitHub/GitHubDesktop)).
- **Homebrew:** `brew install --cask github` ([cask github](https://formulae.brew.sh/cask/github), "GitHub Desktop").

Check it worked: Windows `winget list --id GitHub.GitHubDesktop --exact` shows a row; macOS
`ls -d "/Applications/GitHub Desktop.app"`.

## 9. GitHub CLI (optional)

`gh`, GitHub on the command line (useful if you publish your own fork). Official install docs:
https://github.com/cli/cli#installation

- **Windows, winget** (GitHub's own command, [install_windows.md](https://github.com/cli/cli/blob/trunk/docs/install_windows.md)):
  `winget install --id GitHub.cli --source winget`. The manifest's installer is a machine-scope MSI, so an administrator
  prompt is likely (not verified).
- **macOS, Homebrew** ([install_macos.md](https://github.com/cli/cli/blob/trunk/docs/install_macos.md), formula
  [gh](https://formulae.brew.sh/formula/gh)): `brew install gh`.
- **Ubuntu, GitHub's apt repository:** copy the block under "Debian" from
  https://github.com/cli/cli/blob/trunk/docs/install_linux.md (it adds GitHub's keyring and repository, then
  `sudo apt install gh`); the same page lists the key fingerprint to check.
- **Direct:** precompiled binaries and the Windows MSI are on https://github.com/cli/cli/releases/latest.

Check it worked: `gh --version` prints a line starting `gh version 2.` (exact format not verified).

## 10. OrcaSlicer (optional)

A community slicer that also supports Bambu Lab printers. The tools do not use it; install it only if you want to
compare. Official: https://github.com/OrcaSlicer/OrcaSlicer/releases/latest (Windows x64 and arm64 installers, a macOS
universal `.dmg`, Linux AppImages and Flatpaks).

- **Windows, winget** (expect an administrator prompt: machine scope):
  `winget install --id SoftFever.OrcaSlicer -e --source winget --scope machine`
  (id source: [winget-pkgs manifests/s/SoftFever/OrcaSlicer](https://github.com/microsoft/winget-pkgs/tree/master/manifests/s/SoftFever/OrcaSlicer)).
- **macOS, Homebrew:** `brew install --cask orcaslicer` ([cask orcaslicer](https://formulae.brew.sh/cask/orcaslicer)).
- **Ubuntu:** download the AppImage or Flatpak from the releases page (no apt package).

Check it worked: Windows `winget list --id SoftFever.OrcaSlicer --exact`; macOS `ls -d /Applications/OrcaSlicer.app`.

## 11. Blender (optional)

Only `tools\stability_check.py --render` uses Blender (headless). It was written for the Blender 5.x Python API and is
not tested on older versions. Without Blender, that render is skipped with a message; everything else works. After
installing, set `blender_exe` in `config\paths.yaml` (guide 04). Official: https://www.blender.org/download/

- **Windows, direct:** click **Windows Installer** (currently v5.2.3 LTS) and run it.
- **Windows, winget** (expect an administrator prompt: machine scope):
  `winget install --id BlenderFoundation.Blender -e --source winget --scope machine`
  (id source: [winget-pkgs manifests/b/BlenderFoundation/Blender](https://github.com/microsoft/winget-pkgs/tree/master/manifests/b/BlenderFoundation/Blender)).
- **macOS Apple silicon:** click **macOS Apple Silicon** ("Requires macOS 13 (Ventura) or newer"), or
  `brew install --cask blender` ([cask blender](https://formulae.brew.sh/cask/blender), 5.2.3; it adds a `blender`
  command).
- **macOS Intel:** blender.org lists no Intel build of Blender 5.2. The Homebrew cask installs Blender 4.5 on Intel Macs
  (read from the cask's download URLs); this project's render script was not tested with 4.5.
- **Ubuntu:** click **Linux** on blender.org ("glibc 2.28 or newer"). Ubuntu 24.04's own `blender` package is version
  4.0 ([Launchpad](https://launchpad.net/ubuntu/noble/+package/blender)), older than the version the script was
  written for, so the blender.org download is the better choice.

Check it worked: macOS (Homebrew) and Linux, `blender --version` prints the version on its first line (exact wording
not verified). Windows: `winget list --id BlenderFoundation.Blender --exact` shows a row.

## Check everything at once

Run the read-only check for your system from the project folder:

```powershell
powershell -ExecutionPolicy Bypass -File install\check.ps1     # Windows
```

```bash
bash install/check.sh                                          # macOS or Ubuntu (not run there yet)
```

It prints one row per app (PASS, FAIL, or `--` for an optional app you skipped) with its version, and a last line
`RESULT: PASS` or `RESULT: FAIL`. Next: [03 - Get the project](03-get-the-project.md).
If anything here failed, see [09 - Troubleshooting](09-troubleshooting.md).

## Sources

Every id and command above was read from these official pages for this release:

- winget: [overview](https://learn.microsoft.com/en-us/windows/package-manager/winget/),
  [install command](https://learn.microsoft.com/en-us/windows/package-manager/winget/install),
  [list command](https://learn.microsoft.com/en-us/windows/package-manager/winget/list),
  [troubleshooting (scope)](https://learn.microsoft.com/en-us/windows/package-manager/winget/troubleshooting#scope-for-specific-user-vs-machine-wide),
  [microsoft/winget-pkgs manifests](https://github.com/microsoft/winget-pkgs/tree/master/manifests)
- Homebrew: [brew.sh](https://brew.sh/), [Installation](https://docs.brew.sh/Installation),
  [Support Tiers](https://docs.brew.sh/Support-Tiers), [formulae.brew.sh](https://formulae.brew.sh/)
- Ubuntu packages: [Launchpad, Ubuntu 24.04 "noble"](https://launchpad.net/ubuntu/noble)
- Anthropic account: [Claude Code setup, Authenticate](https://code.claude.com/docs/en/setup#authenticate),
  [Authentication](https://code.claude.com/docs/en/authentication), [claude.ai](https://claude.ai),
  [claude.com/pricing](https://claude.com/pricing), [platform.claude.com](https://platform.claude.com),
  [Log in to your Claude account](https://support.claude.com/en/articles/13189465-log-in-to-your-claude-account),
  [Log in to your Console account](https://support.claude.com/en/articles/13371040-log-in-to-your-console-account),
  [Verify your phone number](https://support.claude.com/en/articles/8287232-verify-your-phone-number),
  [Use Claude Code with your Pro or Max plan](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan),
  [change email](https://support.claude.com/en/articles/8452276-how-do-i-change-the-email-address-associated-with-my-account),
  [supported countries](https://www.anthropic.com/legal/supported-regions)
  (all read on 2026-10-22)
- Claude Code: [setup](https://code.claude.com/docs/en/setup), [VS Code](https://code.claude.com/docs/en/vs-code),
  [Marketplace: anthropic.claude-code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
- Claude Desktop: [download](https://claude.com/download),
  [Install Claude Desktop](https://support.claude.com/en/articles/10065433-installing-claude-desktop)
- Git: [Windows](https://git-scm.com/install/windows), [macOS](https://git-scm.com/install/mac), [Linux](https://git-scm.com/install/linux)
- VS Code: [Windows](https://code.visualstudio.com/docs/setup/windows), [macOS](https://code.visualstudio.com/docs/setup/mac),
  [Linux](https://code.visualstudio.com/docs/setup/linux), [command line](https://code.visualstudio.com/docs/configure/command-line)
- Python: [Windows downloads](https://www.python.org/downloads/windows/), [3.12.10](https://www.python.org/downloads/release/python-31210/),
  [Using Python on Windows](https://docs.python.org/3.12/using/windows.html),
  [Microsoft Learn: Python on Windows](https://learn.microsoft.com/en-us/windows/dev-environment/python)
- Bambu Studio: [download](https://bambulab.com/en/download/studio),
  [quick start](https://wiki.bambulab.com/en/software/bambu-studio/studio-quick-start),
  [GitHub releases](https://github.com/bambulab/BambuStudio/releases/latest)
- GitHub: [Desktop download](https://desktop.github.com/download/),
  [Installing GitHub Desktop](https://docs.github.com/en/desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop),
  [GitHub CLI install docs](https://github.com/cli/cli#installation)
- OrcaSlicer: [releases](https://github.com/OrcaSlicer/OrcaSlicer/releases/latest)
- Blender: [download](https://www.blender.org/download/)
