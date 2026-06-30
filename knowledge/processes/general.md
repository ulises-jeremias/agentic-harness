---
type: process
updated: 2026-06-30
confidence: high
---

# General Process Patterns

> Cross-tool workflow patterns discovered during sessions.
> Add entries with: `./bin/assistant-memory add --type process "..."`

---

## Task Type Routing

| Type | Pattern |
|------|---------|
| Bug fix | discover → fix → review → PR |
| Feature | discover → plan → implement → review → PR |
| Research | explore → summarize → propose |
| Maintenance | identify → fix → test → commit |
| Data pipeline | inspect → validate → test → PR |

---

## Delivery Workflow

```text
1. Discovery  — inspect repo (README → docs/ → AGENTS.md → CONTRIBUTING)
2. Planning   — break into tasks, identify risks
3. Implement  — work with appropriate persona constraints
4. Review     — quality, security, correctness gate
5. PR         — push branch, open draft PR
```

## Communication Defaults

> Override in AGENTS.md with your preferred language settings.

- **User communication**: configure in AGENTS.md
- **Technical output** (tickets, PRs, commits): English (recommended)
- **Documentation**: English (recommended)

---

## Common Patterns

### When starting any session

```text
1. Check knowledge/ for context: ./bin/assistant-memory search "topic"
2. Check pending items: ./bin/assistant-memory todo
3. If working on a repo: inspect before acting
```

### When something unexpected happens

```text
1. Document the behavior
2. Search knowledge/ for similar cases: ./bin/assistant-memory search "symptom"
3. If new pattern: save it → ./bin/assistant-memory add --type learning "..."
4. If needs follow-up: ./bin/assistant-memory add --type todo "..."
```

### Knowledge saving trigger

```text
After any session where you learn something:
→ ./bin/assistant-memory add --type learning "Pattern: ..."
→ ./bin/assistant-memory add --type process "Tool: CLI usage pattern"
```

---

## Notes

<!-- Add cross-tool patterns as you discover them -->

---

## History

| Date | Pattern | Context |
|------|---------|---------|
| _YYYY-MM-DD_ | _Pattern discovered_ | _Session context_ |
