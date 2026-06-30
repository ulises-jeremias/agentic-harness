#!/usr/bin/env bash
# scripts/migrate-knowledge.sh
# Add YAML frontmatter to existing knowledge entries that don't have it.
# This is a best-effort migration — entries remain readable without frontmatter.
#
# Usage:
#   bash scripts/migrate-knowledge.sh [--dry-run] [--type learnings|processes|todos|skills]
#
# Options:
#   --dry-run    Show what would be changed without writing files
#   --type       Migrate only this knowledge type (default: all)

set -euo pipefail
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KNOWLEDGE="${WORKSPACE_ROOT}/knowledge"

DRY_RUN=false
TYPE_FILTER=""
for arg in "$@"; do
  case "${arg}" in
    --dry-run) DRY_RUN=true ;;
    --type=*) TYPE_FILTER="${arg#*=}" ;;
    --type) echo "Use --type=<type>" >&2; exit 1 ;;
    -h|--help) echo "Usage: $0 [--dry-run] [--type=learnings|processes|todos|skills]"; exit 0 ;;
  esac
done

TODAY=$(date '+%Y-%m-%d')
ADDED=0
SKIPPED=0

process_file() {
  local f="$1" type="$2"
  local content
  content=$(cat "$f")

  # Skip if already has frontmatter
  if echo "${content}" | head -1 | grep -q "^---$"; then
    SKIPPED=$((SKIPPED + 1))
    return
  fi

  # Build minimal frontmatter
  local fm="---
type: ${type}
created: ${TODAY}
---"

  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "  [dry-run] would add frontmatter to: ${f#"${WORKSPACE_ROOT}/"}"
  else
    printf '%s\n\n%s\n' "${fm}" "${content}" > "${f}"
    echo "  ✓ Migrated: ${f#"${WORKSPACE_ROOT}/"}"
    ADDED=$((ADDED + 1))
  fi
}

echo ""
echo "Knowledge Migration"
echo "-------------------"

for dir in "${KNOWLEDGE}"/*/; do
  [[ -d "${dir}" ]] || continue
  type_name=$(basename "${dir}")
  if [[ -n "${TYPE_FILTER}" && "${type_name}" != "${TYPE_FILTER}" ]]; then
    continue
  fi
  for f in "${dir}"*.md; do
    [[ -f "${f}" ]] || continue
    # Skip README files
    [[ "$(basename "${f}")" == "README.md" ]] && continue
    process_file "${f}" "${type_name%s}"  # strip trailing 's': learnings→learning
  done
done

echo ""
if [[ "${DRY_RUN}" == "true" ]]; then
  echo "  Dry run complete. Run without --dry-run to apply."
else
  echo "  Added frontmatter: ${ADDED}  Skipped (already have it): ${SKIPPED}"
fi
echo ""
