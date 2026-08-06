# Example 1 — Pair: Fix a Bug (sanitized)

**Task:** Fix off-by-one in auth cache TTL.

**Request:** `examples/swarms/fix-a-bug/request.md`

```text
Implement fix for auth cache expiring immediately under concurrent load.
See issue #123 — TTL should be 300s, currently effective 0 due to int division.
```

**Run (offline, no LLM):**

```bash
agent-toolkit swarm start --recipe pair --ui tmux --runner skeleton "Fix auth cache TTL off-by-one"
# Created: 20260806T120000Z-abcdef
```

**Worktrees:**

- `agent-toolkit-swarm/20260806T120000Z-abcdef/implementer` at `.agent-toolkit/swarm/runs/20260806T120000Z-abcdef/worktrees/implementer`
- `agent-toolkit-swarm/20260806T120000Z-abcdef/reviewer` (lazy, created after implementer commit)

**Handoff:**

```json
{
  "type": "commit",
  "from": "implementer",
  "to": "reviewer",
  "commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "branch": "agent-toolkit-swarm/20260806T120000Z-abcdef/implementer",
  "artifact": "artifacts/implementation-report.md"
}
```

**Artifacts (sanitized):**

- `artifacts/task-contract.md` — TTL spec, acceptance: cache hit rate >95% under 100 concurrent.
- `artifacts/implementation-report.md` — changed `ttl // 1000` to `ttl / 1000.0`, updated test `test_cache_ttl`.
- `artifacts/review.md` — reviewer: no security issues, complexity low, coverage added, approved with nit.
- `artifacts/final-report.md` — final candidate at `agent-toolkit-swarm/20260806T120000Z-abcdef/reviewer`, human approval pending.

**Cost report (sanitized, no live LLM):**

```text
budget: max_total_tokens=900000, max_cost_usd=4.00, wall=7200s
usage: total_tokens=0 (skeleton runner, no LLM call)
trace events: 12 (run_created, worktree_created, handoff_created, etc.)
```

**Cleanup:**

```bash
agent-toolkit swarm status 20260806T120000Z-abcdef
agent-toolkit swarm cleanup 20260806T120000Z-abcdef --dry-run
agent-toolkit swarm cleanup 20260806T120000Z-abcdef  # preserves dirty, keeps branches
```

See `artifacts/` below for full sanitized files.
