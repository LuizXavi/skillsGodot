"""Create a bounded Markdown inventory of a Godot project (Python stdlib only)."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import config_section, config_value, md, project_files, read_text, rel, require_project, root_arg, safe_output


def snapshot(root: Path) -> str:
    config = require_project(root)
    files = project_files(root)
    counts = Counter(path.parent.relative_to(root).parts[0] if path.parent != root else "." for group in files.values() for path in group)
    main = config_value(config_section(config, "application"), "run/main_scene") or "unknown"
    features = config_value(config_section(config, "application"), "config/features") or "unknown"
    renderer = config_value(config_section(config, "rendering"), "renderer/rendering_method") or "unspecified"
    autoload = config_section(config, "autoload")
    autoload_names = re.findall(r"(?m)^\s*([\w-]+)\s*=", autoload)
    input_actions = re.findall(r"(?m)^\s*([\w-]+)\s*=", config_section(config, "input"))
    classes: list[tuple[str, str]] = []
    for path in files[".gd"]:
        source = read_text(path)
        if source is None:
            continue
        match = re.search(r"(?m)^\s*class_name\s+(\w+)", source)
        if match:
            classes.append((match.group(1), rel(path, root)))
    lines = ["# Project snapshot", "", f"Project: `{md(root.name)}`", "", "## Configuration", ""]
    lines += ["- `project.godot`: found", f"- Main scene: `{md(main)}`", f"- Declared features: `{md(features)}`", f"- Renderer: `{md(renderer)}`"]
    lines += [f"- Autoloads ({len(autoload_names)}): {', '.join('`' + md(x) + '`' for x in autoload_names[:30]) or 'none'}", f"- Input actions ({len(input_actions)}): {', '.join('`' + md(x) + '`' for x in input_actions[:30]) or 'none'}", "", "## Files", ""]
    lines += [f"- `{suffix}`: {len(paths)}" for suffix, paths in files.items()]
    lines += ["", "Top-level areas (Godot file counts):", ""]
    lines += [f"- `{md(name)}`: {count}" for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:30]]
    lines += ["", f"## Named script classes ({len(classes)})", ""]
    lines += [f"- `{md(name)}` — `{md(path)}`" for name, path in classes[:60]] or ["- None found"]
    if len(classes) > 60:
        lines.append(f"- … {len(classes) - 60} more omitted")
    lines += ["", "## Largest scripts (bytes; size is not a defect)", ""]
    largest = sorted(files[".gd"], key=lambda path: (-path.stat().st_size, rel(path, root)))[:10]
    lines += [f"- `{md(rel(path, root))}`: {path.stat().st_size} bytes" for path in largest] or ["- None found"]
    lines += ["", "## Scene entry points", "", f"- Main: `{md(main)}`"]
    lines += [f"- `{md(rel(path, root))}`" for path in files[".tscn"][:12] if "res://" + rel(path, root) != main]
    lines += ["", "## Scope and limits", "", "Static inventory only. `.res` files are counted, never parsed. Large or unreadable text files are skipped. Ignored directories, nested repositories, links, backup trees and binary assets are excluded. Configuration values are selected identifiers only; no full scripts or secrets are copied."]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Godot project root")
    parser.add_argument("--output", type=Path, help="Markdown destination (default PROJECT_SNAPSHOT.md in project)")
    args = parser.parse_args()
    try:
        root = root_arg(args.project)
        safe_output(root, args.output or root / "PROJECT_SNAPSHOT.md", snapshot(root))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
