---
name: godot-gdscript
description: Write and review GDScript for Godot with clear types, lifetimes, signals, and version-aware APIs. Use for scripts, resources, and scene behavior.
metadata:
  short-description: Write and review GDScript for Godot with clear types, lifetimes, signals, and version-aware APIs
---

# Godot Gdscript

Confirm the target Godot version and inspect neighboring scripts before choosing syntax or APIs. Type public fields, parameters, and return values where it clarifies contracts or catches invalid state; keep inferred locals concise. Use enums/constants for finite states and avoid stringly typed state transitions.

Keep `_process` and `_physics_process` small: route input, advance time-dependent behavior, and update only what needs per-frame work. Separate pure calculations from Node lifecycle so rules can be checked without constructing a scene. Awaited signals and timers create lifetime boundaries; ensure the owning node still exists and repeated requests cannot launch duplicate work.

Prefer signals for outward events, explicit method calls for owned collaborators, and Resources for reusable authored data. Avoid mutable shared Resources when instances are expected to diverge; duplicate intentionally and specify duplication depth when nested resources matter. Guard invalid indices, freed objects, empty collections, and non-finite numeric results at meaningful boundaries rather than blanket null checks.

Use project style, annotations, and naming conventions. Check API uncertainty against official docs for the exact engine version. Preserve `.gd.uid` when moving scripts and update every scene/resource path. Route whole-project changes through [Godot development](../../../godot-game-development/SKILL.md).
