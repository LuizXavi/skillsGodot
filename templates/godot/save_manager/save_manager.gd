extends RefCounted

const MAX_SAFE_JSON_INT := 9007199254740991

# Use a game-specific path. This template never chooses an existing save slot.
var path: String
var version: int
var defaults: Dictionary
var validator: Callable
var migrations: Dictionary = {} # from_version -> Callable(data) returning Dictionary


func _init(save_path: String, schema_version: int, default_data: Dictionary, validate: Callable = Callable()) -> void:
	path = save_path
	version = schema_version
	defaults = default_data.duplicate(true)
	validator = validate


func load_data() -> Dictionary:
	var primary := _read_candidate(path)
	var backup := _read_candidate(path + ".bak")
	if primary["status"] == "future" or backup["status"] == "future":
		return {"status": "future", "data": {}}
	var chosen: Dictionary = {}
	for candidate in [primary, backup]:
		if candidate["status"] == "ok" and (chosen.is_empty() or candidate["generation"] > chosen["generation"]):
			chosen = candidate
	if not chosen.is_empty():
		return {"status": "ok", "data": chosen["data"].duplicate(true), "source": chosen["source"], "generation": chosen["generation"], "migrated": chosen["migrated"]}
	if primary["status"] == "absent" and backup["status"] == "absent":
		return {"status": "absent", "data": defaults.duplicate(true)}
	return {"status": "corrupt", "data": {}}


func save_data(data: Dictionary) -> Dictionary:
	if version < 1 or version > MAX_SAFE_JSON_INT or not _valid(data):
		return {"status": "invalid"}
	var existing := load_data()
	if existing["status"] == "future":
		return {"status": "future"}
	var generation: int = int(existing.get("generation", 0)) + 1
	if generation > MAX_SAFE_JSON_INT:
		return {"status": "invalid"}
	var payload := JSON.stringify(data)
	var envelope := JSON.stringify({"version": version, "generation": generation, "payload": payload, "sha256": payload.sha256_text()})
	var absolute := ProjectSettings.globalize_path(path)
	var parent := absolute.get_base_dir()
	if DirAccess.make_dir_recursive_absolute(parent) != OK:
		return {"status": "write_failed"}
	var temp := absolute + ".tmp"
	var file := FileAccess.open(temp, FileAccess.WRITE)
	if file == null:
		return {"status": "write_failed"}
	file.store_string(envelope)
	file.flush()
	var write_error := file.get_error()
	file.close()
	if write_error != OK or _read_candidate(temp)["status"] != "ok":
		return {"status": "write_failed"}
	var primary := _read_candidate(absolute)
	var backup := _read_candidate(absolute + ".bak")
	if primary["status"] == "ok" and (backup["status"] != "ok" or primary["generation"] >= backup["generation"]):
		if FileAccess.file_exists(absolute + ".bak") and DirAccess.remove_absolute(absolute + ".bak") != OK:
			return {"status": "write_failed"}
		if DirAccess.rename_absolute(absolute, absolute + ".bak") != OK:
			return {"status": "write_failed"}
	elif FileAccess.file_exists(absolute):
		# Keep a corrupt original for inspection until the new snapshot is verified.
		if FileAccess.file_exists(absolute + ".corrupt"):
			DirAccess.remove_absolute(absolute + ".corrupt")
		if DirAccess.rename_absolute(absolute, absolute + ".corrupt") != OK:
			return {"status": "write_failed"}
	if DirAccess.rename_absolute(temp, absolute) != OK:
		return {"status": "write_failed"}
	return {"status": "ok", "generation": generation}


