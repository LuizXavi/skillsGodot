extends SceneTree

const Inventory = preload("res://templates/godot/inventory_manager/inventory_manager.gd")
const SaveManager = preload("res://templates/godot/save_manager/save_manager.gd")
const Crafting = preload("res://templates/godot/crafting_system/crafting_system.gd")
const Prestige = preload("res://templates/godot/prestige_system/prestige_system.gd")
const Offline = preload("res://templates/godot/offline_progress/offline_progress.gd")
const DebugMenu = preload("res://templates/godot/debug_menu/debug_menu.gd")

var failures := 0
var test_dir := ""


func _initialize() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--test-dir="):
			test_dir = arg.trim_prefix("--test-dir=")
	if test_dir.is_empty():
		push_error("Missing isolated --test-dir")
		quit(1)
		return
	_test_inventory_and_crafting()
	_test_prestige_and_offline()
	_test_save()
	_test_debug_menu()
	if failures == 0:
		print("TOOLKIT_SMOKE: OK")
		quit(0)
	else:
		push_error("TOOLKIT_SMOKE: %d failures" % failures)
		quit(1)


func _check(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		push_error(message)


func _test_inventory_and_crafting() -> void:
	var inventory = Inventory.new()
	_check(inventory.define_item("ore", "Ore", "RAW", 1, 2), "define ore")
	_check(inventory.define_item("bar", "Bar", "BARS", 2, 5), "define bar")
	_check(not inventory.define_item("bad", "Bad", "OTHER"), "reject category")
	_check(inventory.add("ore", 5), "add ore")
	_check(not inventory.remove("ore", 6) and inventory.quantity("ore") == 5, "no overdraft")
	_check(inventory.list_items("RAW", "quantity").size() == 1, "category filter")
	_check(inventory.list_items("ALL", "value")[0]["id"] == "bar", "value sort")
	_check(inventory.list_items("ALL", "quantity")[0]["id"] == "ore", "quantity sort")
	_check(inventory.list_items("ALL", "name")[0]["id"] == "bar", "name sort")
	_check(inventory.list_items("ALL", "rarity")[0]["id"] == "bar", "rarity sort")
	for category in Inventory.CATEGORIES:
		var expected := 1 if category == "RAW" or category == "BARS" else 0
		_check(inventory.list_items(category).size() == expected, "supported category " + category)
	_check(not inventory.replace_counts({"unknown": 4}), "reject unknown save id")
	var boundary = Inventory.new()
	boundary.define_item("ore", "Ore", "RAW")
	boundary.define_item("bar", "Bar", "BARS")
	_check(boundary.replace_counts({"ore": Inventory.MAX_QUANTITY}), "import maximum quantity")
	_check(not boundary.add("ore", 1) and boundary.quantity("ore") == Inventory.MAX_QUANTITY, "addition respects maximum quantity")
	_check(not boundary.replace_counts({"ore": 1, "bar": Inventory.MAX_QUANTITY + 1}) and boundary.quantity("ore") == Inventory.MAX_QUANTITY and boundary.quantity("bar") == 0, "invalid import is atomic")
	var crafting = Crafting.new()
	_check(crafting.define_recipe("smelt", {"ore": 2}, {"bar": 1}, 30, ["furnace"]), "define recipe")
	var locked = crafting.plan_start("smelt", inventory.counts, [], 100, "job-1")
	_check(not locked["ok"] and inventory.quantity("ore") == 5, "locked recipe does not consume")
	var start = crafting.plan_start("smelt", inventory.counts, ["furnace"], 100, "job-1")
	_check(start["ok"] and start["counts"]["ore"] == 3 and inventory.quantity("ore") == 5, "atomic start plan")
	_check(not crafting.plan_finish(start["job"], start["counts"], 129)["ok"], "duration gate")
	var finished = crafting.plan_finish(start["job"], start["counts"], 130)
	_check(finished["ok"] and finished["counts"]["bar"] == 1, "finish output")
	_check(not crafting.plan_start("smelt", {"ore": 1}, ["furnace"], 100, "job-2")["ok"], "insufficient input")
	_check(crafting.define_recipe("alloy", {"ore": 2, "bar": 1}, {"bar": 2}), "define multi-input recipe")
	_check(not crafting.plan_start("alloy", inventory.counts, [], 100, "job-3")["ok"] and inventory.quantity("ore") == 5, "late missing ingredient cannot partially consume")
	var overflow = crafting.plan_start("smelt", inventory.counts, ["furnace"], Crafting.MAX_INT - 29, "job-overflow")
	_check(not overflow["ok"] and overflow["reason"] == "time_overflow" and inventory.quantity("ore") == 5, "job timestamp overflow rejected")


func _test_prestige_and_offline() -> void:
	var prestige = Prestige.new()
	var state := {"run": {"score": 120, "ore": 9}, "permanent": {"tokens": 2, "unlock": 1}}
	_check(not prestige.plan_reset(state, {"score": 0, "ore": 0}, 121, {"tokens": 1})["ok"], "prestige threshold")
	var reset = prestige.plan_reset(state, {"score": 0, "ore": 0}, 100, {"tokens": 1})
	_check(reset["ok"] and reset["state"]["run"]["ore"] == 0 and reset["state"]["permanent"]["tokens"] == 3 and reset["state"]["permanent"]["unlock"] == 1, "preserve permanent state")
	_check(state["run"]["ore"] == 9, "prestige plan does not mutate source")
	var offline = Offline.new()
	var simulate = func(old_state: Dictionary, seconds: int) -> Dictionary:
		old_state["coins"] += seconds
		return {"state": old_state, "summary": {"coins": seconds}}
	var before := {"coins": 0}
	var grant = offline.plan(before, 100, 1000, 60, simulate)
	_check(grant["ok"] and grant["state"]["coins"] == 60 and grant["anchor_utc"] == 1000 and grant["summary"]["coins"] == 60, "offline cap and summary")
	var again = offline.plan(grant["state"], grant["anchor_utc"], 1000, 60, simulate)
	_check(again["elapsed_seconds"] == 0 and again["state"]["coins"] == 60, "offline idempotence")
	var backwards = offline.plan(grant["state"], 1000, 900, 60, simulate)
	_check(backwards["anchor_utc"] == 1000 and backwards["clock_backwards"], "backward clock anchor")
	_check(before["coins"] == 0, "offline plan does not mutate source")


func _test_save() -> void:
	var save_path := test_dir.path_join("slot.json")
	var defaults := {"inventory": {"ore": 0}, "anchor_utc": 0}
	var validate = func(data: Dictionary) -> bool:
		return data["inventory"].size() == 1 and typeof(data["inventory"].get("ore")) == TYPE_INT and data["inventory"]["ore"] >= 0 and data["anchor_utc"] >= 0
	var saves = SaveManager.new(save_path, 2, defaults, validate)
	saves.migrations[1] = func(old: Dictionary) -> Dictionary:
		return {"inventory": {"ore": old.get("ore", 0)}, "anchor_utc": 0}
	_check(saves.load_data()["status"] == "absent", "missing save defaults")
	_check(saves.save_data({"inventory": {"ore": 2}, "anchor_utc": 100})["status"] == "ok", "save first generation")
	_check(saves.save_data({"inventory": {"ore": 3}, "anchor_utc": 200})["status"] == "ok", "save second generation")
	_check(saves.load_data()["data"]["inventory"]["ore"] == 3, "round trip")
	_write(save_path, "truncated")
	var recovered = saves.load_data()
	_check(recovered["status"] == "ok" and recovered["data"]["inventory"]["ore"] == 2, "valid backup recovery")
	_check(saves.save_data({"inventory": {"ore": 4}, "anchor_utc": 300})["status"] == "ok", "replace corrupt primary")
	_check(saves.load_data()["data"]["inventory"]["ore"] == 4, "replacement is readable")
	var offline = Offline.new()
	var loaded = saves.load_data()["data"]
	var grant = offline.plan(loaded, loaded["anchor_utc"], 305, 60, func(old: Dictionary, seconds: int) -> Dictionary:
		old["inventory"]["ore"] += seconds
		return {"state": old, "summary": {"ore": seconds}})
	var committed: Dictionary = grant["state"]
	committed["anchor_utc"] = grant["anchor_utc"]
	_check(saves.save_data(committed)["status"] == "ok", "persist offline gain with anchor")
	var reloaded = saves.load_data()["data"]
	_check(reloaded["inventory"]["ore"] == 9 and offline.plan(reloaded, reloaded["anchor_utc"], 305, 60, func(old, seconds): return {"state": old, "summary": {}})["elapsed_seconds"] == 0, "offline gain saved exactly once")
	_check(saves.save_data({"inventory": {"unknown": 1}, "anchor_utc": 300})["status"] == "invalid", "schema rejects unknown ID")
	var limits_path := test_dir.path_join("integer_limits.json")
	var limits = SaveManager.new(limits_path, 1, {"value": 0, "nested": []})
	_check(limits.save_data({"value": 9007199254740991, "nested": []})["status"] == "ok", "maximum exact JSON integer saves")
	_check(limits.load_data()["data"]["value"] == 9007199254740991, "maximum exact JSON integer round trip")
	for unsafe_value in [9007199254740993, -9007199254740993, 9223372036854775807, -9223372036854775807 - 1]:
		_check(limits.save_data({"value": unsafe_value, "nested": []})["status"] == "invalid", "reject unsafe JSON integer")
		_check(limits.load_data()["data"]["value"] == 9007199254740991, "unsafe integer did not alter save")
	_check(limits.save_data({"value": 0, "nested": [9007199254740993]})["status"] == "invalid", "reject nested unsafe integer")
	_check(limits.save_data({"value": -9007199254740991, "nested": []})["status"] == "ok", "minimum exact JSON integer saves")
	_check(limits.load_data()["data"]["value"] == -9007199254740991, "minimum exact JSON integer round trip")
	var migration_path := test_dir.path_join("old.json")
	_write_envelope(migration_path, 1, 1, {"ore": 7})
	var migrated = SaveManager.new(migration_path, 2, defaults, validate)
	migrated.migrations[1] = saves.migrations[1]
	var old = migrated.load_data()
	_check(old["status"] == "ok" and old["migrated"] and old["data"]["inventory"]["ore"] == 7, "sequential migration")
	var future_path := test_dir.path_join("future.json")
	_write_envelope(future_path, 3, 1, {"inventory": {"ore": 8}, "anchor_utc": 0})
	var future = SaveManager.new(future_path, 2, defaults, validate)
	_check(future.load_data()["status"] == "future" and future.save_data(defaults)["status"] == "future", "future version preserved")
	_write_envelope(future_path + ".bak", 2, 2, {"inventory": {"ore": 1}, "anchor_utc": 0})
	_check(future.load_data()["status"] == "future" and future.save_data(defaults)["status"] == "future", "future primary blocks backup downgrade")
	var stale_path := test_dir.path_join("stale.json")
	_write_envelope(stale_path, 2, 1, {"inventory": {"ore": 1}, "anchor_utc": 0})
	_write_envelope(stale_path + ".bak", 2, 2, {"inventory": {"ore": 2}, "anchor_utc": 0})
	var stale = SaveManager.new(stale_path, 2, defaults, validate)
	_check(stale.save_data({"inventory": {"ore": 3}, "anchor_utc": 0})["status"] == "ok", "save after newer backup")
	_check(stale.load_data()["data"]["inventory"]["ore"] == 3, "new generation promoted")
	var corrupt_path := test_dir.path_join("corrupt.json")
	_write(corrupt_path, "{")
	var corrupt = SaveManager.new(corrupt_path, 2, defaults, validate)
	_check(corrupt.load_data()["status"] == "corrupt", "corruption is not absence")


func _test_debug_menu() -> void:
	var menu = DebugMenu.new()
	var calls := [0]
	var registered = menu.add_action("test", func(): calls[0] += 1)
	root.add_child(menu)
	_check(registered == OS.is_debug_build(), "debug registration gate")
	if OS.is_debug_build():
		_check(menu.run_action("test") and calls[0] == 1 and menu.visible, "debug callback")
	else:
		_check(not menu.run_action("test") and not menu.visible, "release callback gate")
	menu.queue_free()


func _write(path: String, contents: String) -> void:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		_check(false, "fixture write")
		return
	file.store_string(contents)
	file.close()


func _write_envelope(path: String, schema_version: int, generation: int, data: Dictionary) -> void:
	var payload := JSON.stringify(data)
	_write(path, JSON.stringify({"version": schema_version, "generation": generation, "payload": payload, "sha256": payload.sha256_text()}))
