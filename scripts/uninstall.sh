#!/usr/bin/env bash
# scripts/uninstall.sh
# Gracefully remove AI Workspace artifacts from the system.
# This script removes the runtime state created by the workspace — it does
# NOT delete the workspace repository itself.
#
# Usage:
#   bash scripts/uninstall.sh [options]
#
# Options:
#   --dry-run          Show what would be removed without removing anything
#   --keep-knowledge   Skip removing knowledge/ contents
#   --keep-loops       Skip removing loops/ run artifacts
#   -h, --help         Show this help

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DC_HOME="${AI_WORKSPACE_DC_HOME:-${HOME}/.local/share/ai-workspace/dev-companion}"
WORKTREES_HOME="${AI_WORKSPACE_WORKTREES_DIR:-${HOME}/.local/share/ai-workspace/worktrees}"

DRY_RUN=false
KEEP_KNOWLEDGE=false
KEEP_LOOPS=false

for arg in "$@"; do
  case "${arg}" in
    --dry-run) DRY_RUN=true ;;
    --keep-knowledge) KEEP_KNOWLEDGE=true ;;
    --keep-loops) KEEP_LOOPS=true ;;
    -h | --help)
      sed -n '2,/^$/p' "$0" | grep '^#' | sed 's/^# \?//'
      exit 0
      ;;
    *)
      echo "Unknown flag: ${arg}. Run $0 --help" >&2
      exit 1
      ;;
  esac
done

_c() { [[ -t 1 ]] && printf '\033[%sm%s\033[0m' "$1" "$2" || printf '%s' "$2"; }
ok() { _c "1;32" "  ✓"; echo " $*"; }
dry() { _c "0;37" "  ~"; echo " [dry-run] $*"; }
warn() { _c "1;33" "  !"; echo " $*"; }

remove() {
  local path="$1"
  if [[ ! -e "${path}" && ! -L "${path}" ]]; then
    return
  fi
  if [[ "${DRY_RUN}" == "true" ]]; then
    dry "would remove: ${path}"
    return
  fi
  rm -rf "${path}"
  ok "removed: ${path}"
}

echo ""
echo "AI Workspace Uninstall"
echo "────────────────────────────────────────────"
echo ""
warn "This removes runtime artifacts. The repo itself is NOT deleted."
if [[ "${DRY_RUN}" == "true" ]]; then
  warn "DRY RUN — no changes will be made."
fi
echo ""

# ── Devcompanion queue ───────────────────────────────────────────────────────
echo "DevCompanion queue (${DC_HOME}):"
for subdir in queue/pending queue/processing queue/done queue/failed artifacts; do
  remove "${DC_HOME}/${subdir}"
done

# ── Worktrees ────────────────────────────────────────────────────────────────
echo ""
echo "Loop worktrees (${WORKTREES_HOME}):"
remove "${WORKTREES_HOME}"

# ── Active session state ─────────────────────────────────────────────────────
echo ""
echo "Session state:"
for state_file in .active-pack .active-persona .active-profile .persona-history; do
  remove "${WORKSPACE_ROOT}/${state_file}"
done

# ── Loop runs ────────────────────────────────────────────────────────────────
if [[ "${KEEP_LOOPS}" == "false" ]]; then
  loops_dir="${WORKSPACE_ROOT}/loops"
  if [[ -d "${loops_dir}" ]]; then
    echo ""
    echo "Loop run artifacts (${loops_dir}/*/runs/):"
    while IFS= read -r -d '' run_dir; do
      remove "${run_dir}"
    done < <(find "${loops_dir}" -mindepth 2 -maxdepth 2 -name "runs" -type d -print0 2>/dev/null)
    while IFS= read -r -d '' state_md; do
      remove "${state_md}"
    done < <(find "${loops_dir}" -mindepth 2 -maxdepth 2 -name "STATE.md" -print0 2>/dev/null)
  fi
fi

# ── Knowledge base ───────────────────────────────────────────────────────────
if [[ "${KEEP_KNOWLEDGE}" == "false" ]]; then
  echo ""
  echo "Knowledge base (${WORKSPACE_ROOT}/knowledge/):"
  warn "Skipped by default — use caution, this removes all learnings!"
  warn "To remove, re-run with: --force-remove-knowledge"
  # Knowledge removal requires explicit extra flag — not done here by default
fi

# ── Auto-generated files ─────────────────────────────────────────────────────
echo ""
echo "Auto-generated files:"
remove "${WORKSPACE_ROOT}/projects.yaml"

# ── Scheduler entries (hints only) ───────────────────────────────────────────
echo ""
echo "Scheduler cleanup (manual steps required):"
echo "  systemd:  systemctl --user disable --now ai-workspace-*.timer 2>/dev/null"
echo "  launchd:  launchctl unload ~/Library/LaunchAgents/ai-workspace.*.plist 2>/dev/null"
echo ""

if [[ "${DRY_RUN}" == "true" ]]; then
  echo "Dry run complete. Re-run without --dry-run to apply."
else
  ok "Workspace runtime artifacts removed. The repo itself remains at ${WORKSPACE_ROOT}."
fi
echo ""
