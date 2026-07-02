# Example: Refactor Module

## Request

Refactor a legacy billing module into smaller services without changing behavior.

## Traditional Estimate

5 days

## AI-Adjusted Estimate

- Optimistic: 2.5 days
- Expected: 3.5 days
- Conservative: 5 days

## Why It Changed

- AI can help identify extraction boundaries, update call sites, and draft tests.
- The estimate does not collapse because behavior preservation and regression risk dominate.
- Strong existing tests would move the estimate toward optimistic.

## Risks

- Weak test coverage.
- Hidden coupling with reporting or invoicing flows.
- Production correctness requirements.
