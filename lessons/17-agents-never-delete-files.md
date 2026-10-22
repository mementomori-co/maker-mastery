# Lesson 17: agents never delete files, not even their own

Area: agent and tool hygiene

This lesson merges several incidents of the same kind.

| What happened | Root cause | Rule now |
|---|---|---|
| A CAD agent revising a test part removed two of its own earlier STLs and their renders after exporting replacements. A media agent deleted stale images it had rendered earlier so a folder held one file per item. Another agent deleted a `__pycache__` folder its own Python run had created. A coupon agent deleted two of its own draft documents after a material change. Every agent reported the deletion; nothing of the maker's was lost. | Each agent judged its own outputs, caches or drafts as exempt from "delete nothing". Briefs that asked for a revision did not repeat the rule, and some agents read "delete nothing" as "delete nothing of the maker's". | Deleting any file is the maker's decision only, including an agent's own drafts, caches and outputs. A file that must not be used is renamed with a `SUPERSEDED_` prefix or moved into a `_superseded_*` folder. Before any regenerate or in-place edit, copy the current file (outputs, sources and proofs) into that folder; the file count must never drop. Every brief that may replace files says this in one line. Run Python with `-I -B` so no cache folder is written; if something is created by accident, leave it and report it. |

How to check: count files in the working folder before and after an agent run; any drop is reported to the maker with the file names.
