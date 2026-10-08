---
name: godot-ui-review
description: Review Godot UI layout, readability, interaction states, keyboard/gamepad navigation, and responsive behavior.
metadata:
  short-description: Review Godot UI layout, readability, interaction states, keyboard/gamepad navigation, and responsive behavior.
---

# Godot Ui Review

Inspect the relevant scene and project stretch/resolution policy. Review the full path at base size, smallest supported size, and a different aspect ratio. Check hierarchy, readable text, clipping, contrast, safe-area use, empty/full/error states, and whether the primary action is clear. Preserve established visual style unless the task asks to change it.

Exercise mouse/touch and keyboard or gamepad as supported. Check initial focus, navigation neighbors, modal focus return, disabled/locked states, pause behavior, and whether decorative Controls intercept input. Confirm Containers own managed child geometry and that overlays consume only intended events. Check longer strings and largest expected values.

Give findings by severity with the screen/state and concrete impact; distinguish rendering evidence from assumptions. Fix only within the requested scope and verify visually after edits. Headless checks cannot establish layout or real input. See [godot-2d-ui](../../../godot-2d-ui/SKILL.md) for implementation guidance and [mobile](../../godot/mobile/SKILL.md) for device-specific review.
