---
id: SR-005
title: "EARS requirement-grammar review of the issue #2 semantic-module-contract specification"
type: SpecReview
analysis: ears-conformance
scope: "spec/stakeholder/StR-001, spec/functional/FR-001..FR-006, spec/non-functional/NFR-001"
review_set: subset
---
# EARS requirement-grammar review of the issue #2 semantic-module-contract specification

## Summary

The 99 SHALL-bearing statements of the eight requirement-bearing artifacts on
`2-semantic-module-contract` (StR-001 Stakeholder Need; FR-001..FR-006
Description, Behavior and Constraint cells; NFR-001 Statement) were read for
EARS pattern, single obligation, named subject and decidable response, against
quire 0.31.0 (engine 0.46.0). The engine reports **14/20 documents grammar-clean
(70%), 27 findings: `ears:non-singular` 20, `quality:agentless-passive` 7**,
concentrated in FR-004, FR-005 and FR-006. The dominant defect is mechanical and
uniform: a bullet that states two obligations joined by `and` or `;` where the
merged `spec-objects-business` migration — the model for this migration, and
**27/27 documents grammar-clean, zero findings, zero multi-`SHALL` lines across
its own 87 SHALL statements** — writes two bullets. Splitting them is the whole
fix for 20 of the 27.

The engine's own statement unit is a **physical line**, so three further
compound statements (the FR-004, FR-005 and FR-006 Descriptions) escape the
count purely because their prose is hard-wrapped; the true non-singular
population is 23 of 99, and 70% grammar-clean is optimistic rather than earned
(FND-103). Pattern selection is otherwise good: every unwanted condition that is
stated uses `If … then … SHALL`, and no statement anywhere uses an
`On`/`Upon`/`After`/`During` trigger — the engine agrees, reporting zero
`non-canonical-trigger`, zero `missing-subject`, zero `vague-response` and zero
`unclassifiable`.

One high sits under the mechanical layer: FR-006 governs `semantic.imports` with
two triggers that disagree about when the field stops being `{}` (FND-101). The
mediums are one obligation placed on a stakeholder rather than on the module —
the exact defect `spec-objects-business` dispositioned in its own EARS review —
one Behavior paragraph carrying no modal at all, two agentless `SHALL be
reached` allocations, and two responses no test can decide.

## Verdict

