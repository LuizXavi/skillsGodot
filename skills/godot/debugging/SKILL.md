---
name: godot-debugging
description: Diagnose Godot runtime errors, scene failures, input issues, and intermittent behavior from reproducible evidence.
metadata:
  short-description: Diagnose Godot runtime errors, scene failures, input issues, and intermittent behavior from reproducible evidence.
---

# Godot Debugging

Reproduce the failure and preserve the first relevant error, stack trace, engine version, scene, and steps. Reduce to the smallest failing path while keeping the same lifecycle and input conditions. Inspect the node/resource that owns the state and the transition that first violates its expected invariant.

Use breakpoints and targeted logs at state boundaries; include stable identifiers and values that distinguish repeated instances. Remove noisy temporary logging after diagnosis. Check signal connection count, node lifetime, scene-tree timing, resource paths/UIDs, process mode, and pause state where relevant. Do not “fix” a symptom by suppressing an error or adding broad null guards without establishing why state is absent.

Test the original reproduction plus the nearest boundary case and a normal path. For intermittent defects, repeat enough runs to determine whether the change affects the failure rate. Keep saves and project data safe by using temporary state when a reproduction mutates persistence. Report what reproduces, the root cause, and the evidence for the fix; distinguish engine/editor environment problems from game behavior.

Use [Godot development](../../../godot-game-development/SKILL.md) for project-level validation and [save-system guidance](../../../godot-save-system/SKILL.md) when persistence is involved.
