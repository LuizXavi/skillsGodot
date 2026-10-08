extends RefCounted

const MAX_INT := 9223372036854775807

# Pure planning: caller commits returned counts and job in one state snapshot.
var recipes: Dictionary = {}


func define_recipe(id: String, ingredients: Dictionary, outputs: Dictionary, duration_seconds: int = 0, requirements: Array = []) -> bool:
	if id.is_empty() or recipes.has(id) or ingredients.is_empty() or outputs.is_empty() or duration_seconds < 0:
		return false
	for group in [ingredients, outputs]:
		for item_id in group:
			if typeof(item_id) != TYPE_STRING or item_id.is_empty() or typeof(group[item_id]) != TYPE_INT or group[item_id] <= 0:
				return false
	for requirement in requirements:
		if typeof(requirement) != TYPE_STRING or requirement.is_empty():
			return false
	recipes[id] = {"id": id, "ingredients": ingredients.duplicate(true), "outputs": outputs.duplicate(true), "duration_seconds": duration_seconds, "requirements": requirements.duplicate()}
	return true


func plan_start(id: String, counts: Dictionary, unlocked: Array, now_utc: int, job_id: String) -> Dictionary:
	if not recipes.has(id) or job_id.is_empty() or now_utc < 0:
		return {"ok": false, "reason": "invalid_recipe_or_job"}
	var recipe: Dictionary = recipes[id]
	if now_utc > MAX_INT - recipe["duration_seconds"]:
		return {"ok": false, "reason": "time_overflow"}
	for requirement in recipe["requirements"]:
		if not unlocked.has(requirement):
			return {"ok": false, "reason": "locked"}
	var next_counts := counts.duplicate(true)
	for item_id in recipe["ingredients"]:
		var amount: int = recipe["ingredients"][item_id]
		if typeof(next_counts.get(item_id, 0)) != TYPE_INT or next_counts.get(item_id, 0) < amount:
			return {"ok": false, "reason": "insufficient"}
		next_counts[item_id] -= amount
		if next_counts[item_id] == 0:
			next_counts.erase(item_id)
	var job := {"job_id": job_id, "recipe_id": id, "finish_utc": now_utc + recipe["duration_seconds"], "outputs": recipe["outputs"].duplicate(true)}
	return {"ok": true, "counts": next_counts, "job": job}


func plan_finish(job: Dictionary, counts: Dictionary, now_utc: int) -> Dictionary:
	if typeof(job.get("finish_utc")) != TYPE_INT or now_utc < job["finish_utc"] or typeof(job.get("outputs")) != TYPE_DICTIONARY:
		return {"ok": false, "reason": "not_ready"}
	var next_counts := counts.duplicate(true)
	for item_id in job["outputs"]:
		var amount = job["outputs"][item_id]
		if typeof(item_id) != TYPE_STRING or typeof(amount) != TYPE_INT or amount <= 0 or typeof(next_counts.get(item_id, 0)) != TYPE_INT or next_counts.get(item_id, 0) < 0 or next_counts.get(item_id, 0) > 2147483647 - amount:
			return {"ok": false, "reason": "invalid_output"}
		next_counts[item_id] = next_counts.get(item_id, 0) + amount
	return {"ok": true, "counts": next_counts}
