# The Complete Stack — agentic-workstation + agentic-harness

> Integrated tutorial: how all 3 layers of the Personal DX Stack work together.

**Time**: ~2.5 hours | **Prerequisites**: None — starts from zero

---

## The 3-Layer Architecture

| Layer | Repository | What it provides |
|-------|-----------|-----------------|
| L1 — Infrastructure | **agentic-workstation** | Skills, agents, MCP templates, CLI helpers, dotfiles |
| L2 — Runtime | **agentic-harness** | Memory, personas, packs, loops, job queues |
| L3 — Application | Your project repo | AGENTS.md with project-specific routing |

You can use L1 alone (skills without memory). You can use L2 alone (memory without skills). Together, they form a complete AI-native development workflow.

---

## Part 1: Setup the Foundation (30 min)

### Install the workstation (L1)

Skills-only (fastest):

```bash
curl -fsSL https://github.com/ulises-jeremias/agentic-workstation/releases/latest/download/install-skills.sh | bash
```

Or full workstation with dotfiles:

```bash
chezmoi init --apply ulises-jeremias/agentic-workstation
```

Verify:

```bash
dots-doctor
```

```text
Skills: 52 bundled
Agents: 13 configured
MCP templates: 6
CLI tools: dots-doctor, dots-skills, dots-devcompanion, dots-mcp, dots-loop
```

### Clone the harness (L2)

```bash
git clone https://github.com/ulises-jeremias/agentic-harness ~/.ai-workspace
cd ~/.ai-workspace
bash scripts/workspace-init.sh
```

Verify:

```bash
./bin/workspace-context
```

```text
=== Workspace Context Snapshot ===
Harness dir: /home/you/.ai-workspace
Workstation skills: detected (52 skills)
Knowledge entries: 0
Active packs: none
```

Both layers are connected — the harness discovers the workstation's skills automatically.

---

## Part 2: Configure Your First Project (20 min)

### Create the project

```bash
mkdir ~/projects/hello-stack
cd ~/projects/hello-stack
git init
cat > hello.py << 'EOF'
"""Hello Stack — demo project for the complete agentic stack."""
import argparse

def main():
    parser = argparse.ArgumentParser(description="Hello Stack CLI")
    parser.add_argument("--name", default="World", help="Name to greet")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
EOF
git add . && git commit -m "feat: initial hello-stack project"
```

### Add AGENTS.md (L3)

Create `AGENTS.md` in the project root:

```markdown
# AGENTS.md — hello-stack

## Routing

| Task | Delegate to |
|------|------------|
| Jira tasks | jira-assistant skill |
| Planning | planner subagent |
| Implementation | implementer subagent |
| Code review | code-reviewer subagent |
| PR creation | github-cli-workflow skill |

## Conventions

- Python 3.12+
- Conventional Commits: feat:, fix:, docs:, chore:
- pytest for testing
- argparse for CLI
```

### Link the project to the harness

```bash
cd ~/.ai-workspace
./bin/project-indexer link ~/projects/hello-stack hello-stack
```

### Create a pack

`~/.ai-workspace/packs/hello-stack.yaml`:

```yaml
name: hello-stack
repos:
  - path: projects/hello-stack
    primary: true
conventions:
  commits: conventional-commits
  language: python
  framework: argparse
  testing: pytest
```

---

## Part 3: End-to-End Task (45 min)

### Start your AI session

```bash
cd ~/.ai-workspace
./bin/workspace-context load --pack packs/hello-stack.yaml
claude  # or opencode / cursor
```

```text
[AI reads AGENTS.md]
Workspace context loaded: hello-stack
Skills available: 52 (jira-assistant, github-cli-workflow, planner, implementer, code-reviewer, ...)
Knowledge: 0 entries (new workspace)
```

### Find work to do

```text
Check if there are any GitHub issues on the hello-stack project.
```

The AI uses the **project-indexer** to find the repo, then `gh issue list`:

```text
No open issues. Let's create one: "Add --greeting flag to customize the greeting".
```

### Plan the feature

```text
Delegate to the planner subagent for this feature.
```

The **planner** (from workstation) produces a plan using the project's conventions (from the harness pack).

### Implement

