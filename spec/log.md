---
type: log
title: "Update Log"
description: "Chronological log of structural changes to this bundle."
---
# Update Log

## History

* **2026-09-04** — migrated to the semantic-module contract (agent-ix/spec-objects-safety#2, Track A wave 4 of agent-ix/quoin#286). Manifest 0.2.0 → 0.3.0. The archetypes are now authored in TypeSpec importing `@agent-ix/semantic-core` 0.1.0 and emitted to fifteen JSON Schema 2020-12 documents under `spec_objects_safety/schemas/`; `data_schema` is the reference form `{schema, digest}` on both object types, and the manifest carries the quoin FR-070 `semantic` block. The skeletons became executable typed fixtures — a `## Properties` table with a `sysml` alternate and `## Invariants` `ocl` fences — with seven negative counterparts, each failing for its own stated reason.

  **The safety content of the change is the epistemic distinction.** Every scored axis — severity, likelihood, ISO 26262 exposure and controllability, FMEA detection — admits either its own ordinal scale or one of `unknown`, `not_assessed`, `not_applicable`. Those three share no member with any scale, so "nobody looked" cannot be sorted, scored or read as `negligible`, `E0`, `C0` or `none`. Nothing declares a `default` anywhere, and `status: accepted` requires a `provenance` naming who accepted the risk and when: schema validity is not a safety claim, and a document does not reach risk acceptance by validating.

  **[RAN]** The three advisory lint allow-lists were widened with the same three tokens. At 0.2.0 the only value that got past them was a scale value, so an author who had not scored an axis was nudged towards `negligible` or `none` — the exact collapse this module exists to prevent. Refusing the honest token was the defect; widening an advisory list to admit it is not a relaxation of the gate.

  **No new type, and no new verb.** A control, risk, asset, incident, interface or evidence record is named by `SemanticId` and never redeclared here — `spec-objects-security`, `spec-objects-architecture`, `spec-objects-operational` and `engineering-assurance` own those. `semantic.imports` stays `{}` with the reason in the manifest: the map pins imported semantic *packages* at exact versions and none of those four publishes a semantic contract yet (agent-ix/spec-objects-security#13, agent-ix/spec-objects-architecture#8, agent-ix/spec-objects-operational#6). An aspirational pin would be a claim about a contract that does not exist.

  The `traceability` model is unchanged fact for fact, and is asserted so. `spec-objects-security`'s hazard-coverage work reads it across the repository boundary, so changing a verb, a direction or an object type from this side would silently repoint a neighbour's coverage check.

  **[RAN]** The eight-review round found one thing worth more than the migration
itself: **the incoming `mitigates` edge these checks require is authorable
nowhere in the catalog.** `spec-objects-security`'s `control` declares
`mitigates: [threat, risk, vulnerability]` and the `spec-artifacts-iso`
`FR`/`NFR` archetypes declare no `mitigates` at all, so `unmitigated-hazard` —
the check this module exists for — cannot yet tell a mitigated hazard from an
unmitigated one. It is filed as agent-ix/spec-objects-safety#4 and NOT fixed
from this side: a neighbour reads this model across the repository boundary, and
NFR-001-AC-4 freezes it for that reason.

  The same round hardened three things in the schemas. Every record and value
model is now sealed twice — `unevaluatedProperties` is a 2020-12 keyword a
consumer on an older dialect ignores wholesale, which would admit a `Hazard`
carrying `analysis` while `required` and `enum` still failed closed, so
`additionalProperties: false` says the same thing in every dialect.
`status: accepted` now requires the `assessment` or `analysis` being accepted
alongside the `provenance`: an acceptance of nothing scored is the module's
central failure wearing a lifecycle state. And FR-004 now states the scale
members in the requirement rather than only in `typespec/main.tsp` — the claim
that `not_assessed` never reads as safe is a claim about exact member sets, so
the member sets belong where the claim is made. `Severity` is recorded as the
IEC 61508 / MIL-STD-882 four-band scale rather than ISO 26262 `S0..S3`, and no
ASIL is derivable from it or claimed.

  Two upstream defects are carried as strict expected failures rather than worked around: a manifest refusal that names nothing (agent-ix/quire-rs#221, #394) and a legacy prose `## Properties` block that errors as well as warning under `legacy_forms: warning` (agent-ix/quire-rs#391). The FR-035 gate runs against the module-manifest schema at `spec-artifacts-iso` CR-012 because no release carries it (agent-ix/spec-artifacts-iso#36, filed here); a drift test proves the pinned copy is the released schema plus exactly the CR-012 pointers, and fails the moment a release makes the pin unnecessary. FR-001-AC-1's "at least one role" half contradicts FR-001's own body and is filed as agent-ix/spec-objects-safety#3 rather than edited here.


* **2026-08-18** — module minted (agent-ix/spec-objects-security#7, ADR-0011 P2 wave B). Two object types, `hazard` and `failure_mode`, in their own module rather than as an extension of `spec-objects-security`. Two reasons, and the second decided it: the lineage is IEC 61508 / ISO 26262 / FMEA rather than STRIDE, so merging would make one module's applicability signals answer for two regulatory domains; and **[RAN]** across the ecosystem, only `spec-artifacts-iso` and `spec-artifacts-process` run the FR-035 manifest-schema gate — the five `spec-objects-*` repositories and `spec-artifacts-app` do not, so a new key in any of them ships unvalidated. A new repository lets the gate arrive **with** the module instead of being retrofitted, and it does: `test_manifest_validates_against_fr035_schema` is green on the first commit, with no skip and no escape hatch.

  `hazard` and `failure_mode` are separate types, not one type with a variant. A failure mode answers "what breaks"; a hazard answers "what state must never be reached", and the second is not derivable from the first — which is the reason STPA exists, since components each behaving exactly as specified can still interact into a harmful state. Their tables differ for the same reason: FMEA scores effect/cause/detection, hazard analysis scores severity/likelihood, and collapsing them would force one table to mean two things.

  `Mitigation` on a hazard is optional deliberately. An identified-but-unmitigated hazard is a real and reportable state; requiring the section would push authors to write a placeholder rather than leave the gap visible.

  The lexicon is asserted structurally from day one — `{definition: <text>}` and nothing else — because of the defect it prevents: an unquoted comma inside a YAML flow mapping is read as an entry separator, which silently truncated two definitions in `spec-objects-security` (#6). Every definition here is quoted.

  **No new verbs, and that is the finding.** The ticket assumed safety-chain verbs `causes` and `contributes_to` would be added to the iso vocabulary. Applying that vocabulary's own first criterion for an addition — *"check the existing 76; a near-synonym is a reason not to add"* — says otherwise: `arises_from` ("Risk arises from a threat/vulnerability") records exactly the fact `causes` would, read from the hazard end, which is also the natural authoring direction. A hazard arising from several failure modes is several `arises_from` edges, so `contributes_to` would be a second word for the same thing. The first draft of this module declared both verbs plus a `safety-relevant` role, and `quire validate` reported three `UnknownEdgeType`/`UnknownRole` advisories — the correct signal, and the prompt to apply the criteria rather than extend the vocabulary to match what had been written. TC-007 now fails if a future edit reaches for a verb the iso vocabulary lacks.
