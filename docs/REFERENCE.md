# CLI Reference

> Auto-generated from `bin/*` `--help` output.
> Run `bash scripts/generate-reference.sh` to regenerate.

---

## `assistant-memory`

```text

assistant-memory — Manage assistant knowledge base

Usage:
  assistant-memory add --type <type> <content>   Add new entry
  assistant-memory search <query>                Search knowledge base
  assistant-memory list [type]                   List entries by type
  assistant-memory todo                          Show pending todos
  assistant-memory review                        Review key items (session start)
  assistant-memory inject                        Output context block for injection
  assistant-memory help                          Show this help

Types for add:
  skill      New skill or tool discovery
  process    Process pattern (workflow, tool usage)
  learning   General session learning
  todo       Pending item to follow up

Examples:
  assistant-memory add --type learning "Always run tests before committing"
  assistant-memory add --type todo "Investigate slow query in reports endpoint"
  assistant-memory search "deploy"
  assistant-memory list
  assistant-memory inject   # paste output at start of session

```

## `devcompanion`

```text

devcompanion — standalone background job queue for AI Workspace

Usage:
  devcompanion queue <project> [options]   Queue a job for an indexed project
  devcompanion run-once [--no-llm]         Run oldest pending job
  devcompanion status                      Show queue state and indexed projects
  devcompanion sync-todos                  Regenerate knowledge/todos/pending.md from queue
  devcompanion done <job-id>               Move a job to done
  devcompanion templates                   List available job templates
  devcompanion projects                    List indexed projects
  devcompanion help                        Show this help

queue options:
  --template <name>    Use a predefined job template
  --request "..."      Custom request (required if no --template)
  --id <id>            Custom job ID (default: <project>-<timestamp>)
  --no-llm             Skip LLM, generate skeleton plan only

Queue path:
  /home/ulisesjcf/.local/share/ai-workspace/dev-companion/queue
  (override with AI_WORKSPACE_DC_HOME env var)

Examples:
  devcompanion queue my-api --template code-review
  devcompanion queue my-api --template investigate --request "slow response on /users"
  devcompanion queue my-api --request "add pagination to GET /users"
  devcompanion run-once
  devcompanion run-once --no-llm    # skeleton plan, no LLM needed
  devcompanion status
  devcompanion done my-api-20260406-120000

Workflow:
  1. devcompanion queue <project> --template <template>
  2. devcompanion run-once            (or: let a background worker pick it up)
  3. devcompanion done <job-id>

Docs:
  docs/DEVCOMPANION.md

```

## `project-indexer`

```text
project-indexer - Simple clone + symlink manager

Usage:
  project-indexer init               # Initialize workspace directories
  project-indexer clone <org/repo>  # Clone repo + create symlink
  project-indexer add <path>       # Add symlink for existing repo
  project-indexer remove <repo>     # Remove symlink (keeps repo)
  project-indexer list              # List all symlinks
  project-indexer scan              # Scan repos and symlinks
  project-indexer help             # Show this help

Examples:
  project-indexer init
  project-indexer clone owner/my-project
  project-indexer clone owner/my-other-project
  project-indexer list

Notes:
  - No aliases - symlinks use the repo name directly
  - ./repos/ and ./projects/ are gitignored
```

## `workspace-context`

```text
workspace-context — AI Workspace session state snapshot

Usage:
  workspace-context                         Print session context snapshot
  workspace-context snapshot                Same as above
  workspace-context load packs/<pack>.yaml  Load a context pack
  workspace-context personas                List available personas
  workspace-context use-persona <name>      Activate a persona

Examples:
  workspace-context
  workspace-context load packs/my-client.yaml
  workspace-context use-persona reviewer
```
