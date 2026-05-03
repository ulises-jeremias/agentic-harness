# AI Workspace

> A portable agentic harness — persistent memory, project context, and workflow orchestration for your AI assistant.

Works with Claude Code, opencode, Cursor, Gemini CLI, and GitHub Copilot.

---

## What is this?

The **AI Workspace** is a framework that sits between you and your AI tool. It gives your AI:

- **Persistent memory** across sessions via `knowledge/`
- **Project context** with symlinked repos and packs
- **Workflow orchestration** with skills, personas, and job queues
- **Consistent conventions** so the AI knows *how* to work, not just *what* to do

```text
Your AI Tool  ←→  AI Workspace  ←→  Your Repos
               (this repo)
               Memory, context,
               routing, skills
```

---

## Quick Start

```bash
# 1. Clone as your personal workspace
git clone <this-repo> ~/.ai-workspace
cd ~/.ai-workspace

# 2. Run setup — creates your personal branch and configures the workspace
./scripts/workspace-init.sh

# 3. Index your repos
./bin/project-indexer clone owner/my-repo

# 4. Open in your AI tool — reads AGENTS.md automatically
opencode        # or: claude / cursor / gemini
```

### Workspace branch modes

The setup script manages a personal (or shared) Git branch automatically — no more `rm -rf .git && git init`.

```bash
# Personal workspace (default) — creates branch: user-workspace/<git-username>
./scripts/workspace-init.sh

# Shared team workspace — creates branch: account-workspace/<name>
./scripts/workspace-init.sh --account-workspace=my-team
```

If the branch already exists (locally or on the remote), the script switches to it and reminds you to pull from `main`. The setup runs non-interactively — no Enter-pressing required.

> [!TIP]
> Edit `.workspace.yaml` after setup to set your GitHub org and default clone directory.

---

## Structure

```text
ai-workspace/
├── AGENTS.md              # AI orchestration instructions (main config)
├── CLAUDE.md              # Symlink → AGENTS.md (opencode / Cursor)
├── GEMINI.md              # Symlink → AGENTS.md (Gemini CLI)
├── CONTRIBUTING.md        # How to extend the workspace
├── bin/
│   ├── project-indexer    # Clone repos + manage symlinks
│   ├── assistant-memory   # Knowledge base CLI
│   ├── devcompanion       # Background job queue
│   └── workspace-context  # Session state snapshot
├── docs/                  # Guides and references
├── knowledge/             # Persistent AI memory (processes, learnings, todos)
├── personas/              # Work mode definitions (implementer, reviewer, etc.)
├── packs/                 # Context bundles per client/project
├── templates/jobs/        # Job templates for devcompanion
├── projects/              # Symlinks to repos (gitignored, local)
└── repos/                 # Cloned repos (gitignored, local)
```

---

## Docs

| Guide | Description |
|-------|-------------|
| [`docs/SETUP.md`](docs/SETUP.md) | Initial setup and AI tool configuration |
| [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) | The agentic harness philosophy |
| [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md) | Task routing and skill usage patterns |
| [`docs/PERSONAS.md`](docs/PERSONAS.md) | Work mode personas |
| [`docs/PACKS.md`](docs/PACKS.md) | Context packs for project switching |
| [`docs/PROJECTS.md`](docs/PROJECTS.md) | Managing repos and symlinks |
| [`docs/DEVCOMPANION.md`](docs/DEVCOMPANION.md) | Background job queue guide |
| [`docs/KNOWLEDGE.md`](docs/KNOWLEDGE.md) | Knowledge base usage |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to extend and contribute |

---

## Key Concepts

### Agentic Harness

The workspace acts as a **harness** — it doesn't replace your AI tool, it amplifies it by providing context, memory, and routing that survives across sessions.

### Ralph Loop

The four-layer loop your AI runs in:

```text
Backing Specs → Context Engineering → Persistent Memory → Fix the Loop
```

Each session, the AI reads `AGENTS.md` → checks `knowledge/` → works → saves discoveries back. The loop improves itself over time.

### Personas

Personas constrain what the AI *does* in a session — not who it is. `personas/reviewer.md` means "analyze and report, no changes". Use them to avoid scope creep.

### Packs

Packs bundle project-specific context (repos, process docs, IDs) so you can switch between clients with a single command.

---

## Validation

```bash
# Verify setup
./bin/project-indexer list          # shows indexed repos
./bin/assistant-memory todo         # shows pending items
./bin/workspace-context             # session state snapshot

# Queue a test job
./bin/devcompanion queue my-project --template code-review
./bin/devcompanion run-once --no-llm
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `project-indexer: command not found` | Run `chmod +x ./bin/*` |
| DevCompanion: "No LLM provider" | Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` |
| Pending jobs stuck | Run `./bin/devcompanion status` |
| Skills not loading | Check your AI tool's skill pack configuration |
