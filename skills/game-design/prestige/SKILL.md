---
name: godot-prestige-design
description: Design prestige resets, permanent rewards, scaling, and replay pacing with explicit carryover and exploit rules.
metadata:
  short-description: Design prestige resets, permanent rewards, scaling, and replay pacing with explicit carryover and exploit rules.
---

# Godot Prestige Design

Specify exactly what resets, what persists, what is granted, and when the action becomes irreversible. Show the player an estimate before confirmation, based on current state and documented rounding. Define whether rewards depend on lifetime peak, current run, elapsed time, or another measure; prevent repeated claims from the same run.

Keep reset calculation pure: take a validated snapshot and return reward plus new state. Apply the result once through a versioned transition, including run identifier or equivalent idempotency marker where saves or interruptions could repeat it. List currencies, upgrades, inventory, unlocked content, achievements, and queued production explicitly rather than relying on “reset everything” traversal.

Evaluate time-to-next-prestige and first-run versus repeat-run pacing. Ensure early rewards do not make later choices meaningless. Test zero reward, threshold boundaries, rounding, repeated activation, save interruption, maximum reward, and migration of older saves. Communicate permanent gains and lost progress before commitment.

For project implementation, pair with [godot-save-system](../../../godot-save-system/SKILL.md) and the [prestige system template](../../../templates/godot/prestige_system/README.md).
