# Example: Database Migration

## Request

Add a new required billing field and backfill existing customer records in production.

## Traditional Estimate

3 days

## AI-Adjusted Estimate

- Optimistic: 1.5 days
- Expected: 2.25 days
- Conservative: 3.5 days

## Why It Changed

- AI can draft migration scripts, backfill code, validation checks, and rollback notes.
- Production safety, data verification, and rollout sequencing are only weakly compressible.
- The implementation may be short while the confidence-building work remains substantial.

## Risks

- Incomplete historical data.
- Long-running migrations or lock contention.
- Rollback strategy may require manual planning.
