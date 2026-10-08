# Debug menu

## Purpose
Tiny `PanelContainer` that displays named callback buttons in debug builds. It becomes invisible and rejects actions in release builds. The menu does not know a game's runtime or state model.

## Files
`debug_menu.gd` — one `Control` script.

## Installation
Copy into a Godot 4 project, attach it to a `PanelContainer` in a debug scene or instantiate it from code, then add it under a `Control` parent. Keep production logic outside the callbacks.

## Dependencies
Godot 4 UI nodes; no autoloads or addons.

## Usage
```gdscript
const DebugMenu = preload("res://templates/godot/debug_menu/debug_menu.gd")
var menu = DebugMenu.new()
add_child(menu)
menu.add_action("Grant test ore", func(): grant_test_ore())
```

## Customization
Style the `PanelContainer` and buttons with your theme, or gate visibility more tightly in your scene. `OS.is_debug_build()` is checked on registration and invocation, so an exported release cannot trigger these callbacks through this menu. Do not put secrets in debug callbacks or ship unrelated debug commands elsewhere.
