---
name: ai-time-calibrator
description: Use when estimating software development time, implementation effort, sprint scope, project timelines, or comparing traditional engineering estimates against AI-assisted development estimates.
---

# AI Time Calibrator

Use this skill to estimate software development work in an AI-assisted workflow. Do not assume all work speeds up equally. Separate code generation from verification, integration, decision-making, and risk.

## Core Workflow

1. Identify the task type. If the request mixes multiple kinds of work, split it into smaller estimate components.
2. Ask only for missing information that materially changes the estimate. If the user needs a quick estimate, state assumptions instead.
3. Apply AI compression only to implementation work that AI can accelerate.
4. Keep verification, integration, human bottlenecks, and risk visible.
5. Return optimistic, expected, and conservative estimates.
6. Explain what got faster, what did not, and why.

## Task Type Defaults

- Boilerplate or scaffolding: very high AI acceleration.
- CRUD, API endpoint, or standard backend feature: high acceleration if existing patterns are clear.
- Test generation: high drafting acceleration, but human verification remains important.
- Frontend page or component: medium to high acceleration; visual QA and polish remain important.
- Refactor: medium acceleration; test coverage determines risk.
- Debugging: highly variable; estimate investigation separately if reproduction is unclear.
- Architecture or technical design: low to medium acceleration; AI helps explore, humans decide.
- Requirements or stakeholder alignment: low acceleration.
- Cross-system integration: variable; external dependencies dominate.

## Estimation Formula

```text
calibrated effort =
  implementation effort after AI compression
  + verification effort
  + integration effort
  + risk buffer
  + human bottleneck time
```

## Response Format

Use this structure unless the user asks for another format:

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

## Calibration Rules

- Prefer ranges over single-point estimates.
- Do not reduce time spent on unclear requirements, approvals, waiting, or production safety just because AI is available.
- For debugging, separate "time to reproduce/diagnose" from "time to implement fix".
- For high-risk production work, use conservative estimates even when implementation looks easy.
- If the user provides a traditional estimate, calibrate from it. If not, estimate from task breakdown and state confidence.
- If acceptance criteria are unclear, either ask for clarification or label the estimate low confidence.
