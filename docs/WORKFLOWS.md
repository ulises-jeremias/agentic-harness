# Workflows

> Common task flows and delegation patterns for the orchestrator.

---

## Orchestrator Flow

The AI session acts as a **central orchestrator**:

```text
User Task
    │
    ▼
┌─────────────────────┐
│ 1. Determine Type   │
│    - Discovery      │
│    - Code Review    │
│    - Project Mgmt   │
│    - UI/UX          │
│    - Background     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 2. Delegate         │
│    - Skills         │
│    - Subagents      │
│    - Direct exec    │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 3. Report           │
│    - Results        │
│    - Save knowledge │
│    - Follow-ups     │
└─────────────────────┘
```

---

## Task Type Routing

| Task Type | Action |
|-----------|--------|
| Discovery / repo inspection | `dev-assistant` skill |
| Generic delivery | `workflow-generic-project` skill |
| Code review | `code-reviewer` subagent |
| Security audit | `security-reviewer` subagent |
| TDD workflow | `tdd-guide` subagent |
| Refactor / cleanup | `refactor-cleaner` subagent |
| UI/UX design | `ui-ux-pro-max` skill |
| JIRA tasks | `jira-assistant` skill |
| ClickUp tasks | `clickup-cli` skill |
| Confluence | `confluence-assistant` skill |
| Deferred work | `agent-toolkit devcompanion queue` |

> Customize this table in `AGENTS.md` to match your installed skills.

---

## Common Workflows

### 1. Code Review

```text
User: "review the auth module"

1. dev-assistant → inspect codebase conventions
2. code-reviewer → analyze code quality, security, maintainability
3. Report findings
4. Save if valuable pattern discovered
```

### 2. Project Management Task

```text
User: "create a task in my project backlog"

1. Read knowledge/processes/<tool>.md for IDs and patterns
2. Use the appropriate skill (jira-assistant / clickup-cli)
3. Report task ID and URL
```

### 3. Repository Discovery

```text
User: "explore the my-service repo"

1. Read my-service/README.md
2. Read my-service/AGENTS.md or CLAUDE.md (if exists)
3. Identify stack, structure, conventions
4. Report summary
5. Save key findings to knowledge/ if reusable
```

### 4. Delivery Flow

```text
User: "implement feature X"

1. dev-assistant → discovery and convention check
2. workflow-generic-project → planning phase
3. Implementation
4. code-reviewer → review
5. github-cli-workflow → draft PR
```

### 5. Background / Deferred Work

```text
User: "do a code review of my-project in the background"

1. agent-toolkit devcompanion queue my-project --template code-review
2. agent-toolkit devcompanion run-once
3. Show generated plan.md artifact to user
```

---

## Skills vs Subagents

### Skills

Skills are **loaded instructions** that provide domain-specific guidance:

- Loaded on demand via the `skill` tool
- Provide CLI patterns, best practices, and tool-specific workflows
- Examples: `jira-assistant`, `confluence-assistant`, `clickup-cli`, `ui-ux-pro-max`

Use skills for:

- Repeated tasks with known patterns
- CLI tool usage
- Best practice guidance

### Subagents

Subagents are **autonomous agents** that can perform complex tasks:

- Invoked as specialized agents with focused mandates
- Can run tools, read code, produce artifacts independently
- Examples: `code-reviewer`, `security-reviewer`, `tdd-guide`, `refactor-cleaner`

Use subagents for:

- Complex multi-step analysis
- Independent execution
- Specialized deep dives

---

## Knowledge Saving Flow

After completing valuable work:

```text
Task completed
    │
    ▼
┌─────────────────────┐
│ Valuable pattern?   │
│ - New skill         │
│ - New process       │
│ - Learned approach  │
└─────────┬───────────┘
          │
          ▼
    ┌─────┴─────┐
    │           │
   Yes          No
    │           │
    ▼           ▼
Add to       Done
knowledge/
```

```bash
./bin/assistant-memory add --type learning "Pattern: always run X before Y in this repo"
./bin/assistant-memory add --type todo "Follow up: migrate auth to new pattern"
```

---

## Best Practices

1. **Always inspect before acting** — Use `dev-assistant` for first-time work on a repo
2. **Save valuable discoveries** — Knowledge benefits future sessions
3. **Use appropriate delegation** — Skills for patterns, subagents for deep work
4. **Report in user's language** — Match what the user wrote in
5. **Technical output in English** — Tickets, PRs, commits, docs always in English
6. **Plan before implementing** — Never skip the plan phase for non-trivial work