**CONDITIONAL on the grammar posture.** The bundle is materially below the model
it names: `spec-objects-business` reaches 100% grammar-clean and this branch
reaches 70%, on statements that are in several places the same sentences with
two bullets merged into one. Twenty of the 27 engine findings are a
split-the-bullet edit with no semantic decision attached. FND-101 needs a
wording decision before FR-006 is implementable; the remaining mediums are
wording plus one missing modal. No spec artifact was edited by this review.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-101 | high | FR-006 governs `semantic.imports` with two triggers that disagree. Line 42: "Until `agent-ix/spec-objects-security#13`, `agent-ix/spec-objects-architecture#8` and `agent-ix/spec-objects-operational#6` land, `semantic.imports` SHALL be `{}`" — the field stops being empty when the three issues land. Line 43: "When a neighbouring module publishes its semantic contract, this module SHALL add it to `semantic.imports` at that exact version in the same change that first names one of its types in a shipped fixture" — the field stops being empty when a fixture first names a type. A state where all three have landed and no fixture names a type satisfies one statement and violates the other, and no criterion covers the transition (FR-006-AC-3 asserts `{}` only). One implementer would populate `imports` on the neighbour's release; another would leave it empty indefinitely. Pick one trigger and state the other as its rationale — `While no shipped fixture names a type of a neighbouring module, `semantic.imports` SHALL be `{}`` reads the fixture rule as authoritative and keeps the three issues as the reason. `Until` is additionally a non-canonical state keyword for which the model repo already uses `While` in the identical construct (`spec-objects-business` FR-005: "While no committable index carries Quire 0.46.0, the module SHALL NOT declare `quire` in `pyproject.toml`"). | FR-006 | wrong-requirement |
| FND-102 | medium | All 20 `ears:non-singular` findings are one shape: two obligations in one bullet, where `spec-objects-business` writes two. The clearest proof is a line the two repos share almost verbatim — safety FR-002:71 "The generator SHALL write files under `spec_objects_safety/schemas/` only, and SHALL edit `manifest.yaml` only at `data_schema.digest` values" is business FR-002:88-89, split into "The generator SHALL write files under … only." and "The generator SHALL edit `manifest.yaml` only at `data_schema.digest` values." The rest: FR-002:74 (copy plus `--clean` removal), FR-003:52 (install plus list), FR-003:61, FR-004:50 (admit plus forbid), FR-004:51, FR-004:52 (require plus admit-optional), FR-004:55 (membership plus disjointness), FR-004:63 (no redeclaration plus every item a `$ref`), FR-005:48 (ship alternate plus identical extraction), FR-005:49, FR-005:50 (declare clauses plus source span), FR-005:51 (heading declared plus required headings present), FR-005:53 (placeholder-free plus substantive), FR-005:54 (distinct `Identifier` plus `object` equals `type`), FR-005:56 (three obligations), FR-006:38, FR-006:39, FR-006:42, NFR-001:14 (keep unchanged plus add only `required: false`). Each half is separately verifiable and several already have separate acceptance criteria, so the merge costs traceability for nothing. | FR-002, FR-003, FR-004, FR-005, FR-006, NFR-001 | wrong-requirement |
| FND-103 | medium | The 70% figure is measured per physical line, so a compound statement escapes it by wrapping. Three Descriptions carry two `SHALL` each across a line break and are reported clean: FR-004 ("Each declared object type SHALL have its own emitted schema … and the scored axes SHALL keep 'unknown', 'not assessed' and 'not applicable' distinct"), FR-005 ("Each object type's authoring skeleton SHALL be a document the engine validates and extracts … and each named refusal SHALL have a fixture that fails for that reason"), FR-006 ("The module SHALL point at the control, risk, architecture, operational and evidence types … and SHALL declare no type, field or vocabulary that duplicates one of them"). NFR-001's Statement is the control case: the same construct on one line is flagged. The real non-singular population is 23 of 99 statements, not 20, and no reader should take 70% as the conformance level. The model repo is not exposed to this: `grep -n "SHALL.*SHALL"` over its FR, NFR, StR and US artifacts returns nothing, so its 100% holds at line level and paragraph level alike. | FR-004, FR-005, FR-006 | wrong-requirement |
| FND-104 | medium | StR-001's Stakeholder Need places the obligation on the stakeholder, not on the system: "A team working to a safety standard **SHALL** record hazards and failure modes as first-class specification objects". Nothing this module builds can discharge or violate a duty held by a team, so the statement is unfalsifiable by any test, and StR-001-VC-1/VC-2 in fact verify the module rather than the team. The model repo dispositioned exactly this in its own EARS review (business FND-235, "StR-001's Stakeholder Need places the obligation on the module") and now reads "The Filament platform, spec authors, and agent CLI generators require that the module SHALL make …". Restate as the module's obligation with the team as the beneficiary. The response is also compound (validated on the same path, and linkable to mitigating requirements), which is why the two VC rows split cleanly along it. | StR-001 | wrong-requirement |
| FND-105 | medium | FR-003 Behavior line 51 carries no modal at all: "Measured against quire 0.46.0: a refused schema drops that object type alone, while a manifest key the loader cannot parse drops every object type of the module … Both refusals are silent … which `agent-ix/quire-rs#221` and `agent-ix/quire-rs#394` record as engine defects; the naming half of FR-003-AC-6 is blocked on them". Positioned among SHALL bullets it reads as a requirement, but it obliges nobody — it is a measurement of the current engine plus a disposition of an acceptance criterion. As written nothing in the bundle is violated if the engine's behaviour changes, and FR-003-AC-6's blocked half rests on prose the grammar does not count. Move it to Inputs or to a Notes block, and keep in Behavior only what this module SHALL do. The same class was raised and applied in the model repo (business FND-223, a ten-row obligation table with no governing SHALL). | FR-003 | missing-requirement |
| FND-106 | medium | Two obligations state a reachability property with no agent: FR-006:38 "A control SHALL be reached through the incoming `mitigates` edge the manifest `traceability` model already declares" and FR-006:39 "An evidence record SHALL be reached through `EvidenceRef.target`, a `SemanticId`". Both are flagged `quality:agentless-passive`, and the gap is real rather than stylistic — neither says whether the reacher is Quire's traceability check, Quoin, `spec-objects-security`'s hazard-coverage query, or a human reader, so a failure to reach one allocates to no component and FR-006-AC-2 tests the schema shape instead. The model repo's passives all name the agent and pass clean (business FR-004:71, "Every … item SHALL be validated by `$ref` to the semantic-core 0.1.0 model, never by a copied definition"). Name the consumer, or restate as this module's own obligation: "The module SHALL express every control reference as an incoming `mitigates` edge and SHALL NOT list a control on the hazard or failure-mode record." | FR-006 | wrong-requirement |
| FND-107 | medium | Two responses are not decidable, and the vague-verb lexicon does not catch either because neither uses a listed verb. FR-005:53 "Every skeleton SHALL be free of placeholder tokens and SHALL have substantive content in every asserted section" — "substantive" states no threshold, and FR-005-AC-7 restates the same word ("Every skeleton is placeholder-free with non-empty asserted sections"), so what the test asserts (non-empty) is strictly weaker than what the requirement says. FR-005:56 "its error SHALL carry detail beyond the `expect` token" — "detail beyond" is unmeasurable as written, and FR-005-AC-5 repeats it verbatim. State the placeholder token set and the minimum section content, and state what the error must additionally carry (a path, a locator name, a line span). | FR-005 | wrong-requirement |
| FND-108 | medium | FR-005:49 "No artifact SHALL carry both Properties forms; the second form SHALL be refused" leaves two things undecided. "The second" is order-dependent — the refusal target depends on document order, which no other statement makes significant — and the refusal names no agent and no diagnostic severity, in a module whose manifest declares `legacy_forms: warning` and whose NFR-001-AC-3 turns on a Properties section yielding a warning rather than an error. An implementer cannot tell whether the second form is an error or a warning, nor which component emits it. Restate as "If an artifact carries both a typed `## Properties` table and a `sysml` fence, then `quire.validate_document` SHALL report an error naming both blocks." | FR-005 | wrong-requirement |
| FND-109 | medium | FR-003-CON-3 packs three obligations into one constraint cell with the trigger buried in the middle: "The FR-035 gate SHALL never skip. When the installed `spec-artifacts-iso` schema predates CR-012 the gate SHALL run against the pinned revision copy and SHALL fail if that copy differs from the installed schema anywhere outside the CR-012 paths." Three `SHALL`, one unconditional and two under a state that is also a temporary one. Split into `The FR-035 gate SHALL never skip.` plus `While the installed spec-artifacts-iso schema predates CR-012, the gate SHALL run against the pinned revision copy.` plus `If the pinned copy differs from the installed schema outside the CR-012 paths, then the gate SHALL fail.` The third half is the one FR-003-AC-7 actually verifies. | FR-003 | wrong-requirement |
| FND-110 | low | FR-004:59 "If `status` is `accepted`, then `provenance` SHALL be required" uses the right pattern but names no agent (`quality:agentless-passive`) and, more usefully, no schema: `Hazard.json`, `FailureMode.json` or both. FR-004-AC-8 exercises "a record" without saying which type, so the criterion under-determines its own fixture. Restate as "If a `Hazard` or `FailureMode` record declares `status: accepted`, then its schema SHALL require `provenance`." | FR-004 | wrong-requirement |
| FND-111 | low | Three constraint cells state prohibitions in agentless passive: FR-004-CON-3 "No constraint in these schemas SHALL be relaxed to make a fixture, a skeleton or a corpus document pass", FR-005-CON-1 "No corpus repository or vendored fixture SHALL be edited", FR-006-CON-1 "No safety-only synonym SHALL be minted for a verb or a type another module already declares". The intended agent is the implementer of this change, and naming it costs a clause: "No change under this requirement SHALL relax / SHALL edit / SHALL mint …". FR-005 Behavior already writes the FR-005-CON-1 obligation in exactly that agented form on line 57 ("No corpus repository, vendored corpus fixture, or sibling module SHALL be edited by this requirement"), so the fix is to carry that wording into the cell. Cosmetic, but it is three of the seven agentless findings and the model repo carries none. | FR-004, FR-005, FR-006 | wrong-requirement |
| FND-112 | low | Two trigger-form nits the engine does not flag. FR-002:56 "When no `$id` or `$ref` is relative, the generator SHALL record the normalization as `applied: false`" is the complement of the preceding `If … then` bullet and states a condition, not an event; `If … then` keeps the pair symmetric. FR-005:58 "The semantic tests SHALL fail, never skip, when the Quire wheel is absent" puts the trigger last, where EARS leads with it: "If the Quire wheel is absent, then the semantic tests SHALL fail rather than skip." Neither changes what gets built. Recorded to note what is *not* wrong: no statement in the bundle uses `On`, `Upon`, `After` or `During`, and the engine reports zero `non-canonical-trigger`. | FR-002, FR-005 | wrong-requirement |
| FND-113 | low | FR-002:62 states a human procedure as a system obligation: "If the manifest `version` changes, then the bump procedure SHALL be: edit the `@jsonSchema` base … and the manifest `version` in the same commit, run `make schemas`, and commit … together". The subject is "the bump procedure" rather than an actor, and the three imperatives fall on a maintainer, which no test can hold. The enforceable half is already stated twice with proper subjects — FR-002:66 (the generator fails on a version mismatch) and FR-002:69 (the check exits non-zero on a stale file) — and FR-002-AC-8 verifies those. Demote the bullet to a Notes or Rationale line and keep the two agented statements as the obligation. | FR-002 | wrong-requirement |
| FND-114 | low | FR-001's Description states an obligation the same document retracts: "The module SHALL declare two object types, each with a body contract, an authoring skeleton, **and a role**", while its "No new verbs" section concludes "No role is declared either … the `safety-relevant` capability tag this module first reached for turned out to be unnecessary". The acceptance-criterion instance of this contradiction is already on the review record and is not restated here; it is recorded at this locus because the Description *is* the requirement statement this lens reads, it is the first text an implementer meets, and a grammar pass that fixes the criterion and leaves the Description would leave the requirement still asserting a role. Drop "and a role" from the Description in the same edit. | FR-001 | wrong-requirement |

