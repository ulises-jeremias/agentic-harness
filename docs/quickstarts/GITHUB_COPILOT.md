# GitHub Copilot Quick Start

> 5-minute setup to use agentic-harness with GitHub Copilot.

## Prerequisites

- GitHub Copilot extension installed in VSCode or JetBrains
- agentic-harness cloned to `~/.ai-workspace`

## Setup

```bash
cd ~/.ai-workspace
bash scripts/workspace-init.sh
```

The harness symlinks `.github/copilot-instructions.md` to `AGENTS.md`. Copilot reads this file for global instructions.

## First Session

1. Open VSCode with the harness directory: `code ~/.ai-workspace`
2. Open Copilot Chat
3. Ask:

```text
Read AGENTS.md. What tools and skills are available?
```

## Load a Pack

In the integrated terminal:

```bash
./bin/workspace-context load --pack packs/my-project.yaml
```

Then in Copilot Chat, paste the workspace context:

```text
Here's my current workspace context:
[paste output of ./bin/workspace-context]
```

## Copilot-Specific Features

### Inline completions

Copilot's inline completions are context-aware of your open files but don't automatically include harness context. For harness-aware work, use Copilot Chat explicitly.

### Copilot Chat

Copilot Chat works best with explicit context. After loading a pack, tell Copilot:

```text
I'm working on [project]. We use [conventions]. The current task is [description].
```

### Agent mode (Coding Agent)

In Copilot's agent mode, reference the harness:

```text
Based on AGENTS.md routing, delegate code review to the code-reviewer subagent.
```

### .github/copilot-instructions.md

The harness provides this as a symlink. You can customize it per project by creating a pack that includes project-specific instructions. Individual repos can also have their own `.github/copilot-instructions.md`.

## Limitations

- Copilot has a smaller context window than Claude Code (~32K for inline, larger for Chat)
- Harness context must be explicitly pasted into Chat sessions
- Dev companion background jobs require a different tool (Claude Code or opencode)

## Verify It Works

Ask Copilot Chat: "What's in the AGENTS.md routing table?"

## Troubleshooting

- **"Copilot doesn't read harness context"**: Copilot doesn't auto-load harness files — paste workspace-context output into Chat
- **"Symlink broken"**: Run `bash scripts/workspace-init.sh` to recreate the `.github/copilot-instructions.md` symlink
