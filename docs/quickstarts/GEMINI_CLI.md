# Gemini CLI Quick Start

> 5-minute setup to use agentic-harness with Gemini CLI.

## Prerequisites

- Gemini CLI installed
- agentic-harness cloned to `~/.ai-workspace`

## Setup

```bash
cd ~/.ai-workspace
bash scripts/workspace-init.sh
```

Gemini CLI reads `GEMINI.md` which is symlinked to `AGENTS.md`.

## First Session

```bash
cd ~/.ai-workspace
gemini
```

Start with:

```text
Read GEMINI.md and workspace-context output. What do you know about my setup?
```

## Load a Pack

```bash
./bin/workspace-context load --pack packs/my-project.yaml
gemini
```

## Use Personas

```bash
./bin/workspace-context load --persona architect
gemini
```

## Key Advantage

Gemini 2.5 Pro has a 1M token context window — the largest of any supported tool. This means you can:

- Load your entire knowledge base without truncation
- Include multiple large packs simultaneously
- Process very large codebases with full context

## Key Files

| File | Purpose |
|------|---------|
| `GEMINI.md` | Symlink to AGENTS.md |
| `~/.gemini/` | Gemini CLI configuration |

## Verify It Works

Ask Gemini: "What does the routing table in GEMINI.md say?"

## Troubleshooting

- **"GEMINI.md not found"**: Run `bash scripts/workspace-init.sh` in the harness directory
- **"1M context seems slow"**: Large context can increase latency — use packs to load only what's needed
