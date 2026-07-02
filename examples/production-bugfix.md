# Example: Production Bugfix

## Request

Investigate and fix an intermittent production checkout failure.

## Traditional Estimate

2 days

## AI-Adjusted Estimate

- Optimistic: 0.5 day
- Expected: 1.5 days
- Conservative: 2.5 days

## Why It Changed

- AI may accelerate log analysis, hypothesis generation, and patch drafting.
- Intermittent bugs remain hard when reproduction is unclear.
- Rollout safety and verification can exceed implementation time.

## Risks

- No reliable reproduction yet.
- Third-party payment API may be involved.
- Fix may require production monitoring before confidence is high.
