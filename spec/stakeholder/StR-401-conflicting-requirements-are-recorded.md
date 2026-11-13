---
id: StR-401
title: "Conflicting requirements are recorded and closed by a design or a person"
type: StR
---
# StR-401: Conflicting requirements are recorded and closed by a design or a person

## Stakeholder Need

A team that finds two requirements it cannot satisfy together **SHALL** record the
conflict as a first-class specification object, so that it is closed by a design element or
accepted by a named person, and cannot be left silently resolved in whichever direction the
last author preferred. Source: PLAT-1480.

## Rationale

A conflict between requirements is a risk-model input whether or not the requirements concern
safety: an unresolved latency-versus-audit conflict is as capable of shipping as an unmitigated
hazard. When nothing records it, the reading an author picked is invisible, and a release
cannot be checked for open conflicts. Recording it in this module places it beside the hazard
and risk records it informs.

## Validation Criteria

| ID | Criteria | Validation |
|----|----------|------------|
| StR-401-VC-1 | A corpus with an open conflict is reported as incomplete; closing it by a design element or by a named person clears the report. | Demonstration |
