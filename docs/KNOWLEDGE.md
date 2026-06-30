# Knowledge API

The `assistant-memory` CLI provides a stable write API for syncing discoveries, patterns, learnings, and todos to the knowledge base.

## Adding entries

```bash
assistant-memory add --type <type> [--from-skill <name>] [--tags a,b,c] <content>
```

### Parameters

| Flag | Required | Description |
|------|----------|-------------|
| `--type` | Yes | Entry type: `skill`, `process`, `learning`, `todo` |
| `--from-skill` | No | Origin skill name for cross-repo traceability |
| `--tags` | No | Comma-separated tags (applied to frontmatter for skill entries) |
| `content` | Yes | Free-text entry content |

### Behaviors by type

| Type | Target file | Format |
|------|-------------|--------|
| `skill` | `knowledge/skills/discovered.md` | Markdown section with optional YAML frontmatter (`created`, `source_skill`, `tags`) |
| `process` | `knowledge/processes/general.md` | Table row with Date, What, Notes (source if --from-skill) |
| `learning` | `knowledge/learnings/general.md` | Table row with Date, Learning, Context (skill name if --from-skill) |
| `todo` | `knowledge/todos/pending.md` | Checklist item with optional `(from <skill>)` suffix |

## Examples

```bash
# Simple learning
assistant-memory add --type learning "Always verify test coverage before merging"

# Skill discovery with origin tracking
assistant-memory add --type skill --from-skill my-skill --tags jira,workflow "Custom workflow for issue triage"

# Process pattern from a skill
assistant-memory add --type process --from-skill my-skill "Use feature branches for all changes"

# Todo with traceability
assistant-memory add --type todo --from-skill my-skill "Investigate slow query in reports endpoint"
```

## Searching

```bash
assistant-memory search <query> [--tag T] [--project P] [--since YYYY-MM-DD]
assistant-memory search --tag my-skill
assistant-memory search --since 2026-01-01
```

## Version negotiation

Skills using `--from-skill` should check that `assistant-memory` supports the flag:

```bash
assistant-memory add --type learning --from-skill test "probe" >/dev/null 2>&1 && echo "API available"
```

If `--from-skill` is not supported (older version), fall back to the plain `add` without flags.
