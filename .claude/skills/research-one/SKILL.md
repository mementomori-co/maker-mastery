---
name: research-one
description: Use when ONE narrow question needs primary sources before it can be verified and filed. Runs the researcher in a fresh context and writes a claims table to research\inbox\<topic>\<question>.md; /research-topic calls this once per question.
argument-hint: <topic-slug> | <question-slug> | <question text>
context: fork
agent: researcher
---
## Overview
Input: $ARGUMENTS, three fields separated by ` | `: topic slug, question slug, the question.

## When to use
One narrow question, answerable from one or two primary pages. For a whole topic use `/research-topic`; for checking an existing claim use `/verify`.

## Steps
1. Parse the three fields. Output path: `research\inbox\<topic-slug>\<question-slug>.md`.
2. Fetch primary sources (official first: wiki.bambulab.com, the Bambu store and TDS pages, the BambuStudio GitHub source, then staff forum posts; community sources labelled "community"). On HTTP 402/403 use `curl -sL -A "Mozilla/5.0" <url> -o <scratch file under work\>` and read the file.
3. Write the claims table in the researcher's required format: `# | claim | value / short quote | source URL | official / community | version or date on page`, then `## Not found` and `## Pages fetched`. Keep quotes short (about 15 words); paraphrase the rest.
4. Return only the path and counts (claims, official, community, not found).

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "I remember this from training." | Memory is not a source. Fetch it, or write it under Not found. |
| "The search snippet shows the number." | A snippet is not the page. Fetch it or mark "snippet only". |

## Red flags
- A row without a URL fetched this run.
- A number without unit, condition, or version.

## Verification
- [ ] File exists at the output path.
- [ ] Every row has a fetched URL and a quote.
- [ ] Community rows labelled; Not found lists what was searched.
