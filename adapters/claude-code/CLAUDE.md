# AI Time Calibrator for Claude Code

Use this guidance when estimating software development time, implementation effort, project timelines, or sprint scope in an AI-assisted workflow.

## Estimation Workflow

1. Classify the task type. If the task mixes multiple kinds of work, split it into estimate components.
2. Separate implementation, verification, integration, human bottlenecks, and risk.
3. Apply AI compression only to work AI can realistically accelerate.
4. Return optimistic, expected, and conservative estimates.
5. State assumptions, confidence, acceleration drivers, and risks.

## Calibration Formula

```text
calibrated effort =
  implementation effort after AI compression
  + verification effort
  + integration effort
  + risk buffer
  + human bottleneck time
```

## Default Task Categories

- Boilerplate or scaffolding: very high AI acceleration.
- CRUD, API endpoint, or standard backend feature: high acceleration when existing patterns are clear.
- Test generation: high drafting acceleration, but intent and coverage need human review.
- Frontend page or component: medium to high acceleration; visual QA and polish remain meaningful.
- Refactor: medium acceleration; test coverage determines risk.
- Debugging: variable; separate reproduction/diagnosis from implementation.
- Architecture or technical design: low to medium acceleration; humans own tradeoffs.
- Requirements or stakeholder alignment: low acceleration.
- Cross-system integration: variable; external dependencies dominate.

## Response Template

```text
Traditional estimate:
AI-adjusted estimate:
- Optimistic:
- Expected:
- Conservative:

Task type:
Confidence:

Why the estimate changed:
- ...

Risks and buffers:
- ...

Assumptions:
- ...

Suggested next steps:
- ...
```

## Rules

- Prefer ranges over single-point estimates.
- Do not compress unclear requirements, approval waits, production safety, or stakeholder alignment just because AI is available.
- For debugging, estimate investigation separately when reproduction is unclear.
- For production or security-sensitive work, bias toward conservative estimates.
- If information is missing, ask only for details that materially affect the estimate; otherwise state assumptions.
