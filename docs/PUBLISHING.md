# Publishing this project on GitHub

This guide is for the maintainer: the person who publishes this folder as a public GitHub repository and creates the
v1.0.0 release. It assumes you have never done this before. If you only want to use the project, you do not need this
page; start at [02 - Install](02-install.md).

About the labels on this page: a button, menu or field name in **bold** is quoted from the official page linked in that
part (fetched 2026-10-22; the organization profile picture steps were re-read on docs.github.com the same day). A name marked "(label not verified)" was not found in the official docs; your screen may word
it slightly differently. GitHub changes its screens from time to time, so if a label has moved, the linked page is the
reference.

What you need before you start:

- A GitHub account that you have signed in to in your browser. Signing up is something you do yourself, at
  https://github.com/signup.
- Git for Windows, VS Code and the project's `.venv` (from [02 - Install](02-install.md) and
  [04 - First run](04-first-run.md)).
- This project folder open in VS Code (**File > Open Folder...**), and a terminal in it (**Terminal > New Terminal**,
  [VS Code terminal docs](https://code.visualstudio.com/docs/terminal/basics)). Every command below is typed in that
  terminal, from the project folder.

The order matters: a, b, c, then the checklist in f, then d. Section e is for after the release.

## a. Create the empty repository on github.com

Official guide: https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository

1. In the upper-right corner of any GitHub page, click the **+** icon, then click **New repository**.
2. **Owner**: use the **Owner** dropdown menu to pick your own account, or the GitHub organization you publish under
   (then also do [Organization profile picture](#organization-profile-picture) in part c).
3. Repository name: type `maker-mastery` exactly (lowercase, with the hyphen). The field label is not quoted in the
   guide (label not verified).
4. Description: you can leave it empty here; you add the About text in part c.
5. Visibility: choose **Public** (label not verified; the guide says "Choose a repository visibility").
6. Do **NOT** add a README, a .gitignore or a licence. Leave those options off (labels not verified). This folder
   already has `README.md`, `.gitignore` and `LICENSE`, and GitHub's guide warns that adding files on GitHub when you
   push an existing repository can cause a merge conflict
   ([adding locally hosted code](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)).
7. Click **Create repository**. You land on the **Quick Setup** page. Leave it open.

### What "owner" means, and filling in `mementomori-co`

The owner is the GitHub account the repository belongs to: your username, or the organization's name if you publish
under an organization. It is the part of the address right after `github.com/`. If your username were `your-username`, the repository address would be
`https://github.com/your-username/maker-mastery`.

The project's files cannot know your username in advance, so they say `mementomori-co` instead. Replace it everywhere it
matters, before you push:

1. In VS Code press **Ctrl+Shift+H** (the **Replace in Files** command,
   [VS Code default keyboard shortcuts](https://code.visualstudio.com/docs/reference/default-keybindings)). The menu route
   is **Edit > Replace in Files** (menu location not verified). The Search view opens with a Replace box
   ([VS Code: search and replace](https://code.visualstudio.com/docs/editing/codebasics)).
2. In the search box type exactly `mementomori-co` (with the angle brackets).
3. In the Replace box type your GitHub username, with no angle brackets and no spaces.
4. Click the ellipsis below the search box (**Toggle Search Details**) to show the **files to include** and
   **files to exclude** boxes.
5. In **files to include** paste this one line:

   ```text
   README.md, CHANGELOG.md, SECURITY.md, CONTRIBUTING.md, RELEASE_NOTES_v1.0.0.md, docs/03-get-the-project.md
   ```

   This page (`docs/PUBLISHING.md`) is left out on purpose: it explains the placeholder and must keep it.
6. Check the result list: it should show matches only in those 6 files. Then click the Replace All button next to the
   Replace box (label not verified; the VS Code guide says you "can replace across all files from the Replace text
   box"). Confirm if VS Code asks.
7. Press **Ctrl+S** in any file that is still open with unsaved changes.
8. Search for `mementomori-co` once more with **files to include** empty. The only remaining matches should be in
   `docs/PUBLISHING.md`.

## b. Push the local repository

Official guide: https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github

The folder is already a Git repository, with the commits already in the repo on a branch called `main`. Its commits carry the
author name "Memento Mori" and the e-mail address `memento-mori@example.invalid`. Both are set for **this repository
only** (`git config user.name` without `--global`), so they do not change Git on the rest of your PC
([GitHub: setting your username in Git](https://docs.github.com/en/get-started/git-basics/setting-your-username-in-git)).
Check it:

```powershell
git config user.name
git config user.email
git log --oneline
```

You should see `Memento Mori`, `memento-mori@example.invalid`, then one line per commit already in the repo.

> The commits are deliberately not linked to any GitHub account. GitHub links a commit to a user by matching the
> commit's e-mail address to an address on a GitHub account
> ([GitHub: troubleshooting commits](https://docs.github.com/en/pull-requests/how-tos/commit-changes/troubleshooting-commits)),
> and `.invalid` is a reserved name that is never a real domain ([RFC 2606](https://www.rfc-editor.org/rfc/rfc2606)),
> so no account can own that address. If you want your own name on future commits, set your own identity for this
> repository before you commit; GitHub's no-reply address option is under **Settings > Emails**
> ([GitHub: setting your commit email address](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address)):
>
> ```powershell
> git config user.name "Your Name"
> git config user.email "you@users.noreply.github.com"
> ```

1. Commit the `mementomori-co` replacement from part a first:

   ```powershell
   git add -A
   git commit -m "Fill in GitHub owner"
   ```

   Before you run `git add -A`, run `git status` and read the list: it should show only the 6 files from part a. If
   anything else is listed, see part g before you continue.

2. Connect the folder to your new GitHub repository. Type your username in place of `mementomori-co`:

   ```powershell
   git remote add origin https://github.com/mementomori-co/maker-mastery.git
   git remote -v
   ```

   The second line should print the address twice, ending in `(fetch)` and `(push)`.

3. Make sure the branch is called `main`:

   ```powershell
   git branch -M main
   ```

   The branch is already `main`, so this changes nothing; it is the standard step from GitHub's guide and is safe to
   run. (`-M` renames the current branch, [git-branch docs](https://git-scm.com/docs/git-branch).)

4. Send the commits to GitHub:

   ```powershell
   git push -u origin main
   ```

5. **The sign-in prompt.** The first time, Git for Windows opens a browser window for you to sign in to GitHub. This
   is Git Credential Manager, which comes with Git for Windows. You may first be asked to authorize an app, and to
   complete two-factor authentication if your account uses it. After that, the sign-in is stored in Windows Credential
   Manager and Git does not ask again
   ([GitHub: caching your credentials](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git)).
   You never type your GitHub password into the terminal. If the terminal itself asks for a password, stop, do not
   type it, and check that Git for Windows is up to date (guide [02 - Install](02-install.md)).

6. Refresh the repository page on GitHub. You should see the README with the banner.

## c. Repository settings

### About and topics

Official guide: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics

1. On the repository's main page, in the top right, click the gear icon to the right of "About" (the guide shows the
   icon; the word "gear" is not verified).
2. In the description field (label not verified) paste this text exactly:

   ```text
   Claude Code AI agents and a cited knowledge library for makers: 3D printing (Bambu Lab), CAD and organic modeling, electronics and LEDs, Raspberry Pi, Blender rendering, MCP and agent engineering. Quality gates and tools built in. The AI researches, prepares and checks; you build.
   ```

3. Under "Topics", add these 20 topics one at a time (type one, then click it in the dropdown or keep typing to create
   it). GitHub allows at most 20 topics, lowercase letters, numbers and hyphens only:

   ```text
   claude-code
   claude
   anthropic
   ai-agents
   agentic-ai
   mcp
   model-context-protocol
   maker
   diy
   3d-printing
   bambu-lab
   cad
   blender
   electronics
   raspberry-pi
   arduino
   game-development
   knowledge-base
   claude-skills
   prompt-engineering
   ```

4. If GitHub shows "Suggested" topics, decline them; the list above is already the maximum.
5. Click **Save changes**.

### Social preview image

Official guide: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview

1. Under the repository name, click **Settings**. If you cannot see it, open the dropdown menu, then click
   **Settings**.
2. Under "Social preview", click **Edit**. (It is on the first settings page, which is usually called General; that
   name is not verified.)
3. Click **Upload an image...** and choose `assets\brand\social-preview.png` from this folder.

The file is 1280 x 640 pixels, about 220 KB, with a solid background, which matches GitHub's advice (PNG, JPG or GIF
under 1 MB; 1280 by 640 for best display).

### Organization profile picture

Only if you publish under a GitHub **organization**. On a personal account this step is optional: your own profile
picture is yours to choose, and the project does not need it changed
([GitHub: personalize your profile, "Changing your profile picture"](https://docs.github.com/en/account-and-profile/tutorials/personalize-your-profile)).

The image is `assets\brand\org-avatar-500.png`: 500 x 500 pixels, the MEMENTO MORI crest centred on a solid #0A0A0A
background, with margin so a round crop cuts nothing. Like every file in `assets\brand\`, it is not covered by the MIT
License (see `NOTICE.md`).

Official guide: https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile#uploading-an-image

1. In the upper-right corner of GitHub, click your profile picture, then click **Organizations**.
2. Select the organization by clicking on it.
3. Under the organization name, click **Settings**. If you cannot see the "Settings" tab, select the dropdown menu, then
   click **Settings**.
4. Under the profile picture, click **Upload new picture**, then select `assets\brand\org-avatar-500.png` from this
   folder. If GitHub shows a crop box, keep the whole square (crop step not verified).

### Optional: Discussions

Official guide: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/enabling-or-disabling-github-discussions-for-a-repository

1. Click **Settings**.
2. Scroll down to the "Features" section and select **Discussions**.

### Optional, recommended: private vulnerability reporting

`SECURITY.md` tells people to report security problems privately. That only works once you switch it on.

Official guide: https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository

1. Click **Settings**.
2. In the "Security and quality" section of the sidebar, click **Advanced Security**.
3. Under "Advanced Security", to the right of "Private vulnerability reporting", click **Enable**.

Reporters then see a **Report a vulnerability** button on the repository's "Advisories" page.

## d. Create release v1.0.0 "First Light"

Do the checklist in part f first.

Official guide: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository

You need the release file `dist\maker-mastery-v1.0.0.zip`. It is built by the packaging step after your
"Fill in GitHub owner" commit, so the ZIP contains your real username. The `dist` folder is ignored by Git, so the ZIP
is never committed; it is only attached to the release. If the file is not there, stop here.

Get its SHA-256 checksum (a fingerprint people can use to check their download):

```powershell
(Get-FileHash dist\maker-mastery-v1.0.0.zip -Algorithm SHA256).Hash
```

([Microsoft: Get-FileHash](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash))
Copy the long line of letters and numbers it prints.

1. On the repository's main page, to the right of the list of files, click **Releases**.
2. At the top of the page, click **Draft a new release**.
3. Open the **Choose a tag** dropdown menu, type `v1.0.0`, then click **Create new tag**. Git does not need a tag on your
   PC; GitHub creates the tag on the chosen branch (not verified on the guide page whether this happens at
   **Publish release** or earlier).
4. In the **Target** dropdown menu, choose `main`.
5. In the "Release title" field type exactly: `v1.0.0 — First Light` (the dash is an em dash; copy it from here).
6. Open `RELEASE_NOTES_v1.0.0.md` in VS Code, select everything (**Ctrl+A**), copy it, and paste it into the
   "Describe this release" field. Do not click **Generate release notes**; it would replace the text.
7. In the pasted text, find the line `SHA-256 of maker-mastery-v1.0.0.zip: <filled at packaging>` and replace
   `<filled at packaging>` with the checksum you copied. Do this only in the GitHub box, not in the file: the file is
   inside the ZIP, so changing it would change the checksum.
8. Drag `dist\maker-mastery-v1.0.0.zip` from File Explorer into the binaries box below the description (or click the
   box to choose the file). Wait until the upload finishes.
9. Leave **This is a pre-release** off. Selecting **Set as latest release** is optional; GitHub assigns "latest" by
   version number if you leave it.
10. Click **Publish release**. If you want to look again first, click **Save draft** instead and publish later.

After publishing, the release page lists your ZIP under "Assets", next to the **Source code (zip)** and
**Source code (tar.gz)** links that GitHub adds to every release
([downloading source code archives](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)).

## e. Tracking downloads

- **Release downloads.** GitHub counts downloads of files you attach to a release (release assets). The documented way
  to read that number is the Releases API: "the number of times people download a release asset"
  ([about releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)). Open this
  address in your browser, with your username in place of `mementomori-co`:

  ```text
  https://api.github.com/repos/mementomori-co/maker-mastery/releases
  ```

  Find `"name": "maker-mastery-v1.0.0.zip"` and read the `"download_count"` next to it
  ([REST API: releases](https://docs.github.com/en/rest/releases/releases),
  [release assets](https://docs.github.com/en/rest/releases/assets)). Published releases are visible to everyone, so
  no sign-in is needed. Whether the Releases web page also shows a count next to each file is not verified.
- **The README badge.** The "Release downloads" badge in `README.md` uses
  [Shields.io: downloads, all assets, all releases](https://shields.io/badges/git-hub-downloads-all-assets-all-releases).
  It shows a number once the release with its ZIP exists and your username has replaced `mementomori-co`. Badge images are
  cached, so it may lag behind the API (not verified how long).
- **Traffic.** On the repository page click **Insights**, then **Traffic** in the left sidebar. It shows views,
  unique visitors and full clones for the past 14 days, plus referring sites and popular content. Clones and visitors
  update hourly; all dates are in UTC+0
  ([viewing traffic](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository),
  [REST API: traffic](https://docs.github.com/en/rest/metrics/traffic)). Older days drop off, so write the numbers
  down if you want a longer history.
- **What is NOT counted as a release download.** **Download ZIP** under the **Code** button, and the
  **Source code (zip)** / **Source code (tar.gz)** links on the release, are source code archives that GitHub builds on
  request; they are not release assets, and `download_count` is a field of release assets only. So those downloads do
  not appear in the release download count or the badge. (This follows from GitHub's documented data model; no page
  states it in one sentence.)

## f. Before you publish: checklist

Tick every line before part d.

- [ ] **Privacy scan with your private denylist.** Keep the denylist outside this folder, with your real name,
      usernames, e-mail addresses, home folder, printer serials and anything else personal, one per line (format in
      `config\denylist.example.txt`). Then run:

      ```powershell
      .venv\Scripts\python.exe -B tools\privacy_scan.py . --denylist C:\Private\my-denylist.txt --exclude-dir __pycache__
      ```

      (Use the path of your own denylist.) It must end with no findings. Fix every finding, commit, and run it again.
      See [07 - Tools reference](07-tools-reference.md#privacy_scanpy).
- [ ] **`mementomori-co` replaced** in the 6 files from part a, committed and pushed. Search once more for `mementomori-co`: only
      this page may still contain it.
- [ ] **README in light and dark mode.** Open the repository page and read the README. Then switch GitHub's theme:
      your profile picture (upper right) > **Settings** > **Appearance** > "Theme mode", pick the other theme, and
      read it again
      ([managing your theme settings](https://docs.github.com/en/get-started/accessibility/managing-your-theme-settings)).
      Check that the banner and the "Memento Mori family" strip match the theme, the small crests in the Domains
      tables, the credits and the footer show, the badges load, the three diagrams draw, and no link shows `mementomori-co`.
- [ ] **Organization profile picture** (organizations only): `assets\brand\org-avatar-500.png` is uploaded (part c).
- [ ] **Social preview.** In **Settings**, under "Social preview", the image shows the crest and the title. Pasting the
      repository address into a chat app may still show an older cached card for a while (not verified).
- [ ] **About and topics** are saved and show on the main page: 20 topics.
- [ ] **Self-test** passes: `.venv\Scripts\python.exe -B tools\selftest.py` ends with `RESULT: PASS`.
- [ ] **Release file** `dist\maker-mastery-v1.0.0.zip` exists, was built after your owner commit, and you have its
      SHA-256.

## g. What NOT to do

- **Never commit** `config\paths.yaml` (your machine's paths), the `.venv\` folder, `work\`, `dist\`, or a denylist
  with real names in it. `.gitignore` already ignores `config/paths.yaml`, `config/denylist.txt`, `.venv/`, `work/` and
  `dist/`; a denylist kept outside this folder can never be committed at all. If `git status` lists any of them, do not
  run `git add -A`; ask Claude Code to help you find out why.
- **Never paste tokens or keys**: no GitHub tokens, API keys, stream keys or printer access codes in the terminal
  history you share, in commits, issues, release notes, screenshots or the About text. Git Credential Manager signs
  you in through the browser, so this guide never needs a token.
- **Never force-push** (`git push --force`) to `main` after people may have downloaded the project.
- **Do not let Claude Code publish for you.** Creating the repository, pushing, changing settings and publishing the
  release are your clicks. Claude Code can prepare files and run the checks.

---

Unofficial community project. Not affiliated with or endorsed by Anthropic or Bambu Lab. Claude and Bambu Lab are
trademarks of their owners.
