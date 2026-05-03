# Contributing to AI Workspace

> How to contribute knowledge, tools, and patterns back to your team or the community.

---

## Philosophy

This workspace is **personal**, but its knowledge artifacts can be **shared assets**. When you discover something valuable — a new pattern, a useful process, an improved CLI — consider extracting it for others.

---

## What to Contribute

### Knowledge Artifacts

- Process documentation (tool workflows, integration patterns)
- Tool integration guides
- Training materials and how-to guides

### CLI Tools

- Scripts in `bin/` that could help others
- Improvements to existing tools

### Documentation

- Setup guides
- Workflow documentation
- Troubleshooting tips

---

## Contribution Workflow

### 1. Document Locally First

When you discover something valuable:

```bash
# Add to knowledge base
./bin/assistant-memory add --type learning "New pattern: ..."
```

### 2. Prepare the Artifact

Create the artifact in the appropriate location:

```text
knowledge/
├── processes/
│   └── jira/
│       └── spaces/
│           └── new-client.md    # New JIRA project documented
├── skills/
│   └── discovered.md            # New skill added
```

### 3. Create PR

```bash
# Create feature branch
git checkout -b feat/add-new-pattern

# Commit with clear message
git commit -m "docs: add pattern documentation for X

- What was discovered
- When to use it
- Example

Use case: Needed to track tasks for new project.
Detected via: Discovery during project onboarding."
```

### 4. PR Template

```markdown
## Summary

Brief description of the contribution.

## What Changed

- Knowledge artifact added
- Documentation updated
- CLI tools added/improved

## Use Case

Why is this valuable? When would someone use this?

## Discovery Context

How was this discovered? What triggered the finding?

## Testing

- [ ] Knowledge base search works
- [ ] CLI tools functional
- [ ] Documentation accurate
```

---

## Extracting Patterns Upstream

Some patterns are better suited for upstream repos (workstation config, shared skills registries, etc.):

| Pattern Type | Target |
|-------------|--------|
| Dotfiles, shell config | Your workstation config repo |
| AI workspace orchestrator | This repo (fork or PR) |
| Skill definitions | Your skills registry |
| General patterns | Shared team knowledge base |

### Example: Dotfiles Discovery

If you discover a useful shell alias during work:

1. Add to local dotfiles (chezmoi or similar)
2. If pattern is reusable → PR to your workstation config
3. Document in workspace knowledge if useful for AI sessions

---

## Knowledge Extraction Checklist

Before creating a PR, verify:

- [ ] Artifact is complete (not placeholder)
- [ ] Paths are verified
- [ ] Documentation is accurate
- [ ] Use case is clear
- [ ] Discovery context is included
- [ ] No secrets/tokens included

---

## Questions?

- Open an issue for discussion
- Ask in your team's communication channel
- Tag relevant people in the PR
