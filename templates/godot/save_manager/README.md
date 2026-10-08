# Save manager

## Purpose
Versioned JSON snapshots with sequential migrations, schema validation, a temporary write, and a previous valid backup. Loading reports `absent`, `ok`, `future`, or `corrupt`; unknown future saves are never overwritten. The script never picks a real game save path.

## Files
`save_manager.gd` — one `RefCounted` script.

## Installation
Copy to a Godot 4 project. Pass a new, game-specific path (for example `user://my_game/slot_1.json`), current schema version, default data, and a validator. Register one migration for each earlier version. Test migration with copies of old saves before release.

## Dependencies
Godot 4; no addons. The caller owns autosave scheduling and a consistent snapshot of all related state.

## Usage
```gdscript
const SaveManager = preload("res://templates/godot/save_manager/save_manager.gd")
var saves = SaveManager.new("user://my_game/slot_1.json", 2, {"coins": 0}, func(data): return data["coins"] >= 0)
saves.migrations[1] = func(old): return {"coins": int(old.get("money", 0))}
var loaded = saves.load_data()
if loaded["status"] == "ok" or loaded["status"] == "absent":
    var state = loaded["data"]
    # Apply state, then save a consistent snapshot when appropriate.
    var result = saves.save_data(state)
```

## Customization
The defaults define required keys and types; add range and ID rules in the validator. JSON data must be plain values, arrays, and string-key dictionaries. Because Godot parses JSON numbers as floats, integral values within the exact JSON range (−9,007,199,254,740,991 to +9,007,199,254,740,991) are restored as integers unless a default field is a float. Integers outside that range are rejected with `status: invalid` before writing; represent larger economy values as decimal strings and parse them with game-specific checked arithmetic. Migration results are checked against the current schema. If the primary is corrupt, a valid backup is used; a corrupt primary is retained as `.corrupt` when writing a replacement. Backup replacement and file rename are best-effort filesystem operations, not a power-loss guarantee. Do not consume irreversible rewards until the save result is `ok`. Use unique temporary paths for tests, never a player's slot.
