# `maker` schema - what was forked from where

OpenSpec custom schema for Memento Mori Maker Mastery projects. Resolved first from this folder because it sits at
`openspec/schemas/maker/` (OpenSpec `src/core/artifact-graph/resolver.ts:124-126`). Validate after install with
`openspec schema validate maker` (pasted into the VS Code terminal; see the project `README.md`).

## Forked files (OpenSpec 1.14.0, https://github.com/Fission-AI/OpenSpec, commit 2500d6da971336167548b53731a35b2127df35ac, MIT)

| File here | Copied from | Changes |
|---|---|---|
| `schema.yaml` | `schemas/spec-driven/schema.yaml` | `name: maker`; description; two artifacts added at the top (`assessment`, `constitution-check`); `proposal.requires` = `[assessment, constitution-check]`; paragraphs marked "Maker Mastery:" added to the `proposal`, `design` and `apply` instructions. OpenSpec's instruction text is otherwise verbatim. |
| `templates/proposal.md` | `schemas/spec-driven/templates/proposal.md` | unchanged |
| `templates/spec.md` | `schemas/spec-driven/templates/spec.md` | unchanged |
| `templates/design.md` | `schemas/spec-driven/templates/design.md` | unchanged |
| `templates/tasks.md` | `schemas/spec-driven/templates/tasks.md` | unchanged |
| `LICENSE-openspec.txt` | `LICENSE` | unchanged (MIT, Copyright (c) 2024 OpenSpec Contributors) |
| `templates/assessment.md` | new (Maker Mastery) | concept from spec-kit `extensions/assess/` (see below) |
| `templates/constitution-check.md` | new (Maker Mastery) | concept from spec-kit `templates/plan-template.md` "Constitution Check" + "Complexity Tracking" (see below) |

## Artifact graph
`assessment` (requires nothing) -> `constitution-check` (requires assessment) -> `proposal` (requires both) ->
`specs` and `design` (require proposal) -> `tasks` (requires specs + design) -> `apply` (requires tasks, tracks `tasks.md`).
Field contract honoured: `id`, `generates`, `description`, `template`, `instruction`, `requires` per artifact;
`apply.requires`, `apply.tracks`, `apply.instruction` (`src/core/artifact-graph/types.ts`). Templates must sit in
`templates/` next to `schema.yaml` (`src/commands/schema.ts:205-228`).

Gates OpenSpec does not enforce (it only checks that files exist): the `VERDICT:` line in `assessment.md` and the
`GATE:` line in `constitution-check.md` are read by the agent and by the maker, same pattern as the community `anvil`
schema's `VERDICT:` line (OpenSpec `docs/customization.md` > Community Schemas).

## Attribution
- OpenSpec: MIT. "Copyright (c) 2024 OpenSpec Contributors" - full text in `LICENSE-openspec.txt`; required because
  `schema.yaml` and four templates are substantial copies.
- spec-kit (https://github.com/github/spec-kit, commit e1fa857a7f536b22760d48c1aa9ace41df0fd1dc, MIT, Copyright GitHub, Inc.):
  the assessment funnel (intake -> research -> define -> shape -> decide, go / needs-clarification / kill scorecard,
  `ASSUMPTION` tag, mandatory "Evidence against") and the Constitution Check / Complexity Tracking gate are reused as
  concepts and rewritten; the scorecard criterion names are theirs. spec-kit itself is not installed.
