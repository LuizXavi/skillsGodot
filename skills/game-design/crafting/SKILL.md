---
name: godot-crafting-design
description: Design crafting recipes, station requirements, queue behavior, ingredient consumption, and failure-safe results.
metadata:
  short-description: Design crafting recipes, station requirements, queue behavior, ingredient consumption, and failure-safe results.
---

# Godot Crafting Design

Represent recipes as stable IDs with explicit ingredients, output, duration, station/tier requirements, and optional byproducts. Decide whether crafting consumes ingredients on enqueue or completion, whether jobs can be cancelled, and how refunds behave. Reserve or consume materials atomically so simultaneous queues cannot spend the same stock.

Define queue capacity, ordering, speed modifiers, offline progression, and what happens if a station is removed or an unlock changes during a job. Keep recipe definitions separate from active job state. A completed job should produce exactly once, including after save/load; use a job ID or persisted phase when operations cross persistence boundaries.

Check insufficient materials, exact quantities, repeated enqueue, full output inventory, cancellation, save during every phase, locked station, and output overflow. Make blocked reasons visible to players. Avoid silently discarding byproducts or queue progress.

Use [crafting system template](../../../templates/godot/crafting_system/README.md) when appropriate. For inventory transaction semantics, consult [inventory design](../inventory/SKILL.md); for persistence, [godot-save-system](../../../godot-save-system/SKILL.md).
