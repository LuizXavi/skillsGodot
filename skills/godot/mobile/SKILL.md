---
name: godot-mobile
description: Design and validate Godot game behavior for touch devices, Android lifecycle, safe areas, variable screens, and memory limits.
metadata:
  short-description: Design and validate Godot game behavior for touch devices, Android lifecycle, safe areas, variable screens, and memory limits.
---

# Godot Mobile

Identify target Android versions, aspect ratios, orientation policy, renderer, and minimum device before changing settings. Treat cutouts, rounded corners, gesture regions, and system bars as usable-area constraints; anchor interactive UI inside the safe area and validate it on narrow and tall screens.

Make touch targets large enough for fingers, avoid hover-only information, and ensure multi-touch does not accidentally trigger duplicate actions. Handle touch cancellation, app pause/resume, focus loss, and interrupted gestures. Persist important state at safe checkpoints because mobile may suspend or terminate the process without a normal close callback.

Set resolution/stretch policy intentionally and test multiple aspect ratios, including 9:16 portrait when applicable; do not assume desktop window scaling predicts Android layout. Test finger scrolling and orientation changes without losing selection or triggering buttons under the gesture. Track texture/audio memory, scene instantiation spikes, battery use, and sustained frame time on representative hardware. Release unused large resources and avoid loading every level or asset at startup. Profile before lowering visual quality globally.

Validate an exported build on device: launch, orientation, safe areas, touch flow, pause/resume, low-memory recovery where practical, and performance during a representative session. A desktop emulator or headless run cannot establish device behavior. For 2D Control layout details, use [godot-2d-ui](../../../godot-2d-ui/SKILL.md); for persistence, [godot-save-system](../../../godot-save-system/SKILL.md).
