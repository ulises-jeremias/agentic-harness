# Part 3: L3 — CI Sweeper

> Build an autonomous loop that detects CI failures and opens fix PRs.

**Time**: 30 minutes | **Tier**: L3 (unattended) | **Risk**: Medium — creates draft PRs

---

## What You'll Learn

- Maker/checker pattern for autonomous writes
- max_iterations for self-correcting loops
- Worktree-based safe edits
- Progressive L1→L2→L3 promotion
- Exit condition DSL

---

## Step 1: Start at L1 (Observe First)

**Never start a loop at L3.** Begin by observing:

```bash
./bin/loop init ci-sweeper --template ci-sweeper --tier 1
```text

The L1 version is configured to **observe only** — no writes. Let it run for a few days so you see what it would do.

---

## Step 2: Run L1 and Review

```bash
./bin/loop run ci-sweeper --verbose
```text

```text
[L1 - OBSERVE ONLY] CI failures detected:
  - backend: lint check failing on feat/ACME-456 branch
  - frontend: type-check error in components/Header.tsx

Would create draft PRs for: 2 failures
Would open PRs: 0 (L1 — observation only)
Report saved to: loops/ci-sweeper/report.md
```text

Review the report. Are these real failures? Are the proposed fixes correct? Running at L1 for a week builds confidence.

---

## Step 3: Promote to L2 (Draft PRs Only)

After a week of clean L1 reports:

```bash
# Edit LOOP.md: change tier: L1 to tier: L2
# Add to allowlist: [create_draft_pr, comment]
```text

```yaml
tier: L2
allowlist:
  - comment
  - create_draft_pr
deny:
  - merge
  - approve
  - close
  - force-push
  - delete-branch
```text

Now the loop creates **draft** PRs:

```bash
./bin/loop run ci-sweeper
```text

```text
[L2 - DRAFT PRs ONLY]
  backend (lint fix): Draft PR #150 created
  frontend (type error): Draft PR #151 created
  Draft PRs require manual review before publishing
```text

Wait for the CI on the draft PRs to pass. Review them. If they look good after a month, consider L3.

---

## Step 4: Understand the Maker/Checker Pattern

L3 loops use **two agents** working together:

```text
Maker agent                    Checker agent
  │                               │
  │ 1. Detects CI failure         │
  │ 2. Diagnoses root cause       │
  │ 3. Creates worktree           │
  │ 4. Makes fix                  │
  │ 5. Opens DRAFT PR             │
  │                               │
  │        6. Reviews diff ──────→│
  │                               │ 7. Runs tests on fix
  │                               │ 8. Checks for regressions
  │        9. Verdict ───────────→│
  │                               │
  │ 10. If approved: mark ready   │
  │ 11. If rejected: rollback     │
```text

The checker agent (verifier) is the safety net. It runs independently from the maker.

> **Hard gate:** During `loop run`, mutating `gh` commands are intercepted by
> `bin/loop-gh-gate`. merge/close require a JSON receipt under
> `runs/<id>/verifier-receipts/` or the command exits with code 78.

---

## Step 5: Promote to L3

```yaml
tier: L3
allowlist:
  - comment
  - create_draft_pr
  - mark_ready_for_review
deny:
  - merge
  - approve
  - close
  - force-push
  - delete-branch
exit_conditions:
  - goal_met
  - budget_exhausted
  - human_escalation
  - max_iterations       # New: stop after N fix attempts
  - consecutive_failures # New: stop if fixes keep failing
budget:
  max_tokens: 100000
  max_runs_per_day: 48
  max_wall_seconds: 900
  max_iterations: 3      # Max 3 fix attempts per failure
```text

---

## Step 6: First L3 Run

```bash
./bin/loop run ci-sweeper --verbose
```text

```text
[L3 - AUTONOMOUS]
  Iteration 1:
    backend (lint): fix applied → CI running...
    frontend (type): fix applied → CI running...

  Iteration 2:
    backend (lint): CI PASSED ✓ → PR #152 marked ready
    frontend (type): CI FAILED — retrying with different approach

  Iteration 3:
    frontend (type): CI PASSED ✓ → PR #153 marked ready

  Summary: 2 fixes, 2 successful, 0 escalations
  Budget: 78,432 / 100,000 tokens used
```text

---

## Step 7: Schedule Aggressively

```bash
./bin/loop schedule ci-sweeper --cron "0 */1 * * *"
```text

L3 runs every hour — catching failures quickly.

---

## Exit Conditions Deep Dive

```yaml
exit_conditions:
  - goal_met              # All failures fixed → stop
  - budget_exhausted      # Hit token limit → stop
  - human_escalation      # Security issue or complex failure → escalate
  - max_iterations        # Tried 3 times, still failing → escalate
  - consecutive_failures  # 3 failures in a row → escalate
```text

### When exit conditions trigger

```text
Run 1: 2 failures, both fixed       → goal_met → STOP
Run 2: 1 failure, fix works         → goal_met → STOP
Run 3: 1 failure, fix fails         → retry (iteration 2/3)
Run 4: same failure, fix fails again → retry (iteration 3/3)
Run 5: still failing                → max_iterations → ESCALATE
```text

The loop knows when to stop trying. Without exit conditions, a loop would retry forever.

---

## Cost Analysis

```bash
./bin/loop cost ci-sweeper --monthly
```text

```text
LOOP: ci-sweeper (L3)
Per run:  ~30,000 tokens  ~$0.30
Per day:  ~720,000 tokens ~$7.20  (24 runs/day max)
Per month: ~21,600,000 tokens ~$216.00

Optimization: Only 2-3 runs/day actually have failures.
Realistic cost: ~$20-30/month.
```text

---

## What You Built

| Component | L1 (Triage) | L2 (Babysitter) | L3 (Sweeper) |
|-----------|------------|-----------------|-------------|
| Writes | No | Draft comments | Draft PRs + mark ready |
| Autonomy | Manual | Human reviews | Maker/checker automated |
| Frequency | 1/day | 6/day | 24/day |
| Verifier | None | code-reviewer | code-reviewer on every PR |
| Iterations | 1 | 1 | Up to 3 |
| Cost/month | ~$0.90 | ~$27.00 | ~$30.00 |

### Key L3 Lessons

1. **Never start at L3**: Always progress L1 → L2 → L3 over weeks
2. **Maker/checker is the safety net**: Two agents independently verify
3. **Exit conditions prevent infinite loops**: max_iterations, consecutive_failures
4. **Worktree edits are safe**: Changes in isolated worktrees, not main branch
5. **Budget is a hard limit**: L3 uses more tokens — budget prevents runaway costs

---

## Verify It Worked

```bash
./bin/loop status --tier 3
./bin/loop audit ci-sweeper --last 5 --summary
./bin/loop cost ci-sweeper --monthly --alert 50.00
```text

---

## Next Step

In [Part 4](04-capstone-custom-loop.md), you'll design your own loop from scratch using the loop engineering discipline.
