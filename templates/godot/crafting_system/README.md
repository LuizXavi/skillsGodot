# Crafting system

## Purpose
Defines recipes by stable ID, ingredients, outputs, duration, and requirement IDs. `plan_start` checks all inputs and returns a new inventory plus a job; `plan_finish` returns a new inventory when that job is ready. Neither function mutates the caller's state.

## Files
`crafting_system.gd` — one `RefCounted` script.

## Installation
Copy into a Godot 4 project. Define recipes from your data catalog. Store `counts` and a list or dictionary of active jobs in your game's saved state.

## Dependencies
Godot 4. Compatible with `inventory_manager` count dictionaries; no direct script dependency.

## Usage
```gdscript
const Crafting = preload("res://templates/godot/crafting_system/crafting_system.gd")
var crafting = Crafting.new()
crafting.define_recipe("smelt_iron", {"iron_ore": 2}, {"iron_bar": 1}, 30, ["furnace"])
var start = crafting.plan_start("smelt_iron", inventory.counts, ["furnace"], Time.get_unix_time_from_system(), "job-1")
if start["ok"]:
    # Commit start["counts"] AND start["job"] in the same game/save transaction.
    pass
```

## Customization
Use a collision-free `job_id` and reject IDs already present in your job store. On completion, commit `plan_finish(...)["counts"]` and removal of that job together; this prevents duplicate output. The caller controls clocks, concurrent jobs, storage caps, and whether a failed save blocks spending. A start time plus duration beyond Godot's signed 64-bit integer range returns `time_overflow`. Zero duration still creates a job that can be completed immediately.
