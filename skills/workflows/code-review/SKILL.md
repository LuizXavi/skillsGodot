---
name: godot-code-review
description: Review Godot changes for correctness, regressions, lifecycle risks, compatibility, and missing validation.
metadata:
  short-description: Review Godot changes for correctness, regressions, lifecycle risks, compatibility, and missing validation.
---

# Godot Code Review

Review the diff against the stated behavior and project version. Trace changed state through callers, signals, scenes, Resources, and save/load paths. Prioritize concrete defects with user impact: invalid state, duplicate rewards, lost items, stale references, broken input, incompatible saves, or unverified platform assumptions.

For each finding, identify the file/line, trigger, consequence, and smallest remedy. Separate certain defects from questions or style preferences. Check error paths and boundaries, not just the intended happy path. Treat tests as evidence for covered behavior only; a headless test does not prove graphical layout, touch behavior, or device performance.

Do not report speculative concerns as bugs without a plausible path. If no actionable defect is found, say so and note only meaningful coverage gaps. Avoid rewriting the patch during review unless asked to fix it. For UI findings, use [godot-2d-ui](../../../godot-2d-ui/SKILL.md); for persistence, [godot-save-system](../../../godot-save-system/SKILL.md).
