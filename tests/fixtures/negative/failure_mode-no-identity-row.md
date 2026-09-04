---
id: negative-002
title: "FailureModeWithoutIdentity"
type: failure_mode
object: failure_mode
expect: semantic.record-invalid
because: "FailureMode.json requires at least one identity field"
---
# [negative-002] FailureModeWithoutIdentity

## Description

The controller stops publishing pressure commands while remaining powered.

## Analysis

| Effect | Cause | Detection |
| ------ | ----- | --------- |
| Deceleration is not applied. | Publish task starvation. | direct |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| component | String | 1..1 | minLength: 1 |
