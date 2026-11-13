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
 * rules. Every grammar item is a `$ref` to `@agent-ix/semantic-core` and
 * is never redeclared here; this namespace contributes archetype shapes only.
 *
 * SAFETY RULE FOR EVERY MODEL BELOW: nothing here computes, infers or defaults
 * a safety judgement. There is no default severity, no default likelihood, no
 * default detection and no default status; an unscored axis is stated with an
 * explicit `EpistemicState` member, never by omission and never by a scale's
 * safe end.
 */
@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-safety/")
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

/**
 * A harm: the thing that happens to a person, property or the environment
 * (the manifest `lexicon` entry `harm` is the definition). A harm is not a
 * hazard (a state) and not a hazardous situation (a case in which a hazard
 * state coincides with something that can be hurt).
 *
 * The seal forbids `severity`, `probability`, `score`, `status` and
 * `acceptance`. Severity belongs to a risk estimate, because the same harm is
 * more or less severe depending on the situation and the controls in place.
 * There is no `status` because `LifecycleStatus` includes `accepted`, and an
 * acceptance of a harm means nothing: acceptance is recorded only on the
 * residual-risk decision.
 *
 * The chain edge `arises_from` (harm to hazardous situation) is authored in the
 * document's relationships, not in this record, so no key here lists situations.
 */