```text
Implement the plan. Delegate to implementer.
```

The **implementer** subagent:
1. Reads project conventions from the pack
2. Creates branch: `feat/add-greeting-flag`
3. Writes code following Python patterns
4. Commits with Conventional Commits format

### Review

```text
Review the changes. Delegate to code-reviewer.
```

The **code-reviewer** subagent checks:
- Code quality and conventions
- Test coverage
- Security (via security-reviewer if needed)

### Create PR

```text
Push and create a PR. Use github-cli-workflow.
```

The **github-cli-workflow** skill creates a well-formatted PR with:
- Conventional Commits title
- What/Why/Changes/Testing sections
- Link to the issue

---

## Part 4: Automate with Loops (30 min)

Now that manual workflow works, automate recurring tasks.

### Create a daily triage loop

```bash
cd ~/.ai-workspace
./bin/loop init daily-triage --template daily-triage --tier 1
```

Edit `loops/daily-triage/LOOP.md` to point at hello-stack:

```yaml
request: |
  Scan hello-stack for open issues. Write a report.
```

Run it:

```bash
./bin/loop run daily-triage
```

```text
[L1 - OBSERVE ONLY]
Issues found: 1 (ACME-456 — in progress)
Report saved: loops/daily-triage/report.md
```

### Schedule it

```bash
./bin/loop schedule daily-triage
```

```text
Next run: tomorrow 09:00
```

---

## Part 5: Cross-Session Memory (15 min)

### Session 1: Save learnings

```bash
./bin/assistant-memory add --type learning "hello-stack uses argparse with ArgumentDefaultsHelpFormatter"
./bin/assistant-memory add --type process "hello-stack workflow: planner → implementer → code-reviewer → github-cli-workflow"
./bin/assistant-memory add --type todo "Add CI workflow for hello-stack tests"
```

### Session 2: AI remembers

```bash
cd ~/.ai-workspace
./bin/assistant-memory inject
claude
```

```text
Previous session learnings:
- hello-stack uses argparse with ArgumentDefaultsHelpFormatter
- hello-stack workflow: planner → implementer → code-reviewer → github-cli-workflow
- Pending: Add CI workflow for hello-stack tests

What would you like to work on?
```

The AI remembers everything from yesterday. No repetition needed.

---

## What You Built

```text
agentic-workstation (L1)          agentic-harness (L2)          hello-stack (L3)
┌─────────────────────┐          ┌─────────────────────┐       ┌──────────────────┐
│ 52 skills            │          │ knowledge/           │       │ AGENTS.md        │
│ 13 sub-agents        │──────────│ packs/hello-stack    │───────│ hello.py         │
│ 6 MCP templates      │  skills  │ personas/            │  ctx  │ tests/           │
│ dots-* CLI           │  agents  │ loops/daily-triage   │       │ .github/         │
└─────────────────────┘          │ bin/assistant-memory  │       └──────────────────┘
                                  │ bin/workspace-context │
                                  │ bin/devcompanion      │
                                  └─────────────────────┘
```

### Layer interaction

| Action | L1 provides | L2 provides | L3 consumes |
|--------|------------|------------|------------|
| Plan feature | planner subagent | Pack conventions | AGENTS.md routing |
| Implement | implementer subagent | Knowledge patterns | Source code |
| Review | code-reviewer subagent | Persona guardrails | PR diff |
| Create PR | github-cli-workflow | Pack config (repo URL) | Branch + commits |
| Daily triage | jira-assistant skill | Loop scheduler | Issues |
| Next session | (skills persist) | Memory injection | Current task |

---

## Related

- [Day in the Life](DAY_IN_THE_LIFE.md) — workstation-only workflow walkthrough
- [Your First PR](https://github.com/ulises-jeremias/agentic-harness/blob/main/docs/tutorials/FIRST_PR.md) — harness-specific first PR
- [Loop Creation Workshop](https://github.com/ulises-jeremias/agentic-harness/blob/main/docs/tutorials/LOOP_WORKSHOP/README.md) — build autonomous loops
- [Multi-Client Setup](https://github.com/ulises-jeremias/agentic-harness/blob/main/docs/tutorials/MULTI_CLIENT_SETUP.md) — manage multiple clients
