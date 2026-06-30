---
type: process
updated: 2026-06-30
scopes: [clickup]
confidence: medium
---

# ClickUp Patterns

> Your ClickUp setup and common patterns.

**Note**: This file is populated as we learn about your ClickUp usage. Update as we discover new patterns.

---

## Setup

<!-- Fill in when you provide info -->

### Connection
- **Tool**: `clickup-cli` skill (via opencode/claude skill pack)
- **Workspace ID**: <!-- your workspace ID -->
- **My User ID**: <!-- your user ID -->
- **CLI config**: `~/.config/clickup/config.yml`

### Organization
- **Spaces**: <!-- list your spaces -->
- **Common Lists**: <!-- list frequently-used list IDs -->

---

## Quick Reference

<!-- Populate with your space/list IDs as you discover them -->

| Space | ID |
|-------|----|
| <!-- Space Name --> | <!-- ID --> |

---

## Common Patterns

### Task Operations

```bash
# List tasks in a space
clickup task list --space-id <SPACE_ID>

# Create a task
clickup task create --list-id <LIST_ID> --name "Task title" --description "Details"

# Update task status
clickup task update <TASK_ID> --status "In Progress"

# Add a comment
clickup comment add <TASK_ID> --text "Comment text"
```

### Key ID Formats

- Workspace ID: numeric (e.g., `123456`)
- Space ID: numeric (e.g., `9876543`)
- List ID: numeric (e.g., `901700012345`)
- Task ID: alphanumeric (e.g., `abc123def`)

---

## User Preferences

- **Language**: English for task titles/descriptions
- **Workflow**: <!-- describe your typical workflow -->

---

## Notes

<!-- Add notes as you learn -->

---

## History

| Date | What Learned |
|------|--------------|
|      |              |
