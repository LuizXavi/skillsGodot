---
name: game-inventory-design
description: Design inventory rules, capacity, stacking, item identity, sorting, and player feedback for a game economy.
metadata:
  short-description: Design inventory rules, capacity, stacking, item identity, sorting, and player feedback for a game economy.
---

# Game Inventory Design

Define the player-facing rules first: what occupies a slot, stack limits, weight or volume (if any), equipment interaction, overflow behavior, and whether locked items can move or be sold. Decide stable item identity separately from localized display names. Define how upgrades affect existing contents and what happens when capacity shrinks below current usage.

Model transfers as atomic operations: validate source, destination, quantity, stack compatibility, and capacity before mutating either side. Partial transfer should return the exact moved amount. Avoid losing items when a destination is full or a transaction fails. Keep authoritative inventory state outside UI; expose change events so views refresh only affected rows where practical.

Test empty/full inventory, max and over-max stacks, split/merge, duplicate IDs, invalid quantities, upgrade/downgrade capacity, save/load, and two-sided transfer failure. Make unavailable actions legible and preserve focus/input behavior. Reuse [inventory manager template](../../../templates/godot/inventory_manager/README.md) if it matches the project. For 2D interface implementation see [godot-2d-ui](../../../godot-2d-ui/SKILL.md); for persistence see [godot-save-system](../../../godot-save-system/SKILL.md).
