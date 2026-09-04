import "@typespec/json-schema";
import "@agent-ix/semantic-core";

using TypeSpec.JsonSchema;
using AgentIx.Semantic.Core;

/**
 * Safety object declaration schemas (agent-ix/spec-objects-safety#2).
 *
 * One model per safety object type this module contributes, each validating
 * that type's Quire declaration record (fields, relations, clauses; quire-rs
 * FR-070..FR-072) with type-specific required keys, forbidden keys, and item
 * rules. Every grammar item is a `$ref` to `@agent-ix/semantic-core` 0.1.0 and
 * is never redeclared here; this namespace contributes archetype shapes only.
 *
 * The `$id` base embeds the manifest `version` by intent: one schema URL names
 * exactly one immutable byte sequence, so a downstream fixture reader that
 * pinned a version can never silently read later bytes. A bump edits this base
 * and `manifest.yaml`'s `version` in one commit and re-runs `make schemas`.
 *
 * SAFETY RULE FOR EVERY MODEL BELOW: nothing here computes, infers or defaults
 * a safety judgement. There is no default severity, no default likelihood, no
 * default detection and no default status; an unscored axis is stated with an
 * explicit `EpistemicState` member, never by omission and never by a scale's
 * safe end.
 */
@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-safety/0.3.0/")
namespace AgentIx.SpecObjects.Safety;

// ---------------------------------------------------------------------------
// Support models
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// SEALED TWICE, ON PURPOSE.
//
// `...Record<never>` emits `unevaluatedProperties: {"not": {}}`, which is a
// 2020-12 keyword: a consumer validating against draft-07 or earlier ignores it
// and accepts a `Hazard` carrying `analysis`, or a `FailureMode` carrying
// `assessment` — the exact conflation these models refuse. `required` and
// `enum` still fail closed in every dialect, so the failure would be silent and
// partial. `@extension("additionalProperties", false)` states the same rule in
// a keyword every dialect back to draft-04 honours, and is redundant only where
// the consumer is already on 2020-12.
//
// This is a line comment rather than a doc comment on purpose: a floating `/**
// */` block above a model is emitted as that model's `description`, and the
// model it would land on here is `IdentityField` — the one model deliberately
// left OPEN, whose shipped schema would then describe itself as sealed.
// ---------------------------------------------------------------------------

/**
 * Open marker: a `FieldDecl` flagged as identity. Used only as the `@contains`
 * predicate for the "≥ 1 identity field" item rule; it is deliberately open so
 * it matches any identity-flagged field.
 */
model IdentityField {
  identity: true;
}

/**
 * How bad the harm is if the hazard state is reached. The ordinal buckets the
 * ecosystem authors in; a repository working to a specific standard maps its
 * own scale onto them rather than inventing a column. `negligible` is the safe
 * end of a *scored* axis — it is an assessment, not an absence of one.
 */
enum Severity {
  negligible,
  marginal,
  critical,
  catastrophic,
}

/** How often the hazard state is expected to be reached. */
enum Likelihood {
  incredible,
  improbable,
  remote,
  occasional,
  probable,
  frequent,
}

/**
 * ISO 26262 exposure: how much of the operating time the situation obtains.
 * `E0` means "incredible", a scored value; it does not mean "not looked at".
 */
enum Exposure {
  E0,
  E1,
  E2,
  E3,
  E4,
}

/**
 * ISO 26262 controllability: whether the people involved can avoid the harm.
 * `C0` means "controllable in general", a scored value.
 */
enum Controllability {
  C0,
  C1,
  C2,
  C3,
}

/**
 * Whether, and how directly, a failure can be observed before it causes harm.
 * `none` is a scored value — nothing observes this failure — and is the worst
 * case on the axis, not a missing assessment.
 */
enum Detection {
  none,
  indirect,
  direct,
  automatic,
}

/**
 * The epistemic states an assessed axis may carry INSTEAD of a scale value.
 *
 * This enum exists because the three states below are routinely collapsed into
 * a scale's safe end, and each collapse hides a different thing:
 *
 *   * `unknown` — the axis was looked at and cannot be determined yet. Someone
 *     tried; the answer is not available.
 *   * `not_assessed` — nobody has looked. This is the state a backlog of
 *     unanalysed hazards is in, and it is the one that must never read as
 *     `negligible`, `E0`, `C0` or `none`.
 *   * `not_applicable` — the axis does not apply to this object, with a reason
 *     the author states in prose. Distinct from both of the above and from any
 *     scale value.
 *
 * None of the three is a scale member, so no consumer can sort them into an
 * ordering with `negligible` or compute a risk number from them by accident.
 */
enum EpistemicState {
  `unknown`,
  not_assessed,
  not_applicable,
}

/**
 * Where a safety object sits in its own lifecycle. Authored, never inferred:
 * schema validity is not a safety claim, and no value here is reached by a
 * document merely validating.
 */
enum LifecycleStatus {
  identified,
  analysed,
  mitigated,
  accepted,
  transferred,
  closed,
}

