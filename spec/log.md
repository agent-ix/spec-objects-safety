# Log

## FR-001-AC-1 role clause

FR-001's body decided no role is declared; `allowed_links` target concrete
object types. FR-001-AC-1 is corrected to match: it requires a `data_schema` and
an `allowed_links` map and states that no role is declared. TC-002 asserts each
clause, including that neither object type has `roles`.

## Which end authors `mitigates`

The control end authors it: `spec-objects-security` `control.mitigates` gains
`hazard` and `failure_mode` (FR-007). The direction stays `incoming` and the
safety `traceability` block is unchanged (NFR-001).