func _read_candidate(candidate_path: String) -> Dictionary:
	if not FileAccess.file_exists(candidate_path):
		return {"status": "absent"}
	var file := FileAccess.open(candidate_path, FileAccess.READ)
	if file == null:
		return {"status": "corrupt"}
	var raw := file.get_as_text()
	file.close()
	var envelope_parser := JSON.new()
	if envelope_parser.parse(raw) != OK:
		return {"status": "corrupt"}
	var envelope = envelope_parser.data
	if typeof(envelope) != TYPE_DICTIONARY:
		return {"status": "corrupt"}
	if not _whole_number(envelope.get("version")) or not _whole_number(envelope.get("generation")) or typeof(envelope.get("payload")) != TYPE_STRING or typeof(envelope.get("sha256")) != TYPE_STRING:
		return {"status": "corrupt"}
	if envelope["version"] < 1 or envelope["generation"] < 1 or envelope["payload"].sha256_text() != envelope["sha256"]:
		return {"status": "corrupt"}
	if envelope["version"] > version:
		return {"status": "future"}
	var payload_parser := JSON.new()
	if payload_parser.parse(envelope["payload"]) != OK:
		return {"status": "corrupt"}
	var data = payload_parser.data
	if typeof(data) != TYPE_DICTIONARY:
		return {"status": "corrupt"}
	var old_version: int = int(envelope["version"])
	var migrated := old_version != version
	# JSON represents numbers as floats; migrate/validate after strict integer coercion.
	data = _coerce_json_numbers(data, defaults)
	while old_version < version:
		if not migrations.has(old_version) or typeof(migrations[old_version]) != TYPE_CALLABLE or not migrations[old_version].is_valid():
			return {"status": "corrupt"}
		data = migrations[old_version].call(data.duplicate(true))
		if typeof(data) != TYPE_DICTIONARY:
			return {"status": "corrupt"}
		old_version += 1
	data = _coerce_json_numbers(data, defaults)
	if not _valid(data):
		return {"status": "corrupt"}
	return {"status": "ok", "data": data, "generation": int(envelope["generation"]), "source": candidate_path, "migrated": migrated}


func _whole_number(value: Variant) -> bool:
	return (typeof(value) == TYPE_INT and value >= -MAX_SAFE_JSON_INT and value <= MAX_SAFE_JSON_INT) or (typeof(value) == TYPE_FLOAT and not is_nan(value) and not is_inf(value) and absf(value) <= float(MAX_SAFE_JSON_INT) and floorf(value) == value)


func _coerce_json_numbers(value: Variant, shape: Variant = null) -> Variant:
	if typeof(value) == TYPE_FLOAT and typeof(shape) != TYPE_FLOAT and _whole_number(value):
		return int(value)
	if typeof(value) == TYPE_DICTIONARY:
		for key in value:
			var child_shape = shape.get(key) if typeof(shape) == TYPE_DICTIONARY else null
			value[key] = _coerce_json_numbers(value[key], child_shape)
	elif typeof(value) == TYPE_ARRAY:
		for index in range(value.size()):
			var element_shape = shape[0] if typeof(shape) == TYPE_ARRAY and not shape.is_empty() else null
			value[index] = _coerce_json_numbers(value[index], element_shape)
	return value


func _valid(data: Dictionary) -> bool:
	if not _plain(data) or not _matches_defaults(data, defaults):
		return false
	return not validator.is_valid() or validator.call(data) == true


func _matches_defaults(value: Dictionary, shape: Dictionary) -> bool:
	for key in shape:
		if not value.has(key) or typeof(value[key]) != typeof(shape[key]):
			return false
		if typeof(shape[key]) == TYPE_DICTIONARY and not _matches_defaults(value[key], shape[key]):
			return false
	return true


func _plain(value: Variant) -> bool:
	match typeof(value):
		TYPE_NIL, TYPE_BOOL, TYPE_STRING:
			return true
		TYPE_INT:
			return value >= -MAX_SAFE_JSON_INT and value <= MAX_SAFE_JSON_INT
		TYPE_FLOAT:
			return not is_nan(value) and not is_inf(value)
		TYPE_ARRAY:
			for element in value:
				if not _plain(element):
					return false
			return true
		TYPE_DICTIONARY:
			for key in value:
				if typeof(key) != TYPE_STRING or not _plain(value[key]):
					return false
			return true
	return false
