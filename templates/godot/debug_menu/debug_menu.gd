extends PanelContainer

# Add as a Control child. No gameplay state or autoload is required.
var _actions: Dictionary = {}
var _list: VBoxContainer


func _ready() -> void:
	visible = OS.is_debug_build()
	if not visible:
		return
	_list = VBoxContainer.new()
	add_child(_list)
	for label in _actions:
		_add_button(label)


func add_action(label: String, callback: Callable) -> bool:
	if not OS.is_debug_build() or label.is_empty() or _actions.has(label) or not callback.is_valid():
		return false
	_actions[label] = callback
	if is_node_ready():
		_add_button(label)
	return true


func run_action(label: String) -> bool:
	if not OS.is_debug_build() or not _actions.has(label) or not _actions[label].is_valid():
		return false
	_actions[label].call()
	return true


func _add_button(label: String) -> void:
	var button := Button.new()
	button.text = label
	button.pressed.connect(func() -> void: run_action(label))
	_list.add_child(button)
