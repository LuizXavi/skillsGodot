extends RefCounted

const CATEGORIES := ["RAW", "BARS", "ALLOYS", "GEMS", "EQUIPMENT", "CRAFTING"]
const SORTS := ["quantity", "name", "rarity", "value"]
const MAX_QUANTITY := 2147483647

var catalog: Dictionary = {}
var counts: Dictionary = {}


func define_item(id: String, name: String, category: String, rarity: int = 0, value: int = 0) -> bool:
	if id.is_empty() or name.is_empty() or not CATEGORIES.has(category) or rarity < 0 or value < 0 or catalog.has(id):
		return false
	catalog[id] = {"id": id, "name": name, "category": category, "rarity": rarity, "value": value}
	return true


func quantity(id: String) -> int:
	return int(counts.get(id, 0))


func add(id: String, amount: int) -> bool:
	if not catalog.has(id) or amount <= 0 or amount > MAX_QUANTITY - quantity(id):
		return false
	counts[id] = quantity(id) + amount
	return true


func remove(id: String, amount: int) -> bool:
	if not catalog.has(id) or amount <= 0 or quantity(id) < amount:
		return false
	var remaining := quantity(id) - amount
	if remaining == 0:
		counts.erase(id)
	else:
		counts[id] = remaining
	return true


func replace_counts(next_counts: Dictionary) -> bool:
	for id in next_counts:
		if typeof(id) != TYPE_STRING or not catalog.has(id) or typeof(next_counts[id]) != TYPE_INT or next_counts[id] < 0 or next_counts[id] > MAX_QUANTITY:
			return false
	counts = next_counts.duplicate(true)
	for id in counts.keys():
		if counts[id] == 0:
			counts.erase(id)
	return true


func list_items(category: String = "ALL", sort_by: String = "name") -> Array:
	if (category != "ALL" and not CATEGORIES.has(category)) or not SORTS.has(sort_by):
		return []
	var rows: Array = []
	for id in catalog:
		var item: Dictionary = catalog[id]
		if category == "ALL" or item["category"] == category:
			var row := item.duplicate(true)
			row["quantity"] = quantity(id)
			rows.append(row)
	rows.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		if a[sort_by] == b[sort_by]:
			return a["id"] < b["id"]
		if sort_by == "name":
			return a[sort_by] < b[sort_by]
		return a[sort_by] > b[sort_by]
	)
	return rows