## Automated Checks

| Check | Result |
|---|---|
| `quire validate --scope <worktree> "spec/**/*.md"` | Exit 0. Zero errors. 27 grammar warnings on the in-scope artifacts. |
| Grammar summary | 🚧 14/20 docs grammar-clean (70%); `ears:non-singular` 20, `quality:agentless-passive` 7. |
| `ears:non-singular` | ❌ 20 flagged lines, plus 3 wrapped statements the line-based check misses (FND-102, FND-103). |
| `ears:vague-response` | ✅ zero. Two semantically unverifiable responses caught by reading (FND-107). |
| `ears:missing-subject` | ✅ zero flagged. Two statements name a non-actor subject (FND-104, FND-113). |
| `ears:non-canonical-trigger` | ✅ zero. No `On`/`Upon`/`After`/`During` anywhere; one `Until` state clause where the model repo writes `While` (FND-101). |
| `ears:unclassifiable` | ✅ zero. |
| `quality:agentless-passive` | ❌ 7: FR-004:59, FR-004:72, FR-005:49, FR-005:64, FR-006:38, FR-006:39, FR-006:50 (FND-106, FND-110, FND-111). |
| Unwanted-condition pattern | ✅ every stated unwanted condition uses `If … then … SHALL` (FR-002:55/57/58/66/69, FR-003:53, FR-004:59). |
| Modal present on every Behavior statement | ❌ FR-003:51 carries none (FND-105). |
| This review validates | ✅ `quire validate` on `spec/reviews/2-semantic-module-contract/ears-conformance.md` exits 0 with no structural error. |