@extension("additionalProperties", false)
model Harm {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  provenance?: Provenance;
  evidence?: EvidenceRef[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/**
 * A hazardous situation: a case in which a hazard state coincides with
 * something that can be hurt. It promotes the free string
 * `HazardContext.situation` to a first-class object; that string stays valid
 * on `Hazard` and nothing here migrates it.
 *
 * The seal forbids `severity`, `probability`, `score` and `acceptance`: those
 * are judgements, and a judgement is a risk estimate of this situation. The
 * edge to the hazard it arises from (`arises_from`) is authored in the
 * document's relationships.
 */
@extension("additionalProperties", false)
model HazardousSituation {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  provenance?: Provenance;
  evidence?: EvidenceRef[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/**
 * Whether an estimate is made before any control is assumed or on the
 * assumption that named controls are in place. Declared with no default: a
 * person chooses.
 */
enum EstimatePhase {
  pre_control,
  post_control,
}

/**
 * A level a person enters on an estimate: any non-empty text that is none of
 * the three `EpistemicState` members. The project's acceptability policy names
 * the levels; this module fixes no list, so a project can use its own scale.
 * Excluding the three members keeps a marker distinct from every level, so a
 * project cannot name a level `not_assessed`.
 */
@extension("not", #{ `enum`: #["unknown", "not_assessed", "not_applicable"] })
@minLength(1)
scalar EstimateLevelText extends string;

/**
 * A level entered on an estimate, or one of the `EpistemicState` markers.
 * A marker validates only through the marker branch.
 */
union EstimateLevel {
  EstimateLevelText,
  EpistemicState,
}

/**
 * The judgement of a risk estimate: one person's view of how bad (`severity`)
 * and how likely (`probability`) the harm is for one hazardous situation,
 * before any control is assumed (`pre_control`) or on the assumption that named
 * controls are in place (`post_control`).
 *
 * Every member is required and entered by a named person: there is no default
 * for `phase`, `severity` or `probability`, and the seal forbids `score`,
 * `region`, `level`, `acceptable` and `acceptance`, so no tool derives or stores
 * a score, a region or an acceptance. `provenance` carries `assertedBy` and
 * `assertedAt`.
 */
@extension("additionalProperties", false)
model EstimateJudgement {
  phase: EstimatePhase;
  severity: EstimateLevel;
  probability: EstimateLevel;

  @minLength(1)
  rationale: string;

  provenance: Provenance;
  ...Record<never>;
}

/**
 * A risk estimate object. The judgement sits under `estimate`, whole or
 * refused, the same shape `Hazard.assessment` has; it is optional on the record
 * because Quire populates a declaration record's `fields`, `clauses`,
 * `operations` and `relations` only, so the document-level requirement is the
 * manifest's table and frontmatter locators until the Markdown mapping for
 * module-specific keys lands.
 *
 * `phase` is also a top-level frontmatter key of the document, so required
 * relations can select on it. The edges `estimates` (to the situation) and
 * `assumes` (to controls) are authored in the document's relationships, not in
 * this record.
 */
@extension("additionalProperties", false)
model RiskEstimate {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  estimate?: EstimateJudgement;
  evidence?: EvidenceRef[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Acceptability policy, residual-risk decisions, benefit-risk and the overall
// evaluation (FR-101, FR-103, FR-104, FR-106, FR-107).
//
// Every value here is written by a person. The seal on each model forbids a
// score, a region on a decision record, a ratio, a total and a date, and no
// member has a default, so no tool derives, stores or defaults a score, a
// region or an acceptance.
// ---------------------------------------------------------------------------

/**
 * A level or region name a project chooses: text that is not blank and not an
 * unfilled `<placeholder>`.
 */
@minLength(1)
@pattern("^[^<>\\s][^<>]*$")
scalar PolicyName extends string;

/**
 * Text a person wrote (a rationale, a benefit, a product): not blank and not an
 * unfilled `<placeholder>`.
 */
@minLength(1)
@pattern("^[^<>\\s][^<>]*$")
scalar StatedText extends string;

/** A named person who decided: not blank and not an unfilled `<placeholder>`. */
@minLength(1)
@pattern("^[^<>\\s][^<>]*$")
scalar PersonName extends string;

/**
 * One region of the policy. `outside_acceptable` is set by the project's
 * people and has no default: a region that omits it is refused.
 */
@extension("additionalProperties", false)
model PolicyRegion {
  name: PolicyName;
  outside_acceptable: boolean;
  ...Record<never>;
}

/** The region the policy assigns to one severity and probability pairing. */
@extension("additionalProperties", false)
model PolicyCell {
  severity: PolicyName;
  probability: PolicyName;
  region: PolicyName;
  ...Record<never>;
}

/**
 * The policy table: the severity levels, the probability levels, the regions
 * and the region of each pairing. A level name is listed once per list.
 * Whether every pairing has exactly one cell naming a listed region is a
 * cross-row rule a JSON Schema cannot state; it is checked over the document
 * by the engine's table assertions once they can (see the manifest).
 */
@extension("additionalProperties", false)
model PolicyTable {
  @minItems(1)
  @uniqueItems
  severities: PolicyName[];

  @minItems(1)
  @uniqueItems
  probabilities: PolicyName[];

  @minItems(1)
  regions: PolicyRegion[];

  @minItems(1)
  cells: PolicyCell[];

  ...Record<never>;
}

/**
 * An acceptability policy object. The table sits under `policy`, whole or
 * refused, optional on the record for the reason `RiskEstimate.estimate` is.
 */
@extension("additionalProperties", false)
model AcceptabilityPolicy {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  policy?: PolicyTable;
  evidence?: EvidenceRef[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/**
 * A decision not yet made. `decided_by` is refused: nobody has decided.
 */
@extension("additionalProperties", false)
model UndecidedDetermination {
  decision: "undecided";
  rationale?: StatedText;
  ...Record<never>;
}

/**
 * A decision a named person made. The rationale and `decided_by` are required
 * and non-blank. There is no default for `decision`; a decision date or history
 * comes from version control, not from a field.
 */
@extension("additionalProperties", false)
model DecidedDetermination {
  decision: "accepted" | "not_accepted";
  rationale: StatedText;
  decided_by: PersonName;
  ...Record<never>;
}

/** The decision on a residual risk: undecided, or decided by a named person. */
union Determination {
  UndecidedDetermination,
  DecidedDetermination,
}

/**
 * A residual-risk record. The post-control severity and probability live only
 * on the referenced `risk_estimate`; the record carries the decision. The
 * `estimate` reference and the policy reference are edges authored in the
 * document's relationships, not members here.
 */
@extension("additionalProperties", false)
model ResidualRisk {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  determination?: Determination;
  evidence?: EvidenceRef[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/** A benefit-risk decision not yet made. */
@extension("additionalProperties", false)
model UndecidedBenefitDetermination {
  benefit: StatedText;
  decision: "undecided";
  rationale?: StatedText;
  ...Record<never>;
}

/** A benefit-risk decision a named person made. */
@extension("additionalProperties", false)
model DecidedBenefitDetermination {
  benefit: StatedText;
  decision: "accepted" | "not_accepted";
  rationale: StatedText;
  decided_by: PersonName;
  ...Record<never>;
}

/** The weighing of a benefit against the residual risks a record covers. */
union BenefitDetermination {
  UndecidedBenefitDetermination,
  DecidedBenefitDetermination,
}

/**
 * A benefit-risk record. The residual risks it covers are `references` edges
 * to `residual_risk` documents, authored in the document's relationships.
 */
@extension("additionalProperties", false)
model BenefitRisk {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  determination?: BenefitDetermination;
  evidence?: EvidenceRef[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/** An overall evaluation not yet decided. */
@extension("additionalProperties", false)
model UndecidedEvaluation {
  product: StatedText;
  decision: "undecided";
  rationale?: StatedText;
  ...Record<never>;
}

/** An overall evaluation a named person decided. */
@extension("additionalProperties", false)
model DecidedEvaluation {
  product: StatedText;
  decision: "accepted" | "not_accepted";
  rationale: StatedText;
  decided_by: PersonName;
  ...Record<never>;
}

/** The decision on the residual risk of the product taken together. */
union EvaluationDetermination {
  UndecidedEvaluation,
  DecidedEvaluation,
}

/**
 * The overall residual-risk evaluation of one product. The residual risks and
 * benefit-risk records it considers are `references` edges authored in the
 * document's relationships; the tooling does not aggregate them into the
 * decision.
 */
@extension("additionalProperties", false)
model OverallResidualRiskEvaluation {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  determination?: EvaluationDetermination;
  evidence?: EvidenceRef[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}
