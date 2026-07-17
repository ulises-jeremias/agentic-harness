# Loop CLI Reference — agentic-harness

> Complete reference for the `bin/loop` CLI — all subcommands, flags, exit codes, and examples.

---

<!-- markdownlint-disable MD024 -->

## Overview

```text
bin/loop <subcommand> [options]

Subcommands:
  init      Create a new loop from a template
  run       Execute one loop iteration
  status    List all loops with metadata
  audit     Show run history and state evolution
  cost      Estimate token cost per run or monthly
  schedule  Install or remove systemd/launchd timer
```

---

## `bin/loop init`

Create a new loop from a template in `templates/loops/`.

```bash
bin/loop init <name> [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--template` | string | (required) | Template name from `templates/loops/<name>/` |
| `--tier` | 1,2,3 | 1 | Safety tier |
| `--schedule` | cron | (none) | Optional cron expression for scheduling |
| `--description` | string | (template default) | Human-readable loop description |
| `--force` | flag | false | Overwrite existing loop directory |

### Examples

```bash
# Create a Tier 1 daily triage loop
bin/loop init daily-triage --template daily-triage --tier 1 --description "Morning issue scan"

# Create a Tier 2 PR reviewer that runs every 4 hours
bin/loop init pr-babysitter --template pr-babysitter --tier 2 --schedule "0 */4 * * *"

# Create a Tier 3 CI fixer with a description
bin/loop init ci-sweeper --template ci-sweeper --tier 3 --description "Auto-fix common CI failures"

# Force overwrite an existing loop
bin/loop init daily-triage --template daily-triage --force
```

### What it creates

```text
loops/<name>/
├── LOOP.md        # Loop contract: purpose, tier, exit conditions, template ref
├── STATE.md       # Execution state: last run, exit code, decisions, cost accumulator
└── .schedule      # (optional) cron expression if --schedule was provided
```

---

## `bin/loop run`

Execute one iteration of a loop.

```bash
bin/loop run <name> [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--dry-run` | flag | false | Preview what would happen without executing |
| `--force` | flag | false | Bypass `max_runs_per_day` budget gate (and run even if exit conditions are met) |
| `--verbose` | flag | false | Print detailed execution logs |

### Examples

```bash
# Run a loop iteration
bin/loop run daily-triage

# Dry-run to see what would happen
bin/loop run daily-triage --dry-run

# Force run even if today's budget is exhausted
bin/loop run pr-babysitter --force

# Verbose output for debugging
bin/loop run ci-sweeper --verbose
```

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Loop completed successfully |
| 1 | Loop completed with exit condition met (stopping future runs) |
| 2 | Loop failed — check STATE.md for error details |
| 3 | Loop skipped — exit condition prevented execution |
| 4 | Invalid loop — LOOP.md missing or malformed |
| 5 | Tier violation — attempted Tier 3 operation on Tier 1 loop |
| 78 | Hard gate denial — `gh` mutation blocked by `bin/loop-gh-gate` (allowlist/deny/receipt) |

---

## `bin/loop status`

List all loops and their current state.

```bash
bin/loop status [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--json` | flag | false | Output as JSON |
| `--tier` | 1,2,3 | (all) | Filter by tier |
| `--active` | flag | false | Show only loops with recent runs (< 24h) |

### Examples

```bash
# List all loops
bin/loop status

# Filter by tier
bin/loop status --tier 2

# Show only active loops
bin/loop status --active

# JSON output for scripting
bin/loop status --json
```

### Output format

```text
NAME              TIER  LAST RUN            STATUS     SCHEDULE
daily-triage      1     2026-07-03 09:00   success    every 24h
pr-babysitter     2     2026-07-03 12:00   success    every 4h
ci-sweeper        3     2026-07-03 11:30   failed     every 1h
changelog-drafter 2     (never)             pending    every 168h
```

---

## `bin/loop audit`

