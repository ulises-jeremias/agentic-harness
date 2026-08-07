# CLI Reference

> Auto-generated from `bin/*` `--help` output.
> Run `bash scripts/generate-reference.sh` to regenerate.

---

## `agent-toolkit memory`

```text

agent-toolkit memory — Manage assistant knowledge base

Usage:
  agent-toolkit memory add --type <type> [--from-skill <name>] [--tags a,b,c] <content>
                                                  Add new entry (with optional origin tracking)
   agent-toolkit memory search [--tag T] [--project P] [--since YYYY-MM-DD]
                    [--min-confidence low|med|high] [--semantic] <query>
                                                    Search knowledge base (with filters)
  agent-toolkit memory index build                              Build semantic index
  agent-toolkit memory list [type]                   List entries by type
  agent-toolkit memory todo                          Show pending todos
  agent-toolkit memory review                        Review key items (session start)
  agent-toolkit memory review --stale                Review stale entries (interactive batch)
  agent-toolkit memory review --stale --auto-renew   Auto-extend all stale entries by 1 year
  agent-toolkit memory review --stale --delete       Delete stale entries (use FORCE=1 to execute)
  agent-toolkit memory inject                        Output context block for injection
  agent-toolkit memory help                          Show this help

Types for add:
  skill      New skill or tool discovery
  process    Process pattern (workflow, tool usage)
  learning   General session learning
  todo       Pending item to follow up

Add flags:
  --from-skill <name>   Origin skill name (for cross-repo traceability)
  --tags a,b,c          Comma-separated tags (applied to frontmatter for skill type)

Examples:
  agent-toolkit memory add --type learning "Always run tests before committing"
  agent-toolkit memory add --type skill --from-skill dots-harness-knowledge-sync --tags jira,workflow "New workflow pattern"
  agent-toolkit memory add --type todo "Investigate slow query in reports endpoint"
  agent-toolkit memory search "deploy"
  agent-toolkit memory list
  agent-toolkit memory inject   # paste output at end of session

```

## `agent-toolkit devcompanion`

```text

agent-toolkit devcompanion — standalone background job queue for AI Workspace

Usage:
  agent-toolkit devcompanion queue <project> [options]   Queue a job for an indexed project
  agent-toolkit devcompanion run-once [--no-llm]         Run oldest pending job
  agent-toolkit devcompanion status                      Show queue state and indexed projects
  agent-toolkit devcompanion sync-todos                  Regenerate knowledge/todos/pending.md from queue
  agent-toolkit devcompanion done <job-id>               Move a job to done
  agent-toolkit devcompanion templates                   List available job templates
  agent-toolkit devcompanion projects                    List indexed projects
  agent-toolkit devcompanion help                        Show this help

queue options:
  --template <name>    Use a predefined job template
  --request "..."      Custom request (required if no --template)
  --id <id>            Custom job ID (default: <project>-<timestamp>)
  --no-llm             Skip LLM, generate skeleton plan only

Queue path:
  /home/ulisesjcf/.local/share/agentic-harness/dev-companion/queue
  (override with HARNESS_DC_HOME env var)

Examples:
  agent-toolkit devcompanion queue my-api --template code-review
  agent-toolkit devcompanion queue my-api --template investigate --request "slow response on /users"
  agent-toolkit devcompanion queue my-api --request "add pagination to GET /users"
  agent-toolkit devcompanion run-once
  agent-toolkit devcompanion run-once --no-llm    # skeleton plan, no LLM needed
  agent-toolkit devcompanion status
  agent-toolkit devcompanion done my-api-20260406-120000

Workflow:
  1. agent-toolkit devcompanion queue <project> --template <template>
  2. agent-toolkit devcompanion run-once            (or: let a background worker pick it up)
  3. agent-toolkit devcompanion done <job-id>

Docs:
  docs/DEVCOMPANION.md

```

## `agent-toolkit project`

```text
agent-toolkit project - Simple clone + symlink manager

Usage:
  agent-toolkit project init               # Initialize workspace directories
  agent-toolkit project clone <org/repo>  # Clone repo + create symlink
  agent-toolkit project add <path>       # Add symlink for existing repo
  agent-toolkit project remove <repo>     # Remove symlink (keeps repo)
  agent-toolkit project list              # List all symlinks
  agent-toolkit project scan              # Scan repos and symlinks
  agent-toolkit project help             # Show this help

Examples:
  agent-toolkit project init
  agent-toolkit project clone owner/my-project
  agent-toolkit project clone owner/my-other-project
  agent-toolkit project list

Notes:
  - No aliases - symlinks use the repo name directly
  - ./repos/ and ./projects/ are gitignored
```

## `agent-toolkit workspace`

```text
agent-toolkit workspace — AI Workspace session state snapshot

Usage:
  agent-toolkit workspace                         Print session context snapshot
  agent-toolkit workspace snapshot                Same as above
  agent-toolkit workspace load packs/<pack>.yaml  Load a context pack
  agent-toolkit workspace personas                List available personas
  agent-toolkit workspace use-persona <name>      Activate a persona

Examples:
  agent-toolkit workspace
  agent-toolkit workspace load packs/my-client.yaml
  agent-toolkit workspace use-persona reviewer
```
