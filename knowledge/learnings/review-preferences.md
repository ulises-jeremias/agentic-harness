# Review Preferences

> SAMPLE — Replace with your team's code review preferences.

## 2026-07-03 — Reviewer preferences

**Context**: After several PR reviews, clear patterns emerged in reviewer feedback.

**What the reviewer prioritizes**:

1. **Correctness**: Does the code do what it claims? Tests should prove it.
2. **Clarity**: Can a new team member understand this in 5 minutes?
3. **Consistency**: Does it follow existing patterns in the codebase?
4. **Safety**: Are edge cases handled? What happens on failure?

**What the reviewer does NOT care about**:

- Minor formatting (let the formatter handle it)
- Naming bikeshedding (unless genuinely misleading)
- Personal style preferences (follow the existing codebase style)

## 2026-07-02 — PR description template expectations

**Context**: Reviewer noted that PR descriptions were inconsistent.

**Expected PR description format**:

```markdown
## What
[1-2 sentences describing the change]

## Why
[Reason for the change — link to issue or ticket]

## Changes
[Bullet list of what changed — files, functions, behavior]

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing steps documented
- [ ] Edge cases considered
```

**Why**: Consistent PR descriptions speed up review by setting clear expectations about scope and verification.