Show detailed run history and state evolution.

```bash
bin/loop audit <name> [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--last` | int | 10 | Show last N runs |
| `--since` | date | (all) | Show runs since date (ISO 8601) |
| `--summary` | flag | false | Aggregate stats only |
| `--json` | flag | false | Output as JSON |

### Examples

```bash
# Audit last 10 runs
bin/loop audit daily-triage

# Audit last 50 runs
bin/loop audit daily-triage --last 50

# Since a specific date
bin/loop audit pr-babysitter --since 2026-06-01

# Summary only
bin/loop audit ci-sweeper --summary
```

### Output format

```text
LOOP: daily-triage (Tier 1)
Total runs: 45 | Success: 42 | Failed: 2 | Skipped: 1
Avg tokens/run: 4,821 | Total cost: $2.35

Last 5 runs:
  #45  2026-07-03 09:00  success  4,912 tokens  $0.03
  #44  2026-07-02 09:00  success  4,756 tokens  $0.03
  #43  2026-07-01 09:00  skipped  (exit: cost_exceeds)
  #42  2026-06-30 09:00  success  4,801 tokens  $0.03
  #41  2026-06-29 09:00  failed   (error: JIRA auth timeout)
```

---

## `bin/loop cost`

Estimate token costs for a loop.

```bash
bin/loop cost <name> [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--last` | int | 10 | Use last N runs for estimation |
| `--monthly` | flag | false | Project monthly cost |
| `--alert` | float | (none) | Check against cost threshold, exit 1 if exceeded |
| `--json` | flag | false | Output as JSON |

### Examples

```bash
# Estimate per-run cost
bin/loop cost daily-triage

# Project monthly cost
bin/loop cost pr-babysitter --monthly

# Cost alert — exit code 1 if monthly exceeds $10
bin/loop cost ci-sweeper --monthly --alert 10.00

# Based on last 30 runs
bin/loop cost daily-triage --last 30
```

### Output format

```text
LOOP: daily-triage
Based on: 45 runs (last: 2026-07-03)

Per run:  ~4,821 tokens  ~$0.03
Per day:  ~4,821 tokens  ~$0.03  (1 run/day)
Per month: ~144,630 tokens ~$0.90  (30 runs/month)
Per year:  ~1,759,665 tokens ~$10.95 (365 runs/year)

Model: claude-sonnet-4-20250514 (input: $3/M, output: $15/M)
```

---

## `bin/loop schedule`

Install or manage OS-level timer for a loop.

```bash
bin/loop schedule <name> [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--cron` | string | (from LOOP.md) | Override cron expression |
| `--list` | flag | false | List all scheduled loops |
| `--remove` | flag | false | Remove schedule for this loop |
| `--status` | flag | false | Check schedule health |
| `--dry-run` | flag | false | Print timer files without installing |

### Platform support

| Platform | Scheduler | Location |
|----------|-----------|----------|
| Linux (systemd) | systemd user timer | `~/.config/systemd/user/agentic-harness-<name>.*` |
| macOS | launchd agent | `~/Library/LaunchAgents/com.agentic-harness.<name>.plist` |
| Windows (WSL2) | systemd user timer | Same as Linux |
| Other | Manual instructions | Prints commands to run |

### Examples

```bash
# Schedule a loop with its default cron
bin/loop schedule daily-triage

# Schedule with custom cron
bin/loop schedule pr-babysitter --cron "0 */6 * * *"

# List all scheduled loops
bin/loop schedule --list

# Check schedule health
bin/loop schedule --status

# Remove a schedule
bin/loop schedule daily-triage --remove

# Dry-run — print timer files without installing
bin/loop schedule ci-sweeper --dry-run
```

### Output (schedule)

