# Verification status and known limitations

What has actually been run, where, and with what result, and what has not been checked yet. Read this before you rely
on a claim that something "is tested". Back to the start: [01 - What this is](01-what-this-is.md).

## What was run

| | |
|---|---|
| Version | tag `v1.0.1` (commit `dc065713e8ea90d20b16766325aa858e84f3ea58`), a fresh clone from GitHub |
| Date | 2026-11-22 |
| Where | one Windows PC, Python 3.12.10, a new virtual environment, not run as administrator |
| Packages | `requirements.txt` with `constraints.txt`; all 37 packages installed at the pinned versions |
| What | `tools\selftest.py`, which runs the 15 test files in `tools\tests\` (229 checks) |
| Who | the maintainer, working with an AI coding assistant, in a separate copy of the repository |

This is a maintainer's own run. It is **not** independent verification and **not** an outside audit: no one outside
the maintainer's own setup has reported repeating it, and no outside user has yet reported running the whole kit.

Every figure on this page comes from this one run on `v1.0.1`. None of them is from the testing done for the original
v1.0.0 release; [RELEASE_NOTES_v1.0.0.md](../RELEASE_NOTES_v1.0.0.md) records what was seen on the build PC at that
time.

## Results

| Install | Checks passed | Skipped | Failed |
|---|---|---|---|
| Default (`requirements.txt`) | 218 | 11 | 0 |
| With the optional open3d 0.20.0 (`requirements-optional.txt`) | 229 | 0 | 0 |

The 11 skipped checks are all in `tools\tests\test_render_critic.py`. They need the optional open3d package, so a
default install skips them and still ends with `RESULT: PASS`. [04 - First run](04-first-run.md) and
[07 - Tools reference](07-tools-reference.md) show what that looks like.

The optional install changed none of the 37 pinned package versions. It added 46 packages in total: open3d itself,
which `requirements-optional.txt` pins at 0.20.0, and 45 further packages that pip installed with it. `constraints.txt`
lists none of the 46, so the versions of those 45 are whatever pip picks on the day you install.

## What these results show, and what they do not

They show that the Python tools and the hook scripts pass their unit tests on one PC.

They do **not** show any of the following:

- **Live use with Claude Code.** The agents, skills and commands were not exercised in a live Claude Code session, and
  the hooks were tested as scripts, not while firing in a live session.
- **Bambu Studio and Blender.** No test starts either program. `tools\slice_cli.py` is tested for its guards and its
  locking only; the tests never launch the slicer. Real slicing of a real model is not covered.
- **Anything at a physical printer.** The rule that no AI ever starts, sends, uploads or queues a print is part of the
  operating rules ([06 - Print safety](06-print-safety.md)). These unit tests do not test that rule end to end with a
  real printer. You press Print yourself, and you check the file before you do.
- **Other computers.** One machine and one Python build. Running the project on macOS or Linux is not supported yet
  ([02 - Install](02-install.md)).
- **Every file.** No test covers `tools\selftest.py` itself, `tools\stability_render.py`,
  `examples\calibration-cube\make_cube.py`, `tools\setup.ps1` or the scripts in `install\`.

## Things to know about the self-test

- **`PASS` means nothing failed.** A line can read `PASS` with some of its checks skipped, and a whole file can read
  `SKIPPED` when a package is missing; the result is still `PASS`. Read the skipped counts, not only the last line.
- **Nothing runs the tests for you.** The repository has no continuous integration. The self-test runs only when
  someone runs it.
- **One test writes inside the project folder, and can destroy a file of yours.** Read
  [Before you run setup or the self-test](#before-you-run-setup-or-the-self-test) first.
- **Temporary folders are left behind.** The tests create folders whose names start with `mm_` in your system's
  temporary folder and do not remove most of them.

## Before you run setup or the self-test

`tools\setup.ps1` runs the self-test automatically as its last step. Everything in this section applies to setup as
well as to `tools\selftest.py`.

**Both** of the following must be true before every run. Neither is enough without the other.

**A. Use a disposable clone.** Run setup and the self-test only in a fresh, disposable clone of the repository (a new
`git clone` or a newly extracted ZIP) that contains none of your own work and nothing you could not replace. A folder
you have started to work in is not disposable, even when the check in B passes.

**B. Confirm the collision-prone file is absent.** From the repository root, in PowerShell:

```powershell
Test-Path .\knowledge\_selftest_bad_note.md
```

Go on only if this prints `False` **and** the folder is a disposable clone. If it prints `True`, stop. Do not
overwrite, delete or automatically clean up the file, and do not run setup or the self-test. Find out what the file is
first: it may be your own, or it may be left over from a run that was interrupted.

**Why.** One test, `test_hook_mode_blocks_bad_knowledge_note` in `tools\tests\test_config_and_cli.py`, writes a file at
`knowledge\_selftest_bad_note.md` inside the project folder and then deletes it. It does not check first whether a file
is already there, so a file you have at that path is overwritten and then deleted. This is a defect in the test and it
has not been corrected yet. The check in B covers this one known file. It does not make the self-test safe to run in a
folder that holds your work, which is why A is required as well.

**If the folder you work in needs setup again** (for example to add the optional open3d package, or because `.venv` is
missing), do not run setup there. Set up a fresh clone instead, and move your own files into it after setup has
finished.

## Check it yourself

Only when A and B above both hold (a fresh, disposable clone, and `Test-Path .\knowledge\_selftest_bad_note.md`
printing `False`), and after setup ([04 - First run](04-first-run.md)):

```
.venv\Scripts\python.exe -B tools\selftest.py
```

Compare the skipped counts with the table above. If your result differs, please report it: see
[CONTRIBUTING.md](../CONTRIBUTING.md), or [SECURITY.md](../SECURITY.md) for a security problem.
