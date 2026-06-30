#!/usr/bin/env bash
# scripts/validate-context.sh
# Validate all context files (packs, job templates, personas) against their JSON Schemas.
# Exit 0 = all valid. Exit 1 = one or more violations.
#
# Usage:
#   ./scripts/validate-context.sh                  # validate everything
#   ./scripts/validate-context.sh --surface packs  # validate one surface
#
# Surfaces: packs | jobs | personas | all (default)

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMAS="${WORKSPACE_ROOT}/schemas"

# ── colors ────────────────────────────────────────────────────────────────────
_c() { [[ -t 1 ]] && printf '\033[%sm%s\033[0m' "$1" "$2" || printf '%s' "$2"; }
ok()   { _c "1;32" "  ✓"; echo " $*"; }
fail() { _c "1;31" "  ✗"; echo " $*"; }
info() { _c "1;34" "  →"; echo " $*"; }

# ── parse args ────────────────────────────────────────────────────────────────
SURFACE="all"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --surface) SURFACE="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [--surface packs|jobs|personas|all]"
      exit 0 ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

# ── validator (python) ────────────────────────────────────────────────────────
# Inline Python so we have no Node/npm dependency.
validate_file() {
  local file="$1" schema="$2"
  python3 - "$file" "$schema" <<'PYEOF'
import sys, json, pathlib

try:
    import yaml  # type: ignore
    _YAML = True
except ImportError:
    _YAML = False

try:
    import jsonschema  # type: ignore
except ImportError:
    print("  [skip] jsonschema not installed — run: pip install jsonschema")
    sys.exit(0)

file_path, schema_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
content = file_path.read_text(encoding="utf-8")

# Strip YAML frontmatter from .md files (--- ... ---)
if file_path.suffix == ".md":
    lines = content.splitlines()
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end is not None:
            content = "\n".join(lines[1:end])
        else:
            print(f"  [warn] {file_path.name}: frontmatter not closed with ---")
            sys.exit(0)
    else:
        # No frontmatter — nothing to validate for persona files
        print(f"  [skip] {file_path.name}: no YAML frontmatter found")
        sys.exit(0)

# Parse YAML
if _YAML:
    instance = yaml.safe_load(content)
else:
    # Fallback: try JSON (only works for .json files)
    try:
        instance = json.loads(content)
    except Exception:
        print(f"  [skip] {file_path.name}: PyYAML not installed, cannot parse YAML")
        sys.exit(0)

schema = json.loads(schema_path.read_text(encoding="utf-8"))

validator = jsonschema.Draft202012Validator(schema)
errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))

if errors:
    for e in errors:
        path = " → ".join(str(p) for p in e.path) or "(root)"
        print(f"  [error] {file_path.name} [{path}]: {e.message}")
    sys.exit(1)

sys.exit(0)
PYEOF
}

# ── surfaces ──────────────────────────────────────────────────────────────────
ERRORS=0

run_packs() {
  info "Validating packs/ ..."
  local schema="${SCHEMAS}/pack.schema.json"
  if [[ ! -f "$schema" ]]; then
    fail "Schema not found: $schema"
    return 1
  fi
  local found=0
  for f in "${WORKSPACE_ROOT}/packs/"*.yaml; do
    [[ -e "$f" ]] || continue
    found=$((found + 1))
    if validate_file "$f" "$schema" 2>&1; then
      ok "$(basename "$f")"
    else
      fail "$(basename "$f") — schema violation"
      ERRORS=$((ERRORS + 1))
    fi
  done
  if [[ $found -eq 0 ]]; then ok "packs/ (no files)"; fi
}

run_jobs() {
  info "Validating templates/jobs/ ..."
  local schema="${SCHEMAS}/job.schema.json"
  if [[ ! -f "$schema" ]]; then
    fail "Schema not found: $schema"
    return 1
  fi
  local found=0
  for f in "${WORKSPACE_ROOT}/templates/jobs/"*.yaml; do
    [[ -e "$f" ]] || continue
    found=$((found + 1))
    if validate_file "$f" "$schema" 2>&1; then
      ok "$(basename "$f")"
    else
      fail "$(basename "$f") — schema violation"
      ERRORS=$((ERRORS + 1))
    fi
  done
  if [[ $found -eq 0 ]]; then ok "templates/jobs/ (no files)"; fi
}

run_personas() {
  info "Validating personas/ frontmatter ..."
  local schema="${SCHEMAS}/persona-frontmatter.schema.json"
  if [[ ! -f "$schema" ]]; then
    fail "Schema not found: $schema"
    return 1
  fi
  local found=0
  for f in "${WORKSPACE_ROOT}/personas/"*.md; do
    [[ -e "$f" ]] || continue
    found=$((found + 1))
    if validate_file "$f" "$schema" 2>&1; then
      ok "$(basename "$f")"
    else
      fail "$(basename "$f") — schema violation"
      ERRORS=$((ERRORS + 1))
    fi
  done
  if [[ $found -eq 0 ]]; then ok "personas/ (no files)"; fi
}

# ── dispatch ──────────────────────────────────────────────────────────────────
echo ""
echo "Context Validation"
echo "------------------"

case "$SURFACE" in
  packs)    run_packs ;;
  jobs)     run_jobs ;;
  personas) run_personas ;;
  all)      run_packs; run_jobs; run_personas ;;
  *)        echo "Unknown surface: $SURFACE" >&2; exit 1 ;;
esac

echo ""
if [[ $ERRORS -gt 0 ]]; then
  _c "1;31" "  $ERRORS violation(s) found."; echo " Fix them before committing."
  exit 1
else
  _c "1;32" "  All context files valid."; echo ""
  exit 0
fi
