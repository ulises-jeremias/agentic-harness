#!/usr/bin/env bash
# scripts/rename-migrate.sh
# Migration helper for existing clones after the rename from
# ai-workspace → agentic-harness.
#
# Usage:
#   ./scripts/rename-migrate.sh
#
# This script is idempotent — safe to re-run.

set -euo pipefail

MIGRATE_FROM="ulises-jeremias/ai-workspace"
MIGRATE_TO="ulises-jeremias/agentic-harness"

SSH_PATTERN="git@github.com:${MIGRATE_FROM}"
HTTPS_PATTERN="https://github.com/${MIGRATE_FROM}"

SSH_NEW="git@github.com:${MIGRATE_TO}"
HTTPS_NEW="https://github.com/${MIGRATE_TO}"

# ── Detect remote ────────────────────────────────────────────────────────────
REMOTE_URL="$(git remote get-url origin 2>/dev/null || true)"

if [[ -z "${REMOTE_URL}" ]]; then
  printf "No 'origin' remote found — nothing to migrate.\n"
  exit 0
fi

printf "Current remote origin: %s\n" "${REMOTE_URL}"

# ── Check if migration is needed ─────────────────────────────────────────────
if [[ "${REMOTE_URL}" != "${SSH_PATTERN}" ]] && \
   [[ "${REMOTE_URL}" != "${SSH_PATTERN}.git" ]] && \
   [[ "${REMOTE_URL}" != "${HTTPS_PATTERN}" ]] && \
   [[ "${REMOTE_URL}" != "${HTTPS_PATTERN}.git" ]]; then
  printf "Remote does not match '%s' — no migration needed.\n" "${MIGRATE_FROM}"
  exit 0
fi

# ── Determine the new URL ────────────────────────────────────────────────────
if [[ "${REMOTE_URL}" == "${SSH_PATTERN}" ]] || \
   [[ "${REMOTE_URL}" == "${SSH_PATTERN}.git" ]]; then
  NEW_URL="${SSH_NEW}"
else
  NEW_URL="${HTTPS_NEW}"
fi

# Strip trailing .git for comparison
REMOTE_BASE="${REMOTE_URL%.git}"
NEW_BASE="${NEW_URL%.git}"

if [[ "${REMOTE_BASE}" == "${NEW_BASE}" ]]; then
  printf "Remote already points to '%s' — nothing to do.\n" "${MIGRATE_TO}"
  exit 0
fi

# ── Apply ────────────────────────────────────────────────────────────────────
printf "Updating remote origin:\n"
printf "  Old: %s\n" "${REMOTE_URL}"
printf "  New: %s\n" "${NEW_URL}"
git remote set-url origin "${NEW_URL}"
printf "Done. Remote updated successfully.\n"
printf "\n"
printf "Verify with: git remote -v\n"
