# Contributing

Thank you for helping. This project is a Claude Code operating system for makers: 3D printing, CAD, electronics, rendering, game dev and more. 3D printing on Bambu Lab printers is the flagship example, with rules, a verified knowledge library, agents and skills, a print-quality gate and slicing and audit helpers. Contributions of every size are welcome: a corrected fact, a new knowledge note, a lesson, a tool fix.

By contributing you agree that your contribution is released under the MIT License (see [LICENSE](LICENSE)) and that you follow the [Code of Conduct](CODE_OF_CONDUCT.md). Brand assets are not open for contributions; see [NOTICE.md](NOTICE.md).

The repository lives at `https://github.com/mementomori-co/maker-mastery`.

## The one rule that never bends

**No AI ever starts, sends, uploads or queues a print.** Agents, skills, commands, hooks, MCP servers and tools in this repository may prepare, slice and check print files. Only the maker presses Print, in Bambu Studio. A pull request that adds any route to start, send, upload or queue a print (LAN, cloud, printer API, MCP tool, hook or prompt) will be closed. If you find such a route, report it privately as described in [SECURITY.md](SECURITY.md).

## Adding a knowledge note

Knowledge notes live in `knowledge/<NN-category>/`, one topic per file, with a kebab-case file name. Every category has an `index.md`.

1. **Check first.** Search the category for an existing note on the topic. Merge into it rather than adding a near-duplicate.
2. **Start from the template.** Copy `templates/note.md`. Keep its header lines (`Applies to:` and `Verified:`) and its sections: Facts, what it means in practice, Not verified / open questions, Sources.
3. **Every fact needs a public source.** End each fact with a link to where it can be checked. Preferred order: the Bambu Lab wiki, the Bambu Lab store or technical data sheet, the Bambu Studio source code on GitHub (https://github.com/bambulab/BambuStudio), then staff forum posts. Community posts are labelled "community". A fact without a source goes under "Not verified / open questions".
4. **Numbers carry their condition.** Write the printer, nozzle, material, temperature or test method a number applies to.
5. **Slicer settings by label and key.** Write the exact user-interface path as `Tab > Section > Setting` and the configuration key. Mark a label you could not check as "(label not verified)". Never copy Bambu Studio profile JSON files, vendor data sheets or vendor images into the repository: link to them.
6. **Quote little.** At most about 15 words verbatim from any one source; paraphrase the rest and cite the public URL.
7. **Update the index.** Add a one-line summary of the note to the category's `index.md`.
8. **Fact-check before merge.** Every new or changed fact is checked independently before the pull request is merged: a second person, or the `fact-checker` agent in a fresh context that sees only the claims and not your reasoning (the `/verify` skill does this). Paste the result (VERIFIED / CONTRADICTED / UNVERIFIABLE per claim, with the URL) into the pull request. Only VERIFIED facts are merged as facts.

## Adding a lesson

Lessons in `lessons/` are short post-mortems: what happened, the root cause, and the rule that now prevents it. Keep them general: no names, places, accounts or personal project details. Add the lesson to `lessons/INDEX.md`.

## Run the privacy scan before every pull request

The privacy scan looks for personal data before it leaves your machine: your name and handles, user-profile paths, e-mail addresses, private IP addresses, secret-looking values, printer serials, and metadata hidden inside images, 3MF and other ZIP files and PDFs.

1. Copy `config/denylist.example.txt` to a folder **outside** the repository and fill it with your own details (name, handles, city, printer nicknames). Never commit your real denylist. The repository's `.gitignore` also ignores `config/denylist.txt` in case you keep it there.
2. From the repository folder, run (PowerShell):

   ```powershell
   .venv\Scripts\python.exe -B tools\privacy_scan.py . --denylist C:\path\to\your-denylist.txt
   ```

3. Exit code 0 means clean. Exit code 1 lists every hit as `path:line: [rule] context`: fix each one, then run the scan again. Exit code 2 means the scan could not finish; read the error before trusting the result.
4. If an image or 3MF carries metadata, `tools/strip_metadata.py` removes it.

## Code changes

- Python 3.12 or newer. Prefer the standard library; any new dependency goes into `requirements.txt` and a row in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
- No hard-coded drive letters, user folders or install paths. Machine-specific values live only in `config/paths.yaml` (copied from `config/paths.example.yaml`) and are read through `tools/mm_config.py`.
- Code adapted from another project needs its licence: add the credit and the licence text to [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
- Run the tests in `tools/tests/` before you open the pull request.

## Pull request checklist

- [ ] The privacy scan exits 0 on the changed files.
- [ ] Every new fact has a public source and an independent fact-check result.
- [ ] Nothing in the change can start, send, upload or queue a print.
- [ ] Third-party code, text or dependencies are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
- [ ] [CHANGELOG.md](CHANGELOG.md) has a line under "Unreleased" for user-visible changes.
