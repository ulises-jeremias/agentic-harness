# Example 2 — Team: Implement a Feature (sanitized)

**Task:** Add pagination to `/api/users` without breaking public contract.

**Run:**

```bash
agent-toolkit swarm start --recipe team --ui herdr --runner skeleton "Add pagination to /api/users"
# Run: 20260806T121000Z-bb1234, awaiting_plan_approval
agent-toolkit swarm approvals 20260806T121000Z-bb1234
agent-toolkit swarm approve 20260806T121000Z-bb1234 plan
# → running → planner produces artifacts, hands off to implementer
```

**Planner artifacts (read-only):**

- `task-contract.md` — paginate with `?page&per_page`, default 20, max 100.
- `acceptance-criteria.md` — existing clients without pagination still work (default page 1).
- `risk-assessment.md` — low risk, but public contract change needs architect gate if pagination headers added.
- `context-manifest.json` — includes `src/api/users.py`, `tests/test_users.py`, persona `planner`.

**Flow:** planner → implementer (commit) → reviewer (feedback) → architect (batch integration, final report) → human approval.

**Handoff example:**

```yaml
type: commit
from: implementer
to: reviewer
commit: cccccccccccccccccccccccccccccccccccccccc
branch: agent-toolkit-swarm/20260806T121000Z-bb1234/implementer
artifact: artifacts/implementation-report.md
```

**Review:** blocking feedback once (missing per_page validation), implementer fixes, reviewer then approves.

**Architect:** owns module boundaries, dependency direction, ensures `Link` header optional, no breaking change, merges owned branches in integration worktree, produces final report.

**Cost (offline):** tokens 0, wall 12s, cost $0.00 (skeleton). See `artifacts/` sanitized.
