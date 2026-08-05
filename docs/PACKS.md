# Packs

> Context bundles for switching between clients or projects.

---

## What are Packs?

A pack is a YAML file that bundles all the context the AI needs for a specific client or project:

- Which repos to work with
- Project-specific IDs (JIRA project, ClickUp space, etc.)
- Conventions (branch naming, commit format, deploy targets)
- Process docs to load
- AI behavior notes

Instead of re-explaining context every session, you load a pack.

---

## Usage

### Load a pack

```bash
agent-toolkit workspace load packs/my-client.yaml
```

This outputs the pack contents as context and marks it as the active pack (saved to `.active-pack`).

### See active pack

```bash
agent-toolkit workspace     # shows active pack in snapshot
```

### Deactivate

```bash
rm .active-pack
```

---

## Pack Structure

```yaml
name: my-client
description: Context pack for My Client project

# Repos to work with
repos:
  - name: my-api
    path: projects/my-api
    stack: Python / FastAPI

# Process docs to inject
process_docs:
  - knowledge/processes/jira.md

# Key IDs — so the AI doesn't have to ask
ids:
  jira_project: "PROJ"
  # slack_channel: "#my-client-dev"

# Git / PR conventions
conventions:
  branch_pattern: "feat/<ticket>-<description>"
  commit_format: conventional
  pr_target: main

# AI behavior overrides
ai:
  delivery_skill: workflow-generic-project
  language: english
  notes: |
    - Always check AGENTS.md before working on any repo
    - Draft PRs only, never merge directly
```

---

## Creating a Pack

1. Copy the example:

```bash
cp packs/example-client.yaml packs/my-client.yaml
```

1. Fill in your values:

```bash
vim packs/my-client.yaml
```

1. Load it:

```bash
agent-toolkit workspace load packs/my-client.yaml
```

---

## What goes in a Pack vs knowledge/

| Information type | Where |
|-----------------|-------|
| Project-specific IDs, repos, conventions | `packs/<client>.yaml` |
| General tool patterns (how JIRA works) | `knowledge/processes/jira.md` |
| Session learnings and corrections | `knowledge/learnings/` |
| Pending todos | `knowledge/todos/` |

Packs are **per-project context**. Knowledge is **general and cross-project**.

---

## Pack Naming

- Use lowercase with hyphens: `my-client.yaml`, `internal-tools.yaml`
- One pack per client or major project context
- Packs can be committed to git (no secrets) or gitignored (if they contain sensitive IDs)
