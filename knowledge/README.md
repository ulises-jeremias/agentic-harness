---
type: index
updated: 2026-06-30
---

# Knowledge Base

> Persistent memory for your AI workspace. Stores learned patterns, processes, tool preferences, and pending tasks across sessions.

**Core principle**: The AI checks this directory **before asking you**. Save what you learn. Avoid repeating yourself.

---

## Structure

> [!NOTE]
> The entries in `learnings/` and `processes/` are **SAMPLE content** — replace them with your own learnings from AI sessions. Each file is labeled with "SAMPLE" at the top.

```text
knowledge/
├── README.md                  # This index
├── learnings/
│   ├── general.md             # Cross-cutting patterns and conventions
│   ├── python-patterns.md     # Python-specific patterns
│   ├── git-workflow.md        # Branch naming, commit, and merge conventions
│   └── review-preferences.md  # Reviewer expectations and PR format
├── processes/
│   ├── general.md             # Feature dev workflow, release process
│   ├── jira.md                # JIRA usage patterns (if applicable)
│   ├── clickup.md             # ClickUp usage patterns (if applicable)
│   └── confluence.md          # Confluence usage patterns (if applicable)
├── skills/
│   └── discovered.md          # New tool capabilities discovered during sessions
└── todos/
    └── pending.md             # Auto-generated from devcompanion queue
```

---

## CLI Usage

```bash
# Search for existing knowledge before asking
./bin/assistant-memory search "topic"

# Add a new learning after a session
./bin/assistant-memory add --type learning "Pattern: X works better than Y"

# Add a pending follow-up
./bin/assistant-memory add --type todo "Investigate why X behaves differently"

# Review pending items at session start
./bin/assistant-memory todo

# Show top learnings for context injection
./bin/assistant-memory inject
```

---

## Rules

1. **Check before asking** — if we've learned it before, use it
2. **Save after learning** — if the user teaches something, document it
3. **Save after discovering** — if a pattern emerges, record it
4. **Review todos at session start** — check `./bin/assistant-memory todo`

---

## What belongs here

| Type | Where | Example |
|------|-------|---------|
| Code patterns and conventions | `learnings/<topic>.md` | Conventional Commits, Python project structure |
| Process workflows | `processes/<tool>.md` | Release process, feature development flow |
| General patterns | `processes/general.md` | Cross-cutting team practices |
| Git/branch conventions | `learnings/git-workflow.md` | Branch naming, merge strategy |
| Review preferences | `learnings/review-preferences.md` | PR format, reviewer priorities |
| Discovered capabilities | `skills/discovered.md` | New tool features found during sessions |
| Session learnings | `learnings/general.md` | Any cross-cutting pattern or insight |
| Background job queue | `todos/pending.md` | Auto-generated from devcompanion |

## What does NOT belong here

| Thing | Put it instead |
|-------|---------------|
| Project-specific data (IDs, credentials) | `.workspace.yaml` (gitignored) |
| Client-sensitive information | Project pack in `packs/<client>/` (gitignored) |
| Large datasets or files | External storage, reference by path |
| Secrets or tokens | Environment variables, never files |
