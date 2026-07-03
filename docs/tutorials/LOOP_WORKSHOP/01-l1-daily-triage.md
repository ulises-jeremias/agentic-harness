# Part 1: L1 — Daily Issue Triage

> Build a read-only loop that scans open issues and writes a morning report.

**Time**: 30 minutes | **Tier**: L1 (report-only) | **Risk**: None — read-only

---

## What You'll Learn

- LOOP.md contract format
- STATE.md state tracking
- Tier 1 safety: no writes, no comments, no labels
- Budget configuration
- Exit conditions

---

## Step 1: Create the Loop

```bash
cd ~/.ai-workspace
./bin/loop init daily-triage --template daily-triage --tier 1
```

Expected output:

```text
Created: loops/daily-triage/
├── LOOP.md    # Loop contract
├── STATE.md   # Execution state
```

---

## Step 2: Understand LOOP.md

Open `loops/daily-triage/LOOP.md`. Let's walk through each section:

### Metadata

```yaml
name: daily-triage
description: "Triage new issues and propose labels (report-only)"
tier: L1
cadence: 1d
```

- **tier: L1** — This loop cannot modify anything. No PRs, no comments, no labels.
- **cadence: 1d** — Designed to run once per day.

### Goal

```yaml
goal: |
  Review all open issues created in the last 24 hours.
  Propose labels and priority scores. Do NOT apply them — write a report.
```

### Permissions

```yaml
allowlist: []         # Nothing allowed
deny:
  - merge
  - close
  - label            # Cannot label issues
  - comment          # Cannot comment
  - push             # Cannot push
```

The empty `allowlist` means: this loop cannot write anything. The `deny` list is explicit but redundant — with an empty allowlist, everything is denied.

### Budget

```yaml
budget:
  max_tokens: 30000
  max_runs_per_day: 1
  max_wall_seconds: 300
```

- **max_tokens**: 30K tokens per run (~$0.03 with Claude Sonnet)
- **max_runs_per_day**: 1 — won't run more than once per 24 hours
- **max_wall_seconds**: 300 — 5 minute timeout

### Request (the AI prompt)

```yaml
request: |
  You are running the daily-triage loop for this repository.
  1. List all open issues created in the last 24 hours (use gh cli).
  2. For each issue, propose priority and labels.
  3. Write a report.md with the proposals.
  4. Do NOT make any changes — this is observation-only.
  5. If you find a security issue: escalate immediately.
```

---

## Step 3: Dry-Run

Always dry-run first:

```bash
./bin/loop run daily-triage --dry-run --verbose
```

Expected output:

```text
[DRY-RUN] Would run: daily-triage (Tier 1)
  Purpose: Review open issues from last 24h, write report
  Budget: 30,000 tokens max
  Permissions: read-only (allowlist is empty)
  Would generate: loops/daily-triage/report.md
  No changes will be made.
```

---

## Step 4: First Real Run

```bash
./bin/loop run daily-triage
```

Check the output:

```bash
cat loops/daily-triage/report.md
```

Expected output (example):

```markdown
# Daily Triage Report — 2026-07-03

## Issues Created in Last 24 Hours

### #142 — Login page 500 error on invalid email
- **Priority**: high
- **Proposed Labels**: bug, frontend, p1
- **Summary**: Form validation missing for email format, causing 500 instead of 422

### #143 — Add dark mode toggle to settings
- **Priority**: medium
- **Proposed Labels**: enhancement, frontend, ux
- **Summary**: Feature request for dark mode support in user settings

## Escalations
None.
```

---

## Step 5: Check STATE.md

After the run, check the state:

```bash
cat loops/daily-triage/STATE.md
```

```yaml
loop: daily-triage
last_run: "2026-07-03T09:00:00Z"
last_exit_code: 0
total_runs: 1
successful_runs: 1
total_tokens: 4821
last_output: "Report saved to report.md — 2 issues found, 0 escalated"
```

The STATE.md persists between runs. The next run reads this state — it knows what happened last time.

---

## Step 6: Schedule It

Now make it automatic:

```bash
./bin/loop schedule daily-triage
```

```text
Created: ~/.config/systemd/user/agentic-harness-daily-triage.service
Created: ~/.config/systemd/user/agentic-harness-daily-triage.timer
Next run: 2026-07-04 09:00:00 UTC
```

Verify:

```bash
./bin/loop schedule --list
```

```text
NAME           SCHEDULE    NEXT RUN            ENABLED
daily-triage   every 24h   2026-07-04 09:00    yes
```

---

## What You Built

| Component | What it does |
|-----------|-------------|
| LOOP.md | The loop's contract — immutable between runs |
| STATE.md | Execution state — evolves with each run |
| report.md | The loop's output — read-only, never modifies anything |
| Schedule | systemd timer runs it every 24 hours |

### Key L1 Lessons

1. **Tier 1 is safe by design**: empty allowlist, explicit deny list
2. **Budget prevents runaway costs**: max_tokens, max_wall_seconds
3. **STATE.md is the loop's memory**: carries context between runs
4. **Exit conditions stop bad loops**: budget_exhausted, human_escalation
5. **Always dry-run first**: before running anything for real

---

## Verify It Worked

```bash
# Check loop status
./bin/loop status --tier 1

# Check last run details
./bin/loop audit daily-triage --last 1

# Check cost
./bin/loop cost daily-triage
```

---

## Next Step

You have a working L1 loop. In [Part 2](02-l2-pr-babysitter.md), you'll add write capability — drafting PR comments with a human approval gate.
