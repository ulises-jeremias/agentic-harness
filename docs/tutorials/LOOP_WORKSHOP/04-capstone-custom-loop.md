# Part 4: Capstone — Build Your Own Loop

> Design a custom loop from scratch using the loop engineering discipline.

**Time**: 30 minutes | **Tier**: Your choice | **Risk**: Depends on your design

---

## What You'll Learn

- Loop design process: purpose → tier → permissions → budget → exit conditions
- Safety review checklist
- Progressive deployment strategy
- Common anti-patterns to avoid

---

## Step 1: Define Your Purpose

Start with a single sentence describing what the loop does:

> "Every Monday morning, scan all repos for outdated dependencies and open a draft PR updating them."

Or:

> "After every release, update the CHANGELOG with commits since the last tag."

Or:

> "Every hour, check if any PRs have been stale (>3 days no activity) and ping the author."

### Purpose checklist

- [ ] Can be described in one sentence
- [ ] Has clear input (what the loop reads)
- [ ] Has clear output (what the loop produces)
- [ ] Frequency makes sense (daily? hourly? weekly?)

---

## Step 2: Choose Your Tier

| Tier | Writes? | Best for |
|------|---------|----------|
| L1 | No | Reports, alerts, notifications, analysis |
| L2 | Draft only | PR reviews, changelog drafts, label suggestions |
| L3 | Yes (gated) | Auto-fixes, dependency updates, CI correction |

**Rule**: Start one tier below your target. If you want an L3 loop, deploy it at L2 first.

---

## Step 3: Define Permissions

### L1 Template

```yaml
allowlist: []
deny:
  - merge
  - close
  - label
  - comment
  - push
  - create_pr
```

### L2 Template

```yaml
allowlist:
  - comment          # What you need — be specific
deny:
  - merge
  - approve
  - close
  - force-push
  - delete-branch
  - label            # Deny anything you don't need
```

### L3 Template

```yaml
allowlist:
  - comment
  - create_draft_pr
  - mark_ready
deny:
  - merge            # NEVER allow merge at L3
  - approve          # NEVER allow self-approval
  - force-push       # NEVER force-push
  - delete-branch
```

---

## Step 4: Set Your Budget

| Loop type | max_tokens/run | max_runs/day | Est. monthly |
|-----------|---------------|-------------|-------------|
| Light (report) | 10,000 | 1 | ~$1 |
| Medium (review) | 50,000 | 6 | ~$30 |
| Heavy (auto-fix) | 100,000 | 24 | ~$200 |

### Budget formula

```
monthly_cost = max_tokens/run × max_runs/day × 30 × token_price
```

For Claude Sonnet (~$10/M tokens):

| Config | Cost/month |
|--------|-----------|
| 10K × 1/day | ~$3 |
| 50K × 6/day | ~$90 |
| 100K × 24/day | ~$720 |

Set your budget **conservatively** — you can increase it after observing real usage.

---

## Step 5: Write Exit Conditions

Every loop needs exit conditions. Here are the standard ones:

### Required exit conditions

```yaml
exit_conditions:
  - goal_met           # Task complete → stop
  - budget_exhausted   # Hit token limit → stop
  - human_escalation   # Something needs a human → escalate
```

### Optional exit conditions (L2+)

```yaml
  - max_iterations: 3       # Stop retrying after N attempts
  - consecutive_failures: 3 # Stop if failing repeatedly
  - cost_exceeds: 5.00      # Stop if daily cost exceeds threshold
  - error_rate > 0.1        # Stop if >10% of runs fail
```

---

## Step 6: Write the Request (AI Prompt)

The `request` is the prompt the loop sends to the AI. Write it like a job description:

```yaml
request: |
  You are running the [loop-name] loop for this repository.
  1. [Step 1 of the workflow]
  2. [Step 2]
  3. ...
  Constraints:
  - Do NOT [forbidden action]
  - Max [N] [items] per run
  - If [escalation condition]: escalate immediately
  Output:
  - Write [report.md / plan.md / state update]
```

### Example: Dependency Updater Loop

```yaml
request: |
  You are running the dependency-updater loop.
  1. Scan all repos in the active pack for outdated dependencies.
     - Python: use `pip list --outdated` or uv
     - Node: use `npm outdated` or pnpm
  2. For each outdated package that has a compatible update:
     a. Create a worktree for the repo
     b. Update the dependency to the latest compatible version
     c. Run tests
  3. If tests pass: open a DRAFT PR with the update
  4. If tests fail: rollback, note the failure in report.md
  5. Max 3 PRs per run
  6. Do NOT update major versions — those need human review
  7. If you find a CVE (security vulnerability): escalate immediately
  Output: report.md with updated packages, PRs opened, failures
```

