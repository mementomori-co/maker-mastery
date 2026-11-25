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

This is a maintainer's own run. It is **not** an outside audit, and no outside user has yet reported running the whole
kit.

## Results

| Install | Checks passed | Skipped | Failed |
|---|---|---|---|
| Default (`requirements.txt`) | 218 | 11 | 0 |
| With the optional open3d 0.20.0 (`requirements-optional.txt`) | 229 | 0 | 0 |

The 11 skipped checks are all in `tools\tests\test_render_critic.py`. They need the optional open3d package, so a
default install skips them and still ends with `RESULT: PASS`. [04 - First run](04-first-run.md) and
[07 - Tools reference](07-tools-reference.md) show what that looks like.

Installing open3d changed none of the pinned package versions. It brought in 46 further packages that
`constraints.txt` does not pin, so their versions are whatever pip picks on the day you install.

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
- **One test writes inside the project folder.** It creates `knowledge\_selftest_bad_note.md` and deletes it again.
  If a run is interrupted the file can be left behind; delete it.
- **Temporary folders are left behind.** The tests create folders whose names start with `mm_` in your system's
  temporary folder and do not remove most of them.

## Check it yourself

From the project folder, after setup ([04 - First run](04-first-run.md)):

```
.venv\Scripts\python.exe -B tools\selftest.py
```

Compare the skipped counts with the table above. If your result differs, please report it: see
[CONTRIBUTING.md](../CONTRIBUTING.md), or [SECURITY.md](../SECURITY.md) for a security problem.
