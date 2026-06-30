# Example: Two-Repo PR Babysitter

> A PR review loop that watches two repos and posts comments every 15 minutes (L2).

## What it does

Every 15 minutes, this loop:

1. Lists open PRs in both `api` and `frontend` repos that have no review in the last hour
2. Posts review comments (never approves or merges)
3. Writes `plan.md` with which PRs were reviewed

## Setup

```bash
cd ~/.ai-workspace

# 1. Index both repos
./bin/project-indexer clone owner/my-api
./bin/project-indexer clone owner/my-frontend

# 2. Load the multi-repo pack
cp examples/pr-babysitter/pack.yaml packs/my-project.yaml
./bin/workspace-context load packs/my-project.yaml

# 3. Initialize the loop
./bin/loop init pr-babysitter

# 4. Run once (L2 — posts comments but no merges)
./bin/loop run pr-babysitter
```

## Sample pack

See `pack.yaml` — loads context for both repos.

## Cost note

PR babysitter is high cost (reads PR diffs). Start with `max_runs_per_day: 4` (every 6h).
Only upgrade to `max_runs_per_day: 96` (every 15m) when you are sure the loop produces
useful reviews.
