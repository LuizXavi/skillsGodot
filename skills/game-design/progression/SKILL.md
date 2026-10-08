---
name: godot-progression-design
description: Plan player progression, unlock dependencies, level curves, milestones, and pacing across a game.
metadata:
  short-description: Plan player progression, unlock dependencies, level curves, milestones, and pacing across a game.
---

# Godot Progression Design

Map the progression graph and the player action that satisfies each node. Distinguish visible goals, hidden conditions, optional content, and hard gates. Check that every required node is reachable and that the player receives enough information to understand the next useful action. Avoid dead ends caused by mutually exclusive or consumed resources unless recovery is designed.

For level curves, state the formula, index origin, rounding, cap, and behavior after cap. Plot or tabulate representative values and compare the resulting play time against target pacing. Evaluate combined sources of progress and multipliers; local curve inspection can miss runaway totals. Keep progression rules deterministic and separate from display formatting.

Test threshold just below/at/above, skipped milestones, repeated claims, save/load, reset/prestige interaction, inaccessible branches, and maximum level. Confirm that UI communicates locked requirements and progress. Record whether a content gate is intentional or a balancing assumption.

For idle game curves use [idle economy](../idle-economy/SKILL.md); for reset interactions use [prestige](../prestige/SKILL.md).
