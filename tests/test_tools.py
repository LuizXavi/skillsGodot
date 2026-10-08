"""Behavioral tests using temporary projects; no Godot executable required."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, REPO / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


analyzer = load("analyzer", "tools/project_analyzer/analyze.py")
context = load("context", "tools/context_generator/generate.py")
mapper = load("mapper", "tools/dependency_mapper/map.py")
validator = load("validator", "tools/validation/validate.py")


class ToolTests(unittest.TestCase):
    def test_snapshot_identifies_largest_script(self):
        large = self.root / "scripts" / "large.gd"
        large.parent.mkdir(exist_ok=True)
        large.write_text("extends Node\n" + "# sizeable\n" * 500, encoding="utf-8")
        report = analyzer.snapshot(self.root)
        section = report.split("## Largest scripts", 1)[1]
        self.assertIn("scripts/large.gd", section.split("\n")[2])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "project.godot").write_text('[application]\nrun/main_scene="res://scenes/Main.tscn"\nconfig/features=PackedStringArray("4.3")\n[autoload]\nStore="*res://scripts/Store.gd"\n[input]\njump={}\n', encoding="utf-8")
        (self.root / "scripts").mkdir()
        (self.root / "scenes").mkdir()
        (self.root / "scripts" / "Store.gd").write_text('class_name StoreClass\nsignal changed\nextends Node\n', encoding="utf-8")
        (self.root / "scripts" / "Player.gd").write_text('extends StoreClass\nvar scene = preload("res://scenes/Main.tscn")\nvar dynamic_scene = load(path)\nfunc go():\n    Store.changed.connect(go)\n', encoding="utf-8")
        (self.root / "scenes" / "Main.tscn").write_text('[gd_scene]\n[ext_resource type="Script" path="res://scripts/Player.gd" id="1"]\n[connection signal="pressed" from="Button" to="." method="_on_pressed"]\n', encoding="utf-8")
        (self.root / "scenes" / "cache.res").write_bytes(b"binary")
        (self.root / ".godot").mkdir()
        (self.root / ".godot" / "ignored.gd").write_text("class_name IgnoreMe")
        (self.root / "ignored").mkdir()
        (self.root / "ignored" / ".gdignore").write_text("")
        (self.root / "ignored" / "ignored.gd").write_text("class_name IgnoreMeToo")
        (self.root / "nested").mkdir()
        (self.root / "nested" / ".git").mkdir()
        (self.root / "nested" / "ignored.gd").write_text("class_name IgnoreNested")

    def test_snapshot_counts_and_ignores(self):
        report = analyzer.snapshot(self.root)
        self.assertIn("`.gd`: 2", report)
        self.assertIn("`.res`: 1", report)
        self.assertIn("StoreClass", report)
        self.assertNotIn("IgnoreMe", report)
        self.assertIn("jump", report)

    def test_context_focus_is_compact_and_path_only(self):
        report = context.generate(self.root, "player")
        self.assertIn("scripts/Player.gd", report)
        self.assertIn("## Direct static dependencies", report)
        self.assertLess(report.index("- `scripts/Player.gd`"), report.index("- `scripts/Store.gd`"))
        self.assertNotIn("var dynamic_scene", report)
        self.assertIn("Main.tscn", report)  # entry point metadata

    def test_general_context_ranks_entry_and_autoload_over_addons(self):
        (self.root / "addons").mkdir()
        (self.root / "addons" / "Huge.gd").write_text("extends Node\n" * 2000, encoding="utf-8")
        report = context.generate(self.root)
        section = report.split("## Files to inspect first\n\n", 1)[1].split("\n## Direct", 1)[0]
        self.assertLess(section.index("scenes/Main.tscn"), section.index("addons/Huge.gd"))
        self.assertLess(section.index("scripts/Store.gd"), section.index("addons/Huge.gd"))
        self.assertEqual(report, context.generate(self.root))

    def test_dependency_literals_dynamic_classes_signals_autoloads(self):
        report = mapper.map_project(self.root)
        self.assertIn("preload", report)
        self.assertIn("res://scenes/Main.tscn", report)
        self.assertIn("extends", report)
        self.assertIn("scripts/Store.gd", report)
        self.assertIn("`load(...)` expression", report)
        self.assertIn("autoload mention", report)
        self.assertIn("Declared `changed`", report)
        self.assertIn("Used `changed`", report)
        self.assertIn("`pressed` in `scenes/Main.tscn` (scene connection)", report)

    def test_output_refuses_existing_source_and_rewrites_own_report(self):
        from common import safe_output
        source = self.root / "notes.md"
        source.write_text("human content", encoding="utf-8")
        with self.assertRaises(ValueError):
            safe_output(self.root, source, "report")
        report = self.root / "AI_CONTEXT.md"
        safe_output(self.root, report, "first")
        safe_output(self.root, report, "second")
        self.assertIn("second", report.read_text(encoding="utf-8"))

    def test_missing_project_config_is_an_error(self):
        (self.root / "project.godot").unlink()
        for operation in (analyzer.snapshot, context.generate, mapper.map_project):
            with self.subTest(operation=operation.__name__), self.assertRaisesRegex(ValueError, "project.godot"):
                operation(self.root)

    def test_output_rejects_linked_parent(self):
        from common import safe_output
        linked = self.root / "linked"
        try:
            linked.symlink_to(self.root / "scenes", target_is_directory=True)
        except OSError:
            self.skipTest("directory symlinks unavailable")
        with self.assertRaisesRegex(ValueError, "link or junction"):
            safe_output(self.root, linked / "AI_CONTEXT.md", "report")

    def test_validator_skills_links_templates_duplicates(self):
        skills = self.root / "skills" / "godot"
        skills.mkdir(parents=True)
        skill = skills / "SKILL.md"
        skill.write_text('---\nname: godot-test\ndescription: >\n  A useful skill.\n---\n[ok](../../project.godot)\n[bad](missing.md)\n', encoding="utf-8")
        templates = self.root / "templates" / "inventory"
        templates.mkdir(parents=True)
        (self.root / "copy-a.txt").write_text("same")
        (self.root / "copy-b.txt").write_text("same")
        issues = validator.validate(self.root)
        self.assertTrue(any("broken local link" in item for item in issues))
        self.assertTrue(any("template missing README.md: templates/inventory" in item for item in issues))
        self.assertTrue(any("template has no files" in item for item in issues))
        self.assertTrue(any("exact duplicate" in item for item in issues))
        self.assertFalse(any("invalid required name" in item for item in issues))

    def test_validator_accepts_scalar_metadata_mapping(self):
        skills = self.root / "skills" / "godot" / "movement"
        skills.mkdir(parents=True)
        (skills / "SKILL.md").write_text(
            '---\nname: godot-movement\ndescription: A movement skill.\nmetadata:\n  short-description: "Useful for movement"\n---\n',
            encoding="utf-8",
        )
        self.assertEqual(validator.validate(self.root), [])

    def test_validator_rejects_invalid_metadata_values_and_duplicate_keys(self):
        invalid = [
            '---\nname: godot-test\ndescription: Valid\nmetadata:\n  tags: [godot, game]\n---\n',
            '---\nname: godot-test\ndescription: Valid\nmetadata:\n  summary: "unclosed\n---\n',
            '---\nname: godot-test\ndescription: Valid\nmetadata:\n  summary: first\n  summary: second\n---\n',
        ]
        for source in invalid:
            with self.subTest(source=source):
                self.assertIsNone(validator.frontmatter(source))

    def test_validator_checks_godot_template_leaves(self):
        templates = self.root / "templates" / "godot"
        valid = templates / "movement"
        valid.mkdir(parents=True)
        (valid / "README.md").write_text("# Movement template\n", encoding="utf-8")
        (valid / "movement.gd").write_text("extends Node\n", encoding="utf-8")
        missing = templates / "combat"
        missing.mkdir()
        (missing / "combat.gd").write_text("extends Node\n", encoding="utf-8")
        issues = validator.validate(self.root)
        self.assertTrue(any("template missing README.md: templates/godot/combat" in item for item in issues))
        self.assertFalse(any("template missing README.md: templates/godot/movement" in item for item in issues))
        self.assertFalse(any(item == "template missing README.md: templates/godot" for item in issues))

    def test_validator_accepts_nested_godot_template_tree(self):
        leaf = self.root / "templates" / "godot" / "movement"
        leaf.mkdir(parents=True)
        (leaf / "README.md").write_text("# Movement template\n", encoding="utf-8")
        (leaf / "movement.gd").write_text("extends Node\n", encoding="utf-8")
        self.assertEqual(validator.validate(self.root), [])

    def test_cli_commands(self):
        for relative, name in [("tools/project_analyzer/analyze.py", "PROJECT_SNAPSHOT.md"), ("tools/context_generator/generate.py", "AI_CONTEXT.md"), ("tools/dependency_mapper/map.py", "DEPENDENCY_MAP.md")]:
            with self.subTest(relative=relative):
                result = subprocess.run([sys.executable, str(REPO / relative), str(self.root), "--output", str(self.root / name)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((self.root / name).exists())

    def test_validator_cli_clean_skill_tree(self):
        clean = self.root / "collection"
        (clean / "skills" / "godot" / "movement").mkdir(parents=True)
        (clean / "skills" / "godot" / "movement" / "SKILL.md").write_text('---\nname: godot-movement\ndescription: A movement skill.\n---\n# Movement\n', encoding="utf-8")
        (clean / "templates" / "movement").mkdir(parents=True)
        (clean / "templates" / "movement" / "README.md").write_text("# Usage\n", encoding="utf-8")
        (clean / "templates" / "movement" / "move.gd").write_text("extends Node\n", encoding="utf-8")
        result = subprocess.run([sys.executable, str(REPO / "tools/validation/validate.py"), str(clean)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 issue(s)", result.stdout)

    def test_validator_missing_skill_and_required_metadata(self):
        first = self.root / "skills" / "godot" / "missing"
        second = self.root / "skills" / "godot" / "incomplete"
        first.mkdir(parents=True)
        second.mkdir(parents=True)
        (first / "note.md").write_text("# No skill", encoding="utf-8")
        (second / "SKILL.md").write_text("---\nname: bad_name\n---\n# Incomplete", encoding="utf-8")
        issues = validator.validate(self.root)
        self.assertTrue(any("missing SKILL.md: skills/godot/missing" in item for item in issues))
        self.assertTrue(any("invalid required name: skills/godot/incomplete/SKILL.md" in item for item in issues))
        self.assertTrue(any("missing required description" in item for item in issues))

    def test_frontmatter_rejects_non_subset_required_values(self):
        invalid = [
            '---\nname: "unclosed\ndescription: Valid\n---\n',
            '---\nname: [array]\ndescription: Valid\n---\n',
            '---\nname: first\nname: second\ndescription: Valid\n---\n',
            '---\nname: first\ndescription: {map: value}\n---\n',
        ]
        for value in invalid:
            with self.subTest(value=value):
                self.assertIsNone(validator.frontmatter(value))


if __name__ == "__main__":
    unittest.main()