## Posture Comparison

The comparison repo is the merged `agent-ix/spec-objects-business` migration,
measured with the same binary on the same day.

| Measure | spec-objects-safety (this branch) | spec-objects-business (merged) |
|---|---|---|
| Documents grammar-clean | 14/20 (70%) | 27/27 (100%) |
| Grammar findings | 27 | 0 |
| Lines carrying two or more `SHALL` | 20 | 0 |
| Agentless passives | 7 | 0 (every passive names its agent with `by …`) |
| Criteria property-extractable | 31/56 (55%) | 27/45 (60%) |
| EARS review on the record | this document | `spec/reviews/4-semantic-data-schemas/ears-conformance.md`, 16 findings, all dispositioned |

The model repo's cleanliness is not an accident of simpler content — its FR-002
is the same requirement as this one, at 29 `SHALL` to this module's 30 — it is
the residue of an EARS review that was run and applied before merge. Holding
this branch to the same bar is therefore asking for what the ecosystem already
did once, not for a new standard.

## Notes

- `--strict` would escalate all 27 warnings to a failing exit. That is the gate
  the model repo can pass today and this branch cannot; it is the cheapest way
  to keep the posture once FND-102 is applied.
- FR-004's Inputs table enumerates all seven vocabularies (`Severity`,
  `Likelihood`, `Exposure`, `Controllability`, `Detection`, `LifecycleStatus`,
  `EpistemicState`) with their members and lineage, and its lines 38-40 name the
  three advisory lint allow-lists. That table is what grounds FR-004-AC-6 and
  FR-004-AC-12 for this lens, and it is the vocabulary a grammar reading of
  those criteria depends on.
- FR-004's criteria run AC-1..AC-6, then AC-12, then AC-7..AC-11. Out of lens
  and harmless to the grammar, but a reader scanning for AC-12 will not find it
  where the sequence puts it.
- No spec artifact was edited by this review. Findings are reported for
  disposition by the branch author.
