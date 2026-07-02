from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "estimate.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


class EstimateCliTests(unittest.TestCase):
    def test_text_estimate_for_crud_api(self) -> None:
        result = run_cli("--traditional-hours", "24", "--task-type", "crud_api")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Traditional estimate: 24.0h", result.stdout)
        self.assertIn("Task type: crud_api", result.stdout)
        self.assertIn("optimistic:   6.0h", result.stdout)
        self.assertIn("expected:     9.1h", result.stdout)
        self.assertIn("conservative: 14.4h", result.stdout)
        self.assertIn("Confidence: medium", result.stdout)

    def test_json_estimate_includes_adjustments(self) -> None:
        result = run_cli(
            "--traditional-hours",
            "16",
            "--task-type",
            "frontend_page",
            "--verification-hours",
            "2",
            "--risk-buffer",
            "0.2",
            "--format",
            "json",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["task_type"], "frontend_page")
        self.assertEqual(payload["confidence"], "medium")
        self.assertAlmostEqual(payload["ai_adjusted_estimate_hours"]["optimistic"], 8.16)
        self.assertAlmostEqual(payload["ai_adjusted_estimate_hours"]["expected"], 12.0)
        self.assertAlmostEqual(payload["ai_adjusted_estimate_hours"]["conservative"], 15.84)

    def test_markdown_estimate(self) -> None:
        result = run_cli(
            "--traditional-hours",
            "24",
            "--task-type",
            "crud_api",
            "--format",
            "markdown",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# AI-Assisted Estimate", result.stdout)
        self.assertIn("- Task type: `crud_api`", result.stdout)
        self.assertIn("| Optimistic | 6.0h |", result.stdout)
        self.assertIn("| Expected | 9.1h |", result.stdout)
        self.assertIn("| Conservative | 14.4h |", result.stdout)

    def test_output_writes_report_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "reports" / "estimate.md"
            result = run_cli(
                "--traditional-hours",
                "24",
                "--task-type",
                "crud_api",
                "--format",
                "markdown",
                "--output",
                str(output_path),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertTrue(output_path.exists())
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("# AI-Assisted Estimate", content)
            self.assertIn("| Expected | 9.1h |", content)

    def test_list_task_types(self) -> None:
        result = run_cli("--list-task-types")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("crud_api:", result.stdout)
        self.assertIn("frontend_page:", result.stdout)

    def test_requires_task_type_for_estimate(self) -> None:
        result = run_cli("--traditional-hours", "8")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--task-type is required", result.stderr)

    def test_rejects_negative_hours(self) -> None:
        result = run_cli("--traditional-hours", "-1", "--task-type", "crud_api")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--traditional-hours must be non-negative", result.stderr)

    def test_rejects_unknown_task_type(self) -> None:
        result = run_cli("--traditional-hours", "8", "--task-type", "unknown")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid choice", result.stderr)

    def test_custom_rules_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            rules_path = Path(tmp_dir) / "custom-task-types.yaml"
            rules_path.write_text(
                """
version: 0.1.0
task_types:
  custom_task:
    label: Custom team task
    ai_compression:
      optimistic: 0.50
      expected: 0.75
      conservative: 1.00
    confidence: low
""".lstrip(),
                encoding="utf-8",
            )

            list_result = run_cli("--rules", str(rules_path), "--list-task-types")
            self.assertEqual(list_result.returncode, 0, list_result.stderr)
            self.assertIn("custom_task: Custom team task", list_result.stdout)
            self.assertNotIn("crud_api:", list_result.stdout)

            estimate_result = run_cli(
                "--rules",
                str(rules_path),
                "--traditional-hours",
                "10",
                "--task-type",
                "custom_task",
                "--format",
                "json",
            )
            self.assertEqual(estimate_result.returncode, 0, estimate_result.stderr)
            payload = json.loads(estimate_result.stdout)
            self.assertEqual(payload["task_type"], "custom_task")
            self.assertEqual(
                payload["ai_adjusted_estimate_hours"],
                {"optimistic": 5.0, "expected": 7.5, "conservative": 10.0},
            )


if __name__ == "__main__":
    unittest.main()
