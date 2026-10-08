"""Generate a compact, architecture-oriented AI context card (stdlib only)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import config_section, config_value, md, project_files, rel, require_project, root_arg, safe_output
from dependency_mapper.map import collect_project


def _resource_path(value: str) -> str | None:
    return value[6:] if value.startswith("res://") else None


def generate(root: Path, focus: str | None = None) -> str:
    config = require_project(root)
    files = project_files(root)
    graph = collect_project(root)
    all_paths = [path for group in files.values() for path in group]
    known = {rel(path, root) for path in all_paths}
    main_scene = config_value(config_section(config, "application"), "run/main_scene") or "unknown"
    main_path = _resource_path(main_scene)
    autoloads: dict[str, str] = graph["autoloads"]
    autoload_paths = {_resource_path(value) for value in autoloads.values()}
    initial = {value for value in {main_path, *autoload_paths} if value in known}
    # Two static hops include scripts attached to the opening scene and their direct loads.
    connected = set(initial)
    for _ in range(2):
        for kind, origin, target, certainty in graph["edges"]:
            if origin not in connected or certainty == "heuristic":
                continue
            destination = _resource_path(target) or target
            if destination in known:
                connected.add(destination)
    focus_terms = [term.lower() for term in re.findall(r"[\w-]+", focus or "") if len(term) >= 2]
    matches = {rel(path, root) for path in all_paths if focus_terms and any(term in rel(path, root).lower() for term in focus_terms)}

    def score(path: Path) -> tuple[int, str]:
        relative = rel(path, root)
        lower = relative.lower()
        value = 0
        if relative in matches:
            value += 1000
        if relative == main_path:
            value += 500
        if relative in autoload_paths:
            value += 420
        if relative in connected:
            value += 320
        value += {".gd": 220, ".tscn": 140, ".tres": 35, ".res": 0}.get(path.suffix.lower(), 0)
        if any(term in lower for term in ("/core/", "player", "game", "state", "main")):
            value += 35
        if lower.startswith(("addons/", "tests/", "test/")):
            value -= 250
        if path.suffix.lower() == ".gd":
            value += min(path.stat().st_size // 1000, 35)
        return -value, lower

    selected = sorted(all_paths, key=score)
    visible = {rel(path, root) for path in selected[:28]}
    direct = [(kind, origin, target) for kind, origin, target, certainty in graph["edges"] if origin in visible and certainty != "heuristic"]
    lines = ["# AI context", "", f"Project: `{md(root.name)}`", f"Main scene: `{md(main_scene)}`", f"Focus: `{md(focus)}` (file path terms only)" if focus else "Focus: general", "", "## Scale", ""]
    lines += [f"- `{suffix}`: {len(paths)}" for suffix, paths in files.items()]
    lines += ["", "## Autoloads", ""]
    lines += [f"- `{md(name)}` → `{md(target)}`" for name, target in sorted(autoloads.items())[:20]] or ["- None declared"]
    lines += ["", "## Files to inspect first", ""]
    lines += [f"- `{md(rel(path, root))}`" for path in selected[:28]] or ["- No Godot files found"]
    if len(selected) > 28:
        lines.append(f"- … {len(selected) - 28} more omitted")
    if focus_terms and not matches:
        lines.append("- No file path matched the focus terms; showing architecture priorities.")
    lines += ["", f"## Direct static dependencies ({len(direct)} from shown files)", ""]
    lines += [f"- `{md(origin)}` — {kind} → `{md(target)}`" for kind, origin, target in direct[:16]] or ["- None detected"]
    if len(direct) > 16:
        lines.append(f"- … {len(direct) - 16} more omitted")
    lines += ["", "## Use and limits", "", f"Dynamic loads in project: {len(graph['dynamic'])}; their destinations are unresolved. This static card ranks the main scene, autoloads and linked scripts before other files. Focus checks file paths only, not source semantics. Read the relevant sources before editing. Binary `.res`, ignored trees and external links are not resolved; no source bodies or configuration secrets are included."]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Godot project root")
    parser.add_argument("--focus", help="terms to prioritize paths, e.g. inventory UI")
    parser.add_argument("--output", type=Path, help="Markdown destination (default AI_CONTEXT.md in project)")
    args = parser.parse_args()
    try:
        root = root_arg(args.project)
        safe_output(root, args.output or root / "AI_CONTEXT.md", generate(root, args.focus))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
