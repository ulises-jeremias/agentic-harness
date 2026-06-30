# Project Management

> Simple clone + symlink manager for the AI Workspace.

---

## Concept

No aliases — symlinks use the **repo name directly**.

```bash
# Clone a repo → symlink created automatically
./bin/project-indexer clone owner/my-project

# Navigate via symlink
cd projects/my-project
```

---

## Directory Structure

```text
ai-workspace/
├── repos/                            # Cloned repos (gitignored)
│   └── github.com/
│       └── owner/
│           └── my-project/
└── projects/                        # Symlinks (gitignored)
    └── my-project → ../repos/github.com/owner/my-project
```

---

## Commands

### Initialize

```bash
./bin/project-indexer init
# Creates repos/ and projects/ directories
```

### Clone + Symlink

```bash
./bin/project-indexer clone owner/my-project
# Clones repo AND creates symlink automatically
```

### Add existing repo

```bash
./bin/project-indexer add ./path/to/existing/repo
# Creates symlink with repo name
```

### List

```bash
./bin/project-indexer list
# Shows all symlinks
```

### Scan

```bash
./bin/project-indexer scan
# Shows repos and their symlink status
```

### Remove symlink (keeps repo)

```bash
./bin/project-indexer remove my-project
```

---

## Working with the AI

When asking the AI to work on a project, reference it by its symlink name:

```text
User: "work on my-project"

1. ./bin/project-indexer clone owner/my-project   (if not cloned)
2. AI uses workdir="projects/my-project"
3. AI inspects README → AGENTS.md → conventions
4. AI works in the repo
```

---

## projects.yaml

`projects.yaml` is **auto-generated** by `bin/devcompanion` from the
`projects/` symlinks. It is gitignored and should never be edited by hand.

```bash
# Regenerate at any time
./bin/devcompanion projects
```

The file is written with a `# Auto-generated — do not edit manually` header
so editors and AI tools know not to treat it as a source of truth.

---

## Why No Aliases?

| Aliases | No Aliases |
|---------|------------|
| Shorter names (`api`) | Full names (`my-api-service`) |
| Manual naming decisions | Zero decisions |
| Potential conflicts | No conflicts |
| Maintenance overhead | Automatic |

The repo name is unique and self-documenting. No need to remember "api → my-api-service".