/**
 * The two axes every safety standard scores a hazard on, plus the two ISO 26262
 * adds. `severity`, `likelihood` and `rationale` are required *when an
 * assessment is present*: a hazard recorded with a half-filled assessment
 * cannot be prioritised, and an unscored backlog is indistinguishable from no
 * analysis. `exposure` and `controllability` are optional because IEC 61508 and
 * FMEA lineages do not score them; when a repository works to ISO 26262 it
 * fills them, and `not_assessed` states that it has not.
 */
@extension("additionalProperties", false)
model HazardAssessment {
  severity: Severity | EpistemicState;
  likelihood: Likelihood | EpistemicState;
  exposure?: Exposure | EpistemicState;
  controllability?: Controllability | EpistemicState;

  @minLength(1)
  rationale: string;

  ...Record<never>;
}

/**
 * The FMEA triple. `detection` is the field that earns `failure_mode` its own
 * type: a failure nobody can detect is a different engineering problem from the
 * same failure with an alarm on it, and neither severity nor likelihood carries
 * that.
 */
@extension("additionalProperties", false)
model FailureAnalysis {
  @minLength(1)
  effect: string;

  @minLength(1)
  cause: string;

  detection: Detection | EpistemicState;

  ...Record<never>;
}

/**
 * The operational situation the hazard state is reached in. A hazard scored
 * without its context is a score that cannot be compared: "the vehicle cannot
 * decelerate" is a different exposure on a motorway than in a parking bay.
 */
@extension("additionalProperties", false)
model HazardContext {
  @minLength(1)
  situation: string;

  phase?: string;
  environment?: string;
  ...Record<never>;
}

/**
 * Who asserted a safety judgement, when, and against what. Required whenever
 * `status` is `accepted` (the `allOf`/`if` rule on both record models), together
 * with the assessment or analysis being accepted: risk acceptance with nobody's
 * name on it, or with nothing scored to accept, is the one status that must
 * never be reachable by a document simply validating.
 */
@extension("additionalProperties", false)
model Provenance {
  @minLength(1)
  assertedBy: string;

  assertedAt: utcDateTime;

  @minLength(1)
  standard?: string;

  @minLength(1)
  method?: string;

  sourceSpan?: SourceLocus;
  ...Record<never>;
}

/**
 * A reference to an evidence record that supports a safety judgement. A
 * reference only: evidence records themselves are owned by
 * `agent-ix/engineering-assurance`, and duplicating one here would create a
 * second copy that drifts. `kind` is an open string for the same reason — the
 * closed evidence-kind vocabulary is the assurance module's to declare, not
 * this module's to mint.
 */
@extension("additionalProperties", false)
model EvidenceRef {
  target: SemanticId;

  @minLength(1)
  kind?: string;

  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Object-type declaration records
// ---------------------------------------------------------------------------

/**
 * A hazard: a system state or condition that can lead to harm.
 *
 * `relations` carries the causal edges (`arises_from`) and is deliberately NOT
 * subject to a "≥ 1 cause" item rule. STPA exists because components each
 * behaving exactly as specified can reach a harmful state together, so a hazard
 * with no failure mode behind it is a valid and important record; requiring a
 * cause would push authors to invent one.
 *
 * There is no `controls` or `mitigations` key. The mitigation edge is authored
 * from the requirement's end (`mitigates`, `direction: incoming` in the
 * manifest's `traceability` block), so a list here would be a second copy of
 * the same fact with nothing keeping the two in step. Controls themselves are
 * `agent-ix/spec-objects-security`'s `control` type, referenced by
 * `SemanticId`, never redeclared here.
 *
 * `operations` and `analysis` are forbidden by the seal: a hazard is a state,
 * it invokes nothing, and the FMEA triple belongs to `FailureMode`.
 */
@extension(
  "allOf",
  #[
    #{
      `if`: #{ required: #["status"], properties: #{ status: #{ `const`: "accepted" } } },
      then: #{ required: #["provenance", "assessment"] },
    }
  ]
)
@extension("additionalProperties", false)
model Hazard {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  assessment?: HazardAssessment;
  context?: HazardContext;
  status?: LifecycleStatus;
  provenance?: Provenance;
  evidence?: EvidenceRef[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/**
 * A failure mode: the manner in which a component fails to perform its intended
 * function.
 *
 * Separate from `Hazard`, not a variant of it. `assessment` and `context` are
 * forbidden by the seal — the severity/likelihood pair scores a *state* and
 * would mean something else here — and `operations` is forbidden for the same
 * reason it is on `Hazard`.
 */
@extension(
  "allOf",
  #[
    #{
      `if`: #{ required: #["status"], properties: #{ status: #{ `const`: "accepted" } } },
      then: #{ required: #["provenance", "analysis"] },
    }
  ]
)
@extension("additionalProperties", false)
model FailureMode {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  analysis?: FailureAnalysis;
  status?: LifecycleStatus;
  provenance?: Provenance;
  evidence?: EvidenceRef[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}
