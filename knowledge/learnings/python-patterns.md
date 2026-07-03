# Python Patterns

> SAMPLE — Replace with your own Python-specific learnings.

## 2026-07-03 — CLI tools use click library with --dry-run convention

**Context**: All CLI tools across the workspace (bin/*) use the `click` library.

**Pattern**: Every CLI command should:
- Support `--dry-run` flag for preview without side effects
- Use `--verbose` for detailed output
- Return meaningful exit codes (0=success, 1=error, 2=validation failure)
- Use `click.echo()` not `print()` for proper testing support

**Where**: `bin/assistant-memory`, `bin/workspace-context`, `bin/devcompanion`

## 2026-07-02 — Testing conventions with pytest

**Context**: The test suite follows specific pytest conventions.

**Pattern**:
- Test files mirror the source structure: `tests/test_module.py` for `bin/module.py`
- Fixtures go in `conftest.py` at the test root
- Use `pytest.raises()` for expected exceptions, not try/except
- Mock external calls (API, subprocess) using `unittest.mock`

## 2026-07-01 — Type hints are mandatory in new code

**Context**: After a bug caused by passing a string where an int was expected.

**Rule**: All new Python functions must have type hints:
```python
def process_items(items: list[str], limit: int = 10) -> dict[str, int]:
    ...
```
Existing code gets type hints opportunistically during refactors — not as a dedicated migration.
