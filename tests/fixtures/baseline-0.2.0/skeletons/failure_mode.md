---
id: FM-001
title: "Brake controller stops publishing pressure commands"
type: failure_mode
---
<!-- failure_mode authoring skeleton (spec-objects-safety). Fill every section
     with substantive content. Contract (manifest body_extraction):
     - Frontmatter MUST carry id, title, and type: failure_mode.
     - "## Description" (H2) is REQUIRED.
     - "## Analysis" (H2) is REQUIRED: a table with headers exactly
       Effect | Cause | Detection and at least one data row.
     - Keep headings unique per level; never leave a section empty.

     A FAILURE MODE IS NOT A HAZARD. This type answers "what breaks"; a
     `hazard` answers "what state must never be reached". One failure mode can
     contribute to several hazards, and a hazard can exist with no failure
     mode behind it. Link them with `causes` / `contributes_to`.

     DETECTION is the column that earns this type:
       none      — nothing observes it; discovered only by its effect
       indirect  — inferable from other signals, by someone looking
       direct    — an explicit signal exists for this failure
       automatic — detected and acted on without a human
     A failure nobody can detect is a different engineering problem from the
     same failure with an alarm on it, and neither severity nor likelihood
     carries that. Checked by the `failure-mode-detection` lint rule. -->

## Description

<!-- What the component does instead of what it should. Be specific about the
     component and the wrong behaviour. -->

## Analysis

| Effect | Cause | Detection |
| ------ | ----- | --------- |
| <what happens downstream> | <why it happens> | direct |
