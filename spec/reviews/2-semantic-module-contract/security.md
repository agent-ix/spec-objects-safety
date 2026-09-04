---
id: SR-009
title: "Security and functional-safety compliance analysis of the issue #2 semantic-module contract"
type: SpecReview
analysis: integrity
scope: "spec/spec.md, spec/functional/FR-001..FR-006, spec/non-functional/NFR-001, spec/tests.md, typespec/main.tsp, spec_objects_safety/manifest.yaml, spec_objects_safety/schemas/, scripts/generate-schemas.mjs, scripts/stage-npm.mjs"
review_set: subset
---
# Security and functional-safety compliance analysis of the issue #2 semantic-module contract

## Summary

Compliance traceability for `agent-ix/spec-objects-safety#2`, run over the
specification and the implementation it describes. The module processes no
personal data at scale, exposes no network surface, authenticates nobody and
stores no secret, so the conventional application-security standards apply only
at their supply-chain and integrity edges. Two other bodies of standards apply
squarely and are the reason this analysis is not a formality:

1. **Functional safety** (IEC 61508, ISO 26262). This module is the schema for
   hazard and failure-mode records — the artifacts a safety case is built from.
   IEC 61508-3 §7.4.4 and ISO 26262-8 clause 11 additionally classify the
   TypeSpec compiler, the JSON-Schema emitter and the Quire engine as *offline
   support tools* whose defects propagate into safety artifacts.
2. **Supply-chain integrity** (NIST SR/SI/SA families, ISO 27001 A.8.2x–A.8.3x,
   SOC 2 CC8/CC9). FR-002 builds a real integrity chain — TypeSpec source →
   emitted bytes → `sha256` in `toolchain.json` → `data_schema.digest` in the
   manifest — and this review asks what enforces it and where it stops.