---

## Step 7: Safety Review Checklist

Before deploying your loop, verify:

### Tier 1 safety

- [ ] `allowlist` is empty
- [ ] `deny` includes all write operations
- [ ] No API tokens accessible
- [ ] Output is a local file (report.md)

### Tier 2 safety

- [ ] `allowlist` is minimal (only what's needed)
- [ ] `deny` includes merge, approve, close, force-push
- [ ] All writes are drafts (comments, draft PRs)
- [ ] `verifier` is configured
- [ ] Human approval gate documented

### Tier 3 safety

- [ ] Maker/checker pattern implemented
- [ ] Exit conditions prevent infinite loops
- [ ] `max_iterations` set (≤ 3)
- [ ] `consecutive_failures` set (≤ 5)
- [ ] Cost alert configured
- [ ] Loop runs in an isolated worktree
- [ ] Never auto-merges

---

## Step 8: Deploy Progressively

```text
Week 1: L1 — Observe only, review every report
Week 2: L1 — If no issues, continue
Week 3: L2 — Draft only, review every output
Week 4: L2 — If output quality is good
Week 5: L2 — One more week of confidence
Week 6: L3 — Autonomous with alerts
```

Never rush from L1 to L3. A week at each tier is the minimum.

---

## Common Anti-Patterns

### "I'll just start at L3 and see what happens"

**Don't.** L3 loops can create PRs, modify branches, and consume budget. Start at L1.

### "My loop doesn't need exit conditions"

**Wrong.** Every loop needs exit conditions. What if it starts consuming 10x the expected budget? What if it hits an edge case and retries forever?

### "allowlist: [merge] for my release loop"

**Never.** No loop should auto-merge. Even release automation should create a PR that a human approves.

### "I'll schedule it every 5 minutes"

**Don't.** Loops cost tokens. Start with the longest acceptable interval and decrease only if needed.

### "The verifier is slowing things down — I'll remove it"

**Don't.** The verifier is your safety net for L2+. Without it, you have no independent check on the loop's output.

---

## Your Turn: Design a Loop

Pick one of these ideas or create your own:

| Idea | Tier | Description |
|------|------|-------------|
| Changelog drafter | L2 | After each release tag, collect commits and draft CHANGELOG entry |
| Stale PR pinger | L1 | Find PRs with no activity in 3+ days, write a report |
| Dependency updater | L3 | Check for outdated deps, open PRs with updates |
| Issue auto-labeler | L2 | Scan new unlabeled issues, propose labels (draft only) |
| Release notes generator | L2 | After CI publishes, collect merged PRs and draft release notes |
| Knowledge base auditor | L1 | Scan knowledge/ for stale entries, write a cleanup report |

### Your Loop Template

```yaml
name: your-loop-name
description: "One sentence description"
tier: L1  # Start at L1
cadence: 1d

goal: |
  What this loop accomplishes

allowlist: []  # L1: empty
deny:
  - merge
  - close
  - label
  - comment
  - push

exit_conditions:
  - goal_met
  - budget_exhausted
  - human_escalation

budget:
  max_tokens: 10000
  max_runs_per_day: 1
  max_wall_seconds: 300

request: |
  You are running the [name] loop.
  1. [Step 1]
  2. [Step 2]
  Output: report.md
```

Create it:

```bash
# Write your LOOP.md
mkdir -p loops/my-custom-loop
# Copy and fill in the template above into loops/my-custom-loop/LOOP.md

# Run it
./bin/loop run my-custom-loop --dry-run
./bin/loop run my-custom-loop

# Check results
cat loops/my-custom-loop/report.md
```

---

## Workshop Complete

You've built:

| Loop | Tier | Capability |
|------|------|-----------|
| Daily Issue Triage | L1 | Read-only reports |
| PR Babysitter | L2 | Draft comments with human gate |
| CI Sweeper | L3 | Autonomous fix PRs with maker/checker |
| Your custom loop | L1-3 | Your design |

### What's next

- [Schedule your loops](https://github.com/ulises-jeremias/agentic-harness/blob/main/docs/LOOP_CLI.md) for autonomous execution
- [Track costs](../PERFORMANCE.md) and adjust budgets
- [Review the loop engineering discipline](../LOOPS.md) for advanced patterns
- [Share your loop](https://github.com/ulises-jeremias/agentic-harness/issues) — contribute a template
