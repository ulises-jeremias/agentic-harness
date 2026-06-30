---
type: learning
updated: 2026-06-30
confidence: high
---

# General Learnings

> Patterns, methodology notes, and insights from AI workspace sessions.
> Add entries with: `./bin/assistant-memory add --type learning "..."`

---

## The Agentic Harness Model

This workspace is an implementation of the **Ralph Loop** paradigm — a methodology for working with AI agents as a continuous, self-improving loop rather than a one-shot tool.

**Reference:** [ghuntley.com/loop](https://ghuntley.com/loop/) (Geoffrey Huntley, Jan 2026)

### Core insight

Instead of building software brick-by-brick (Jenga model), you program the **loop itself**:
define context → give goal → execute → observe → fix → iterate. Learning comes from watching
the loop. When a failure domain appears, fix it so it never happens again.

### This workspace mapped to Ralph concepts

| Ralph concept | This workspace | File/tool |
|---------------|---------------|-----------|
| **Backing specifications** | Orchestration rules, routing, constraints | `AGENTS.md` |
| **Context engineering** | Domain skills loaded per task | Skills system (workstation) |
| **Persistent memory** | Patterns, decisions that survive sessions | `knowledge/` |
| **Fix the loop** | Save discoveries after each session | `bin/assistant-memory` |
| **Monolithic orchestrator** | Single entry point, skills called sequentially | `AGENTS.md` routing |
| **Deferred work queue** | Background tasks that don't block the session | `bin/devcompanion` |

### The loop in practice (each session)

```text
1. Allocate context  → AGENTS.md + skills + knowledge/
2. Set goal          → user presents task
3. Execute           → orchestrator routes, skills execute
4. Watch             → observe failure domains or discoveries
5. Fix               → save learnings via assistant-memory
6. Next iteration    → the loop is slightly better than before
```

### Why monolithic first

Avoid premature multi-agent decomposition:
> "What would microservices look like if the microservices are non-deterministic — a red hot mess."

Single orchestrator calling skills sequentially is the right default. Multi-agent is reserved for tasks that genuinely need parallel isolation.

---

## Persona Philosophy

Personas define **behavioral constraints**, not identity.

**Wrong approach:** "You are a senior software engineer with 10 years of experience..."
**Right approach:** Define what to produce, what to avoid, what a correct output looks like.

Constraints > Identity. See `personas/` directory for examples.

---

## Workflow Patterns

### Starting work on a new project

```text
1. Check knowledge/ for existing context: ./bin/assistant-memory search "project-name"
2. Clone + index: ./bin/project-indexer clone owner/repo-name
3. Inspect repo: README → docs/ → AGENTS.md → CONTRIBUTING
4. Save key findings to knowledge/
```

### When to queue vs interactive

| Situation | Use |
|-----------|-----|
| Quick task, needs back-and-forth | Interactive AI session (default) |
| Long-running, can run async | `devcompanion queue` |
| Blocking the current session | `devcompanion queue` |
| Batch across multiple projects | `devcompanion queue` (one per project) |

### Knowledge saving flow

```text
Task completed
    │
    ▼
Valuable pattern? ──No──→ Done
    │
   Yes
    │
    ▼
./bin/assistant-memory add --type learning "..."
```

---

## Tool Preferences

> Fill this section with your own preferences as you discover them.

| Tool | Purpose | Notes |
|------|---------|-------|
| `bin/devcompanion` | Queue system for deferred work | |
| `bin/project-indexer` | Project symlink management | |
| `bin/assistant-memory` | Knowledge base CLI | |
| `bin/workspace-context` | Session state snapshot and pack loading | |

---

## AI Tool Portability

| Tool | Config file read |
|------|-----------------|
| Claude Code | `AGENTS.md` |
| opencode | `CLAUDE.md` → symlink to `AGENTS.md` |
| Cursor | `CLAUDE.md` |
| GitHub Copilot | `.github/copilot-instructions.md` → symlink to `AGENTS.md` |
| Gemini CLI | `GEMINI.md` → symlink to `AGENTS.md` (optional) |

---

## History

| Date | Learning | Context |
|------|----------|---------|
| _YYYY-MM-DD_ | Created workspace | Initial setup |
