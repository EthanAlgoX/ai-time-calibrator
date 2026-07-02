#!/usr/bin/env python3
"""Minimal AI-assisted estimate calibrator.

The CLI intentionally avoids external dependencies. It reads the repository's
task type rules from rules/task-types.yaml with a small parser for this file's
known structure.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TASK_TYPES_PATH = REPO_ROOT / "rules" / "task-types.yaml"
ESTIMATE_KEYS = ("optimistic", "expected", "conservative")


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return {}
    if value in {"true", "false"}:
        return value == "true"
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value.strip('"').strip("'")


def load_task_types(path: Path = DEFAULT_TASK_TYPES_PATH) -> dict[str, dict[str, Any]]:
    """Load task type calibration rules from the project YAML file.

    This is a narrow parser for rules/task-types.yaml. It supports nested maps,
    scalar values, and list items, which is enough for the v0.1 rule files.
    """
    if not path.exists():
        raise ValueError(f"Task types file not found: {path}")

    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    lines = path.read_text(encoding="utf-8").splitlines()

    for index, raw_line in enumerate(lines):
        line_number = index + 1
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        content = raw_line.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]

        if content.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"Unexpected list item at {path}:{line_number}")
            parent.append(parse_scalar(content[2:]))
            continue

        if ":" not in content:
            raise ValueError(f"Expected key/value at {path}:{line_number}")

        key, raw_value = content.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if not isinstance(parent, dict):
            raise ValueError(f"Cannot add mapping under list at {path}:{line_number}")

        if raw_value:
            parent[key] = parse_scalar(raw_value)
            continue

        container: Any = {}
        for next_line in lines[index + 1 :]:
            if not next_line.strip() or next_line.lstrip().startswith("#"):
                continue
            next_indent = len(next_line) - len(next_line.lstrip(" "))
            if next_indent > indent and next_line.strip().startswith("- "):
                container = []
            break
        parent[key] = container
        stack.append((indent, container))

    task_types = root.get("task_types")
    if not isinstance(task_types, dict):
        raise ValueError("rules/task-types.yaml must contain a task_types mapping")

    for name, task in task_types.items():
        if not isinstance(task, dict):
            raise ValueError(f"Task type {name!r} must be a mapping")
        compression = task.get("ai_compression")
        if not isinstance(compression, dict):
            raise ValueError(f"Task type {name!r} must define ai_compression")
        missing_keys = [key for key in ESTIMATE_KEYS if key not in compression]
        if missing_keys:
            raise ValueError(f"Task type {name!r} missing compression keys: {missing_keys}")

    return task_types


def build_bootstrap_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--rules",
        type=Path,
        default=DEFAULT_TASK_TYPES_PATH,
        help="Path to a task type rules YAML file.",
    )
    return parser


def build_parser(task_types: dict[str, dict[str, Any]]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        parents=[build_bootstrap_parser()],
        description="Calibrate a traditional software estimate for AI-assisted development."
    )
    parser.add_argument(
        "--traditional-hours",
        type=float,
        help="Traditional estimate in engineering hours.",
    )
    parser.add_argument(
        "--task-type",
        choices=sorted(task_types),
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
    parser.add_argument(
        "--format",
        choices=("text", "json", "markdown"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--list-task-types",
        action="store_true",
        help="List supported task types and exit.",
    )
    return parser


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.list_task_types:
        return
    if args.traditional_hours is None:
        parser.error("--traditional-hours is required unless --list-task-types is used")
    if args.task_type is None:
        parser.error("--task-type is required unless --list-task-types is used")
    if args.traditional_hours < 0:
        parser.error("--traditional-hours must be non-negative")
    if args.verification_hours < 0:
        parser.error("--verification-hours must be non-negative")
    if args.risk_buffer < 0:
        parser.error("--risk-buffer must be non-negative")


def estimate(
    traditional_hours: float,
    task: dict[str, Any],
    verification_hours: float,
    risk_buffer: float,
) -> dict[str, float]:
    compression = task["ai_compression"]
    return {
        key: round((traditional_hours * float(compression[key]) + verification_hours) * (1 + risk_buffer), 2)
        for key in ESTIMATE_KEYS
    }


def list_task_types(task_types: dict[str, dict[str, Any]], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(task_types, indent=2, sort_keys=True))
        return

    for name in sorted(task_types):
        task = task_types[name]
        print(f"{name}: {task.get('label', name)}")


def print_estimate_text(args: argparse.Namespace, task: dict[str, Any], adjusted: dict[str, float]) -> None:
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


def print_estimate_markdown(args: argparse.Namespace, task: dict[str, Any], adjusted: dict[str, float]) -> None:
    print("# AI-Assisted Estimate")
    print()
    print(f"- Traditional estimate: {args.traditional_hours:.1f}h")
    print(f"- Task type: `{args.task_type}` ({task['label']})")
    print(f"- Confidence: {task['confidence']}")
    if args.verification_hours:
        print(f"- Fixed verification/review time added: {args.verification_hours:.1f}h")
    if args.risk_buffer:
        print(f"- Risk buffer applied: {args.risk_buffer:.0%}")
    print()
    print("| Range | Estimate |")
    print("| --- | ---: |")
    print(f"| Optimistic | {adjusted['optimistic']:.1f}h |")
    print(f"| Expected | {adjusted['expected']:.1f}h |")
    print(f"| Conservative | {adjusted['conservative']:.1f}h |")


def main(argv: list[str] | None = None) -> int:
    bootstrap_parser = build_bootstrap_parser()
    bootstrap_args, _ = bootstrap_parser.parse_known_args(argv)

    try:
        task_types = load_task_types(bootstrap_args.rules)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    parser = build_parser(task_types)
    args = parser.parse_args(argv)
    validate_args(parser, args)

    if args.list_task_types:
        list_task_types(task_types, args.format)
        return 0

    task = task_types[args.task_type]
    adjusted = estimate(
        traditional_hours=args.traditional_hours,
        task=task,
        verification_hours=args.verification_hours,
        risk_buffer=args.risk_buffer,
    )

    if args.format == "json":
        payload = {
            "traditional_estimate_hours": args.traditional_hours,
            "task_type": args.task_type,
            "task_label": task["label"],
            "ai_adjusted_estimate_hours": adjusted,
            "confidence": task["confidence"],
            "verification_hours": args.verification_hours,
            "risk_buffer": args.risk_buffer,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif args.format == "markdown":
        print_estimate_markdown(args, task, adjusted)
    else:
        print_estimate_text(args, task, adjusted)

    return 0


if __name__ == "__main__":
    sys.exit(main())
