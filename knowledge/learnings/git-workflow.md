# Git Workflow Patterns

> SAMPLE — Replace with your own git workflow learnings.

## 2026-07-03 — Atomic commits for reviewer preference

**Context**: The code reviewer expressed preference for small, atomic commits.

**Rule**: Each commit should address one concern:
- Feature logic in one commit
- Tests for that feature in a second commit (or same if < 50 lines)
- Documentation updates in a third commit
- Never mix refactoring with feature work in the same commit

**Why**: Makes git bisect more useful and PR review faster.

## 2026-07-02 — Squash merge for PRs, rebase for feature branches

**Context**: Team decision on merge strategy.

**Decision**:
- PRs to main: squash merge (clean history, one commit per feature)
- Feature branches: rebase on main before PR (avoids merge commits in PR)
- Never force-push to main or shared branches

**Exception**: Large refactors (>500 lines) may use merge commits to preserve context.
