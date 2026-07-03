# Part 2: L2 — PR Babysitter

> Build a PR-gated loop that reviews open PRs and posts draft comments.

**Time**: 30 minutes | **Tier**: L2 (PR-gated) | **Risk**: Low — draft comments only

---

## What You'll Learn

- Maker/checker pattern
- Human approval gate
- L2 permissions: allowlist with restrictions
- verifier configuration
- Cost scaling with activity

---

## Step 1: Create the Loop

```bash
./bin/loop init pr-babysitter --template pr-babysitter --tier 2
```text

---

## Step 2: Understand L2 Permissions

Open `loops/pr-babysitter/LOOP.md`:

```yaml
allowlist:
  - comment        # Can post comments
deny:
  - merge          # Cannot merge
  - approve        # Cannot approve
  - close          # Cannot close
  - push           # Cannot push
  - label          # Cannot label
```text

**Key difference from L1**: The allowlist now has `comment`. This loop CAN write — but only comments. It CANNOT merge, approve, close, push, or label.

### The Human Gate

L2 loops never auto-merge. They produce output that a human must approve:

```text
Loop writes draft comment
         ↓
Human reviews comment
         ↓
Human publishes or discards
```text

The loop acts as a **reviewer assistant**, not a reviewer replacement.

---

## Step 3: Configure the Verifier

```yaml
verifier: agentic-workstation-code-reviewer
```text

The `verifier` is a separate agent that double-checks the loop's output before it's published. In L2, the verifier runs but the human still has final say.

---

## Step 4: Dry-Run

```bash
./bin/loop run pr-babysitter --dry-run --verbose
```text

```text
[DRY-RUN] Would run: pr-babysitter (Tier 2)
  Purpose: Review open PRs, post draft comments
  Permissions: comment only (no merge/approve/close)
  Verifier: agentic-workstation-code-reviewer
  Budget: 80,000 tokens max
  Would review: 3 open PRs detected
  Would post: draft comments (not published until human approves)
```text

---

## Step 5: First Run

```bash
./bin/loop run pr-babysitter
```text

Check the output:

```bash
cat loops/pr-babysitter/plan.md
```text

```markdown
# PR Babysitter Run — 2026-07-03 14:00

## PRs Reviewed

### #145 — feat: add --name flag to hello.py
- **Status**: No reviews in last 60 minutes
- **Summary**: Adds argparse with --name flag. Clean implementation.
- **Suggestions**:
  1. Add input validation for empty name string
  2. Consider adding --greeting flag for custom greetings
- **Comment**: Draft posted — awaiting human review

### #144 — fix: handle null response in API client
- **Status**: Reviewed 2 hours ago — skipping

## Verifier Notes
- PR #145: `agentic-workstation-code-reviewer` confirmed no security issues
- No escalations needed
```text

---

## Step 6: Schedule (Higher Frequency)

L2 loops run more often because review timeliness matters:

```bash
./bin/loop schedule pr-babysitter --cron "0 */4 * * *"
```text

```text
Next run: 2026-07-03 16:00 UTC
Runs every 4 hours — matches typical PR review cycle
```text

---

## L2 Cost Considerations

```bash
./bin/loop cost pr-babysitter --monthly
```text

```text
LOOP: pr-babysitter
Per run:  ~15,000 tokens  ~$0.15
Per day:  ~90,000 tokens  ~$0.90  (6 runs/day)
Per month: ~2,700,000 tokens ~$27.00 (180 runs/month)
```text

**Optimization**: If costs are high:

1. Reduce frequency: `--cron "0 */8 * * *"` (3 runs/day = $13.50/month)
2. Increase the "no review in last X minutes" threshold
3. Use a cheaper model for L2 (Haiku can review simple PRs)

---

## What You Built

| Component | L1 (Triage) | L2 (Babysitter) |
|-----------|------------|-----------------|
| Writes | No | Draft comments |
| Human gate | N/A | Reviews before publish |
| Frequency | 1/day | 6/day |
| Verifier | None | code-reviewer agent |
| Cost/month | ~$0.90 | ~$27.00 |

### Key L2 Lessons

1. **Allowlist is explicit**: Only `comment` is allowed — everything else denied
2. **The human gate is the safety net**: Loop suggests, human decides
3. **Verifier adds a second opinion**: Independent agent double-checks
4. **Cost scales with frequency**: More runs = more tokens = more money
5. **Budget prevents runaway**: max_tokens and max_runs_per_day are hard limits

---

## Verify It Worked

```bash
./bin/loop status --tier 2
./bin/loop audit pr-babysitter --last 1
./bin/loop cost pr-babysitter --monthly
```text

---

## Try This

1. **Change the review threshold**: Edit LOOP.md and change "60 minutes" to "120 minutes"
2. **Add a new deny rule**: Add `- request-changes` to the deny list
3. **Run it on a real PR**: Find an open PR in one of your projects

---

## Next Step

In [Part 3](03-l3-ci-sweeper.md), you'll build an autonomous L3 loop with write capability — detecting CI failures and opening fix PRs with the maker/checker pattern.
