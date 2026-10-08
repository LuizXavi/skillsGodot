# Godot 4 smoke example

## Purpose
Runs the real template scripts in an isolated temporary Godot project. It checks inventory filtering, crafting without partial consumption, prestige preservation, bounded and repeatable offline progress, save round trips/migration/corruption/backup, and debug gating.

## Files
`project.godot`, `smoke_test.gd`, and `run.ps1`.

## Installation
No installation into a game is required. On Windows, use PowerShell with an installed Godot 4 executable:
```powershell
.\examples\smoke\run.ps1 -Godot 'C:\path\to\Godot_v4.x.exe'
```

## Dependencies
Godot 4 and PowerShell. The runner copies the example and `templates/` into a unique directory under the OS temporary folder, imports that project, runs the test, checks `TOOLKIT_SMOKE: OK`, and cleans up that exact directory.

## Usage
Run from any working directory. A nonzero process exit or a `SCRIPT ERROR` fails the smoke test.

## Customization
Adapt `smoke_test.gd` with domain rules when using these templates in a game. The temporary save path is passed by the runner; never point this example at an existing player save.
