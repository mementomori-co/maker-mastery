# Optional workflow: pair Claude Code with a second Claude chat reviewer

You do not need this to use Memento Mori Maker Mastery. It is for makers who like a second opinion: Claude Code does the
work in VS Code, and a separate Claude chat conversation (on claude.ai or in the Claude app) reviews each step and answers
its questions. The two never talk directly. They share one file, `plan\handoff\TO_CHAT.md`, and you carry the replies.

## How it works
```
Claude Code (VS Code)  --appends a report-->  plan\handoff\TO_CHAT.md
You                    --paste the new report into-->  your Claude chat reviewer
Claude chat            --replies with decisions-->  you paste the reply into the Claude Code panel
```

1. Claude Code appends a report to `plan\handoff\TO_CHAT.md` every time it stops, finishes a step or needs a decision.
   The format is in `TO_CHAT.template.md` in this folder.
2. You copy the newest report into your reviewer chat. The reviewer checks the evidence (file paths, tool output, renders)
   and answers the numbered questions.
3. You paste the reviewer's reply into the Claude Code panel. Claude Code treats it as your answer only for decisions you
   have delegated in writing (see "What a reviewer may decide" below).

## Turn it on
1. Create the folder `plan\handoff\` in the project root (File Explorer > New > Folder, or let Claude create it).
2. Copy `templates\handoff\TO_CHAT.template.md` to `plan\handoff\TO_CHAT.md`.
3. Add this line to the end of your `CLAUDE.md` (or ask Claude to add it):
   `Handoff: every stop, step finish or decision point is appended to plan\handoff\TO_CHAT.md in the format of templates\handoff\TO_CHAT.template.md.`
4. Start your reviewer chat with: "You review the work of a Claude Code session. I will paste reports from its TO_CHAT.md.
   Check every claim against the evidence it cites, answer the numbered questions, and say STOP if anything is unsafe or unverified."
5. If you keep `plan\` out of git, add `plan/` to your `.gitignore`.

## What a reviewer may decide
Write down which decisions you hand to the reviewer, for example in a short list at the top of `TO_CHAT.md`. A sensible default:
- **The reviewer may decide:** technical choices inside a step you already approved (which option to build, whether evidence
  is enough to move to the next step).
- **Only you decide, never the reviewer:** pressing Print (no AI ever starts, sends, uploads or queues a print), deleting files,
  installing software, spending money, signing up for accounts, and anything touching a folder listed under
  `protected_roots` in `config\paths.yaml`. Claude Code marks these `NEEDS_DECISION` and keeps working on what is not blocked.

## Rules for every report
- Header line: `## YYYY-MM-DD HH:MM <your time zone> - STATUS: WORKING|STOPPED|NEEDS_DECISION`, with the real time read from the
  PC clock, never guessed.
- What changed, files to review (full paths), Known flaws, then numbered questions.
- Append only. Never rewrite an earlier report; correct it in a new one.
