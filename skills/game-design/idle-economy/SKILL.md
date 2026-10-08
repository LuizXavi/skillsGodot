---
name: game-idle-economy
description: Design idle production and upgrade economies with explicit formulas, finite bulk purchases, caps, and payback checks.
metadata:
  short-description: Design idle production and upgrade economies with explicit formulas, finite bulk purchases, caps, and payback checks.
---

# Game Idle Economy

Write down starting currency, production rate, upgrade cost, growth rule, effects, caps, and expected session length before tuning. Simulate representative early, middle, and late states. For geometric costs, define precisely whether cost is `base * growth^level` and how a multi-buy sums levels. Handle `growth == 1` as a finite linear sum; for other ratios use a numerically stable formula and guard overflow/non-finite values.

Bulk purchases must never overspend: derive the affordable count under balance, caps, and prerequisites, then charge and apply once. Specify rounding policy and avoid repeated floating-point accumulation where integer currency is intended. Test zero production, insufficient currency, maximum level, very large requested count, growth near one, and extreme levels.

For `n` levels starting at `L`, `sum = base * r^L * (r^n - 1)/(r - 1)` when `r != 1`, or `base * n` when `r == 1`; near one, verify numerical precision against a bounded reference sum. Keep base_cost, growth_rate, income/DPS, multipliers and unlock requirements in authored data rather than scattered literals. Specify whether multipliers add or multiply before comparing builds.

Estimate payback as incremental cost divided by incremental production, with an explicit result for zero or negative production gain. Simulate the full economy because interacting multipliers, unlocks, and offline caps can change payback. Tune against intended pacing and communicate large values consistently.

For absent-time production, use [godot-offline-progress](../../../godot-offline-progress/SKILL.md). If useful, adapt the [offline progress template](../../../templates/godot/offline_progress/README.md).
