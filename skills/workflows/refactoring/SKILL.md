---
name: godot-refactoring
description: Restructure Godot code or scenes while preserving externally observable behavior and project references.
metadata:
  short-description: Restructure Godot code or scenes while preserving externally observable behavior and project references.
---

# Godot Refactoring

State the design pressure and intended boundary before moving code. Map callers, signal connections, scene ownership, serialized Resource references, `res://` paths, and stable `.gd.uid` files. Identify shared mutable data and lifecycle assumptions that a move could change.

Refactor in small coherent steps: extract pure rules, clarify ownership, reduce duplication, or replace a brittle dependency. Keep behavior changes separate unless required to expose the seam, and explain any unavoidable behavior difference. Do not add an abstraction solely to mirror a pattern; use composition or inheritance only where it reduces actual coupling.

Run existing relevant tests/import checks and compare the original user flow. Check scene/resource loading and save compatibility if schemas or IDs moved. Remove obsolete paths only after references are updated. Report the new boundary and evidence that behavior remains intact. For broad conventions see [godot-game-development](../../../godot-game-development/SKILL.md); architectural decisions belong in [architecture](../../godot/architecture/SKILL.md).
