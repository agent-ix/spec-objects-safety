---
type: log
title: "Update Log"
description: "Chronological log of structural changes to this bundle."
---
# Update Log

## History

* **2026-08-18** — module minted (agent-ix/spec-objects-security#7, ADR-0011 P2 wave B). Two object types, `hazard` and `failure_mode`, in their own module rather than as an extension of `spec-objects-security`. Two reasons, and the second decided it: the lineage is IEC 61508 / ISO 26262 / FMEA rather than STRIDE, so merging would make one module's applicability signals answer for two regulatory domains; and **[RAN]** across the ecosystem, only `spec-artifacts-iso` and `spec-artifacts-process` run the FR-035 manifest-schema gate — the five `spec-objects-*` repositories and `spec-artifacts-app` do not, so a new key in any of them ships unvalidated. A new repository lets the gate arrive **with** the module instead of being retrofitted, and it does: `test_manifest_validates_against_fr035_schema` is green on the first commit, with no skip and no escape hatch.

  `hazard` and `failure_mode` are separate types, not one type with a variant. A failure mode answers "what breaks"; a hazard answers "what state must never be reached", and the second is not derivable from the first — which is the reason STPA exists, since components each behaving exactly as specified can still interact into a harmful state. Their tables differ for the same reason: FMEA scores effect/cause/detection, hazard analysis scores severity/likelihood, and collapsing them would force one table to mean two things.

  `Mitigation` on a hazard is optional deliberately. An identified-but-unmitigated hazard is a real and reportable state; requiring the section would push authors to write a placeholder rather than leave the gap visible.

  The lexicon is asserted structurally from day one — `{definition: <text>}` and nothing else — because of the defect it prevents: an unquoted comma inside a YAML flow mapping is read as an entry separator, which silently truncated two definitions in `spec-objects-security` (#6). Every definition here is quoted.

  **No new verbs, and that is the finding.** The ticket assumed safety-chain verbs `causes` and `contributes_to` would be added to the iso vocabulary. Applying that vocabulary's own first criterion for an addition — *"check the existing 76; a near-synonym is a reason not to add"* — says otherwise: `arises_from` ("Risk arises from a threat/vulnerability") records exactly the fact `causes` would, read from the hazard end, which is also the natural authoring direction. A hazard arising from several failure modes is several `arises_from` edges, so `contributes_to` would be a second word for the same thing. The first draft of this module declared both verbs plus a `safety-relevant` role, and `quire validate` reported three `UnknownEdgeType`/`UnknownRole` advisories — the correct signal, and the prompt to apply the criteria rather than extend the vocabulary to match what had been written. TC-007 now fails if a future edit reaches for a verb the iso vocabulary lacks.
