---
name: godot-architecture
description: Choose scene composition, scripts, Resources, signals, groups, and Autoload boundaries for Godot projects. Use when establishing or changing system structure.
metadata:
  short-description: Choose scene composition, scripts, Resources, signals, groups, and Autoload boundaries for Godot projects
---

# Godot Architecture

Inspect `project.godot`, scene ownership, data flow, and local architecture notes first. Prefer composition of small Nodes/scenes for runtime behavior and Resources for authored configuration or reusable definitions. Use inheritance when a stable “is-a” contract genuinely shares behavior; avoid deep scene/script hierarchies that make overrides and ownership hard to trace.

Keep DATA (definitions and state), LOGIC (rules and transitions), and PRESENTATION (nodes rendering state) conceptually distinct, even when a small feature keeps them in one script. Signals communicate events to interested peers; direct references are appropriate for stable, local ownership. Groups suit cross-cutting discovery/actions, not hidden dependency injection.

Use Autoloads for truly global, long-lived services or state with clear ownership, such as scene navigation or a deliberately centralized save service. Do not turn each gameplay system into a singleton. Prefer a scene-owned manager or injected reference when lifetime is local. Document who creates, owns, mutates, and frees each object; identify save boundaries and test seams.

Before restructuring, map call sites, scene/resource references, and `.gd.uid` files. Make the smallest structural change that meets the behavior. Validate the actual project version and relevant scene load/run path. For broad game work, see [Godot development](../../../godot-game-development/SKILL.md); read the target project's architecture notes when available, or use the [architecture template](../../../docs/ARCHITECTURE_TEMPLATE.md) to record missing decisions.
