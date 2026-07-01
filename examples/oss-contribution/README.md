# Example: Knowledge-Driven OSS Contribution

> A one-shot OSS contribution workflow using persona + knowledge base.

## What it does

Using the `oss-contrib` profile:

1. Activates the `implementer` persona
2. Loads the `oss-contrib` skill set
3. Searches the knowledge base for relevant patterns before starting

## Setup

```bash
cd ~/.agentic-harness

# 1. Index the OSS repo you want to contribute to
./bin/project-indexer clone owner/some-oss-project

# 2. Load the OSS contribution profile
#    (creates profiles/oss-contrib.yaml if it doesn't exist)
cat profiles/oss-contrib.yaml   # review the profile

./bin/workspace-context load --profile oss-contrib

# 3. Search knowledge for anything we already know
./bin/assistant-memory search --tag oss "fork workflow"

# 4. Open your AI tool — implementer persona is already active
opencode   # or: claude / cursor / gemini

# 5. The AI knows to:
#    - Fork the repo
#    - Create a feature branch
#    - Implement, test, and open a draft PR
#    - Never merge directly
```

## Profile used

See `profile.yaml` — a copy of `profiles/oss-contrib.yaml`.

## Knowledge snippets

After your first contribution, save what you learned:

```bash
./bin/assistant-memory add --type learning "OSS project X uses pnpm, not npm"
./bin/assistant-memory add --type process "Always run their pre-commit before opening a PR"
```

Next time, the AI already knows.
