# Swarms in agentic-harness — Reference Workspace

This harness is the **L3 demonstration** for Agent Toolkit Swarms. It shows how to use `agent-toolkit swarm`, not how to implement it.

**Ownership:** agent-toolkit owns engine; workstation installs tmux/Herdr; harness shows examples.

## Architecture

```text
agentic-harness/
  .agent-toolkit/swarm.yaml   # sample local config (copy & edit)
  swarms/{pair,team,full}.yaml # example recipe overrides (optional)
  examples/swarms/
    fix-a-bug/               # pair — bug fix, sanitized artifacts
    implement-a-feature/     # team — feature with plan gate
    review-and-refactor/     # full — high-risk with conditional hardener
  docs/SWARMS.md             # this file
  scripts/demo-swarm.sh      # offline fake-runner demo (no LLM cost)
```

## Install dependencies via Workstation

```bash
# agentic-workstation provisions tmux + Herdr + opencode integration
chezmoi update
dots-doctor
herdr --version; tmux -V
herdr integration list --json  # check opencode
```

Or manually: <https://herdr.dev/docs/install/> + `brew install tmux`.

## Run via Herdr (recommended)

```bash
agent-toolkit swarm doctor
agent-toolkit swarm start --recipe pair --ui herdr --runner opencode --model-profile balanced "Fix auth cache TTL"
agent-toolkit swarm status <run-id>
agent-toolkit swarm handoffs <run-id>
agent-toolkit swarm report <run-id>
```

Herdr UI: `herdr plugin link ./integrations/herdr/agent-toolkit-swarm` (from agent-toolkit repo).

## Run via tmux (portable, SSH-friendly)

```bash
agent-toolkit swarm start --recipe pair --ui tmux --runner opencode "Fix auth cache TTL"
agent-toolkit swarm attach <run-id>
# Or manually: tmux -L agent-toolkit-swarm-<run-id> attach -t swarm-<run-id>
```

Semantics, worktrees, handoffs, budgets identical regardless of UI.

## Model & Budget

- Profiles: `economy`/`balanced`/`quality`/`private` (see `agent-toolkit docs/SWARM_MODELS_AND_COSTS.md`)
- Task classes: planning/coding/review/architecture/hardening/qa mapped to `provider/model`
- Budgets: `max_total_tokens`, `max_cost_usd`, `max_wall_seconds`, concurrency 2 default, round-trips 2
- Unknown pricing reported honestly; expensive fallback needs approval

## Observe & Approve

```bash
agent-toolkit swarm list
agent-toolkit swarm status <run-id> --json
agent-toolkit swarm watch <run-id>
agent-toolkit swarm approvals <run-id>
agent-toolkit swarm approve <run-id> plan   # for team/full
agent-toolkit swarm approve <run-id> final  # before base merge (no auto-merge)
```

## Inspect Artifacts

```bash
agent-toolkit swarm artifacts <run-id>
agent-toolkit swarm handoffs <run-id> --json
agent-toolkit swarm logs <run-id> implementer
cat .agent-toolkit/swarm/runs/<run-id>/trace.jsonl
cat .agent-toolkit/swarm/runs/<run-id>/artifacts/final-report.md
```

All under `.agent-toolkit/swarm/runs/<run-id>/` — no upload, no telemetry.

## Cleanup

```bash
agent-toolkit swarm cleanup <run-id> --dry-run
agent-toolkit swarm cleanup <run-id>          # refuses dirty worktrees, never deletes branches
agent-toolkit swarm cleanup <run-id> --force   # only if you intend to discard
```

Branches `agent-toolkit-swarm/<run-id>/<role>` are preserved; never auto-merged to base.

## Demo (no LLM cost)

```bash
./scripts/demo-swarm.sh
# Verifies toolkit, Herdr/tmux, creates fixture repo in /tmp,
# runs pair swarm with --runner skeleton (fake), shows worktree/handoff/report, cleans up.
```

Usable in CI and for YouTube prep without spending tokens. See `scripts/demo-swarm.sh`.

## Examples

- **fix-a-bug** — pair, implementer + reviewer, final candidate ready.
- **implement-a-feature** — team, plan gate, reviewer feedback, architect integration.
- **review-and-refactor** — full, conditional security hardener, QA, promotion `team→full`.

Sanitized cost reports: skeleton runs show `0 tokens, $0.00`.

## Extension

To create recipe overrides: copy `swarms/pair.yaml` → edit → point `swarm.yaml` to it or pass `--recipe` with full path. See `agent-toolkit docs/HOW_TO_CREATE_SWARM_RECIPE.md`.

## Screenshots / Recording

Use `scripts/demo-swarm.sh` as base; record with `asciinema` or Herdr's session replay. Never commit real credentials or private code.
