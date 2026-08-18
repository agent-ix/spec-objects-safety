---
id: HAZ-001
title: "Vehicle cannot decelerate on operator command"
type: hazard
---
<!-- hazard authoring skeleton (spec-objects-safety). Fill every section with
     substantive content. Contract (manifest body_extraction):
     - Frontmatter MUST carry id, title, and type: hazard.
     - "## Condition" (H2) is REQUIRED.
     - "## Assessment" (H2) is REQUIRED: a table with headers exactly
       Severity | Likelihood | Rationale and at least one data row.
     - "## Mitigation" (H2) is OPTIONAL.
     - Keep headings unique per level; never leave a section empty.

     WRITE THE CONDITION AS A STATE, NOT AN EVENT. "The brakes fail" is a
     failure mode wearing a hazard's name. "The vehicle cannot decelerate on
     operator command" is a state, and it stays true regardless of which
     failure produced it — which is what lets several failure modes link to
     one hazard, and what lets a hazard exist with no failure behind it at
     all. STPA exists because components each behaving exactly as specified
     can still reach a harmful state together.

     SEVERITY is how bad the harm is if the state is reached:
       negligible | marginal | critical | catastrophic
     LIKELIHOOD is how often the state is expected to be reached:
       incredible | improbable | remote | occasional | probable | frequent
     Both are checked by lint rules (`quire lint`). If you work to a specific
     standard, map its scale onto these buckets rather than adding a column.

     MITIGATION IS OPTIONAL ON PURPOSE. An identified-but-unmitigated hazard
     is a real and reportable state. Requiring the section would make authors
     write a placeholder instead of leaving the gap visible. -->

## Condition

<!-- The system state or condition that can lead to harm. A state, not an
     event, and not the failure that causes it. -->

## Assessment

| Severity | Likelihood | Rationale |
| -------- | ---------- | --------- |
| critical | remote     | <why these two values, in one line> |

## Mitigation

<!-- What prevents the state being reached, or limits harm once it is. Link to
     the requirements that carry it with `mitigates` / `controls`. Omit this
     whole section if nothing mitigates it yet — that absence is the finding. -->
