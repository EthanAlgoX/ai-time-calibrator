#!/usr/bin/env python3
"""Minimal AI-assisted estimate calibrator.

This prototype intentionally avoids external dependencies so the repository is
usable immediately after clone.
"""

from __future__ import annotations

import argparse
import sys


TASK_TYPES = {
    "boilerplate": {
        "label": "Boilerplate or scaffolding",
        "compression": (0.10, 0.20, 0.40),
        "confidence": "high",
    },
    "crud_api": {
        "label": "CRUD, API endpoint, or standard backend feature",
        "compression": (0.25, 0.38, 0.60),
        "confidence": "medium",
    },
    "test_generation": {
        "label": "Unit, integration, or regression test generation",
        "compression": (0.20, 0.35, 0.60),
        "confidence": "medium",
    },
    "frontend_page": {
        "label": "Frontend page, component, or interaction",
        "compression": (0.30, 0.50, 0.70),
        "confidence": "medium",
    },
    "refactor": {
        "label": "Refactor or codebase cleanup",
        "compression": (0.40, 0.60, 0.80),
        "confidence": "medium",
    },
    "debugging": {
        "label": "Bug investigation or debugging",
        "compression": (0.30, 0.65, 1.00),
        "confidence": "low",
    },
    "architecture": {
        "label": "Architecture or technical design",
        "compression": (0.65, 0.80, 0.95),
        "confidence": "low",
    },
    "requirements": {
        "label": "Requirements, product clarification, or stakeholder alignment",
        "compression": (0.80, 0.90, 1.00),
        "confidence": "low",
    },
    "cross_system_integration": {
        "label": "Cross-system integration",
        "compression": (0.50, 0.75, 1.00),
        "confidence": "low",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calibrate a traditional software estimate for AI-assisted development."
    )
    parser.add_argument(
        "--traditional-hours",
        type=float,
        required=True,
        help="Traditional estimate in engineering hours.",
    )
    parser.add_argument(
        "--task-type",
        choices=sorted(TASK_TYPES),
        required=True,
        help="Task type used to select the default AI compression range.",
    )
    parser.add_argument(
        "--verification-hours",
        type=float,
        default=0.0,
        help="Optional fixed verification, QA, or review time to add after compression.",
    )
    parser.add_argument(
        "--risk-buffer",
        type=float,
        default=0.0,
        help="Optional risk buffer as a decimal, for example 0.20 for 20%%.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    task = TASK_TYPES[args.task_type]
    optimistic_factor, expected_factor, conservative_factor = task["compression"]

    compressed = {
        "optimistic": args.traditional_hours * optimistic_factor,
        "expected": args.traditional_hours * expected_factor,
        "conservative": args.traditional_hours * conservative_factor,
    }

    adjusted = {
        key: (value + args.verification_hours) * (1 + args.risk_buffer)
        for key, value in compressed.items()
    }

    print(f"Traditional estimate: {args.traditional_hours:.1f}h")
    print(f"Task type: {args.task_type} ({task['label']})")
    print("AI-adjusted estimate:")
    print(f"  optimistic:   {adjusted['optimistic']:.1f}h")
    print(f"  expected:     {adjusted['expected']:.1f}h")
    print(f"  conservative: {adjusted['conservative']:.1f}h")
    print(f"Confidence: {task['confidence']}")

    if args.verification_hours:
        print(f"Fixed verification/review time added: {args.verification_hours:.1f}h")
    if args.risk_buffer:
        print(f"Risk buffer applied: {args.risk_buffer:.0%}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
