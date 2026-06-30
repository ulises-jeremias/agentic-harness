# OpenCode — Local Overlay

> Tool-specific addendum to AGENTS.md for OpenCode users.

---

## OpenCode Specific

### Skills integration

OpenCode reads skills from `~/.config/opencode/skills/`. After installing `dots-ai`,
skills like `dots-ai-assistant`, `github-cli-workflow`, etc. are available.

### Using the workspace context tool

OpenCode natively supports `AGENTS.md` — no symlink needed. The workspace context
(personas, packs, knowledge) is read automatically if the tool supports `contextFiles`.

---

## No breaking changes to AGENTS.md

This file adds OpenCode capabilities. AGENTS.md remains the source of truth.
