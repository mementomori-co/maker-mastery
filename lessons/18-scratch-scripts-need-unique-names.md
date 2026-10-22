# Lesson 18: scratch scripts need unique names, and appends assert their target

Area: agent and tool hygiene

| What happened | Root cause | Rule now |
|---|---|---|
| An agent wrote a scratch script with a generic name and ran it, but an older script of the same name left in the shared scratch folder by an earlier agent ran instead, and appended a large block of text to the wrong review file. The agent noticed, cut the file back and confirmed it matched the committed version. | One scratch folder is shared by every agent in a session and scripts are addressed by bare name. A generic name (`append_review.py`, `patch.py`, `fix.py`) is a collision waiting to happen, and an append script that does not check its target writes wherever the old copy pointed. | Scratch files carry a task-specific name (task, purpose, time). An append or patch script asserts its target path and a unique anchor before writing, and the writer re-reads the target and shows the diff afterwards. A review file is appended only by the agent whose review it is. |
| A later agent's write of a scratch file was refused because a stale file of the same name existed; it appended that stale file to a measurement sheet anyway. | A refused write was treated as a warning, not a stop. | A refused write is a stop, never followed by appending a file of the same name. An append script asserts the first line of the text it is about to append. |

How to check: after any scripted append, diff the target file against its previous version and confirm only the intended block was added.
