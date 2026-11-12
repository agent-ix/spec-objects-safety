---
id: SR-013
title: "Dependency analysis of the authorable mitigates edge (PR #30)"
type: SpecReview
analysis: dependency
scope: "agent-ix/spec-objects-safety; spec/functional/FR-007-authorable-mitigates-edge.md, spec/functional/FR-008-mitigation-coverage-findings.md"
review_set: subset
---
# Dependency analysis of the authorable mitigates edge (PR #30)

## Summary

Ticket: PLAT-1407. Checked every upstream FR-007 and FR-008 rely on against
quire-rs origin/main (05afc40, 0.56.1), quire-cli origin/main (7c78592,
0.40.1), and spec-objects-security.

quire-rs already specifies the behaviour FR-007-AC-3 wants at engine level:
FR-038's `Strict` bundle posture makes a dangling reference an error
(`dangling-reference`). FR-026 is the resolver and correctly only records
`Dangling` without failing construction; it is not where this belongs.
quire-cli exposes no path to the Strict posture: FR-004 per-file validation
does no edge resolution, FR-014 `--okf` maps to `BundlePosture::Okf` where a
dangling reference is a warning with exit 0, and FR-004 `--strict` does not
compose with `--okf` (measured exit 0). Neither spec requires the diagnostic to
name the source file path. FR-038-AC-9 also skips absent targets under a
foreign `ix://` authority, so AC-3 holds only for a bare id or an own-authority
target.

The missing requirement belongs in quire-cli, with a small quire-rs AC on the
finding: (1) quire-cli: when `quire validate --okf` runs with `--strict`, a
`dangling-reference` for a target that is a bare id or under the bundle's own
authority SHALL make the command exit non-zero, as FR-004 `--strict` already
does for per-file warnings; (2) quire-rs FR-038: a `dangling-reference`
finding SHALL carry the source document's path in `BundleFinding.path`, and
its message SHALL name the edge type and the unresolved target id, with the
CLI printing that path.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-007 depends on an exit-failing dangling-reference mode in quire-cli that no quire-cli or quire-rs requirement specifies, and its Dependencies list names no quire upstream | spec/functional/FR-007-authorable-mitigates-edge.md:71 |
| FND-002 | low | FR-007's upstream spec-objects-security FR-007 exists only on unmerged spec-objects-security#39; the two PRs must land together or security first | spec/functional/FR-007-authorable-mitigates-edge.md:73 |

## Verdict

FAIL on FND-001. This PR may merge before the quire-cli implementation exists,
since a spec states the target design, but not before the quire-cli requirement
is specified and FR-007 names it as an upstream dependency. PLAT-1407 already
lists quire-rs and quire-cli as repos for this spec ticket.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | e06668b adds depends_on edges and Upstream entries for quire-cli FR-014-AC-11 and quire-rs FR-038-AC-11 (open PRs quire-cli#167 and quire-rs#646) |
| FND-002 | fixed | e06668b states spec-objects-security FR-007 "must land first or together" and adds a depends_on edge to it |
