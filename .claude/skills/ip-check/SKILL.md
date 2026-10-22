---
name: ip-check
description: Use when a design, name, logo, derivative or licence question must be checked against primary IP sources before anything is sold, published or named. Runs the ip-researcher in a fresh context and writes a facts-only table (statute, agency, licence text, platform term) to research\ip\; never legal advice.
argument-hint: <topic-slug> | <question-slug> | <question text>
context: fork
agent: ip-researcher
---
## Overview
IP question: $ARGUMENTS, three fields separated by ` | `: topic slug, question slug, the question.

Output on disk: `research\ip\<topic-slug>\<question-slug>.md` in the ip-researcher's table format, with a `## Needs an attorney` section. The lead then runs `/verify` on that path.

## When to use
Before `/unit-cost` finalises a price, before `/makerworld-publish`, before a brand name or logo is adopted, before any fan-art or AI-generated asset is sold. Not for safety or product-compliance rules (`business-strategist`), not for what a client's own contract says (the maker's attorney).

## Steps
1. Parse the three fields. Check `knowledge\` and `research\verified\ip\` first; link existing facts by path rather than re-fetching them.
2. Fetch the primary pages for the question with WebFetch this run. Start from the source list in the ip-researcher agent, for example (US sources; use your own jurisdiction's equivalents): https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule, https://www.uspto.gov/trademarks/basics/strong-trademarks, https://www.copyright.gov/about/fees.html, https://www.copyright.gov/circs/circ33.pdf, https://www.law.cornell.edu/uscode/text/17/101, https://creativecommons.org/licenses/, and the platform's own terms page (for MakerWorld: https://makerworld.com/en/user-agreement and https://makerworld.com/en/exclusive-model-policy).
3. One row per fact: short quote (about 15 words at most), URL, kind (statute / agency / licence / platform / community), effective or page date. A fee or class without its date is incomplete. A page that returns HTTP 402/403 is written as `fetch blocked (HTTP nnn)` for the lead to re-fetch with `/research-one`.
4. For a trademark question, run the knockout search in the official trademark search system and record the system URL, query string, date and verbatim hit list; do not conclude "clear".
5. `## Needs an attorney`: every judgment the sources leave open (likelihood of confusion, fair use, separability, registrability), with the factors the source names.
6. Write the file; return its path and counts (rows by kind, needs-an-attorney items, not found). Name `/verify <path>` as the next step.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "This is obviously fair use." | Fair use is a judgment. Quote the four factors from the statute and stop. |
| "The fee has not changed." | Fee schedules carry effective dates. Fetch and quote the row. |
| "A single trademark search with no hits means clear." | Record the search; a knockout search is a fact about a query, not a clearance opinion. |
| "I'll skip the attorney section, there is nothing to add." | Every IP question has at least one judgment call. Name it. |

## Red flags (stop and fix)
- Advice phrasing ("you can", "safe to", "allowed to") anywhere in the file.
- A URL not fetched this run; a search snippet used as a page.
- A row of kind `community` with no primary row beside it.
- A write outside `research\ip\`.

## Verification
- [ ] File exists at `research\ip\<topic-slug>\<question-slug>.md`.
- [ ] Every row has quote, fetched URL, kind, date.
- [ ] `## Needs an attorney` is non-empty.
- [ ] Knockout search (if a name or logo) recorded with system URL, query, date, hit list.
- [ ] Path and counts returned; `/verify` named as next step.
