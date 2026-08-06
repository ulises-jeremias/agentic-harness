# Example 3 — Full: High-Risk Change (sanitized)

**Task:** Migrate auth to new JWT issuer with rotation.

**Why full:** touches auth, DB, security, requires QA.

**Run:** `agent-toolkit swarm start --recipe full --ui herdr --runner skeleton "Migrate auth to new JWT"`

**Roles activated lazily:**

1. Planner → task-contract + risk (auth change → security risk)
2. Implementer → commit
3. Refactorer → clean up legacy issuer
4. Architect → integration (public contract, dependency direction)
5. Hardener — *conditional*: planner flagged auth → specialist `security-reviewer` selected (not all specialists). Architect activates via `agent-toolkit swarm activate RUN_ID hardener`.
6. QA → E2E, smoke, acceptance, final validation.

**Specialist selection (trace):**

```json
{"kind":"specialist_selected","role":"hardener","persona":"security-reviewer","reason":"auth JWT change"}
```

**Hardener output:** `artifacts/hardening-report.md` — no hard-coded secrets, rotation tested, no external-directory writes.

**QA:** `artifacts/qa-report.md` — E2E login/refresh/rotation, release smoke.

**Final gate:** human `approve RUN_ID final` before any base-branch merge (no auto-merge by design).

**Promotion:** Started as `team`, architect detected security → `promote RUN_ID --to full` (preserves run ID, branches, trace).

**Sanitized artifacts in `artifacts/`:** task-contract, risk-assessment, hardening-report, qa-report, final-report, cost report (0 tokens offline).
