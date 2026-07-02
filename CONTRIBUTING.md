# Contributing

AI Time Calibrator improves when people contribute real examples, careful rule changes, and adapters for more AI coding tools.

## Useful Contributions

- Real before/after estimate examples.
- New task types with clear evidence.
- Adjustments to AI compression ranges.
- Better CLI output or validation.
- AI-agent adapters for tools such as Claude Code, Cursor, or Windsurf.

## Add a Real Estimate Example

Add a Markdown file under `examples/` with this structure:

```markdown
# Example: Short Name

## Request

What was being built or changed.

## Traditional Estimate

The estimate before AI-assisted calibration.

## AI-Adjusted Estimate

- Optimistic:
- Expected:
- Conservative:

## Why It Changed

- What AI accelerated.
- What remained human-owned or verification-heavy.

## Risks

- Unknowns, dependencies, or quality concerns.
```

Avoid private customer data, secrets, proprietary code, and names of non-public systems.

## Change Calibration Rules

Task type rules live in `rules/task-types.yaml`.

When changing a compression range:

- Explain the scenario the change improves.
- Prefer a range over a single number.
- Keep `optimistic <= expected <= conservative`.
- Keep factors between `0.0` and `1.5`.
- Add or update an example when possible.

## Run Tests

Before opening a pull request:

```bash
python3 -m py_compile scripts/estimate.py
python3 -m unittest discover -s tests
```

## Pull Request Checklist

- The change has a clear reason.
- Tests pass locally.
- README or examples are updated when behavior changes.
- Rule changes include rationale or a real-world example.
