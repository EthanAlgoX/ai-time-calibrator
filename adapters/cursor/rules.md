# AI Time Calibrator Cursor Rules

When asked to estimate software development time, use AI-assisted calibration instead of pre-AI assumptions.

## Required Behavior

- Classify the task type before estimating.
- Split mixed work into implementation, verification, integration, human bottleneck, and risk.
- Apply AI acceleration only to compressible implementation work.
- Return optimistic, expected, and conservative estimates.
- Include assumptions, confidence, acceleration drivers, and risks.

## Formula

```text
calibrated effort =
  implementation effort after AI compression
  + verification effort
  + integration effort
  + risk buffer
  + human bottleneck time
```

## Important Constraints

- Do not treat AI as a flat multiplier over the whole project.
- Do not compress stakeholder alignment, approvals, or unclear requirements much.
- Debugging estimates should separate diagnosis from fix implementation.
- Production, security, compliance, migration, and payment work should use conservative ranges.

## Output Shape

```text
Traditional estimate:
AI-adjusted estimate:
- Optimistic:
- Expected:
- Conservative:

Task type:
Confidence:
Assumptions:
Acceleration drivers:
Risks:
Suggested next steps:
```
