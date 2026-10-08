# Prestige system

## Purpose
Plans a run reset after a score threshold while retaining all permanent state and adding nonnegative integer rewards. It returns a copy, leaving the original state untouched.

## Files
`prestige_system.gd` — one `RefCounted` script.

## Installation
Copy into a Godot 4 project. Keep run state and permanent state in separate dictionaries and save them together.

## Dependencies
Godot 4; no addons.

## Usage
```gdscript
const Prestige = preload("res://templates/godot/prestige_system/prestige_system.gd")
var result = Prestige.new().plan_reset(state, {"score": 0, "level": 1}, 1000, {"tokens": 1})
if result["ok"]:
    # Save result["state"] before enabling irreversible purchases.
    pass
```

## Customization
Replace the score gate with your own eligibility rules if needed. Include pending jobs, timers, and run inventory in the run dictionary or clear them explicitly in the same transaction. A caller must prevent repeating the same prestige on an old snapshot after a failed save or backup rollback.
