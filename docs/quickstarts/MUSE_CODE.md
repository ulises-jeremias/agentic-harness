# Muse Code Quick Start

> 5-minute setup to use agentic-harness with Muse Code (Meta).

## Prerequisites

- Muse Code installed (`curl -fsSL https://dev.meta.ai/install.sh | bash`)
- agentic-harness cloned to `~/.ai-workspace`

## Setup

```bash
cd ~/.ai-workspace
bash scripts/workspace-init.sh
```

Muse Code reads `AGENTS.md` (portable contract; `CLAUDE.md` is symlinked for compatibility). The harness is already configured.

Muse Code skills are available at:

- User scope: `~/.config/muse/skills/` (XDG, also `~/.agents/skills/` universal)
- Project scope: `.agents/skills/<name>/SKILL.md` (Agent Skills spec)

Sync existing Claude skills: `muse skills import --from claude --scope user`

## First Session

```bash
cd ~/.ai-workspace
muse
```

In Muse Code, start with:

```text
Run workspace-context and assistant-memory inject. What do you know about my setup?
```

Muse Code will read `AGENTS.md`, load workspace context, and inject any saved knowledge entries.

## Load a Pack

```bash
# Before starting Muse
./bin/workspace-context load --pack packs/my-project.yaml
muse
```

Muse Code now sees your project repos, conventions, and LLM policy.

## Use Personas

```bash
# Load persona before starting
./bin/workspace-context load --persona implementer
muse
```

## Key Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Primary portable contract (also `CLAUDE.md` symlinked) |
| `~/.config/muse/skills/` | User skills for Muse Code |
| `.agents/skills/` | Project-local skills (Agent Skills spec) |
| `~/.agents/skills/` | Universal skills dir (all tools) |

## Verify It Works

Ask Muse Code: "What persona is active and what packs are loaded?"

It should respond with the active persona constraints and pack context.

## Troubleshooting

- **"AGENTS.md not found"**: Make sure you're in `~/.ai-workspace` when starting Muse
- **"No skills available"**: Install agentic-workstation skills: `curl -fsSL https://github.com/ulises-jeremias/agentic-workstation/releases/latest/download/install-skills.sh | bash` then `muse skills import --from claude --scope user`
- **Sandbox blocks ~/.config/muse**: Muse runs with sandbox on by default; use `muse --disable-sandbox` for debugging or `muse skills list` diagnostics

## See Also

- [Claude Code Quick Start](CLAUDE_CODE.md)
- [OpenCode Quick Start](OPENCODE.md)
