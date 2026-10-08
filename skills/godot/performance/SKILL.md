---
name: godot-performance
description: Measure and improve Godot runtime, rendering, loading, and memory performance when profiling shows a bottleneck.
metadata:
  short-description: Measure and improve Godot runtime, rendering, loading, and memory performance when profiling shows a bottleneck.
---

# Godot Performance

Start with a reproducible slow scenario and capture a baseline on the target device/build. Identify whether time is in scripts, physics, rendering, resource loading, or allocation; optimize the dominant measured cost. Averages can hide frame spikes, so inspect worst frames and repeated-session behavior.

Common candidates include per-frame scene-tree searches, rebuilding large UI lists, excessive signal churn, many physics queries, overdraw, large textures, and synchronous resource loads. Change one cause at a time and compare the same scenario. Cache stable references with clear invalidation; do not preserve stale Nodes across scene changes. Pooling or multithreading adds lifecycle and synchronization costs and should answer an observed problem.

Keep the result behaviorally equivalent: compare output, timing, and memory before/after. Add instrumentation that can be disabled or removed cleanly. Validate on the representative export and hardware; editor numbers can differ. Report measured impact and any scenario that remains untested.

For systematic profiling use the Godot profiler and official docs matching the project version. For UI, consult [godot-2d-ui](../../../godot-2d-ui/SKILL.md).
