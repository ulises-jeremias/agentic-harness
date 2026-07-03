# Cursor Quick Start

> 5-minute setup to use agentic-harness with Cursor.

## Prerequisites

- Cursor installed
- agentic-harness cloned to `~/.ai-workspace`

## Setup

```bash
cd ~/.ai-workspace
bash scripts/workspace-init.sh
```

Cursor reads `CLAUDE.md` (symlinked to `AGENTS.md`) and `.cursor/rules/` for instructions. If you have agentic-workstation installed, Cursor also discovers skills from `~/.cursor/skills/`.

## First Session

1. Open Cursor
2. Open the harness directory: `~/.ai-workspace`
3. In Cursor's AI chat, type:

```text
Run workspace-context and assistant-memory inject. What do you know about my projects?
```

## Load a Pack

In Cursor's terminal:

```bash
./bin/workspace-context load --pack packs/my-project.yaml
```

Then in AI chat:

```text
Load the workspace context snapshot. What project are we working on?
```

## Use Personas

Cursor can load persona constraints. Start a chat with:

```text
Act as the implementer persona. We're going to build a feature.
```

Or load explicitly:

```bash
./bin/workspace-context load --persona implementer
```

## Cursor-Specific Features

### .cursor/rules/

If you have existing `.cursor/rules/` files, they work alongside the harness. The harness doesn't replace them — it adds context layers on top.

### Composer

When using Cursor Composer, the harness context is available through `workspace-context` output. Paste the snapshot into Composer's context window for full harness awareness.

### Agent Mode

In Cursor Agent mode, the harness routing table in AGENTS.md tells the agent which skills and subagents to delegate to.

## Verify It Works

Ask Cursor AI: "Read AGENTS.md and tell me the routing table."

## Troubleshooting

- **"CLAUDE.md not read"**: Ensure you opened `~/.ai-workspace` as the workspace folder in Cursor
- **"Skills don't appear"**: Install agentic-workstation and run `dots-skills sync`
