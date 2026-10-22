---
name: makerworld-publish
description: Use when a model is ready to be published on MakerWorld and needs its licence choice, print profiles, photos and monetisation plan checked against MakerWorld's own pages. Runs the business-strategist in a fresh context and writes a publish plan whose every rule is quoted from a fetched MakerWorld URL.
argument-hint: "<model-slug> | <path to model folder with STL/3MF> | <intent: sell-physical | remix-ok | exclusive | undecided>"
context: fork
agent: business-strategist
---
## Overview
Publish plan for: $ARGUMENTS

Output on disk: `<model folder>\makerworld\publish-plan.md` (licence choice with quoted rule, files, profiles, photo checklist, money mechanics, tracking row) and, if anything could not be fetched, `research\inbox\makerworld\<model-slug>.md`. This skill never uploads anything; the maker publishes by hand.

## When to use
After the model prints and `/preprint-check` has passed on its 3MF; before the upload. Not for pricing physical sales (`/unit-cost`), not for the IP facts themselves (`/ip-check` must already have a file on record for this design).

## Steps
1. Fetch this run, with WebFetch (curl fallback on HTTP 402/403): https://makerworld.com/en/user-agreement, https://makerworld.com/en/exclusive-model-policy, https://makerworld.com/en/faq, https://wiki.bambulab.com/en/makerworld/tutorials/creator-commission-incentives. Record the "last updated" or page date for each. Never use a remembered number.
2. Build the licence matrix from the fetched text: for the Standard Digital File Licence, MakerWorld Exclusive and each Creative Commons option offered in the upload form, one row each with short quoted permissions (about 15 words at most per quote) for commercial use of prints, remixing, re-hosting, and where derivatives may be published. Link a verified MakerWorld note in `knowledge\` if one exists and skip rows it already covers.
3. Match the matrix to the intent argument; list what the intent rules out. If AI tools generated any part of the model, quote the page's rule on AI-generated content and Exclusive eligibility. Undecided: numbered NEEDS MAKER questions.
4. Files: list every STL/3MF with path. Profiles: one per printer you publish for (`knowledge\00-gear-inventory\`), each sliced with the installed CLI per `knowledge\02-bambu-studio\cli-slicing.md` (`tools\slice_cli.py`), each with a `/preprint-check` PASS path. No PASS, no profile in the plan.
5. Photos: quote the real-print photo rule from the fetched page; checklist per listing image (which print, which plate, which filament as recorded in the load record in `knowledge\00-gear-inventory\`).
6. Money: quote the point value, cash-out threshold, boost mechanics, membership fee and commission rates from the fetched pages with dates; add a tracking row template (date, downloads, boosts, points, cash-out).
7. Confirm `research\ip\` has a file for this design; if not, stop and return `NEEDS: /ip-check`. Write the plan; return paths and NEEDS MAKER questions.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "I remember the point value." | Remembered numbers drift. Fetch the page; quote with date. |
| "A render is fine for the cover photo." | Quote MakerWorld's real-print photo rule from the fetched page and follow it. |
| "One printer's profile will work on the other." | Different printer, different profile; each is sliced and `/preprint-check`-ed separately. |
| "The licence does not matter for a free model." | The licence sets what others may do with it. Choose from the quoted matrix against the maker's intent. |

## Red flags (stop and fix)
- A rule or number in the plan with no fetched URL and date beside it.
- A profile listed without a `/preprint-check` PASS path.
- No `/ip-check` file for the design.
- Licence chosen while intent is "undecided".
- Any upload, publish or print action: this skill only writes a plan.

## Verification
- [ ] All four MakerWorld URLs fetched this run; page dates recorded in the plan.
- [ ] Licence matrix rows are quotes, each with URL.
- [ ] Each profile names its 3MF path and its `/preprint-check` PASS path.
- [ ] `/ip-check` file path cited.
- [ ] `publish-plan.md` written; paths and NEEDS MAKER questions returned.
