# AI Time Calibrator

Calibrate software development estimates for AI-assisted workflows.

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
skills/
  codex/SKILL.md             Codex skill adapter
examples/
  crud-api.md                Example estimate
  frontend-page.md           Example estimate
  refactor-module.md         Example estimate
  production-bugfix.md       Example estimate
scripts/
  estimate.py                Minimal dependency-free CLI prototype
```

## Quick Start

Estimate from a traditional duration and a task type:

```bash
python3 scripts/estimate.py --traditional-hours 24 --task-type crud_api
```

Example output:

```text
Traditional estimate: 24.0h
Task type: crud_api
AI-adjusted estimate:
  optimistic: 6.0h
  expected:   9.0h
  conservative: 14.4h
Confidence: medium
```

## Using With Codex

The first AI-agent adapter is available at:

```text
skills/codex/SKILL.md
```

Install or copy it into your Codex skills directory, then ask Codex to estimate development tasks. The skill guides Codex to classify the task, apply AI-era calibration, and return a range with assumptions and risks.

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

This is an early MVP. The current focus is defining a clear estimation model, simple rule files, and AI-agent adapters. Contributions with real before/after estimate examples are especially useful.

## License

MIT
