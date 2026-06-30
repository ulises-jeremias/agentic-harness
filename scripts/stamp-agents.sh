#!/usr/bin/env bash
# scripts/stamp-agents.sh
# Compute a SHA-256 content hash of AGENTS.md (excluding any prior stamp line)
# and update the stamp line at the top of the file.
#
# Usage:
#   bash scripts/stamp-agents.sh [--check]
#
# Options:
#   --check   Exit non-zero if the stamp is missing or stale (for CI/pre-commit)

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS_MD="${WORKSPACE_ROOT}/AGENTS.md"

if [[ ! -f "${AGENTS_MD}" ]]; then
  echo "AGENTS.md not found: ${AGENTS_MD}" >&2
  exit 1
fi

CHECK_MODE=false
[[ "${1:-}" == "--check" ]] && CHECK_MODE=true

# Compute hash of AGENTS.md body (excluding the stamp line itself)
HASH=$(python3 - "${AGENTS_MD}" <<'PYEOF'
import hashlib, pathlib, sys, re

agents = pathlib.Path(sys.argv[1])
content = agents.read_text(encoding="utf-8")
cleaned = re.sub(r"^<!-- spec-hash:[0-9a-f]+ -->\n", "", content, flags=re.MULTILINE)
h = hashlib.sha256(cleaned.encode()).hexdigest()[:12]
print(h)
PYEOF
)

STAMP="<!-- spec-hash:${HASH} -->"
CURRENT_STAMP=$(head -1 "${AGENTS_MD}")

if [[ "${CHECK_MODE}" == "true" ]]; then
  if [[ "${CURRENT_STAMP}" == "${STAMP}" ]]; then
    echo "  ✓ AGENTS.md@${HASH} is current"
    exit 0
  else
    echo "  ✗ AGENTS.md stamp is missing or stale (run: bash scripts/stamp-agents.sh)" >&2
    echo "    Expected: ${STAMP}" >&2
    echo "    Found:    ${CURRENT_STAMP}" >&2
    exit 1
  fi
fi

# Prepend or update the stamp line
python3 - "${AGENTS_MD}" "${STAMP}" <<'PYEOF'
import pathlib, re, sys

agents = pathlib.Path(sys.argv[1])
stamp = sys.argv[2]
content = agents.read_text(encoding="utf-8")

if re.match(r"^<!-- spec-hash:[0-9a-f]+ -->", content):
    content = re.sub(r"^<!-- spec-hash:[0-9a-f]+ -->\n", stamp + "\n", content)
else:
    content = stamp + "\n" + content

agents.write_text(content, encoding="utf-8")
PYEOF

echo "  ✓ AGENTS.md stamped: ${HASH}"
