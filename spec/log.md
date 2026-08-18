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

  Safety-chain edge verbs (`causes`, `contributes_to`) are declared in this module's `allowed_links` but are **not yet in the iso vocabulary**: that addition waits on `spec-artifacts-iso` FR-004 documenting the vocabulary, so it has a rule to satisfy rather than a precedent to set. `mitigates`/`controls` reuse the existing governance cluster rather than gaining safety-only synonyms.
