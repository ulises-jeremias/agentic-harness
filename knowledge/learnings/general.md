# General Learnings

> SAMPLE — Replace with your own learnings from AI sessions.

## 2026-07-03 — Conventional Commits standard

**Context**: During PR review of hello-harness, the reviewer requested Conventional Commits format.

**Decision**: All commits must use Conventional Commits with the following prefixes:
- `feat:` — new features
- `fix:` — bug fixes
- `docs:` — documentation only
- `refactor:` — code changes that don't add features or fix bugs
- `chore:` — maintenance, CI, dependencies
- `test:` — adding or updating tests

**Scope**: Applies to all repos in the workspace.

## 2026-07-02 — Python project structure convention

**Context**: After setting up multiple Python projects, a consistent structure emerged.

**Pattern**: Python projects should follow this layout:
```
project/
├── src/project/    # Package source
├── tests/          # Mirror of src/ structure with test_ prefix
├── pyproject.toml  # Build config and dependencies
├── conftest.py     # Shared pytest fixtures
└── README.md
```

**Evidence**: This structure works well with uv, pytest, and IDE tooling.

## 2026-07-01 — Branch naming for Jira-integrated repos

**Context**: Jira automation links branches to issues when they follow a specific pattern.

**Pattern**: Feature branches use `feat/PROJECTKEY-123-short-description` format.
- Example: `feat/ACME-456-add-login-endpoint`
- Bug fixes: `fix/PROJECTKEY-789-description`
- The Jira key enables automatic issue linking in PRs.
