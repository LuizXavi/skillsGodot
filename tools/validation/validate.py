"""Validate a portable skill collection with a documented stdlib YAML subset.

Frontmatter subset: opening/closing `---`, unindented `name:` and
`description:` scalar keys, optionally single/double quoted. Description may
also use `|` or `>` with indented continuation lines. `metadata:` may contain
an indented mapping of scalar strings. Other YAML features are not
interpreted; use a YAML parser for richer frontmatter.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import is_link, read_text, rel, root_arg, walk_dirs, walk_files

LINK = re.compile(r'!?(?:\[[^\]]*\])\((<[^>]+>|[^\s)]+)(?:\s+["\'][^"\']*["\'])?\)')
NAME = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
REPORTS = {"PROJECT_SNAPSHOT.md", "AI_CONTEXT.md", "DEPENDENCY_MAP.md"}


def frontmatter(source: str) -> dict[str, str] | None:
    lines = source.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return None
    data: dict[str, str] = {}
    index = 1
    while index < end:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", line)
        if not match:
            return None
        key, value = match.groups()
        if key in data:
            return None
        if key == "metadata" and not value:
            index += 1
            nested_keys: set[str] = set()
            while index < end and lines[index].startswith("  "):
                nested = re.fullmatch(r"  ([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", lines[index])
                if not nested:
                    return None
                nested_key, nested_value = nested.groups()
                if nested_key in nested_keys or not nested_value:
                    return None
                parsed = _scalar(nested_value)
                if parsed is None:
                    return None
                nested_keys.add(nested_key)
                data[f"metadata.{nested_key}"] = parsed
                index += 1
            if not nested_keys:
                return None
            continue
        if value in {"|", ">"}:
            continuation = []
            index += 1
            while index < end and (not lines[index] or lines[index][0].isspace()):
                continuation.append(lines[index].strip())
                index += 1
            value = " ".join(part for part in continuation if part)
        else:
            value = _scalar(value)
            if value is None:
                return None
            index += 1
        data[key] = value.strip()
    return data


def _scalar(value: str) -> str | None:
    """Parse one deliberately small YAML scalar string."""
    if value.startswith(("'", '"')) or value.endswith(("'", '"')):
        if len(value) < 2 or value[0] != value[-1] or value[0] in value[1:-1]:
            return None
        return value[1:-1].strip()
    if value.startswith(("[", "{", "!", "&", "*", "- ")) or ": " in value or " #" in value:
        return None
    return value.strip()


def validate(root: Path) -> list[str]:
    issues: list[str] = []
    files = list(walk_files(root))
    file_set = set(files)
    dirs = list(walk_dirs(root))
    skill_dirs = {path.parent for path in files if path.name == "SKILL.md"}
    candidates = []
    for path in dirs:
        if path == root:
            continue
        parts = path.relative_to(root).parts
        legacy = path.parent == root and path.name.startswith("godot-")
        leaf_skill = len(parts) == 3 and parts[0] == "skills"
        direct_skill = len(parts) == 2 and parts[0] == "skills" and any(child.is_file() for child in path.iterdir() if not is_link(child))
        if legacy or leaf_skill or direct_skill:
            candidates.append(path)
    for directory in candidates:
        if directory not in skill_dirs and directory.name != "skills":
            issues.append(f"missing SKILL.md: {rel(directory, root)}")
    names: dict[str, list[str]] = defaultdict(list)
    for directory in sorted(skill_dirs):
        skill = directory / "SKILL.md"
        source = read_text(skill)
        if source is None:
            issues.append(f"unreadable SKILL.md: {rel(skill, root)}")
            continue
        metadata = frontmatter(source)
        if metadata is None:
            issues.append(f"missing or invalid frontmatter: {rel(skill, root)}")
            continue
        name = metadata.get("name", "")
        if not NAME.fullmatch(name):
            issues.append(f"invalid required name: {rel(skill, root)}")
        else:
            names[name].append(rel(skill, root))
        if not metadata.get("description"):
            issues.append(f"missing required description: {rel(skill, root)}")
    for name, paths in sorted(names.items()):
        if len(paths) > 1:
            issues.append(f"duplicate skill name {name}: {', '.join(paths)}")
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        source = read_text(path)
        if source is None:
            continue
        in_fence = False
        for line_number, line in enumerate(source.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK.finditer(line):
                link = unquote(match.group(1).strip("<>"))
                if link.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", link, re.I):
                    continue
                destination = link.split("#", 1)[0].split("?", 1)[0]
                if not destination:
                    continue
                target = (path.parent / destination).resolve()
                if not target.is_relative_to(root) or not target.exists() or is_link(target):
                    issues.append(f"broken local link: {rel(path, root)}:{line_number} -> {link}")
    templates = root / "templates"
    if templates in dirs:
        template_dirs = [directory for directory in dirs if (directory.parent == templates and directory.name != "godot") or directory.parent == templates / "godot"]
        for directory in template_dirs:
            contents = [path for path in files if path.is_relative_to(directory)]
            if directory / "README.md" not in contents:
                issues.append(f"template missing README.md: {rel(directory, root)}")
            if not any(path.name != "README.md" for path in contents):
                issues.append(f"template has no files: {rel(directory, root)}")
    for directory in dirs:
        if directory == root:
            continue
        if not any(path.parent == directory for path in files) and not any(child.parent == directory for child in dirs if child != directory):
            issues.append(f"empty directory: {rel(directory, root)}")
    hashes: dict[bytes, list[str]] = defaultdict(list)
    for path in files:
        if path.name in REPORTS or path.stat().st_size == 0 or path.stat().st_size > 2_000_000:
            continue
        try:
            digest = hashlib.sha256(path.read_bytes()).digest()
        except OSError:
            continue
        hashes[digest].append(rel(path, root))
    for paths in hashes.values():
        if len(paths) > 1:
            issues.append(f"exact duplicate files: {', '.join(sorted(paths))}")
    return sorted(set(issues))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", help="skill collection root")
    args = parser.parse_args()
    try:
        root = root_arg(args.root)
        issues = validate(root)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    for issue in issues:
        print(issue)
    print(f"{len(issues)} issue(s)")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
