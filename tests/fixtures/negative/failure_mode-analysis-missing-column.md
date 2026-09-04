---
id: negative-007
title: "FailureModeWithoutDetection"
type: failure_mode
object: failure_mode
expect: "do not match asserted columns"
because: "Detection is the column that earns this type; a triple without it is not an FMEA row"
---
# [negative-007] FailureModeWithoutDetection

## Description

The controller stops publishing pressure commands while remaining powered.

## Analysis

| Effect | Cause |
| ------ | ----- |
| Deceleration is not applied. | Publish task starvation. |

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| failure_mode_id | UUID | 1..1 | identity |
