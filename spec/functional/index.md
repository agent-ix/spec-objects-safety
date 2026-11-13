---
type: index
title: "Functional"
description: "Index of artifacts in this directory."
---
# Functional

## Contents

* [FR-001: The module declares hazard and failure_mode as separate object types](./FR-001-safety-object-types.md)
* [FR-002: Emit the module's JSON Schemas from a TypeSpec package importing semantic-core](./FR-002-emitted-json-schemas.md)
* [FR-003: Declare the semantic-module contract in the manifest](./FR-003-semantic-manifest-contract.md)
* [FR-004: Type-distinct safety schemas that keep unknown, not-assessed and not-applicable apart](./FR-004-type-distinct-safety-schemas.md)
* [FR-005: Ship the skeletons as executable typed fixtures with negative counterparts](./FR-005-executable-skeletons.md)
* [FR-006: Reference architecture, operational, security and assurance types without redeclaring them](./FR-006-cross-module-references.md)
* [FR-007: A mitigating document can declare a mitigates edge to a hazard or failure_mode](./FR-007-authorable-mitigates-edge.md)
* [FR-008: The hazard and failure-mode coverage checks report unmitigated objects and stay silent on mitigated ones](./FR-008-mitigation-coverage-findings.md)
* [FR-009: A safety-classified NFR that mitigates nothing is reported as unjustified scope](./FR-009-safety-nfr-needs-mitigation-target.md)
* [FR-101: An acceptability policy is a project-authored table of levels and the region each cell belongs to](./FR-101-acceptability-policy.md)
* [FR-102: A risk estimate's levels are checked against the policy's declared levels](./FR-102-estimate-levels-resolve-in-policy.md)
* [FR-103: A residual-risk record holds the post-control estimate, the decision, a rationale and the named decider](./FR-103-residual-risk-record.md)
* [FR-104: No tool computes, stores or defaults a score, a region verdict or an acceptance](./FR-104-no-computed-verdicts.md)
* [FR-105: The tooling reports where a recorded decision disagrees with the policy](./FR-105-decision-policy-discrepancy-report.md)
* [FR-106: A benefit-risk record links the risks, states the benefit and names the decider](./FR-106-benefit-risk-record.md)
* [FR-107: An overall residual-risk evaluation for the product is decided by a named person](./FR-107-overall-residual-risk-evaluation.md)
* [FR-201: The module declares harm as an object type](./FR-201-harm-object-type.md)
* [FR-202: A hazardous situation arises from a hazard and a harm arises from it](./FR-202-hazardous-situation-object-and-chain.md)
* [FR-203: A pre-control risk estimate records person-entered severity and probability for a hazardous situation](./FR-203-pre-control-risk-estimate.md)
* [FR-204: A post-control risk estimate names the controls it assumes](./FR-204-post-control-risk-estimate.md)
* [FR-205: A risk control links to the requirement that implements it and the verification that shows it is effective](./FR-205-control-requirement-and-verification-links.md)
* [FR-301: Every hazard reaches a harm through a hazardous situation, declared as manifest data](./FR-301-hazard-reaches-harm-through-situation.md)
* [FR-302: Every risk control is implemented by a requirement and has a verification, declared as manifest data](./FR-302-risk-control-implemented-and-verified.md)
* [FR-303: Every post-control estimate has a residual-risk record, and the decision and decider are enforced by the schema and the discrepancy report](./FR-303-residual-risk-decided-by-named-person.md)
* [FR-304: The causal chain from failure mode to harm is checked for cycles through the arises_from verb](./FR-304-chain-edges-cannot-cycle.md)
* [FR-305: A quoin risk summary report reads the whole chain and states what each person entered](./FR-305-risk-summary-report.md)
