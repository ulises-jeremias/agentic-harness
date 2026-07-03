# Your First PR with agentic-harness

> Complete end-to-end tutorial: from zero to a merged PR using agentic-harness.

**Time to complete**: ~45 minutes
**Prerequisites**: Git, an AI coding tool (Claude Code, opencode, or Cursor), a GitHub account

---

## What You'll Build

By the end of this tutorial, you'll have:

1. A working agentic-harness instance with persistent memory
2. A pack configured for a sample project
3. A persona constraining the AI to your chosen work mode
4. A completed feature PR created with skill delegation
5. Knowledge saved for future sessions

---

## Session 1: Setup (15 minutes)

### Step 1: Clone and initialize the harness

```bash
git clone https://github.com/ulises-jeremias/agentic-harness ~/.ai-workspace
cd ~/.ai-workspace
bash scripts/workspace-init.sh
```

Expected output:

```text
=== agentic-harness workspace init ===
✓ Directory structure created
✓ .workspace.yaml created
✓ Symlinks verified (CLAUDE.md, GEMINI.md, copilot-instructions.md)
✓ Ready — start your AI session with AGENTS.md
```

### Step 2: Verify the harness works

```bash
./bin/workspace-context
```

You should see a snapshot with:

```text
=== Workspace Context Snapshot ===
Harness dir: /home/you/.ai-workspace
Knowledge entries: 0
Active packs: none
Active persona: none
Loaded skills: (none)
```

### Step 3: Choose your AI tool

| Tool | How to start |
|------|-------------|
| Claude Code | `claude` in the harness directory |
| opencode | `opencode` in the harness directory |
| Cursor | Open the harness directory in Cursor |

Start your AI tool now. The AI will read `AGENTS.md` and understand the harness routing table.

> [!TIP]
> Tell the AI: "Load workspace context and prime with assistant-memory inject"

---

## Session 2: Configure Your Project (10 minutes)

### Step 4: Create a sample project

For this tutorial, we'll create a tiny CLI tool. If you already have a project, skip to Step 5.

```bash
mkdir -p ~/projects/hello-harness
cd ~/projects/hello-harness
git init
echo 'print("Hello from agentic-harness!")' > hello.py
git add . && git commit -m "feat: initial hello-harness project"
```

Push to GitHub (or keep local — we'll use it as-is for the tutorial).

### Step 5: Create a pack for your project

```bash
cp packs/example-client.yaml packs/hello-harness.yaml
```

Edit `packs/hello-harness.yaml`:

```yaml
name: hello-harness
repos:
  - name: hello-harness
    url: ~/projects/hello-harness
    primary: true
conventions:
  commits: conventional-commits
  branch: feat/short-description
  language: python
  testing: "run with: python hello.py"
```

### Step 6: Load the pack

```bash
./bin/workspace-context load --pack packs/hello-harness.yaml
```

Now tell your AI: "Load this pack context and tell me what you know about the hello-harness project."

The AI should respond with the repos, conventions, and language from your pack.

### Step 7: Choose a persona

For implementation work, use the implementer persona:

```bash
./bin/workspace-context load --persona implementer
```

Or tell your AI: "Switch to implementer persona. We're going to add a feature."

---

## Session 3: Implement a Feature (20 minutes)

### Step 8: Plan the feature

Tell your AI:

```text
I want to add a --name flag to hello.py that prints "Hello, <name>!".
Plan the implementation before writing code.
```

The AI should respond with a plan. If you have agentic-workstation skills installed, tell it:

```text
Delegate to the planner subagent for this feature.
```

### Step 9: Implement

After reviewing the plan, tell the AI:

```text
Implement the plan. Create a branch feat/add-name-flag, make the changes, and commit.
```

The AI should:

1. Create a branch: `git checkout -b feat/add-name-flag`
2. Edit `hello.py` to add argparse with a `--name` flag
3. Commit with a Conventional Commits message: `feat: add --name flag to hello.py`

### Step 10: Review your own work

Tell the AI:

```text
Review the changes. Use the code-reviewer subagent if available.
```

The AI should review the code and suggest improvements. Apply any meaningful suggestions.

### Step 11: Push and create a PR

If you're using GitHub:

```bash
git push origin feat/add-name-flag
```

Tell your AI:

```text
Create a pull request for this branch with a description of the changes.
Use the github-cli-workflow skill if available.
```

---

## Session 4: Save Knowledge (5 minutes)

### Step 12: Save what you learned

After the PR is created, save the patterns you discovered:

```bash
./bin/assistant-memory add --type learning "hello-harness uses argparse for CLI flags"
./bin/assistant-memory add --type learning "PR titles should follow feat: <description> format"
./bin/assistant-memory add --type process "Feature workflow: plan -> implement -> review -> PR"
```

### Step 13: Start a new session

Close your AI tool and start a new session. Tell the AI:

```text
Run assistant-memory inject and workspace-context. What do you know about my projects?
```

The AI should recall:

- The hello-harness project and its conventions
- The argparse pattern you used
- Your preferred PR workflow

### Step 14: Queue a background review (optional)

If you have agentic-workstation's dev companion:

```bash
./bin/devcompanion queue hello-harness --template code-review
./bin/devcompanion run-once
```

This runs an automated code review in the background and produces a review report.

---

## What's Next?

You've completed the core workflow. Here's what to explore next:

| Want to... | Try this |
|-----------|---------|
| Automate recurring tasks | [Loop Creation Workshop](LOOPS.md) — start with Tier 1 |
| Work with multiple clients | [Multi-Client Setup Tutorial](tutorials/MULTI_CLIENT_SETUP.md) |
| Switch between work modes | [Personas Guide](PERSONAS.md) — try reviewer and architect |
| Use with other AI tools | [Tool-Specific Quick Starts](quickstarts/) |
| Deepen your knowledge base | [Knowledge API Reference](KNOWLEDGE.md) |

---

## Troubleshooting

### "AGENTS.md not found"

Make sure you're running your AI tool from the harness directory (`~/.ai-workspace`). AGENTS.md must be in the current working directory.

### "workspace-context command not found"

Run `bash scripts/workspace-init.sh` again — it adds `bin/` to your PATH for the current session.

### "Pack validation failed"

Check your pack YAML syntax:

```bash
python3 -c "import yaml; yaml.safe_load(open('packs/hello-harness.yaml'))"
```

### "AI doesn't remember from last session"

Make sure you ran `assistant-memory add` (not just thought about it). Check what's stored:

```bash
./bin/assistant-memory search "hello"
```

### "Persona restrictions are too strict"

If you're stuck because the persona blocks an action you need:

```bash
./bin/workspace-context load --persona implementer  # or just don't load a persona
```
