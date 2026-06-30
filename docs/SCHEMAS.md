# Context Schemas

> JSON Schemas for every context surface in the AI Workspace.
> All schemas live in `schemas/` and are validated automatically in CI.

---

## Validate locally

```bash
# Validate everything
./bin/workspace-context validate

# Validate one surface
./bin/workspace-context validate packs
./bin/workspace-context validate jobs
./bin/workspace-context validate personas
```

---

## Pack schema

**File**: `schemas/pack.schema.json`
**Validates**: `packs/*.yaml`

Required fields: `name`, `description`.

```yaml
# packs/my-project.yaml
name: my-project
description: Context for the Acme API project

repos:
  - name: acme-api
    path: projects/acme-api
    stack: Python / FastAPI
    role: backend

process_docs:
  - knowledge/processes/general.md

ids:
  jira_project: "ACME"
  slack_channel: "#acme-dev"

conventions:
  branch_pattern: "feat/<ticket>-<description>"
  commit_format: conventional
  pr_target: main

ai:
  delivery_skill: workflow-generic-project
  discovery_skill: dev-assistant
  language: english
```

---

## Job template schema

**File**: `schemas/job.schema.json`
**Validates**: `templates/jobs/*.yaml`

Required fields: `name`, `description`, `request`.

```yaml
# templates/jobs/my-task.yaml
name: my-task
description: "One-line summary"
request: |
  Detailed task prompt for the runner.

# Optional
inputs:
  - name: ANTHROPIC_API_KEY
    type: env
    required: true

outputs:
  - name: plan.md
    type: file
    required: true

exit_criteria: [goal_met, budget_exhausted]
max_cost:
  tokens: 50000
```

---

## Persona frontmatter schema

**File**: `schemas/persona-frontmatter.schema.json`
**Validates**: YAML frontmatter in `personas/*.md`

Required fields: `name`.

```markdown
---
name: implementer
allow: [read, write, commit, run_commands, create_pr]
deny: [design]
output_format: code
handoffs:
  - when: "task requires architectural decisions"
    to: architect
---

# Implementer Persona
...
```

### Allowed action types

| Action | Meaning |
|--------|---------|
| `read` | Read files and run read-only commands |
| `write` | Create or modify files |
| `commit` | Make git commits |
| `run_commands` | Execute shell commands |
| `create_pr` | Open pull requests |
| `design` | Produce design docs and ADRs |
| `document` | Write documentation |
| `review` | Review code and provide feedback |
| `deploy` | Trigger deployments |

### Output formats

| Format | Persona use case |
|--------|-----------------|
| `code` | implementer |
| `review` | reviewer |
| `design` | architect |
| `prose` | researcher, writer |
| `mixed` | general-purpose |

---

## Adding new schemas

1. Write the schema in `schemas/<name>.schema.json`.
2. Add a `run_<surface>` function in `scripts/validate-context.sh`.
3. Call it in the `all` case.
4. Update this document.
