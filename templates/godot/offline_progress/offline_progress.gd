extends RefCounted

# simulate(snapshot, elapsed_seconds) -> {"state": Dictionary, "summary": Dictionary}
func plan(snapshot: Dictionary, last_utc: int, now_utc: int, max_seconds: int, simulate: Callable) -> Dictionary:
	if last_utc < 0 or now_utc < 0 or max_seconds < 0 or not simulate.is_valid():
		return {"ok": false, "reason": "invalid_input"}
	if now_utc <= last_utc:
		# Keep the previous anchor so a backward clock cannot replay an interval.
		return {"ok": true, "state": snapshot.duplicate(true), "anchor_utc": last_utc, "elapsed_seconds": 0, "summary": {}, "clock_backwards": now_utc < last_utc}
	var elapsed: int = mini(now_utc - last_utc, max_seconds)
	if elapsed == 0:
		return {"ok": true, "state": snapshot.duplicate(true), "anchor_utc": now_utc, "elapsed_seconds": 0, "summary": {}, "clock_backwards": false}
	var result = simulate.call(snapshot.duplicate(true), elapsed)
	if typeof(result) != TYPE_DICTIONARY or typeof(result.get("state")) != TYPE_DICTIONARY or typeof(result.get("summary")) != TYPE_DICTIONARY:
		return {"ok": false, "reason": "simulation_failed"}
	return {"ok": true, "state": result["state"], "anchor_utc": now_utc, "elapsed_seconds": elapsed, "summary": result["summary"], "clock_backwards": false}
