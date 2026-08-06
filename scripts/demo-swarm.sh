#!/usr/bin/env bash
set -euo pipefail
# Demo: offline swarm without LLM cost — for CI and recording prep.
# 1. verify toolkit, 2. verify Herdr/tmux, 3. init fixture repo, 4. start pair swarm with skeleton runner, 5. show worktree/handoff/report, 6. cleanup.

log() { echo "[demo] $*"; }

TOOLKIT_BIN="agent-toolkit"
if ! command -v agent-toolkit >/dev/null 2>&1; then
  if command -v uv >/dev/null 2>&1 && uv run --project /home/ulisesjcf/.ai-workspace/repos/github.com/ulises-jeremias/agent-toolkit agent-toolkit --version >/dev/null 2>&1; then
    TOOLKIT_BIN="uv run --project /home/ulisesjcf/.ai-workspace/repos/github.com/ulises-jeremias/agent-toolkit agent-toolkit"
    log "using toolkit via uv run (dev)"
  else
    echo "agent-toolkit not found — install via: uv tool install agent-toolkit-cli" >&2
    exit 1
  fi
else
  TOOLKIT_BIN="agent-toolkit"
fi
log "toolkit: $($TOOLKIT_BIN --version 2>&1 || echo ok)"
log "doctor:"
$TOOLKIT_BIN swarm doctor 2>&1 | head -n 20

# Check Herdr/tmux
if command -v herdr >/dev/null 2>&1; then
  log "herdr: $(herdr --version 2>&1 | head -n1)"
else
  log "herdr not found — demo will use tmux"
fi
if command -v tmux >/dev/null 2>&1; then
  log "tmux: $(tmux -V 2>&1)"
else
  echo "tmux not found — install tmux" >&2
  exit 1
fi

# Fixture repo
TMP=$(mktemp -d)
log "fixture: $TMP"
cd "$TMP"
git init -q
git config user.email "demo@example.com"
git config user.name "Demo"
echo "# demo" > README.md
git add .
git commit -qm "init"

# Plan (side-effect free)
log "plan:"
$TOOLKIT_BIN swarm plan --recipe pair --ui auto --runner skeleton --model-profile balanced "Demo: fix typo in README" 2>&1 | head -n 20

# Start (offline, skeleton)
log "start:"
$TOOLKIT_BIN swarm start --recipe pair --ui auto --runner skeleton "Demo: fix typo in README" 2>&1 | tee /tmp/demo-start.log
RUN_ID=$(grep -oE '[0-9]{8}T[0-9]{6}Z-[a-f0-9]{6}' /tmp/demo-start.log | head -n1)
if [[ -z ${RUN_ID:-} ]]; then
  RUN_ID=$(ls .agent-toolkit/swarm/runs | head -n1 || true)
fi
log "run_id: $RUN_ID"

# Show worktree & handoff
log "worktrees:"
ls -R .agent-toolkit/swarm/runs/"$RUN_ID"/worktrees 2>&1 | head -n 20
log "handoff demo:"
$TOOLKIT_BIN swarm handoff create --type artifact --from implementer --to reviewer --artifact artifacts/task-contract.md --run-id "$RUN_ID" 2>&1 | head -n 5
$TOOLKIT_BIN swarm handoffs "$RUN_ID" 2>&1 | head -n 20
$TOOLKIT_BIN swarm task next --role reviewer --run-id "$RUN_ID" 2>&1 | head -n 20

# Status/report
log "status:"
$TOOLKIT_BIN swarm status "$RUN_ID" 2>&1 | head -n 30
log "report:"
$TOOLKIT_BIN swarm report "$RUN_ID" 2>&1 | head -n 30

# Cleanup dry-run then real (should be clean since skeleton didn't dirty)
log "cleanup dry-run:"
$TOOLKIT_BIN swarm cleanup "$RUN_ID" --dry-run 2>&1 | head -n 20
log "cleanup:"
$TOOLKIT_BIN swarm cleanup "$RUN_ID" 2>&1 | head -n 20

log "demo complete — fixture preserved at $TMP (remove manually if desired)"
log "artifacts sanitized, no credentials, no LLM cost"
