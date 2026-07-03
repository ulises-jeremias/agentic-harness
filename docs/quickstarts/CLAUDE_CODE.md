# Claude Code Quick Start

> 5-minute setup to use agentic-harness with Claude Code.

## Prerequisites

- Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- agentic-harness cloned to `~/.ai-workspace`

## Setup

```bash
cd ~/.ai-workspace
bash scripts/workspace-init.sh
```

Claude Code reads `CLAUDE.md` which is symlinked to `AGENTS.md`. The harness is already configured.

## First Session

```bash
cd ~/.ai-workspace
claude
```

In Claude Code, start with:

```text
Run workspace-context and assistant-memory inject. What do you know about my setup?
```

Claude Code will read AGENTS.md (via CLAUDE.md symlink), load workspace context, and inject any saved knowledge entries.

## Load a Pack

```bash
# Before starting Claude
./bin/workspace-context load --pack packs/my-project.yaml
claude
```

Claude Code now sees your project repos, conventions, and LLM policy.

## Use Personas

```bash
# Load persona before starting
./bin/workspace-context load --persona implementer
claude
```

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Symlink to AGENTS.md — routing table |
| `~/.claude/CLAUDE.md` | Global Claude instructions (set by agentic-workstation) |
| `~/.claude/settings.json` | Claude Code settings |

## Verify It Works

Ask Claude Code: "What persona is active and what packs are loaded?"

It should respond with the active persona constraints and pack context.

## Troubleshooting

- **"AGENTS.md not found"**: Make sure you're in `~/.ai-workspace` when starting Claude
- **"No skills available"**: Install agentic-workstation skills: `curl -fsSL https://github.com/ulises-jeremias/agentic-workstation/releases/latest/download/install-skills.sh | bash`
