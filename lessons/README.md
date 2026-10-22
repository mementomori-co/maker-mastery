# Lessons

A lesson is a short post-mortem of a real mistake, written so the same mistake does not happen twice. These lessons came from real print, CAD and agent work and were rewritten to be generic: no project names, dates or personal details.

Claude Code reads this folder at the start of a session (see [../CLAUDE.md](../CLAUDE.md)). The list is in [INDEX.md](INDEX.md).

## Format

Each lesson is one Markdown file named `NN-short-slug.md` (two-digit number, lowercase words joined by hyphens, no dates). It holds:

1. A title: `# Lesson NN: <the rule in a few words>`.
2. An `Area:` line (for example slicing and print, CAD, agent and tool hygiene).
3. A table with exactly these columns, one row per failure:

   | What happened | Root cause | Rule now |
   |---|---|---|
   | The observable failure, described generically. | Why it happened, the mechanism, not the blame. | The rule that prevents it, written so an agent can follow it. |

4. A `How to check:` line: one concrete test that shows whether the rule is being followed.
5. Optional: a reference to a helper in [../tools/](../tools/), a code snippet, and public source URLs for any hardware, software or material fact.

## How to add your own

1. Write the lesson as soon as the mistake is fixed, while the cause is still clear. Own the mistake in one line; the table does the rest.
2. Take the next free number and a slug that names the rule, not the project.
3. Keep it generic if you plan to share it: leave out project names, dates, file paths, serial numbers, account details and anything secret.
4. Every fact about a printer, slicer or material links a public source, or is labelled "not verified".
5. Add one line to [INDEX.md](INDEX.md) under the right heading.
6. If the rule changes how a check works, put it where it is enforced too: the pre-print checklist in [../templates/](../templates/), an agent definition in [../.claude/agents/](../.claude/agents/), or a test for a tool in [../tools/](../tools/).
7. When the same mistake happens again, add a row to the existing lesson instead of a new file, and say why the rule did not stop it.

Templates for notes, part specs and the pre-print checklist live in [../templates/](../templates/).
