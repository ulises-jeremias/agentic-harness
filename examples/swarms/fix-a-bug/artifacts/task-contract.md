# Task Contract — Fix Auth Cache TTL

- **Title:** Fix auth cache immediate expiry under concurrency
- **Acceptance:** hit rate >95% with 100 concurrent, TTL=300s, no regression in auth latency.
- **Risk:** low — single file change, no public API change.