```text
Created: ~/.config/systemd/user/agentic-harness-daily-triage.service
Created: ~/.config/systemd/user/agentic-harness-daily-triage.timer
Enabled: systemctl --user enable agentic-harness-daily-triage.timer
Started: systemctl --user start agentic-harness-daily-triage.timer
Next run: 2026-07-04 09:00:00 UTC
```

### Output (list)

```text
NAME              SCHEDULE    NEXT RUN            ENABLED
daily-triage      every 24h   2026-07-04 09:00    yes
pr-babysitter     every 4h    2026-07-03 13:00    yes
ci-sweeper        every 1h    2026-07-03 10:30    no (paused)
```

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `HARNESS_DIR` | Harness root directory | `$HOME/.ai-workspace` |
| `LOOPS_DIR` | Loops directory | `$HARNESS_DIR/loops` |
| `TEMPLATES_DIR` | Loop templates directory | `$HARNESS_DIR/templates/loops` |
| `DOTS_AI_DEVCOMPANION_LLM_ALLOWLIST` | Allowed LLM providers | (none) |

---

## Loop File Format

### LOOP.md

```yaml
---
name: daily-triage
tier: 1
template: daily-triage
description: "Morning scan of open issues across all project repos"
schedule: "0 9 * * *"
exit:
  - condition: "cost_exceeds 5.00"
    action: "pause"
  - condition: "consecutive_failures > 3"
    action: "stop"
  - condition: "error_rate > 0.1"
    action: "stop_and_alert"
max_tokens: 10000
---
```

### STATE.md

```yaml
---
loop: daily-triage
last_run: "2026-07-03T09:00:00Z"
last_exit_code: 0
total_runs: 45
successful_runs: 42
failed_runs: 2
skipped_runs: 1
total_tokens: 216945
total_cost: 2.35
exit_conditions:
  cost_exceeds_5: false
  consecutive_failures: 0
  error_rate: 0.044
last_output: "3 issues found: 1 new, 2 blocked. Report saved."
---
```

---

## Scheduling Format

### systemd timer expression

The `--schedule` flag accepts systemd `OnCalendar=` format:

| Expression | Meaning |
|-----------|---------|
| `daily` | Every day at midnight |
| `*-*-* 09:00:00` | Every day at 9 AM |
| `hourly` | Every hour |
| `Mon..Fri *-*-* 09:00:00` | Weekdays at 9 AM |
| `*-*-1 09:00:00` | First of every month at 9 AM |

### launchd interval

On macOS, only interval-based scheduling is supported:

| Expression | Converted to |
|-----------|-------------|
| `daily` | StartInterval: 86400 |
| `hourly` | StartInterval: 3600 |

---

## Common Workflows

### Create and run your first loop

```bash
# 1. Create from template
bin/loop init daily-triage --template daily-triage --tier 1

# 2. Dry-run to preview
bin/loop run daily-triage --dry-run

# 3. First real run
bin/loop run daily-triage

# 4. Check results
bin/loop audit daily-triage --last 1

# 5. Schedule for automation
bin/loop schedule daily-triage

# 6. Verify it's scheduled
bin/loop schedule --list
```

### Debug a failing loop

```bash
# 1. Check status
bin/loop status --active

# 2. Audit recent runs
bin/loop audit ci-sweeper --last 5

# 3. Run with verbose output
bin/loop run ci-sweeper --verbose --force

# 4. Check exit conditions in STATE.md
cat loops/ci-sweeper/STATE.md

# 5. Check cost impact
bin/loop cost ci-sweeper --monthly
```

### Promote a loop to a higher tier

```bash
# 1. Review current tier performance
bin/loop audit pr-babysitter --summary

# 2. Edit LOOP.md: change tier: 2 -> tier: 3
#    (manual edit required — no CLI command for tier promotion)

# 3. Run with verbose to verify
bin/loop run pr-babysitter --verbose --dry-run

# 4. Schedule with new tier
bin/loop schedule pr-babysitter --cron "0 */2 * * *"
```

<!-- markdownlint-enable MD024 -->
