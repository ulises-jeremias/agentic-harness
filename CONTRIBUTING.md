# Contributing

This repo is your **personal AI workspace** — a fork-and-own framework. Contributions here mean extending it for your own needs. If you want to contribute back to the upstream starter, open a PR there.

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
