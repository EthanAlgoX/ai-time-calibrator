# AI Time Calibrator Windsurf Rules

Use these rules whenever estimating software engineering effort in an AI-assisted workflow.

## Process

1. Identify the task type or split the task into multiple task types.
2. Keep implementation, verification, integration, human bottlenecks, and risk separate.
3. Apply AI compression to implementation work only when the work is pattern-based or well-specified.
4. Return a range: optimistic, expected, conservative.
5. Explain the estimate in terms of acceleration drivers and remaining risks.

## Calibration Formula

```text
calibrated effort =
  implementation effort after AI compression
  + verification effort
  + integration effort
  + risk buffer
  + human bottleneck time
```

## Heuristics

- Boilerplate, CRUD, test drafting, and repeated framework code often compress strongly.
- UI work still needs visual QA, accessibility checks, and product polish.
- Refactoring depends on test coverage and hidden coupling.
- Debugging is highly variable; reproduction quality matters.
- Architecture and requirements work are only weakly compressed.
- Cross-system integration is limited by external APIs, environments, auth, and coordination.

## Response Format

```text
Traditional estimate:
AI-adjusted estimate:
- Optimistic:
- Expected:
- Conservative:

Task type:
Confidence:
Why the estimate changed:
Risks and buffers:
Assumptions:
Suggested next steps:
```
