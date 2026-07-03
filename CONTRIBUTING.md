# Contributing

[![Good First Issues](https://img.shields.io/github/issues-search/ulises-jeremias/agentic-harness?query=is%3Aissue%20is%3Aopen%20label%3A%22good%20first%20issue%22&label=good%20first%20issue&color=7057ff)](https://github.com/ulises-jeremias/agentic-harness/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
[![Help Wanted](https://img.shields.io/github/issues-search/ulises-jeremias/agentic-harness?query=is%3Aissue%20is%3Aopen%20label%3A%22help%20wanted%22&label=help%20wanted&color=f59e0b)](https://github.com/ulises-jeremias/agentic-harness/issues?q=is%3Aissue+is%3Aopen+label%3A%22help%20wanted%22)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/ulises-jeremias/agentic-harness/pulls)

This repo is your **personal AI workspace** — a fork-and-own framework. Contributions here mean extending it for your own needs. If you want to contribute back to the upstream starter, open a PR.

## How to contribute

| What | Where to start |
|------|---------------|
| Write a tutorial or guide | Check issues labeled [good first issue](https://github.com/ulises-jeremias/agentic-harness/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) |
| Improve documentation | See [docs/](docs/) — many docs welcome contributions |
| Add examples or templates | [templates/](templates/) and [examples/](examples/) directories |
| Improve CLI tools | [bin/](bin/) — Python and shell scripts |
| Design new personas | [personas/](personas/) — work mode definitions |
| Create loop templates | [templates/loops/](templates/loops/) — reusable loop patterns |

**First time contributing?** Check out our [good first issues](https://github.com/ulises-jeremias/agentic-harness/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

---

## What belongs here

| Type | Where |
|------|-------|
| Tool process documentation | `knowledge/processes/` |
| Workflow and routing patterns | `knowledge/processes/general.md` |
| New skill discoveries | `knowledge/skills/discovered.md` |
| Learnings and corrections | `knowledge/learnings/` |
| CLI tool improvements | `bin/` |
| Job templates | `templates/jobs/` |
| Personas | `personas/` |
| Context packs | `packs/` |
| Setup / onboarding docs | `docs/` |

## What belongs elsewhere

| If it's... | Put it in |
|-----------|-----------|
| Machine setup, dotfiles, shell config | Your workstation/dotfiles repo |
| Reusable skill definitions | Your skills pack / opencode skills repo |
| Team-wide patterns and examples | Your team's knowledge base |

---

## Workflow

```bash
# 1. Branch from main
git checkout -b feat/add-my-improvement

# 2. Make your changes

# 3. Commit (English)
git commit -m "docs(knowledge): add process for tool X"

# 4. Push and open PR (if contributing upstream)
git push -u origin feat/add-my-improvement
gh pr create
```

---

## Commit message conventions

```text
feat(scope):     New capability
fix(scope):      Bug or error fix
docs(scope):     Documentation only
chore(scope):    Maintenance, deps, CI
```

Common scopes: `knowledge`, `bin`, `docs`, `templates`, `personas`, `packs`, `ci`

---

## PR checklist

- [ ] No secrets, tokens, credentials, or personal IDs included
- [ ] Knowledge entries use placeholder examples (not real IDs)
- [ ] CLI scripts are executable (`chmod +x bin/my-script`)
- [ ] Docs files use UPPERCASE names (`docs/MY-DOC.md`)
- [ ] No team-specific names, URLs, or tool instances hardcoded

---

## Adding processes

When adding a new tool process (e.g., a new project management tool):

- [ ] Create `knowledge/processes/<tool>.md`
- [ ] Use placeholder IDs, not real ones
- [ ] Document the skill/CLI invocation pattern
- [ ] Add an entry to the routing table in `AGENTS.md`

## Community

- **Questions?** [Open an issue](https://github.com/ulises-jeremias/agentic-harness/issues/new) with the `question` label
- **Feature ideas?** Check [open issues](https://github.com/ulises-jeremias/agentic-harness/issues) first — if it's new, open an issue with the `enhancement` label
- **Found a bug?** Report it with steps, expected behavior, and actual behavior
- **Want to share your setup?** Add an example to `examples/` and open a PR
- **Recognition**: All contributors are acknowledged in the [CHANGELOG](CHANGELOG.md) and release notes
