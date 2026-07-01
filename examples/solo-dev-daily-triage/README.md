# Example: Solo Developer Daily Triage

> A daily issue triage loop for a solo developer — L1 (observe only, no writes).

## What it does

Every day at 8am, this loop:

1. Lists open GitHub issues created in the last 24 hours
2. Proposes labels and priority scores
3. Writes a `report.md` — no actual labels are applied

## Setup

```bash
# 1. Clone agentic-harness
git clone https://github.com/ulises-jeremias/agentic-harness ~/.agentic-harness
cd ~/.agentic-harness
./scripts/workspace-init.sh

# 2. Index your repo
./bin/project-indexer clone owner/my-project

# 3. Initialize the triage loop
./bin/loop init daily-triage

# 4. Run it once to verify
./bin/loop run daily-triage

# 5. Read the output
cat loops/daily-triage/runs/*/report.md
```

## Sample LOOP.md

See `loop.yaml` in this directory — copy to `loops/daily-triage/LOOP.md` to customize.

## Schedule (systemd, Linux)

```bash
# Install timer
mkdir -p ~/.config/systemd/user
cp schedule/agentic-harness-daily-triage.timer ~/.config/systemd/user/
cp schedule/agentic-harness-daily-triage.service ~/.config/systemd/user/
systemctl --user enable --now agentic-harness-daily-triage.timer

# Check logs
journalctl --user -u agentic-harness-daily-triage
```

## Upgrade path

Once you've reviewed 3+ clean L1 reports, upgrade to L2 to apply labels:

```yaml
# loops/daily-triage/LOOP.md
tier: L2
allowlist:
  - label
  - comment
```
