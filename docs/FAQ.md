# FAQ — agentic-harness

> Common questions and answers for new and experienced users.

---

## Getting Started

### Do I need agentic-workstation to use agentic-harness?

No. The harness works standalone with any AI coding tool. However, without agentic-workstation you lose:
- Pre-built skill packs (Jira, GitHub, ClickUp, etc.)
- Dev companion LLM-powered runner
- MCP server templates

You can use the harness for memory, personas, packs, and loops without agentic-workstation. Skills are optional but recommended.

### Which AI tools does the harness support?

Claude Code, opencode, Cursor, GitHub Copilot, and Gemini CLI. Each tool reads a different config file (AGENTS.md, CLAUDE.md, GEMINI.md, .github/copilot-instructions.md). The harness provides symlinks so all tools see the same instructions.

### How long does setup take?

- **First-time setup**: ~5 minutes (clone + `scripts/workspace-init.sh`)
- **With agentic-workstation skills**: ~15 minutes (includes skill installation)
- **With loop scheduling**: ~20 minutes (includes systemd/launchd config)

---

## Context Engineering

### What's the difference between a pack and a profile?

| Feature | Pack | Profile |
|---------|------|---------|
| Purpose | Per-project context | Session preset |
| Contains | Repos, IDs, conventions, LLM policy | Pack + persona + skills |
| File type | `packs/*.yaml` | `profiles/*.yaml` |
| Use case | "I'm working on client X" | "I want implementer mode for client X" |

A pack describes the project. A profile describes how you want to work on it.

### When should I use a persona vs a subagent?

- **Persona**: Session-level. Constrains ALL AI behavior for the entire session. Use for: "Today I'm reviewing code" or "I'm only researching, no changes."
- **Subagent**: Task-level. Delegated from within a persona. Use for: "Plan this feature" (planner) or "Review this PR" (code-reviewer).

Think of personas as your role and subagents as your team.

### How do I handle multiple clients?

Create a pack per client and load it at session start:

```bash
workspace-context load --pack packs/acme-corp.yaml
# ... work on Acme tasks ...
workspace-context load --pack packs/startup-x.yaml
# ... switch to Startup X ...
```

Each pack isolates repos, tools, and LLM policies. No cross-contamination between clients.

### What should I put in knowledge/ vs just documenting in code?

| Put in knowledge/ | Keep in code/docs |
|-------------------|-------------------|
| Patterns discovered during work | API docs and READMEs |
| User preferences (naming, style) | Code comments |
| Process workflows that change | Architecture decisions (ADRs) |
| Gotchas and workarounds | Technical specifications |
| Follow-up todos | Issue trackers |

Knowledge is what the AI learned through interaction. Documentation is what you wrote intentionally.

---

## Loop Engineering

### What tier should my loop start at?

Always start at **Tier 1** (report-only). Tier 1 loops:
- Read data only (no writes, PRs, comments)
- Print a report to terminal/STATE.md
- Cannot cause damage

Move to Tier 2 after you've reviewed Tier 1 output for at least a week. Move to Tier 3 only after Tier 2 has run successfully for at least a month.

### How do loops survive between terminal sessions?

Each loop stores its state in `loops/<name>/STATE.md` (git-tracked). The loop reads its previous state on each run. If you schedule with `bin/loop schedule`, systemd or launchd runs it on a timer — no terminal needed.

### How much do loops cost?

Depends on the loop and model. A rough estimate:

| Tier | Example | Tokens/run | Est. cost/day |
|------|---------|-----------|---------------|
| L1 | Daily issue triage | ~5K | ~$0.05 |
| L2 | PR babysitter (10 PRs) | ~20K | ~$0.20 |
| L3 | CI sweeper (5 repos) | ~50K | ~$0.50 |

Use `bin/loop cost <name> --monthly` for accurate projections based on actual token usage.

---

## Knowledge Base

### How big can knowledge/ get before it causes problems?

The practical limit depends on your AI tool's context window. `assistant-memory inject` outputs all knowledge entries. If your context window is 200K tokens (Claude), you can comfortably store 50-100 knowledge entries before injection dominates the context.

For larger knowledge bases:
- Archive stale entries periodically
- Use the search command instead of inject for targeted lookups
- Split very large entries into multiple smaller ones

### How do I prevent knowledge from getting stale?

Use `assistant-memory review --stale` (coming soon) to detect entries older than your threshold. Review the knowledge base monthly. Archive entries that reference tools/processes that no longer exist.

---

## Dev Companion

### When should I queue vs work interactively?

| Queue when... | Work interactively when... |
|---------------|--------------------------|
| Task will take >5 minutes | Task is quick and you're waiting |
| You have multiple things to do | You need immediate feedback |
| The task is standard (code review, PR) | The task requires exploration |
| You want to batch similar work | You're debugging something |

### Can I run dev companion without an LLM?

Yes. Use `--no-llm` for a skeleton plan. This is useful for Cursor/Copilot-only setups where you drive the LLM inside the IDE with the client's account.

---

## Troubleshooting

### The AI doesn't seem to see my pack/persona/skills

Run `workspace-context` and check the output. It prints every loaded context surface. Missing entries usually mean:
- Pack file has invalid YAML (check with schema validation)
- Persona frontmatter is malformed
- Skills aren't installed or `HARNESS_RUNNER_DIR` isn't set

### My loop stopped working after a repo rename

Loops store repo paths in STATE.md. If you rename or move a repo, update the path in the loop's STATE.md file or re-initialize the loop with `bin/loop init <name> --template <name>`.

### I get "policy_no_provider_available" from dev companion

Your LLM policy is too restrictive. Check:
1. `DOTS_AI_DEVCOMPANION_LLM_ALLOWLIST` — is your provider listed?
2. `DOTS_AI_DEVCOMPANION_LLM_STRICT` — is strict mode blocking fallback?
3. Run `dots-devcompanion llm-status` to see the active policy.
