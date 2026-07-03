# Migration Guide — agentic-harness

> How to adopt agentic-harness incrementally from your existing AI workflow setup.

---

## Incremental Adoption Path

Don't throw away your existing setup. Adopt one layer at a time:

| Phase | What you get | Time investment |
|-------|-------------|----------------|
| Phase 1: Knowledge only | Persistent AI memory across sessions | 10 minutes |
| Phase 2: Context switching | Pack-based project context loading | 20 minutes |
| Phase 3: Guardrails | Persona-based behavioral constraints | 15 minutes |
| Phase 4: Automation | Loop engineering and background jobs | 30 minutes |

---

<!-- markdownlint-disable MD024 -->
## Phase 1: Knowledge Only

### What you keep

Your existing shell setup, Cursor rules, Copilot instructions, Claude Code projects — everything stays as-is.

### What you add

```bash

# Clone the harness
git clone https://github.com/ulises-jeremias/agentic-harness ~/.ai-workspace

# Initialize
cd ~/.ai-workspace && bash scripts/workspace-init.sh

```

Now the AI has persistent memory via `assistant-memory`. Start your AI session with:

```text

Run assistant-memory inject and use the output as context.

```

The AI will now remember patterns, preferences, and todos across sessions.

### Verification

```bash

# Save your first learning
./bin/assistant-memory add --type learning "We use Conventional Commits: feat:, fix:, docs:, chore:"

# Start a new session — the AI should recall this
./bin/assistant-memory inject

```

---

## Phase 2: Context Switching

### What you migrate

Create packs for your active projects instead of manually telling the AI about each repo:

**Before** (manual context):

```text

I'm working on the acme-corp/backend repo. It's a Python FastAPI project.
The Jira project key is ACME. We deploy to AWS via GitHub Actions.

```

**After** (pack-based context):

```bash

workspace-context load --pack packs/acme-corp.yaml
# AI automatically knows repos, conventions, Jira key, deploy details

```

### Creating your first pack

Copy the template and fill in your project details:

```bash

cp packs/example-client.yaml packs/acme-corp.yaml

```

```yaml

name: acme-corp
repos:

  - name: backend
    url: https://github.com/acme-corp/backend

  - name: frontend
    url: https://github.com/acme-corp/frontend
conventions:
  commits: conventional-commits
  branch: feat/JIRA-123-description
  testing: pytest with fixtures from conftest.py
tools:
  ticketing: jira
  jira_project: ACME
llm:
  allowlist:

    - anthropic

```

---

## Phase 3: Guardrails

### What you migrate

If you currently use instructions like:

```text

Just review the code, don't make changes.
Let me approve before you implement anything.
Research only today — no file writes.

```

Replace them with personas:

```bash

# Instead of "just review, don't change"
workspace-context load --persona reviewer

# Instead of "research only"
workspace-context load --persona researcher

# Instead of "let me approve first"
workspace-context load --persona architect

```

### From Cursor rules

If you have `.cursor/rules/` files like:

```text

Always use TypeScript strict mode
Never use any
Prefer composition over inheritance

```

Move these to a pack under `conventions:` instead of scattered rules files.

### From Copilot instructions

If you have `.github/copilot-instructions.md`, the harness already provides a symlink to AGENTS.md. Your project-specific instructions should live in the pack, not in a global file.

---

## Phase 4: Automation

### What you migrate

If you manually run these commands regularly:

```bash

# Manually every morning:
gh issue list --state open --assignee @me

# Manually every few hours:
gh pr list --state open --search "review:required"

# Manually after CI fails:
gh run list --status failure --branch main

```

Replace with loops:

```bash

# Auto-scan issues every morning
bin/loop init daily-triage --template daily-triage --tier 1
bin/loop schedule daily-triage

# Auto-check PRs every 4 hours
bin/loop init pr-babysitter --template pr-babysitter --tier 2
bin/loop schedule pr-babysitter

# Auto-detect CI failures every hour
bin/loop init ci-sweeper --template ci-sweeper --tier 3
bin/loop schedule ci-sweeper

```

---

## Migration Paths by Starting Point

### From vanilla chezmoi

If you use chezmoi for dotfiles:

1. Keep your chezmoi repo as-is
2. Install agentic-harness alongside (separate directory)
3. Optionally: replace chezmoi with agentic-workstation for AI-native features

**Conflicts to watch**: `.gitconfig`, `.zshrc`, `.bashrc` — the harness doesn't manage dotfiles, so no conflicts.

### From Claude Code projects

If you have Claude Code `.claude/projects/`:

1. Each project becomes a pack: `packs/project-name.yaml`
2. Project-specific instructions move to pack `conventions:`
3. `CLAUDE.md` stays as the global routing table

### From Cursor rules

If you have `.cursor/rules/`:

1. Generic rules become personas: `personas/implementer.md`, `personas/reviewer.md`
2. Project-specific rules become pack conventions
3. `.cursor/rules/` can be deleted or kept as fallback

### From GitHub Copilot

If you use `.github/copilot-instructions.md`:

1. The harness symlinks this to AGENTS.md
2. Move project-specific instructions to packs
3. Keep global conventions in AGENTS.md

### From manual prompting

If you type context manually every session:

1. Phase 1: Save repeated context as knowledge entries
2. Phase 2: Create packs for projects
3. Phase 3: Define personas for work modes
4. Phase 4: Automate recurring tasks with loops

---

## Known Breaking Changes

### Pack schema changes

If upgrading from v0.1: pack format changed. See `schemas/pack.schema.json` for current format.

### CLI renames

Old harness (< v0.3) used different CLI names:

- `bin/memory` -> `bin/assistant-memory`
- `bin/context` -> `bin/workspace-context`
- `bin/queue` -> `bin/devcompanion`

### Repository rename

The harness was renamed from `ai-workspace` to `agentic-harness`. If your scripts reference the old name, update them.

---

## Rollback Plan

### If you want to go back

1. Remove the harness directory: `rm -rf ~/.ai-workspace`
2. Remove scheduled loops: `bin/loop schedule --list | xargs bin/loop schedule --remove`
3. Your original setup (Cursor rules, Copilot instructions, Claude projects) is untouched

### If you want to keep some parts

- **Keep knowledge only**: Delete loop dirs, keep knowledge/ and packs/
- **Keep context only**: Delete bin/loop, keep everything else
- **Keep everything but loops**: Don't schedule loops, use harness interactively

<!-- markdownlint-enable MD024 -->
