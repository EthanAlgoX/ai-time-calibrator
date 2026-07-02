from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "estimate.py"

spec = importlib.util.spec_from_file_location("estimate", SCRIPT)
estimate = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(estimate)


class RuleFileTests(unittest.TestCase):
    def test_task_types_have_required_fields(self) -> None:
        task_types = estimate.load_task_types()

        self.assertGreaterEqual(len(task_types), 8)
        for name, task in task_types.items():
            with self.subTest(task_type=name):
                self.assertIsInstance(task.get("label"), str)
                self.assertIn(task.get("confidence"), {"high", "medium", "low"})
                compression = task.get("ai_compression")
                self.assertIsInstance(compression, dict)
                self.assertEqual(
                    set(estimate.ESTIMATE_KEYS),
                    set(compression),
                )

    def test_compression_factors_are_reasonable(self) -> None:
        task_types = estimate.load_task_types()

        for name, task in task_types.items():
            with self.subTest(task_type=name):
                compression = task["ai_compression"]
                optimistic = compression["optimistic"]
                expected = compression["expected"]
                conservative = compression["conservative"]

                for value in compression.values():
                    self.assertGreaterEqual(value, 0.0)
                    self.assertLessEqual(value, 1.5)

                self.assertLessEqual(optimistic, expected)
                self.assertLessEqual(expected, conservative)

    def test_risk_factors_file_exists(self) -> None:
        risk_factors = REPO_ROOT / "rules" / "risk-factors.yaml"

        self.assertTrue(risk_factors.exists())
        content = risk_factors.read_text(encoding="utf-8")
        self.assertIn("risk_factors:", content)
        self.assertIn("unclear_acceptance_criteria:", content)

    def test_calibration_model_file_exists(self) -> None:
        calibration_model = REPO_ROOT / "rules" / "calibration-model.yaml"

        self.assertTrue(calibration_model.exists())
        content = calibration_model.read_text(encoding="utf-8")
        self.assertIn("workflow:", content)
        self.assertIn("output_format:", content)


if __name__ == "__main__":
    unittest.main()
