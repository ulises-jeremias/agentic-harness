# devcompanion — Operational Guide

`bin/devcompanion` is a standalone Python CLI that manages a background job queue
for your AI Workspace. It resolves project paths, queues jobs, runs them (with or
without an LLM), and keeps `knowledge/todos/pending.md` in sync.

---

## Architecture

```text
bin/devcompanion  (standalone Python CLI)
       │
       ├─ reads    projects/              → resolves project name → repo path
       ├─ reads    templates/jobs/        → job templates
       ├─ writes   ~/.local/share/agentic-harness/dev-companion/queue/
       │           ├── pending/           ← jobs waiting to run
       │           ├── processing/        ← job currently running
       │           ├── done/              ← completed jobs
       │           ├── failed/            ← failed jobs
       │           └── artifacts/<id>/    ← plan.md + result.json
       └─ writes   knowledge/todos/pending.md   ← auto-generated
```

**Queue home** defaults to `~/.local/share/agentic-harness/dev-companion/`.
Override with `HARNESS_DC_HOME` env var.

**Runner** — `run-once` uses a built-in skeleton runner by default.
If `HARNESS_RUNNER_DIR` is set and points to a directory containing a
`runner` module with a `main()` entry point, it will be used for full
LLM-powered execution.

> [!IMPORTANT]
> When the workstation baseline is installed, set
> `HARNESS_RUNNER_DIR=$HOME/.local/share/agentic-workstation/dev-companion/runner`
> so this CLI delegates to the same runner that `dots-devcompanion run-once`
> uses. Otherwise the workspace falls back to the built-in skeleton even when
> the workstation provides full LLM support.

```bash
# One-time setup: align the workspace with the workstation runner.
export HARNESS_RUNNER_DIR="$HOME/.local/share/agentic-workstation/dev-companion/runner"
```

---

## When to use devcompanion vs interactive session

| Situation | Use |
|-----------|-----|
| Quick task, needs back-and-forth | Interactive AI session (default) |
| Long-running task, can run async | `devcompanion queue` |
| Task that blocks the current session | `devcompanion queue` |
| Batch of tasks for multiple projects | `devcompanion queue` (one per project) |

**Rule of thumb:** if you'd say "do this while I work on something else" — queue it.

---

## Core workflow

### 1. Queue a job

```bash
# Using a template
./bin/devcompanion queue <project> --template <template-name>

# Custom request
./bin/devcompanion queue <project> --request "describe what you want done"

# Template + extra context
./bin/devcompanion queue <project> --template refactor --request "focus on auth module"

# Skip LLM (skeleton plan only — no API key needed)
./bin/devcompanion queue <project> --template code-review --no-llm
```

### 2. Run the oldest pending job

```bash
# Uses LLM if available, skeleton otherwise
./bin/devcompanion run-once

# Force skeleton (no LLM)
./bin/devcompanion run-once --no-llm
```

Artifacts are written to:
`~/.local/share/agentic-harness/dev-companion/queue/artifacts/<job-id>/`

### 3. Check status

```bash
./bin/devcompanion status
```

Shows pending / processing / done / failed jobs and indexed projects.

### 4. Mark done

```bash
./bin/devcompanion done <job-id>
```

Moves the job to `done/` and refreshes `knowledge/todos/pending.md`.

### 5. Sync todos manually

```bash
./bin/devcompanion sync-todos
```

Regenerates `knowledge/todos/pending.md` from current queue state.

---

## Available templates

```bash
./bin/devcompanion templates
```

| Template | Description |
|----------|-------------|
| `code-review` | Full code review for quality, security, maintainability |
| `create-pr` | Push branch and create a draft PR with generated description |
| `refactor` | Scoped refactoring with tests and PR (requires --request for scope) |
| `investigate` | Root cause analysis or open-ended investigation |
| `fix-ci` | Investigate and fix failing CI checks |

### Adding a custom template

```bash
cat > templates/jobs/my-template.yaml << 'EOF'
name: my-template
description: "What this template does"

request: |
  Perform X on the repository. Steps:

  1. First do this
  2. Then do that
  3. Create a PR
EOF
```

---

## Auto-generated files

Do not edit these manually — they are regenerated on every `queue`, `done`, and `sync-todos` call.

