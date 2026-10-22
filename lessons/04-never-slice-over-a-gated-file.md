# Lesson 04: never slice or copy over a gated file

Area: slicing and print

| What happened | Root cause | Rule now |
|---|---|---|
| A sliced 3MF had passed the print-qa gate and its hash was recorded in the proof. Later, an agent running a "control" experiment exported an unsliced project to the same path. The gated file lost its G-code and checksum entries. The agent's report said "gated files untouched", which was true only for the files it had hashed. The change sat unnoticed in the working tree until someone read the change list line by line. | Nothing refused a write over a gated `*_SLICED.3mf`, and nothing re-checked a gated file's hash after its proof was written. Staging commits by explicit path also hid the unexpected modification instead of raising it. | 1. Gated files are read-only to every agent: experiments and controls write to a separate work folder and never share a path with a proof. 2. The proof's hash is the truth: a self-test re-hashes every file a proof names and fails on a mismatch. 3. The slicing wrapper refuses an output path that already exists as a gated file unless an explicit overwrite flag is given. 4. An unexplained modification of a gated file in `git status` is an incident, not noise. 5. A slice stays in the work folder until its read-back (result file, audits, G-code checks) passes; only then is it copied into the print folder under the gated name. |

How to check: before every commit or hand-off, re-hash each gated print file and compare it with the hash in its proof; any mismatch stops the release.

Tool reference: the slicing and audit helpers in `tools/`. Hash a file on Windows with PowerShell `Get-FileHash <file> -Algorithm SHA256`.
