---
name: godot-performance-audit
description: Audit a Godot workload to locate measured frame-time, loading, rendering, or memory bottlenecks and prioritize fixes.
metadata:
  short-description: Audit a Godot workload to locate measured frame-time, loading, rendering, or memory bottlenecks and prioritize fixes.
---

# Godot Performance Audit

Define target hardware/build, representative scene, workload duration, and acceptable frame/memory budget. Capture baseline with the Godot profiler and platform tools available. Separate script, physics, rendering, loading, and allocation costs; inspect spikes and sustained behavior, not only average FPS.

Rank findings by measured cost, frequency, and player impact. Recommend focused fixes and explain tradeoffs; do not prescribe pooling, threads, or reduced fidelity without evidence. If implementing changes, isolate them so before/after runs use the same setup. Check correctness and resource lifetime after caching or asynchronous loading.

Report environment, reproducible scenario, measured bottleneck, comparison, and remaining uncertainty. State clearly when only editor/desktop measurements exist. Use [godot-performance](../../godot/performance/SKILL.md) for implementation-level optimization; use [godot-2d-ui](../../../godot-2d-ui/SKILL.md) when a large interface is the measured source.
