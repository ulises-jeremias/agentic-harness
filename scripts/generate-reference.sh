#!/usr/bin/env bash
# scripts/generate-reference.sh
# Generate docs/REFERENCE.md from --help output of all bin/* tools.
#
# Usage:
#   bash scripts/generate-reference.sh          # regenerate
#   bash scripts/generate-reference.sh --check  # exit 1 if stale

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${WORKSPACE_ROOT}/docs/REFERENCE.md"

CHECK=false
[[ "${1:-}" == "--check" ]] && CHECK=true

generate() {
  echo "# CLI Reference"
  echo ""
  echo "> Auto-generated from \`bin/*\` \`--help\` output."
  echo "> Run \`bash scripts/generate-reference.sh\` to regenerate."
  echo ""
  echo "---"

  for bin_file in "${WORKSPACE_ROOT}/bin/"*; do
    [[ -f "${bin_file}" ]] || continue
    name=$(basename "${bin_file}")
    echo ""
    echo "## \`${name}\`"
    echo ""
    echo '```text'
    # Try --help first, then help subcommand
    python3 "${bin_file}" --help 2>/dev/null \
      || python3 "${bin_file}" help 2>/dev/null \
      || bash "${bin_file}" --help 2>/dev/null \
      || bash "${bin_file}" help 2>/dev/null \
      || echo "(no --help output available)"
    echo '```'
  done
}

if [[ "${CHECK}" == "true" ]]; then
  current=$(generate 2>/dev/null)
  if [[ -f "${OUT}" && "$(cat "${OUT}")" == "${current}" ]]; then
    echo "  ✓ docs/REFERENCE.md is up to date"
    exit 0
  fi
  echo "  ✗ docs/REFERENCE.md is stale. Run: bash scripts/generate-reference.sh" >&2
  exit 1
fi

generate > "${OUT}" 2>/dev/null
echo "  ✓ Written docs/REFERENCE.md"
