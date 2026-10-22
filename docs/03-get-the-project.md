# 03 - Get the project

There are two ways to get the project folder onto your PC: **Download ZIP** (no Git needed) or **git clone** (easier to
update later). Pick one. Next: [04 - First run](04-first-run.md).

The project's GitHub address is `https://github.com/mementomori-co/maker-mastery`. `mementomori-co` is the GitHub account that
publishes it; on the real page the address is already complete.

## Where to put the folder

Use a short path with no spaces, on a local drive that is **not** synced by OneDrive, for example:

```text
C:\Projects\maker-mastery
```

Why:

- **OneDrive:** on many Windows 11 PCs, Desktop, Documents and Pictures are synced to OneDrive (check: a cloud or
  tick icon beside the folder in File Explorer). The setup script creates a `.venv` folder with thousands of small
  files, and the tools write scratch files into `work\`. Syncing them is slow and can lock files while a tool runs
  (from general experience, not verified against a Microsoft page). Keep the project out of synced folders.
- **Short path:** Windows limits classic paths to 260 characters unless long paths are enabled (Python docs,
  "Removing the MAX_PATH Limitation": https://docs.python.org/3.12/using/windows.html). Deep folders plus Python
  packages can hit that limit.
- **No spaces:** the Bambu Studio command line is more reliable with paths without spaces (see
  `config\paths.example.yaml`).

To create the folder: open File Explorer, click **This PC** (label not verified), open **Local Disk (C:)** (label not
verified), right-click an empty area, choose **New > Folder** (label not verified) and name it `Projects`.

## Option A: Download ZIP

Official guide: https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives

1. Open the project's page on GitHub in your browser.
2. Above the file list, click the **Code** button.
3. Click **Download ZIP**. You should see a file such as `maker-mastery-main.zip` in your Downloads folder (the name
   depends on the branch; not verified).
4. In File Explorer, right-click the ZIP and choose **Extract All...** (label not verified).
5. In the box that asks where to extract, type `C:\Projects` and click **Extract** (label not verified).
6. You should now have a folder such as `C:\Projects\maker-mastery-main`. Rename it to `maker-mastery` (right-click >
   **Rename** (label not verified)), so the path is `C:\Projects\maker-mastery`.
7. Open the folder. You should see `README.md`, `CLAUDE.md`, and the folders `docs`, `knowledge`, `tools` and others.
   The folder `.claude` is also there; File Explorer may hide names that start with a dot only if you set it to.

If you do not see `tools` and `knowledge` directly inside, you have one folder too many (for example
`maker-mastery\maker-mastery-main\...`). Move the inner folder up so `README.md` sits directly in `C:\Projects\maker-mastery`.

About files from a ZIP: Windows marks files downloaded from the internet. PowerShell then refuses to run the unsigned
setup script under its default policy. Guide 04 gives the one-line way around this for that one run.

## Option B: git clone

Official guide: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

1. On the project's GitHub page, click **Code**, stay on **HTTPS**, and click the copy icon next to the address.
2. Open Windows PowerShell (Start, type `PowerShell`).
3. Run these two lines. The second one is `git clone`, the address you copied, and the target folder:

   > **Check the address in the second line against the one you copied in step 1.** The part right after
   > `github.com/` is the GitHub account name in the repository's address. If it differs from your browser's address
   > bar, paste the address you copied in step 1 in its place.

   ```powershell
   New-Item -ItemType Directory -Force C:\Projects | Out-Null
   git clone https://github.com/mementomori-co/maker-mastery.git C:\Projects\maker-mastery
   ```

4. You should see `Cloning into 'C:\Projects\maker-mastery'...` and a few progress lines ending without an error.
5. Check:

   ```powershell
   Test-Path C:\Projects\maker-mastery\CLAUDE.md
   ```

   You should see `True`.

If something goes wrong:

| You see | Do this |
|---|---|
| `git is not recognized` | Go back to [02 - Install](02-install.md), part 1. |
| `fatal: unable to access 'https://github.com/...': ... error: 400` | The address in the `git clone` line is not the repository's address. Make the GitHub account name in the repository's address (right after `github.com/`) match your browser's address bar, or paste the address you copied in step 1, and run the line again. |
| `repository not found` | Check the address on the project's GitHub page and copy it again. |

To update later, run `git -C C:\Projects\maker-mastery pull`. Your own files (`config\paths.yaml`, `.venv\`, `work\`)
are ignored by git, so an update does not overwrite them. Files you edit that git does track, such as
`knowledge\00-gear-inventory\current-load.md`, can make `git pull` stop with a message about local changes; ask Claude
Code to help you commit or set aside your changes before you pull.

Next: [04 - First run](04-first-run.md).
