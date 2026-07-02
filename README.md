# AI Time Calibrator

Calibrate software development estimates for AI-assisted workflows.

[中文说明](README.zh-CN.md)

AI coding agents can dramatically change the time it takes to build software, but many estimates still assume a pre-AI workflow: manual boilerplate, slower test writing, slower documentation lookup, and less automated refactoring. AI Time Calibrator is an open framework for turning traditional engineering estimates into explainable AI-assisted estimates.

The goal is not to make every estimate shorter. The goal is to make estimates more realistic.

## What This Project Does

- Classifies software tasks by how much AI can actually accelerate them.
- Separates implementation time from verification, integration, human decision-making, and unknown risk.
- Produces ranges instead of false-precision single numbers.
- Explains why the calibrated estimate changed.
- Provides reusable rules for humans, AI coding agents, and project planning tools.

## Estimate Model

AI Time Calibrator uses a simple model:

```text
calibrated effort =
  implementation effort after AI compression
  + verification effort
  + integration effort
  + risk buffer
  + human bottleneck time
```

This keeps fast code generation from hiding the parts AI cannot fully compress: acceptance criteria, product judgment, review, QA, deployment, permissions, and coordination.

## Repository Layout

```text
rules/
  task-types.yaml            Task categories and default AI compression ranges
  risk-factors.yaml          Risk multipliers and uncertainty signals
  calibration-model.yaml     Estimation workflow and output contract
adapters/
  claude-code/CLAUDE.md      Claude Code adapter
  cursor/rules.md            Cursor rules adapter
  windsurf/rules.md          Windsurf rules adapter
skills/
  codex/SKILL.md             Codex skill adapter
examples/
  auth-feature.md            Example estimate
  crud-api.md                Example estimate
  database-migration.md      Example estimate
  frontend-page.md           Example estimate
  payment-integration.md     Example estimate
  performance-optimization.md  Example estimate
  refactor-module.md         Example estimate
  production-bugfix.md       Example estimate
scripts/
  estimate.py                Dependency-free CLI prototype
tests/
  test_estimate_cli.py       CLI behavior tests
  test_rules.py              Rule integrity tests
dataset/
  estimates.yaml             Example calibration dataset structure
schema/
  task-types.schema.json      Task type rule schema
  estimate-output.schema.json CLI JSON output schema
  dataset.schema.json         Dataset schema
```

## Dataset

The dataset starts as an example structure for collecting anonymized estimate cases:

```text
dataset/estimates.yaml
```

## Quick Start

List supported task types:

```bash
python3 scripts/estimate.py --list-task-types
```

Estimate from a traditional duration and a task type:

```bash
python3 scripts/estimate.py --traditional-hours 24 --task-type crud_api
```

Example output:

```text
Traditional estimate: 24.0h
Task type: crud_api (CRUD, API endpoint, or standard backend feature)
AI-adjusted estimate:
  optimistic:   6.0h
  expected:     9.1h
  conservative: 14.4h
Confidence: medium
```

Add verification time and risk buffer:

```bash
python3 scripts/estimate.py \
  --traditional-hours 16 \
  --task-type frontend_page \
  --verification-hours 2 \
  --risk-buffer 0.2
```

Generate JSON output:

```bash
python3 scripts/estimate.py --traditional-hours 24 --task-type crud_api --format json
```

Generate Markdown output:

```bash
python3 scripts/estimate.py --traditional-hours 24 --task-type crud_api --format markdown
```

Use a custom task type rules file:

```bash
python3 scripts/estimate.py \
  --rules ./my-team-task-types.yaml \
  --traditional-hours 24 \
  --task-type crud_api
```

Write output to a file:

```bash
python3 scripts/estimate.py \
  --traditional-hours 24 \
  --task-type crud_api \
  --format markdown \
  --output report.md
```

## Schemas

JSON Schema files live in:

```text
schema/
```

They document the task type rule format, CLI JSON output, and dataset records.

## AI Tool Adapters

The first Codex skill adapter is available at:

```text
skills/codex/SKILL.md
```

Install or copy it into your Codex skills directory, then ask Codex to estimate development tasks. The skill guides Codex to classify the task, apply AI-era calibration, and return a range with assumptions and risks.

Example prompt:

```text
Use $ai-time-calibrator to estimate building a CRUD API with tests.
```

Additional adapters:

```text
adapters/claude-code/CLAUDE.md
adapters/cursor/rules.md
adapters/windsurf/rules.md
```

These adapters reuse the same calibration model so estimates stay consistent across tools.

## Core Principle

AI compresses some work much more than others:

| Work type | AI acceleration | Notes |
| --- | --- | --- |
| Boilerplate | Very high | Often highly pattern-based |
| CRUD/API work | High | Strong when existing patterns are clear |
| Test generation | High | Human verification still matters |
| UI implementation | Medium to high | Visual QA and product taste remain important |
| Refactoring | Medium | Depends heavily on test coverage |
| Debugging | Variable | Can be very fast or barely helped |
| Architecture | Low to medium | AI helps explore, humans decide |
| Requirements | Low | Ambiguity is usually a human bottleneck |
| Cross-system integration | Variable | External dependencies dominate |

## Status

This is an early v0.1 project. The current focus is defining a clear estimation model, simple rule files, a tested CLI, and AI-agent adapters. Contributions with real before/after estimate examples are especially useful.

## Testing

Run the local test suite:

```bash
python3 -m py_compile scripts/estimate.py
python3 -m unittest discover -s tests
```

The GitHub Actions workflow runs the same checks on push and pull request.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add task types, propose calibration changes, or submit real-world estimate examples.

## License

MIT
