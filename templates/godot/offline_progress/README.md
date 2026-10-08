# Offline progress

## Purpose
Plans bounded progress between two injected UTC timestamps. Negative time grants nothing and keeps the old anchor. Excess time grants at most `max_seconds` and moves the anchor to `now_utc`, discarding the excess. The returned summary can explain the grant to the player.

## Files
`offline_progress.gd` — one `RefCounted` script.

## Installation
Copy into a Godot 4 project. Persist `anchor_utc` in the same snapshot as every reward and job state. Use `int(Time.get_unix_time_from_system())` for the saved session timestamp. Call the planner only for periods your online simulation has not already counted.

## Dependencies
Godot 4; no network or addons. A game-specific simulation callback is required.

## Usage
```gdscript
const Offline = preload("res://templates/godot/offline_progress/offline_progress.gd")
var result = Offline.new().plan(state, saved_anchor, int(Time.get_unix_time_from_system()), 8 * 3600,
    func(old_state, seconds):
        old_state["coins"] += seconds # Only valid for a constant, uncapped rate.
        return {"state": old_state, "summary": {"coins": seconds}})
if result["ok"]:
    # Save result["state"] and result["anchor_utc"] together before spending gains.
    pass
```

## Customization
Choose a cap from your game's economy. The callback must handle ingredients, capacity, jobs, and rate changes according to your online rules; this template does not assume multiplication is universally correct. A backward clock keeps the old anchor, so progress may remain at zero until the clock catches up; decide whether your game needs a manual recovery policy for large adjustments. Save failure must leave the original snapshot active and block spending of the planned gain. Replaying an older backup can replay time; stronger guarantees need an external authority. Local wall clocks can be changed by the player.
