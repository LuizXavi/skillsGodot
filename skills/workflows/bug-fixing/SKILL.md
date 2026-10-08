---
name: godot-bug-fixing
description: Fix a reproducible Godot defect while preserving existing project conventions and demonstrating the affected behavior.
metadata:
  short-description: Fix a reproducible Godot defect while preserving existing project conventions and demonstrating the affected behavior.
---

# Godot Bug Fixing

Capture the reported steps, expected result, actual result, engine version, and first useful error. Inspect project-local instructions and only the relevant scenes/scripts. Reproduce before editing when possible; identify the violated invariant and the smallest owner responsible for it.

Make a focused change that fixes the cause. Preserve existing save compatibility, scene ownership, input semantics, and signal lifetimes. Add a regression check only when it meaningfully covers the failure and fits the project’s test approach. Do not broaden a bug fix into unrelated cleanup.

Run the narrowest relevant validation and the project’s normal import/script check if available. For a visual or device-specific defect, reproduce on the target context; headless success is not visual proof. Re-run the original steps and one nearby boundary case. Report root cause, changed behavior, checks, and limitations. Use [Godot development](../../../godot-game-development/SKILL.md) for engine-aware conventions and [debugging](../../godot/debugging/SKILL.md) for diagnosis.
