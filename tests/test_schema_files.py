from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO_ROOT / "schema"


class SchemaFileTests(unittest.TestCase):
    def test_schema_files_are_valid_json(self) -> None:
        for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
            with self.subTest(schema=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema["type"], "object")
                self.assertIn("properties", schema)

    def test_expected_schema_files_exist(self) -> None:
        expected = {
            "dataset.schema.json",
            "estimate-output.schema.json",
            "task-types.schema.json",
        }

        actual = {path.name for path in SCHEMA_DIR.glob("*.schema.json")}
        self.assertEqual(expected, actual)

    def test_task_types_schema_documents_required_compression_keys(self) -> None:
        schema = json.loads((SCHEMA_DIR / "task-types.schema.json").read_text(encoding="utf-8"))
        compression = (
            schema["properties"]["task_types"]["additionalProperties"]["properties"]["ai_compression"]
        )

        self.assertEqual(
            compression["required"],
            ["optimistic", "expected", "conservative"],
        )


if __name__ == "__main__":
    unittest.main()
