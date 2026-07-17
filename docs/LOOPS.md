# Loop Engineering Primer

> Loops are recurring AI-driven processes with durable state, safety gates, and
> cost budgets. Inspired by Boris Cherny (Anthropic), Peter Steinberger, Addy
> Osmani, and Cobus Greyling's *Loop Engineering* (2026).
>
> **The shift**: you stop prompting agents and start designing loops that prompt them.

---

## Quick Start

```bash
# Scaffold a new loop from a starter template
./bin/loop init daily-triage

# Run a loop once (manual trigger)
./bin/loop run daily-triage

# Show loop status
./bin/loop status

# See what a run would cost
./bin/loop cost daily-triage

# Audit past runs
./bin/loop audit daily-triage
```

---

## Runner Hierarchy

`bin/loop run` tries AI runners in this order. The first one found is used:

| Priority | Runner | When available |
|----------|--------|----------------|
| 1 | **agentic-workstation runner** | `HARNESS_RUNNER_DIR` points to runner dir; provides multi-provider LLM selection (Anthropic, OpenAI, Ollama, OpenCode) with policy enforcement |
| 2 | **`claude --print`** (Claude Code CLI) | `claude` is in `PATH`; works out of the box for Claude Code users, no extra setup |
| 3 | **Skeleton plan** | Always available; writes a `plan.md` stub with no AI execution |

**Claude Code users** (most common case): loops work natively as long as `claude` is in your PATH.

