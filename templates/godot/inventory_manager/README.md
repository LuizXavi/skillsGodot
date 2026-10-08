# Inventory manager

## Purpose
Small ID based inventory with six item categories, `ALL` filtering, and quantity, name, rarity, or value sorting. Numeric sorts descend; names ascend; ID breaks ties. Zero quantity items remain visible in the catalog.

## Files
`inventory_manager.gd` — one `RefCounted` script.

## Installation
Copy the script into your Godot 4 project and preload or instantiate it. Define each stable item ID from your catalog at startup; save only `counts`.

## Dependencies
Godot 4; no autoloads or addons.

## Usage
```gdscript
const Inventory = preload("res://templates/godot/inventory_manager/inventory_manager.gd")
var inventory = Inventory.new()
inventory.define_item("iron_ore", "Iron ore", "RAW", 1, 2)
inventory.add("iron_ore", 5)
var raw_items = inventory.list_items("RAW", "quantity")
```

## Customization
Add categories in `CATEGORIES`; keep IDs stable across saves. `replace_counts` rejects unknown IDs and negative values, so migrate old IDs before loading. Integer quantities are capped at 2,147,483,647 per item.
