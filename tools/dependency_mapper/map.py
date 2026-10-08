"""Map static Godot references and label unresolved dynamic calls (stdlib only)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import config_section, md, project_files, read_text, rel, require_project, root_arg, safe_output

LITERAL_LOAD = re.compile(r'\b(preload|load)\s*\(\s*["\'](res://[^"\']+)["\']\s*\)')
CALL = re.compile(r'\b(preload|load)\s*\(')
EXTENDS = re.compile(r'(?m)^\s*extends\s+(?:["\'](res://[^"\']+)["\']|(\w+))')
CLASS = re.compile(r'(?m)^\s*class_name\s+(\w+)')
SIGNAL = re.compile(r'(?m)^\s*signal\s+(\w+)')
RESOURCE = re.compile(r'(?m)^\[ext_resource\b[^\n]*\bpath="(res://[^"]+)"')


def collect_project(root: Path) -> dict[str, object]:
    files = project_files(root)
    sources: dict[Path, str] = {}
    for path in files[".gd"] + files[".tscn"] + files[".tres"]:
        content = read_text(path)
        if content is not None:
            sources[path] = content
    classes = {match.group(1): rel(path, root) for path, source in sources.items() if path.suffix == ".gd" for match in CLASS.finditer(source)}
    project_config = require_project(root)
    autoloads = dict(re.findall(r'(?m)^\s*([\w-]+)\s*=\s*"\*?(res://[^"\n]+)"', config_section(project_config, "autoload")))
    edges: list[tuple[str, str, str, str]] = []
    dynamic: list[str] = []
    signal_defs: list[str] = []
    signal_uses: list[str] = []
    for path, source in sorted(sources.items(), key=lambda item: rel(item[0], root)):
        origin = rel(path, root)
        if path.suffix == ".gd":
            literal_spans = []
            for match in LITERAL_LOAD.finditer(source):
                edges.append((match.group(1), origin, match.group(2), "literal"))
                literal_spans.append(match.span())
            for match in CALL.finditer(source):
                if not any(start <= match.start() < end for start, end in literal_spans):
                    dynamic.append(f"`{md(origin)}:{source.count(chr(10), 0, match.start()) + 1}` — `{match.group(1)}(...)` expression")
            for match in EXTENDS.finditer(source):
                target = match.group(1) or classes.get(match.group(2), "")
                if target:
                    edges.append(("extends", origin, target, "literal/class_name"))
            for match in SIGNAL.finditer(source):
                signal_defs.append(f"`{md(match.group(1))}` in `{md(origin)}`")
            for name in autoloads:
                if re.search(r"\b" + re.escape(name) + r"\b", source):
                    edges.append(("autoload mention", origin, name, "heuristic"))
            for match in re.finditer(r'\b(?:connect|emit_signal)\s*\(\s*["\'](\w+)["\']|\b(\w+)\s*\.\s*(?:connect|emit)\s*\(', source):
                signal_uses.append(f"`{md(match.group(1) or match.group(2))}` in `{md(origin)}` (heuristic)")
        else:
            for match in RESOURCE.finditer(source):
                edges.append(("ext_resource", origin, match.group(1), "literal"))
            if path.suffix == ".tscn":
                for match in re.finditer(r'(?m)^\[connection\b[^\n]*\bsignal="([^"]+)"', source):
                    signal_uses.append(f"`{md(match.group(1))}` in `{md(origin)}` (scene connection)")
    return {"edges": edges, "autoloads": autoloads, "dynamic": dynamic, "signal_defs": signal_defs, "signal_uses": signal_uses}


def map_project(root: Path) -> str:
    graph = collect_project(root)
    edges = graph["edges"]
    autoloads = graph["autoloads"]
    dynamic = graph["dynamic"]
    signal_defs = graph["signal_defs"]
    signal_uses = graph["signal_uses"]
    lines = ["# Dependency map", "", f"Project: `{md(root.name)}`", "", "## Autoload declarations", ""]
    lines += [f"- `{md(name)}` → `{md(target)}`" for name, target in sorted(autoloads.items())[:40]] or ["- None found"]
    lines += ["", f"## Static edges ({len(edges)})", ""]
    for kind, origin, target, certainty in edges[:180]:
        if target.startswith("res://"):
            resolved = (root / target[6:]).resolve()
            status = "exists" if resolved.is_relative_to(root) and resolved.is_file() else "unresolved"
        else:
            status = "symbol"
        lines.append(f"- `{md(origin)}` — {kind} → `{md(target)}` ({certainty}; {status})")
    if len(edges) > 180:
        lines.append(f"- … {len(edges) - 180} more omitted")
    lines += ["", f"## Dynamic loads ({len(dynamic)})", ""]
    lines += [f"- {item}" for item in dynamic[:60]] or ["- None detected"]
    if len(dynamic) > 60:
        lines.append(f"- … {len(dynamic) - 60} more omitted")
    lines += ["", f"## Signals ({len(signal_defs)} declarations, {len(signal_uses)} uses)", ""]
    lines += [f"- Declared {item}" for item in signal_defs[:40]]
    lines += [f"- Used {item}" for item in signal_uses[:40]]
    if not signal_defs and not signal_uses:
        lines.append("- None detected")
    lines += ["", "## Limits", "", "This is a bounded static heuristic, not a runtime dependency graph. Dynamic expressions are listed by location but cannot be resolved; autoload mentions and signal uses may include false positives. UID references, inherited scene IDs, binary `.res`, comments and generated paths may need Godot editor verification. No source bodies or configuration secrets are copied."]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Godot project root")
    parser.add_argument("--output", type=Path, help="Markdown destination (default DEPENDENCY_MAP.md in project)")
    args = parser.parse_args()
    try:
        root = root_arg(args.project)
        safe_output(root, args.output or root / "DEPENDENCY_MAP.md", map_project(root))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
