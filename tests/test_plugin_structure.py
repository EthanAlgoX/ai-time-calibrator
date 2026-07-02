from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class PluginStructureTests(unittest.TestCase):
    def test_shared_skill_path_exists(self) -> None:
        skill = REPO_ROOT / "skills" / "ai-time-calibrator" / "SKILL.md"
        metadata = REPO_ROOT / "skills" / "ai-time-calibrator" / "agents" / "openai.yaml"

        self.assertTrue(skill.exists())
        self.assertTrue(metadata.exists())
        self.assertFalse((REPO_ROOT / "skills" / "codex").exists())

    def test_plugin_manifests_are_valid_json(self) -> None:
        manifest_paths = [
            REPO_ROOT / ".codex-plugin" / "plugin.json",
            REPO_ROOT / ".claude-plugin" / "plugin.json",
            REPO_ROOT / ".cursor-plugin" / "plugin.json",
        ]

        for path in manifest_paths:
            with self.subTest(manifest=path):
                manifest = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(manifest["name"], "ai-time-calibrator")
                self.assertEqual(manifest["version"], "0.1.3")
                self.assertEqual(manifest["license"], "MIT")

    def test_codex_and_cursor_manifests_point_to_skills(self) -> None:
        codex = json.loads((REPO_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        cursor = json.loads((REPO_ROOT / ".cursor-plugin" / "plugin.json").read_text(encoding="utf-8"))

        self.assertEqual(codex["skills"], "./skills/")
        self.assertEqual(cursor["skills"], "./skills/")
        self.assertEqual(codex["interface"]["displayName"], "AI Time Calibrator")

    def test_agents_skills_compatibility_link(self) -> None:
        link = REPO_ROOT / ".agents" / "skills"

        self.assertTrue(link.exists())
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.readlink(), Path("../skills"))

    def test_nonstandard_claude_adapter_removed(self) -> None:
        self.assertFalse((REPO_ROOT / "adapters" / "claude-code" / "CLAUDE.md").exists())


if __name__ == "__main__":
    unittest.main()
