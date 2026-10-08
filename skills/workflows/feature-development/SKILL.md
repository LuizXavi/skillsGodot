---
name: godot-feature-development
description: Implement a scoped Godot feature from player behavior through data, logic, presentation, and validation.
metadata:
  short-description: Implement a scoped Godot feature from player behavior through data, logic, presentation, and validation.
---

# Godot Feature Development

Translate the request into observable player behavior and acceptance conditions. Read local architecture/context and inspect neighboring implementation before choosing ownership. Identify persistence, input, UI, economy, and offline effects that the feature actually touches; avoid loading unrelated domain guidance.

Keep authoritative rules in one owner. Separate authored definitions from runtime state where useful, emit clear events for presentation, and make the smallest coherent extension to existing structure. Reuse project components and templates when they fit; adapt their assumptions instead of copying blindly. For breaking save changes, preserve and migrate existing snapshots deliberately.

Implement the complete user path, including unavailable/empty/full/error states that are part of the feature. Validate acceptance conditions and neighboring edge cases with project-appropriate checks. Open and exercise visual flows when layout or input matters. Summarize user-visible result, touched systems, verification, and concrete limitations. Route 2D UI to [godot-2d-ui](../../../godot-2d-ui/SKILL.md), saves to [godot-save-system](../../../godot-save-system/SKILL.md), and offline behavior to [godot-offline-progress](../../../godot-offline-progress/SKILL.md).
