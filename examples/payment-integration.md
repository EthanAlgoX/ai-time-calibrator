# Example: Payment Integration

## Request

Integrate a third-party payment provider for one-time checkout and webhook-based order confirmation.

## Traditional Estimate

6 days

## AI-Adjusted Estimate

- Optimistic: 3 days
- Expected: 4.5 days
- Conservative: 6.5 days

## Why It Changed

- AI can speed up SDK usage, webhook handler scaffolding, tests, and documentation lookup.
- External provider behavior, sandbox differences, and payment correctness limit compression.
- Verification across success, failure, retry, and duplicate webhook cases remains important.

## Risks

- Third-party API quirks.
- Idempotency and financial correctness.
- Staging credentials, webhook tunneling, and deployment access.