Seventeen findings follow: five high, seven medium, five low. The highs are one
theme with four faces — **the integrity chain FR-002 constructs is enforced by
nothing except a developer's own terminal, and both ends of it fail open**.
Nothing here disputes the module's safety modelling, which is the strongest part
of the bundle: `EpistemicState` is a genuine control against the
unassessed-reads-as-safe collapse, and FR-004-CON-2 ("schema validity is not a
safety claim") is the correct posture stated explicitly.

The base review (`base.md`) is not restated. Where a finding touches something it
raised, it says so and adds only the compliance dimension.

## Verdict

**CONDITIONAL** — FND-001..FND-005 must be dispositioned before this contract is
published to a consumer. Each is a stated fact of the current design rather than
a defect discovered in it; what is missing is a requirement that owns the risk.
No spec artifact, schema, script or manifest was edited by this review.

## Applicable Standards

### Functional-safety standards (domain-specific; the reason this module exists)

| Standard | Clauses that bear | Why it applies here |
|---|---|---|
| IEC 61508-1 | §6 (management of functional safety, competence), §7.4 (hazard and risk analysis), §7.5–7.6 (safety requirements and SIL allocation), §7.16 (functional safety assessment) | The `hazard` record and its `Assessment` table are the E/E/PE hazard-and-risk-analysis output; `Severity`/`Likelihood` are its frequency-and-consequence bands. |
| IEC 61508-3 | §7.4.4 (software tool support; T1/T2/T3 classification of offline support tools) | The emitter writes the schema that decides whether a safety record is valid. It is a T2-class tool by function. |
| ISO 26262-3 | §6 (hazard analysis and risk assessment; ASIL determination from S, E, C) | `Exposure` (E0–E4) and `Controllability` (C0–C3) are lifted verbatim from this clause. |
| ISO 26262-2 | §6.4.9 (confirmation measures), §5 (safety culture, roles) | `Provenance.assertedBy` and `LifecycleStatus: accepted` are the record of who confirmed what. |
| ISO 26262-8 | clause 11 (confidence in the use of software tools; TCL/TD), clause 6 (change management), clause 9 (verification) | Same tool-qualification obligation as IEC 61508-3 §7.4.4, plus the change control FR-002's bump procedure describes. |
| FMEA / STPA (methods, not certifiable standards) | — | The `Analysis` triple and the deliberate absence of a "≥ 1 cause" rule on `Hazard.relations`. |

### Mandatory security and privacy standards (applied per the analysis catalog)

| Standard | Version | Scope applied to this component | Region |
|---|---|---|---|
| AICPA SOC 2 | 2017 TSC | CC3 (risk identification), CC4 (monitoring), CC6.1 (secrets in the build), CC7.1–CC7.2 (integrity monitoring, evidence), CC8.1 (change management), CC9.2 (vendor/supply chain), A1.2 (availability of the validation path) | Global |
| ISO/IEC 27001 | 2022 | A.5.17, A.5.19–A.5.20, A.5.33, A.8.8, A.8.15–A.8.16, A.8.24, A.8.25–A.8.26, A.8.28–A.8.32 | Global |
| NIST SP 800-53 | Rev 5 | AU-9, AU-10; CM-2, CM-3, CM-14; IA-5; RA-3, RA-5; SA-10, SA-11, SA-15; SC-8, SC-12, SC-13, SC-24; SI-7, SI-10; SR-3, SR-4, SR-11 | US Federal |
| OWASP ASVS | 5.0.0 | V2 (Validation and Business Logic), V12 (Secure Communication), V13 (Configuration), V14 (Data Protection), V15 (Secure Coding and Architecture), V16 (Security Logging and Error Handling). V3–V11 do not apply: no frontend, no API, no session, no authentication, no authorization, no token, no cryptographic protocol implemented here. | Global |
| EU GDPR | 2016/679 | Art. 5(1)(c), Art. 17, Art. 25, Art. 30, Art. 32 — reachable only through `Provenance.assertedBy`, which is designed to name a person and is published. | EU/EEA |

Chapter-level ASVS citations are used deliberately; sub-requirement numbers are
not quoted where they could not be verified against the 5.0.0 source.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | high | **The integrity chain is enforced only on a developer's machine.** FR-002 builds source → bytes → `toolchain.json` digest → `data_schema.digest`, and `make lint` → `schemas-check` is its gate. No automated pipeline runs it: `ci.yml` is `on: workflow_dispatch` only and its reusable `lib-ci.yml` call installs no Node toolchain, and `release-npm.yml` delegates to a reusable that is publish-only by design ("no build or test toolchain, so this is a publish-only reusable"). FR-002-CON-4 records the cause — the toolchain resolves through a user-level npm config no runner has — but states it as a packaging fact, not as a residual risk with an owner. Net: between a developer's terminal and a published npm tarball, nothing verifies that the shipped `Hazard.json` is the compiled `typespec/main.tsp`, that a digest matches its bytes, or that a schema was not hand-edited (FR-002-CON-1 is `Inspection`-verified). `base.md` FND-008 saw the same collision as a spec inconsistency; the compliance defect is the unowned enforcement gap behind it. Standards: NIST SI-7, SA-10, SA-11, CM-3; ISO A.8.29, A.8.32; SOC2 CC8.1, CC7.1; ASVS V13. | FR-002 Behavior, FR-002-CON-1, FR-002-CON-4, `.github/workflows/ci.yml`, `.github/workflows/release-npm.yml`, `pyproject.toml` `[tool.poe.tasks.lint]` | missing-requirement |
| FND-002 | high | **Two build inputs are fetched over plaintext HTTP, one with certificate checking explicitly disabled.** `package-lock.json` resolves `@agent-ix/semantic-core` from `http://npm.ix/@agent-ix/semantic-core/-/semantic-core-0.1.0.tgz`, and `[tool.poe.tasks.dev-quire]` runs `pip install --index-url http://pypi.ix/root/dev/+simple/ --trusted-host pypi.ix 'quire>=0.46.0'`. The npm side carries a `sha512` integrity hash, which detects tampering after the fact; the pip side has **no hash pinning, no TLS and an explicit `--trusted-host`**, and what it installs is the engine that decides whether a hazard document validates, at a floating `>=0.46.0`. The committed lockfile URL is also why no CI runner can `npm ci` — it is the mechanism behind FND-001 — and it is asserted as correct by TC-024, which pins the internal host into the test suite. Introduced by this branch. Standards: NIST SC-8, SC-12, SC-13, SR-11, SI-7; ISO A.8.24, A.5.19; ASVS V12, V13; SOC2 CC9.2. | `package-lock.json:19`, `pyproject.toml` `[tool.poe.tasks.dev-quire]`, `Makefile` `dev-quire`, `tests/test_schema_emission.py:249-261` | missing-requirement |
| FND-003 | high | **No tool-qualification argument for a toolchain that is safety-relevant by function.** IEC 61508-3 §7.4.4 and ISO 26262-8 clause 11 require, for offline support tools whose output enters a safety artifact, a classification (T1/T2/T3, or TI/TD → TCL) and either qualification evidence or a stated tool-error detection measure. Three tools qualify here: `@typespec/compiler` 1.15.0 and `@typespec/json-schema` 1.15.0 (they write the rules a hazard record is judged by) and Quire 0.46.0 (it applies them). The spec pins all three at exact versions and records them in `toolchain.json` — good configuration control, and the necessary precondition — but no requirement states what a defect in the emitter would do to a safety record, what detects it, or why the official emitter (FR-002-CON-1) is a sufficient argument. Sourcing is not qualification. Determinism (FR-002-CON-3) proves the tool is repeatable, not that it is right. Standards: IEC 61508-3 §7.4.4; ISO 26262-8 cl.11, cl.9; NIST SA-15, SI-7; ISO A.8.25, A.8.30. | FR-002 Inputs, FR-002-CON-1, FR-002-CON-3, FR-005 Inputs, `spec_objects_safety/schemas/toolchain.json` | missing-requirement |
| FND-004 | high | **No safety integrity level, and a severity scale that cannot produce one.** `Exposure` (`E0..E4`) and `Controllability` (`C0..C3`) are ISO 26262-3 verbatim, but `Severity` is the four-band `negligible/marginal/critical/catastrophic` scale of the IEC 61508 / MIL-STD-882 lineage — ISO 26262-3 determines ASIL from S0–S3 × E0–E4 × C0–C3. So a record that fills every ISO 26262 axis this module offers still cannot yield an ASIL, and FR-004's Inputs table claims an "IEC 61508 / ISO 26262 harm severity" lineage for a severity scale ISO 26262 does not define. There is also no `asil`, `sil` or equivalent integrity-level field anywhere in the module, and no mapping to one — yet the integrity level is what every downstream rigor obligation (verification depth, independence of review, architectural measures) is allocated against in both standards. `spec.md` Out of Scope names fourteen exclusions and this is not among them, so it reads as covered when it is absent. Standards: ISO 26262-3 §6.4.3; IEC 61508-1 §7.5–7.6; NIST RA-3; SOC2 CC3.2. | FR-004 Inputs (vocabulary table), `typespec/main.tsp` `Severity`/`Exposure`/`Controllability`, `spec.md` Out of Scope | missing-requirement |
| FND-005 | high | **Both integrity mechanisms that protect a consumer fail open, silently.** A `data_schema` digest mismatch drops that object type with no diagnostic (`agent-ix/quire-rs#394`); an unparseable manifest key empties the whole module, so a consumer sees it as absent (`agent-ix/quire-rs#221`). FR-003 Behavior states both precisely and honestly, and TC-032 carries them as expected failures — but the consequence is not recorded as a security property: a corrupted or substituted schema does not refuse a hazard document, it makes hazard documents **unvalidated and unremarked**. That is the fail-open direction, on the one control that binds a shipped schema to its bytes. The module declares no compensating measure of its own (no fail-secure posture requirement, no startup self-check, no NFR on refusal behaviour), and the engine issues are recorded as someone else's defect rather than as this module's residual risk. Standards: NIST SI-7(5), SC-24, AU-5; ISO A.8.16; SOC2 CC7.2; IEC 61508-1 §7.4. | FR-003 Behavior, FR-003-AC-6, `spec.md` Out of Scope, `spec/tests.md` TC-032 | missing-requirement |
| FND-006 | medium | **Every grammar `$ref` ships unresolvable.** All ten semantic-core references point at `https://schemas.agent-ix.org/semantic-core/0.1.0/<Model>.json`; that host does not resolve in DNS today, and no copy of those schemas ships in the wheel, the sdist or the npm tarball. FR-002 Inputs states the three npm packages are build inputs and that "the published artifact is Markdown and JSON, so none is a runtime dependency of a consumer" — but a consumer validating a record must resolve those refs, so it must either install `@agent-ix/semantic-core` (a runtime dependency the spec says does not exist) or dereference a URL. Two consequences: validators differ on an unresolvable `$ref` — several skip it, i.e. fail open on exactly the grammar items — and whoever registers `schemas.agent-ix.org` later controls how safety records validate for anyone who does resolve it. The repo's own tests avoid the problem with a local `referencing.Registry` (`tests/conftest.py:255-283`), which is the right answer and is nowhere stated as a consumer obligation. Standards: NIST SI-7, SC-8, SR-4; ISO A.8.24; ASVS V13, V15. | `spec_objects_safety/schemas/*.json`, FR-002 Inputs, FR-002-AC-3, `tests/conftest.py:255-283` | missing-requirement |
| FND-007 | medium | **The published artifact carries no provenance attestation.** The npm release path sets `provenance=false` (the shared reusable does so because agent-ix repos are private and npm cannot attest from them), so the digest chain FR-002 builds ends at a developer's disk: nothing binds the published tarball to a commit, a builder or a workflow run. Combined with FND-001 (no CI verification) a consumer installing `@agent-ix/spec-objects-safety` has no mechanism to establish that the schemas it validates hazards against are the ones this repository compiled. Standards: NIST SR-4, CM-14, SA-10; ISO A.8.30, A.5.20; SOC2 CC9.2. | `.github/workflows/release-npm.yml`, `nodejs-actions/.github/workflows/release-npm-module.yml` | missing-requirement |
| FND-008 | medium | **Risk-acceptance attribution is nominal, not accountable.** `Provenance.assertedBy` is `type: string, minLength: 1` — `"x"` satisfies it, and TC-042 uses exactly that. `assertedAt` relies on `format: date-time`, which is an annotation and not an assertion under 2020-12 unless a validator is configured with a format checker; the suite never asserts that a malformed timestamp is refused, so a record with `assertedAt: "yesterday"` validates. Nothing binds either to an authenticated identity or a signature. FR-004's rule that `status: accepted` requires `provenance` is therefore a rule that risk acceptance carries a *name-shaped string*, and the non-repudiation property the schema description claims ("risk acceptance with nobody's name on it is the one status that must never be reachable") is not the property enforced. IEC 61508-1 §6 and ISO 26262-2 §6.4.9 both hang on identifiable, competent parties. Standards: NIST AU-10, AU-9, SI-10; ISO A.8.15, A.5.33; SOC2 CC7.2; IEC 61508-1 §6.2; ISO 26262-2 §6.4.9. | `spec_objects_safety/schemas/Provenance.json`, FR-004 Behavior, `spec/tests.md` TC-042 | wrong-requirement |
| FND-009 | medium | **Only one of four consequential dispositions requires provenance.** The `if/then` rule fires on `status: accepted` alone. `transferred` (the risk is now another party's, and who agreed is unrecorded), `closed` (the hazard is no longer tracked) and `mitigated` (a claim that something addresses it) each carry no `provenance` and no required `EvidenceRef`. Closure and transfer without an asserter are the two states an auditor reconstructing a safety case cannot verify, and `mitigated` with no evidence reference is a claim with nothing behind it — while `EvidenceRef` exists in the module precisely for this. Distinct from the base review's note that `LifecycleStatus` transitions are untested: the gap here is that no requirement asks for the obligation at all. Standards: IEC 61508-1 §7.16; ISO 26262-2 §6.4.9; NIST AU-10; ISO A.5.33; SOC2 CC4.1. | `spec_objects_safety/schemas/Hazard.json` `allOf`, FR-004 Behavior, `EvidenceRef.json` | missing-requirement |
| FND-010 | medium | **"Non-empty" is `minLength: 1`, so a single space satisfies every mandatory judgement field.** `rationale`, `assertedBy`, `effect`, `cause` and `situation` are all `minLength: 1` with no pattern. FR-004 Behavior requires "a non-empty `rationale`" and the schema description explains that an unscored backlog is indistinguishable from no analysis — but `" "`, `"-"` and `"TBD"` all pass, and `rationale` is the single field standing between a scored hazard and an unexplained one. TC-039 tests `rationale: ""` only. A `pattern` requiring a non-whitespace character (and a sensible `minLength` on `rationale`) closes it. Standards: NIST SI-10; ASVS V2; ISO A.8.26. | `HazardAssessment.json`, `FailureAnalysis.json`, `Provenance.json`, `HazardContext.json`, FR-004 Behavior, `spec/tests.md` TC-039 | wrong-requirement |
| FND-011 | medium | **The seal depends on a keyword an older validator silently ignores.** Every model closes with `unevaluatedProperties: {"not": {}}`. That keyword is 2019-09+; a consumer validating with a Draft-07 validator ignores it as unknown, and with it every forbidden-key property the module's type distinctness rests on — a hazard carrying `analysis` or `operations`, a failure mode carrying `assessment`, a record carrying `controls` — is admitted. FR-004-AC-1/AC-3/AC-4 all verify on that seal. Each schema declares `$schema: .../draft/2020-12/schema`, which announces the dialect but does not enforce that a consumer honours it, and no requirement states a minimum validator dialect as a consumer obligation. Standards: NIST SI-10, SI-7; ASVS V2, V15; ISO A.8.26. | `spec_objects_safety/schemas/*.json`, FR-004-AC-1, FR-004-AC-3, FR-004-AC-4 | missing-requirement |
| FND-012 | medium | **The strict schemas are unreachable for every document authored today, leaving an advisory lint as the only check.** `spec.md` Out of Scope states that no extractor maps the `Assessment` and `Analysis` tables into records (`agent-ix/quoin#335`, pending `quire-rs`), so `assessment`, `analysis`, `status` and `provenance` are optional and are verified against hand-built records. In practice, then, the only thing inspecting a `Severity` cell in a real hazard document is `lint_rules.hazard-severity` — declared advisory, "never blocks validation, extraction or sync". The module's headline safety property (an unassessed axis never reads as a safe one) is currently carried by a non-blocking advisory. The dependency is stated honestly and every blocking ticket is named; what is missing is the residual-risk record and a requirement that the strict path becomes mandatory when the extractor lands. Standards: NIST RA-3, SI-7; SOC2 CC3.2, CC4.1; IEC 61508-1 §7.4. | `spec.md` Out of Scope, `manifest.yaml` `lint_rules`, FR-004 Behavior | correct-requirement-no-evidence |
| FND-013 | low | **GDPR reachability sits entirely in `assertedBy`.** The field is designed to name whoever asserted a safety judgement — a natural person in the ordinary case — and this artifact is published to public npm (`publishConfig.access: public`) and to a git history. Art. 17 erasure against a published immutable tarball is not achievable, so the correct control is minimisation at the point of design: require a role or team identifier (the repo's own fixture uses `"safety-board"`, which is exactly right) rather than a personal name, and say so in the requirement. Nothing in FR-004 or the schema description does. Standards: GDPR Art. 5(1)(c), 25(2), 17, 32; NIST PT-3?/SI-12 (minimisation); ISO A.5.34. | `Provenance.json`, `package.json` `publishConfig`, `tests/test_record_schemas.py:68` | missing-requirement |
| FND-014 | low | **A GCP service-account key is base64-transformed into a step output.** `ci.yml` pipes `${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}` through `base64 -w 0` inside an `echo` that appends to `$GITHUB_OUTPUT`. GitHub masks a registered secret's literal value; a base64 encoding of it is a different string and is **not** masked, and it is persisted as a step output for the rest of the job. The secret is also interpolated into the shell script body rather than passed via `env:`. Pre-existing cookiecutter boilerplate — not introduced by this branch — and recorded because the same workflow is the publish path for the module. Standards: NIST IA-5, SC-28, AU-9; ISO A.5.17, A.8.31; SOC2 CC6.1. | `.github/workflows/ci.yml:10-13` | correct-requirement-no-evidence |
| FND-015 | low | **No dependency-vulnerability monitoring for the Node toolchain.** No `npm audit` step, no Dependabot or renovate configuration, and the only CI is manual-dispatch. The lockfile carries ~1,000 transitive packages for the emitter. Impact is bounded (build-time only, no runtime dependency, and the emitted artifact is data) which is why this is low, but FND-001 means a compromised build dependency's output would also reach a published tarball unverified. Standards: NIST RA-5, SR-3; ISO A.8.8; SOC2 CC7.1. | `package-lock.json`, `.github/workflows/ci.yml` | missing-requirement |
| FND-016 | low | **The staging script leaves the repository in a broken-validation state on an interrupted pack.** `scripts/stage-npm.mjs` copies `manifest.yaml`, `schemas/` and `skeletons/` to the repository root and relies on `postpack --clean` to remove them; the script's own comment records that a leftover root `manifest.yaml` makes Filament tooling discover the repo root as a second module and `quire validate` then fail with "no archetype registered". Any interrupted or failed `npm pack` leaves that state behind, and TC-018 asserts the clean state rather than making it unreachable. A `try/finally` in the pack path, or staging into a temporary directory, removes the window. Standards: NIST CM-2, SI-7; SOC2 A1.2; ISO A.8.32. | `scripts/stage-npm.mjs`, `spec/tests.md` TC-018 | wrong-requirement |
| FND-017 | low | **The digest chain records no algorithm agility and no signature.** `toolchain.json` and every `data_schema.digest` use SHA-256, which is correct today; nothing records the algorithm as a versioned choice or provides a path to change it, and no signature covers `manifest.yaml` itself — the file that carries the digests. A tampered manifest with recomputed digests is self-consistent and indistinguishable from a genuine one, which is the gap `provenance` (FND-007) would otherwise close. Standards: NIST SC-12, SC-13, SI-7, CM-14; ISO A.8.24; ASVS V11. | `scripts/generate-schemas.mjs`, `spec_objects_safety/schemas/toolchain.json`, `manifest.yaml` | missing-requirement |

## Compliance Standards Traceability

### Targeted standards

The table under **Applicable Standards** above is the 19.1 content: five
mandatory security and privacy standards, applied at their supply-chain,
integrity and data-protection edges, plus five functional-safety standards that
apply to the domain this module models and to the toolchain that builds it.

### Control mapping

Controls are grouped by functional area. A `—` in the requirement column is a
gap, and every gap names the finding that records it.

**Artifact and configuration integrity**

| Control | Standard | Control name | Module requirement |
|---|---|---|---|
| SI-7 | NIST 800-53 | Software, Firmware, and Information Integrity | FR-002 Behavior (digest chain), FR-002-AC-4, FR-002-AC-9, FR-003-AC-2 — enforcement gap FND-001, fail-open FND-005 |
| CM-2 | NIST 800-53 | Baseline Configuration | FR-002-AC-1, `toolchain.json`; NFR-001-AC-1 (0.2.0 locator baseline) |
| CM-3 | NIST 800-53 | Configuration Change Control | FR-002 Behavior (atomic bump procedure), FR-002-CON-5, FR-002-AC-8 |
| CM-14 | NIST 800-53 | Signed Components | — (FND-007, FND-017) |
| SA-10 | NIST 800-53 | Developer Configuration Management | FR-002-CON-1, FR-002-CON-3 — not enforced in any pipeline (FND-001) |
| SA-11 | NIST 800-53 | Developer Testing and Evaluation | `spec/tests.md` TM-001; TC-015, TC-019, TC-020, TC-021 |
| SA-15 | NIST 800-53 | Development Process, Standards, and Tools | FR-002 Inputs (exact pins) — no tool qualification (FND-003) |
| A.8.32 | ISO 27001 | Change management | FR-002 Behavior, FR-002-CON-5, NFR-001 |
| A.8.29 | ISO 27001 | Security testing in development and acceptance | `spec/tests.md`; gate is developer-local (FND-001) |
| CC8.1 | SOC 2 | Change management | FR-002-AC-8, NFR-001-AC-1..AC-5 |
| V13 | ASVS 5.0 | Configuration | FR-002-CON-2 (no `.npmrc`, no `file:`/`link:`, exact pins), FR-002-CON-4 |

**Supply chain**

| Control | Standard | Control name | Module requirement |
|---|---|---|---|
| SR-3 | NIST 800-53 | Supply Chain Controls and Processes | FR-002 Inputs, FR-002-CON-4 — no vulnerability monitoring (FND-015) |
| SR-4 | NIST 800-53 | Provenance | `toolchain.json` (build-side) — no published attestation (FND-007) |
| SR-11 | NIST 800-53 | Component Authenticity | lockfile `integrity` hashes — plaintext transport and unhashed pip install (FND-002) |
| SC-8 | NIST 800-53 | Transmission Confidentiality and Integrity | — (FND-002, FND-006) |
| SC-12 / SC-13 | NIST 800-53 | Key Establishment / Cryptographic Protection | SHA-256 over emitted bytes (FR-002 Outputs) — no agility, no signature (FND-017) |
| A.5.19 / A.5.20 | ISO 27001 | Supplier relationships / Addressing security in supplier agreements | FR-002 Inputs; `semantic.imports` discipline (FR-006-CON-2) |
| A.8.24 | ISO 27001 | Use of cryptography | FR-002 Outputs (`sha256:` digests) — FND-002, FND-017 |
| A.8.30 | ISO 27001 | Outsourced development | `release-npm.yml` delegation to `nodejs-actions` — FND-007 |
| CC9.2 | SOC 2 | Vendor and business partner risk | FR-002-CON-4, FR-006 Behavior (`imports` pinned only when published) |
| V12 | ASVS 5.0 | Secure Communication | — (FND-002) |

**Validation, input rules and fail-safe behaviour**

| Control | Standard | Control name | Module requirement |
|---|---|---|---|
| SI-10 | NIST 800-53 | Information Input Validation | FR-004 Behavior (required/forbidden keys, closed enums), FR-004-AC-1..AC-12, FR-005-AC-5 — weakened by FND-010, FND-011 |
| SC-24 | NIST 800-53 | Fail in Known State | — (FND-005) |
| RA-3 | NIST 800-53 | Risk Assessment | FR-001 (hazard/failure-mode model), FR-004 (`EpistemicState`), FR-004-CON-2 — integrity level absent (FND-004) |
| A.8.26 | ISO 27001 | Application security requirements | FR-004, FR-005 |
| A.8.28 | ISO 27001 | Secure coding | `scripts/generate-schemas.mjs` (Node built-ins only, no dependency), FR-002-CON-1 |
| CC7.1 | SOC 2 | Detection of configuration changes and vulnerabilities | FR-002-AC-4, FR-002-AC-9 — developer-local only (FND-001); no dependency scanning (FND-015) |
| CC3.2 | SOC 2 | Risk identification | FR-004 Behavior (`EpistemicState`), FR-004-CON-2 |
| V2 | ASVS 5.0 | Validation and Business Logic | FR-004 Behavior, FR-005-AC-5 — FND-010, FND-011 |
| V15 | ASVS 5.0 | Secure Coding and Architecture | FR-004-CON-1, FR-006 (reference, never redeclare) |

**Accountability, evidence and audit**

| Control | Standard | Control name | Module requirement |
|---|---|---|---|
| AU-10 | NIST 800-53 | Non-repudiation | FR-004 Behavior (`accepted` ⇒ `provenance`) — nominal only (FND-008); absent for `transferred`/`closed`/`mitigated` (FND-009) |
| AU-9 | NIST 800-53 | Protection of Audit Information | `Provenance.sourceSpan`, git history — no signature (FND-017) |
| A.5.33 | ISO 27001 | Protection of records | `EvidenceRef.target` (`SemanticId`), FR-006 Behavior |
| A.8.15 / A.8.16 | ISO 27001 | Logging / Monitoring activities | — silent refusals (FND-005); logging of a module load is `quire-rs`'s obligation |
| CC7.2 | SOC 2 | Monitoring for anomalies | — (FND-005) |
| CC4.1 | SOC 2 | Monitoring of controls | `traceability.required_relations` (`unmitigated-hazard`, `unmitigated-failure-mode`), FR-003-AC-5, NFR-001-AC-4 |
| V16 | ASVS 5.0 | Security Logging and Error Handling | FR-003-AC-6 (refusal names the offending key) — expected failure on `quire-rs#221`/`#394` (FND-005) |
| IEC 61508-1 §6 | IEC 61508 | Management of functional safety, competence | `Provenance.assertedBy`/`assertedAt` — FND-008 |
| ISO 26262-2 §6.4.9 | ISO 26262 | Confirmation measures | `LifecycleStatus`, `Provenance` — FND-008, FND-009 |
| ISO 26262-3 §6 | ISO 26262 | Hazard analysis and risk assessment (ASIL) | `HazardAssessment` (S, L, E, C) — no ASIL determinable (FND-004) |
| ISO 26262-8 cl.11 / IEC 61508-3 §7.4.4 | ISO 26262 / IEC 61508 | Confidence in the use of software tools | FR-002 Inputs (exact pins), `toolchain.json` — no TCL, no qualification argument (FND-003) |

### GDPR compliance

The module defines a schema; it operates no processing system, holds no data
subject record and transmits nothing. One field reaches the regulation.

| Article | Requirement | Module coverage |
|---|---|---|
| Art. 5(1)(c) | Data minimisation | Partial — `Provenance.assertedBy` is an open string designed to name whoever asserted a judgement. No requirement constrains it to a role or team identifier (FND-013). |
| Art. 25(1)/(2) | Data protection by design and by default | Gap — the by-design control here is to specify a non-personal identifier form. `EvidenceRef.kind` and `Provenance.method` are correctly non-personal. |
| Art. 17 | Right to erasure | Not achievable for a published artifact: the module publishes to public npm and to a git history, both immutable. Reinforces the minimisation control above (FND-013). |
| Art. 30 | Records of processing | N/A — no processing activity is performed by this component. |
| Art. 32(1)(b) | Confidentiality and integrity of processing | Integrity is addressed by the digest chain (FR-002, FR-003-AC-2); confidentiality is not applicable — every artifact is intended to be public. |
| Art. 32(1)(d) | Regular testing of measures | `spec/tests.md` TM-001 exists; it runs in no pipeline (FND-001). |

Principles addressed: **minimisation** — recommend `assertedBy` be specified as a
role identifier; **integrity** — FR-002 digest chain, FR-003-AC-2;
**accountability** — FR-004 Behavior (`accepted` ⇒ `provenance`), qualified by
FND-008.

### Audit support controls

| Control requirement | Standard reference | Module coverage |
|---|---|---|
| Build reproducibility | NIST SA-10, ISO A.8.32, SOC2 CC8.1 | FR-002-CON-3, TC-021 ✅ |
| Artifact-to-source binding | NIST SR-4, SI-7 | FR-002 digest chain — verified only on a developer machine (FND-001), unattested downstream (FND-007) |
| Toolchain record | ISO 26262-8 cl.11, NIST SA-15 | `toolchain.json` records names and exact versions ✅ — no TCL or qualification (FND-003) |
| Change auditability | NIST CM-3, ISO A.8.32 | FR-002-CON-5 atomic bump; `spec/log.md` is stale for this change (`base.md` FND-011) |
| Judgement attribution | NIST AU-10, IEC 61508-1 §6 | `Provenance` on `accepted` only, unauthenticated (FND-008, FND-009) |
| Refusal diagnostics | ASVS V16, ISO A.8.16, SOC2 CC7.2 | FR-003-AC-6 states the obligation; blocked on `quire-rs#221`/`#394` and carried as an expected failure (FND-005) |
| Coverage findings as evidence | SOC2 CC4.1 | `traceability.required_relations` — `unmitigated-hazard` / `unmitigated-failure-mode`, independently tunable ✅ |
| Evidence linkage | ISO A.5.33, IEC 61508-1 §7.16 | `EvidenceRef` exists and is referenced by `SemanticId` ✅ — never required by any status (FND-009) |

### Out of scope

| Control | Description | Responsible component |
|---|---|---|
| AC-2, AC-3, AC-6; ISO A.5.15–A.5.18; SOC2 CC6.1–CC6.3; ASVS V6–V8 | Identity, authentication, authorization, account and session management | `agent-ix/filament-core-service` (module activation and serving), GitHub and npm (repository and registry access) |
| AU-2, AU-3, AU-6, AU-12; ISO A.8.15–A.8.16 | Runtime audit logging and monitoring of module load, validation and refusal | `agent-ix/quire-rs` (loader and validator diagnostics — `#221`, `#394`), `agent-ix/filament-core-service` |
| SC-7, SC-8 (runtime), AC-17; ASVS V4, V12 | Network boundary, transport protection, API surface | `agent-ix/filament-core-service`, `agent-ix/cloudmanager-local-sync` |
| SC-28, MP-*, PE-* | Data at rest, media and physical protection | Infrastructure (kind/k8s cluster, GitHub, npm, GCP Artifact Registry) |
| CP-9, CP-10; SOC2 A1.2 | Backup and recovery of the module registry | `agent-ix/filament-core-service`, `agent-ix/quoin` (catalog) |
| SI-4, IR-4; SOC2 CC7.3–CC7.4 | Intrusion detection and incident response | Platform operations; incident records are `agent-ix/spec-objects-operational`'s object types |
| GDPR Art. 15, 16, 20 | Subject access, rectification, portability | `agent-ix/filament-core-service` and its data services — this module stores no subject record |
| Closed evidence-kind vocabulary and evidence records themselves | Evidence lifecycle, retention, custody | `agent-ix/engineering-assurance` (FR-006 Behavior fixes `EvidenceRef.kind` as an open string for exactly this reason) |
| `control`, `risk`, `asset`, `threat`, `vulnerability` object types and their controls | Security risk model | `agent-ix/spec-objects-security` (FR-006-AC-1) |
| Digest verification at activation, snapshot resolution of a reference-form `data_schema` | Consumer-side integrity enforcement | `agent-ix/filament-core-service#23`, `agent-ix/quoin` FR-073 |
| Manifest-level `semantic` key refusal at install | Install-time contract validation | `agent-ix/quoin` FR-070 (evidenced by IT-001) |

## Automated Checks

| Check | Result |
|---|---|
| `quire validate --scope <worktree> "spec/**/*.md"` | ✅ Exit 0, no structural failure. Grammar warnings pre-existing on the FR bodies (`base.md` FND-016); registry advisories environmental (`DuplicateModuleName`, `DuplicateArchetype`, `DuplicateInverseEdge`). |
| Lockfile transport | ❌ `package-lock.json:19` resolves `@agent-ix/semantic-core` over `http://npm.ix/...` (FND-002). All 1,000+ other entries resolve `https://registry.npmjs.org/` with `sha512` integrity ✅ |
| Dev-engine install transport | ❌ `pip install --index-url http://pypi.ix/... --trusted-host pypi.ix 'quire>=0.46.0'` — no TLS, no hash pin, floating lower bound (FND-002) |
| Schema `$ref` host reachability | ❌ `schemas.agent-ix.org` does not resolve (DNS, 2026-09-04); ten grammar `$ref`s and every intra-module `$ref` name it (FND-006) |
| Secret handling in workflows | ❌ base64-transformed service-account key written to `$GITHUB_OUTPUT` (FND-014, pre-existing) |
| Integrity gate in CI | ❌ `make lint` / `make schemas-check` run in no workflow; `ci.yml` is `workflow_dispatch`; `release-npm.yml` is publish-only (FND-001) |
| Published-artifact attestation | ❌ `provenance=false` in the shared release reusable (FND-007) |
| Hard-coded secrets in repo | ✅ none — no `.npmrc`, no token, no credential in the tree (FR-002-CON-2, TC-023) |
| Generator dependency surface | ✅ `scripts/generate-schemas.mjs` and `scripts/stage-npm.mjs` use Node built-ins only; the generator writes only under `schemas/` and only `digest:` lines in the manifest, and `--check` writes nothing |
| Digest algorithm | ✅ SHA-256 over rendered bytes, per file and overall — no weak algorithm anywhere (agility and signature: FND-017) |
| Default-value injection | ✅ no `default` in any shipped schema (FR-004-AC-7) — the single most important safety property of the schema set, and it holds |

## Notes

- The three findings that would most change the module's risk posture are cheap:
  FND-001 (run `schemas-check` in a pipeline that can reach the toolchain, or
  state explicitly that the pre-publish gate is a documented manual step with a
  named owner), FND-002 (HTTPS and a hash-pinned engine install), and FND-010 (a
  `pattern` that rejects whitespace-only judgement text). None requires a design
  change.
- FND-004 is the finding most likely to be a deliberate decision the spec simply
  did not record. If the module intends the IEC 61508 severity lineage and treats
  ASIL determination as a downstream repository's mapping, that belongs in
  `spec.md` Out of Scope with the same rigour as the other fourteen exclusions —
  a reader who sees `E0..E4` and `C0..C3` will reasonably assume the ISO 26262
  chain is intended to close.
- The module's positive controls are worth recording as such, because a
  compliance reader should not have to infer them: `EpistemicState` as a first-class
  refusal to let an unassessed axis read as safe; FR-004-CON-2 stating that schema
  validity is not a safety claim; the absence of any `default`; the refusal to
  redeclare a neighbour's type (FR-006); `imports: {}` rather than an aspirational
  pin; and `traceability.required_relations` as data rather than code. These are
  the design decisions that make the findings above fixable rather than structural.
- Findings were measured against the tree at commit `5dc1980`. While this review
  ran, concurrent uncommitted edits appeared in the worktree adding
  `additionalProperties: false` beside `unevaluatedProperties` on the record
  models, which is exactly the closure FND-011 asks for; if those edits land,
  FND-011 is discharged for the affected models and should be re-measured
  rather than carried forward on this text.
- No spec artifact, schema, manifest or script was edited by this review.
