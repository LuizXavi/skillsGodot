extends RefCounted

# Pure state transition. State shape: {"run": Dictionary, "permanent": Dictionary}.
func plan_reset(state: Dictionary, run_defaults: Dictionary, required_run_score: int, permanent_reward: Dictionary) -> Dictionary:
	if typeof(state.get("run")) != TYPE_DICTIONARY or typeof(state.get("permanent")) != TYPE_DICTIONARY:
		return {"ok": false, "reason": "invalid_state"}
	if typeof(state["run"].get("score")) != TYPE_INT or state["run"]["score"] < required_run_score or required_run_score < 0:
		return {"ok": false, "reason": "threshold"}
	var next_state := state.duplicate(true)
	for key in permanent_reward:
		if typeof(key) != TYPE_STRING or typeof(permanent_reward[key]) != TYPE_INT or permanent_reward[key] < 0 or typeof(next_state["permanent"].get(key, 0)) != TYPE_INT or next_state["permanent"].get(key, 0) > 2147483647 - permanent_reward[key]:
			return {"ok": false, "reason": "invalid_reward"}
		next_state["permanent"][key] = next_state["permanent"].get(key, 0) + permanent_reward[key]
	next_state["run"] = run_defaults.duplicate(true)
	return {"ok": true, "state": next_state}