| File | Generated from |
|------|---------------|
| `knowledge/todos/pending.md` | Queue state |
| `projects.yaml` | `projects/` symlinks |

---

## Examples

### Code review on a project

```bash
./bin/devcompanion queue my-project --template code-review
./bin/devcompanion run-once
```

### Investigate a bug

```bash
./bin/devcompanion queue my-api --template investigate \
  --request "GET /users returns 500 on empty database"
./bin/devcompanion run-once
```

### Custom one-off task

```bash
./bin/devcompanion queue my-api \
  --request "add pagination to GET /users endpoint, follow existing patterns"
./bin/devcompanion run-once
```

---

## LLM provider order and policy

When `dots_ai_devcompanion_runner` is available, it picks a provider through an
**explicit policy layer** (see
[`agentic-workstation/docs/DEV_COMPANION_LLM.md`](https://github.com/ulises-jeremias/agentic-workstation/blob/main/docs/DEV_COMPANION_LLM.md)).
By default the order is:

1. **opencode** (local, free)
2. **Ollama** (local, free)
3. **Anthropic** (cloud) — if `ANTHROPIC_API_KEY` is set
4. **OpenAI** (cloud) — if `OPENAI_API_KEY` is set
5. **Skeleton plan** — if nothing is allowed/available

> [!WARNING]
> For client engagements that mandate a single AI account (e.g. only their
> Anthropic key, only their OpenAI key, only OpenCode against their endpoint)
> you **must** lock the runner with the policy variables below before queuing
> jobs. Otherwise the runner will silently use OpenCode/big-pickle if
> available.

```bash
# Example: only Anthropic with the client's key, fail closed otherwise.
export ANTHROPIC_API_KEY="<from client secret store>"
export DOTS_AI_DEVCOMPANION_LLM_ALLOWLIST="anthropic"
export DOTS_AI_DEVCOMPANION_LLM_STRICT="1"

dots-devcompanion llm-status         # verify, never invokes the model
./bin/devcompanion run-once         # honors the same env vars
```

Per-job overrides go inside the `.job` file's `llm` block (subset only — a
job can never widen the global allowlist):

```json
"llm": {
  "enabled": true,
  "allowlist": ["anthropic"],
  "model": "claude-3-7-sonnet-latest",
  "strict": true
}
```

For Cursor/Copilot-only engagements there is no headless adapter today; use
`run-once --no-llm` (skeleton plan + IDE-driven execution). See
[`agentic-workstation/docs/DEV_COMPANION_LLM.md`](https://github.com/ulises-jeremias/agentic-workstation/blob/main/docs/DEV_COMPANION_LLM.md)
for the full reference.

---

## Environment variables

| Variable | Purpose |
|----------|---------|
| `HARNESS_DC_HOME` | Override queue home directory |
| `HARNESS_RUNNER_DIR` | Path to the workstation runner (set to `~/.local/share/agentic-workstation/dev-companion/runner` when both are installed) |
| `ANTHROPIC_API_KEY` | Enable Anthropic LLM provider |
| `OPENAI_API_KEY` | Enable OpenAI LLM provider |
| `DOTS_AI_DEVCOMPANION_LLM_ALLOWLIST` | Comma-separated providers allowed (ordered) |
| `DOTS_AI_DEVCOMPANION_LLM_DENYLIST` | Comma-separated providers always blocked |
| `DOTS_AI_DEVCOMPANION_LLM_PINNED_PROVIDER` | Force a single provider |
| `DOTS_AI_DEVCOMPANION_LLM_PINNED_MODEL` | Override the pinned provider's default model |
| `DOTS_AI_DEVCOMPANION_LLM_STRICT` | `1`/`true` → fail closed when no allowed provider is available |
| `DOTS_AI_DEVCOMPANION_LLM_CONFIG` | Override the policy file path (`~/.config/agentic-workstation/devcompanion-llm.json` by default) |

---

## Troubleshooting

### "Project not found"

```bash
./bin/devcompanion projects          # list indexed projects
./bin/project-indexer clone owner/repo   # add missing project
```

### "No pending jobs"

```bash
./bin/devcompanion status            # verify queue state
```

### "Template not found"

```bash
./bin/devcompanion templates         # list available templates
ls templates/jobs/                   # check template files
```
