# opencode Quick Start

> 5-minute setup to use agentic-harness with opencode.

## Prerequisites

- opencode installed
- agentic-harness cloned to `~/.ai-workspace`

## Setup

```bash
cd ~/.ai-workspace
bash scripts/workspace-init.sh
```

opencode reads `CLAUDE.md` (symlinked to `AGENTS.md`) and `.opencode/` configuration.

## First Session

```bash
cd ~/.ai-workspace
opencode
```

In opencode, start with:

```text
Run workspace-context and assistant-memory inject. Tell me what you know about my setup.
```

## Load a Pack

```bash
# Before starting opencode
./bin/workspace-context load --pack packs/my-project.yaml
opencode
```

## Use Personas

```bash
./bin/workspace-context load --persona reviewer
opencode
```

The reviewer persona constrains opencode to read-only analysis — no file writes or command execution.

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Symlink to AGENTS.md |
| `.opencode/` | opencode configuration directory |
| `~/.config/opencode/` | Global opencode config |

## Verify It Works

Ask opencode: "What workspace context is loaded?"

## Troubleshooting

- **"CLAUDE.md symlink broken"**: Run `bash scripts/workspace-init.sh` to recreate symlinks
- **"Skills not found"**: Install agentic-workstation skills for skill delegation support
