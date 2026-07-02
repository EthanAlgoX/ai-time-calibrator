# Example: Performance Optimization

## Request

Reduce dashboard load time from 6 seconds to under 2 seconds.

## Traditional Estimate

5 days

## AI-Adjusted Estimate

- Optimistic: 2 days
- Expected: 3.5 days
- Conservative: 5.5 days

## Why It Changed

- AI can help inspect queries, identify suspicious code paths, and draft optimization patches.
- Measurement, profiling, and proving the improvement are not fully compressible.
- If the bottleneck is obvious, AI acceleration is strong; if not, discovery dominates.

## Risks

- Missing production-like data locally.
- Cache changes may create correctness issues.
- Performance goals may require infrastructure or product tradeoffs.
