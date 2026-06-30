# Claude Code — Local Overlay

> Tool-specific addendum to AGENTS.md for Claude Code users.
> This file is read AFTER AGENTS.md (via ~/.claude/settings.json contextFiles).

---

## Claude Code Specific

### Sub-agent types

When delegating to specialized agents, use the Claude Code sub-agent types:

- `architect` — system design, tradeoffs, ADRs
- `planner` — complex feature planning
- `Explore` — fast read-only codebase search
- `code-reviewer` — quality and security review

### MCP tools available

If the Claude Code Remote MCP is configured:

- `mcp__claude_ai_Claude_Code_Remote__create_trigger` — schedule recurring loop runs
- `mcp__claude_ai_Claude_Code_Remote__send_later` — defer a message

### Loop scheduling via Claude Code

```text
mcp__claude_ai_Claude_Code_Remote__create_trigger
  cron_expression: "0 8 * * *"
  prompt: "Run bin/loop run daily-triage"
```

---

## No breaking changes to AGENTS.md

This file adds Claude Code capabilities. AGENTS.md remains the source of truth.