**For multi-provider support**: install [agentic-workstation](https://github.com/ulises-jeremias/agentic-workstation) and set:

```bash
export HARNESS_RUNNER_DIR="$HOME/.local/share/agentic-workstation/dev-companion/runner"
```

---

## Loop Directory Contract

Every loop lives in `loops/<loop-name>/`:

```text
loops/daily-triage/
├── LOOP.md        ← declared intent (mostly immutable)
├── STATE.md       ← mutated state (one per run)
└── runs/          ← run artifacts and traces
    └── <run-id>/
        ├── trace.jsonl    ← structured execution log
        ├── plan.md        ← what the agent planned to do
        ├── report.md      ← L1: observation output
        └── diff.patch     ← L2/L3: code changes
```

### LOOP.md (declared intent)

```yaml
---
name: daily-triage
tier: L1
cadence: 1d
goal: Triage new issues and apply labels
allowlist:
  - label
  - comment
deny:
  - merge
  - close
  - force-push
  - delete
exit_conditions:
  - goal_met
  - budget_exhausted
  - human_escalation
budget:
  max_tokens: 50000
  max_runs_per_day: 1
  max_wall_seconds: 600
verifier: agentic-workstation-code-reviewer
---

# Daily Issue Triage Loop

(narrative goal, escalation rules, examples of good vs. bad output)
```

**LOOP.md fields**:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✓ | Kebab-case, matches directory name |
| `tier` | ✓ | `L1` · `L2` · `L3` (see Rollout Tiers) |
| `cadence` | ✓ | `15m` · `1h` · `6h` · `1d` · `1w` |
| `goal` | ✓ | One-sentence objective |
| `allowlist` | ✓ | Actions the loop may take without a human gate |
| `deny` | | Actions explicitly forbidden (belt-and-suspenders) |
| `exit_conditions` | ✓ | When to stop the current run |
| `budget` | ✓ | `max_tokens`, `max_runs_per_day`, `max_wall_seconds` |
| `verifier` | | Skill or agent that signs off on write actions |

### STATE.md (mutated state)

```yaml
---
last_run: 2026-06-30T01:30:00Z
last_run_status: success
last_run_id: 20260630T013000Z-abc123
runs_today: 1
pending: []
escalations: []
---
```

STATE.md is written by `bin/loop run` after each run. Do not edit manually.
It is gitignored by default and machine-local.

---

## Rollout Tiers

| Tier | Autonomy | What it does |
|------|----------|--------------|
| **L1** | Report-only | Reads, analyzes, writes `report.md`. Never mutates external state. |
| **L2** | Assisted | Proposes changes as a draft PR. A human must approve before merge. |
| **L3** | Unattended | May commit/merge for actions in `allowlist`. Everything else escalates. |

> **Principle**: start every new loop at L1. Graduate to L2/L3 only after
> reviewing 3+ consecutive clean L1 runs.

---

## Exit Conditions

```yaml
exit_conditions:
  - goal_met          # agent signals objective is satisfied
  - budget_exhausted  # token/time budget hit
  - human_escalation  # agent cannot decide; pauses for review
  - safe_to_commit    # (L3) all actions are allowlisted
  - requires_pr       # (L2) changes need PR review
  - max_iterations    # fallback: hard limit on sub-agent calls
```

Combine with `any` (default) or `all`:

```yaml
exit_conditions:
  logic: any    # stop on first condition (default)
  conditions:
    - goal_met
    - budget_exhausted
```

---

## Maker / Checker Pattern

Every loop run dispatches two sub-agents:

1. **Implementer** (maker) — executes the goal, produces artifacts
2. **Verifier** (checker) — audits artifacts before any write action

```yaml
verifier: agentic-workstation-code-reviewer   # default for code-touching loops
# verifier: agentic-workstation-architect     # for design/ADR loops
```

The verifier must sign off before any action not in `allowlist`. If the
verifier fails, the run is marked `verifier_failed` and escalated.

> **Hard gate (2026-07-17):** During `loop run`, `bin/loop` installs a PATH-first
> `gh` shim (`bin/loop-gh-gate`) that intercepts mutating commands. Actions must
> be on `allowlist`, not on `deny`, and compatible with the loop tier. **merge**
> and **close** additionally require a JSON verifier receipt under
> `runs/<id>/verifier-receipts/` (see prompt contract). Denied calls exit with
> code `78` and append to `gate-denials.jsonl`. Read-only `gh` commands pass
> through. A separate verifier *agent process* is still optional — the receipt
> is the enforceable check-off.

---

## Reference Patterns

Adapted from [cobusgreyling/loop-engineering](https://github.com/cobusgreyling/loop-engineering):

| Pattern | Tier | Cadence | Cost | Use case |
|---------|------|---------|------|----------|
| `daily-triage` | L1 | 1d | Low | Label new issues |
| `pr-babysitter` | L2 | 15m | High | Comment on open PRs |
| `ci-sweeper` | L2 | 15m | Very High | Fix failing tests |
| `dep-sweeper` | L2 | 1d | Medium | Patch dep updates |
| `changelog-drafter` | L1 | 1d | Low | Draft release notes |
| `post-merge-cleanup` | L2 | 6h | Low | Off-peak housekeeping |
| `issue-triage` | L1 | 4h | Low | Propose-only labeling |

Get a starter: `./bin/loop init <pattern>`

---

## Scheduling

**systemd timer (Linux)**:

```ini
# ~/.config/systemd/user/agentic-harness-daily-triage.timer
[Timer]
OnCalendar=daily
[Install]
WantedBy=timers.target
```

**launchd (macOS)**:

```xml
<!-- ~/Library/LaunchAgents/agentic-harness.daily-triage.plist -->
<key>StartCalendarInterval</key>
<dict><key>Hour</key><integer>8</integer></dict>
```

**Claude Code trigger (in-session)**:

```text
mcp__claude_ai_Claude_Code_Remote__create_trigger
  cron_expression: "0 8 * * *"
  prompt: "Run bin/loop run daily-triage in the agentic-harness"
```

---

## Anti-Patterns

- **Loop creep**: starting at L3 without L1 observation. Always observe first.
- **No budget**: loops without `max_tokens` run until the context limit.
- **Weak allowlist**: allowing `merge` without testing runs in staging.
- **No verifier**: skipping the checker on code-touching L3 loops.
- **Long cadence + high cost**: `1d` cadence at `very-high` cost tier = expensive surprise.

---

## More reading

- [docs/METHODOLOGY.md](METHODOLOGY.md) — Ralph Loop philosophy
- [templates/loops/](../templates/loops/) — starter templates
- [bin/loop](../bin/loop) — CLI reference (`bin/loop help`)
