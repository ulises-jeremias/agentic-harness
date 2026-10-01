<div align="center">

<img alt="agentic-harness" src="static/hero-banner.svg" width="100%">

<br>
<br>

[![Workspace](https://img.shields.io/badge/Workspace-Persistent-06b6d4?style=for-the-badge&labelColor=030712)](#personal-dx-stack)
[![Memory](https://img.shields.io/badge/Persistent-Memory-06b6d4?style=for-the-badge&labelColor=030712)](#key-concepts)
[![Loops](https://img.shields.io/badge/Loop-Engineering-f472b6?style=for-the-badge&labelColor=030712)](#quick-start)
[![CI](https://img.shields.io/github/actions/workflow/status/ulises-jeremias/agentic-harness/ci.yml?style=for-the-badge&label=CI&labelColor=030712&color=06b6d4)](https://github.com/ulises-jeremias/agentic-harness/actions/workflows/ci.yml)
[![Discord](https://img.shields.io/discord/1527933660764831825?style=for-the-badge&label=Discord&logo=discord&logoColor=white&labelColor=030712)](https://discord.gg/bR5VyATgka)

<h3>Persistent workspace for AI-assisted delivery — a reference implementation powered by agent-toolkit.</h3>

<p>
  <strong>agentic-harness</strong> is the persistent workspace layer of the personal Developer Experience stack:<br>
  memory, personas, indexed repos, packs, queues, and feedback loops that keep AI work moving.<br>
  All runtime CLIs come from <a href="https://github.com/ulises-jeremias/agent-toolkit">agent-toolkit</a> — this repo is the reference workspace, not a second engine.
</p>

[Quick Start](#quick-start) · [Key Concepts](#key-concepts) · [Architecture](#architecture) · [Docs](#docs) · [Personal DX Stack](#personal-dx-stack) · [Contributing](CONTRIBUTING.md)

Works with **Claude Code**, **Muse Code**, **opencode**, **Cursor**, **Gemini CLI**, and **GitHub Copilot**.

</div>

---

> [!NOTE]
> **Powered by [agent-toolkit](https://github.com/ulises-jeremias/agent-toolkit)** — the capability distribution layer of the personal DX stack.
>
> ```bash
> uvx agent-toolkit-cli                          # one-shot, no install required
> uv tool install agent-toolkit-cli              # permanent install
> agent-toolkit workspace init --dir my-workspace
> ```
>
> All workspace operations use `agent-toolkit` directly:
> `agent-toolkit workspace context` · `agent-toolkit memory` · `agent-toolkit loop` · `agent-toolkit devcompanion` · `agent-toolkit project`

---

**agentic-harness** is the persistent workspace — the reference implementation that gives your AI durable memory, project context, persona-based guardrails, and loop orchestration across sessions. The runtime is **agent-toolkit**; this repo shows how to wire it.

Think of it as the **workspace that makes your AI coding agents stateful**.

```text
     Your AI Tool  ←→  agentic-harness  ←→  Your Repos
                    (persistent workspace — memory, context,
                     loops, personas, job queues — via agent-toolkit)
```

---

## Quick Start

> "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." — *Peter Steinberger*

```bash
# 1. Clone as your personal workspace
git clone <this-repo> ~/.agentic-harness
cd ~/.agentic-harness
./scripts/workspace-init.sh

# 2. Index a repo
agent-toolkit project clone owner/my-repo

# 3. Start a daily issue triage loop (L1 = observe only, no writes)
agent-toolkit loop init daily-triage
agent-toolkit loop run daily-triage

# 4. Review what the loop found
cat loops/daily-triage/runs/*/report.md

# 5. Check cost and status
agent-toolkit loop status
agent-toolkit loop audit daily-triage

# 6. Open in your AI tool for interactive sessions
muse            # or: claude / opencode / cursor / gemini
```

> **The loop runs autonomously between your sessions.** Wire it to a scheduler when you're ready to upgrade to L2 (PR-gated).

See [docs/LOOPS.md](docs/LOOPS.md) for the full loop reference and anti-patterns.

### Workspace branch modes

```bash
# Personal workspace (default) — creates branch: user-workspace/<username>
./scripts/workspace-init.sh

# Shared team workspace — creates branch: account-workspace/<name>
./scripts/workspace-init.sh --account-workspace=my-team
```

> [!TIP]
> Edit `.workspace.yaml` after setup to set your GitHub org and default clone directory.

---

## Key Concepts

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🔄 Persistent Workspace</h3>
      <sub>This repo is the workspace — not the engine. <code>agent-toolkit</code> provides the CLIs; the harness provides the durable state (memory, packs, personas, loops) that survives across sessions.</sub>
    </td>
    <td width="50%" valign="top">
      <h3>🧬 Ralph Loop</h3>
      <sub>The four-stage cycle your AI runs in:</sub>
      <br>
      <code>Backing Specs → Context Engineering → Persistent Memory → Fix the Loop</code>
      <br><br>
      <sub>Each session, the AI reads <code>AGENTS.md</code> → checks <code>knowledge/</code> → works → saves discoveries. The loop improves itself over time.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🎭 Personas</h3>
      <sub>Personas constrain what the AI <em>does</em> in a session — not who it is. <code>personas/reviewer.md</code> means "analyze and report, no changes".</sub>
      <br><br>
      <sub>Workspace selections from Toolkit's catalog:<br>
      🛠️ <code>implementer</code> · 🔍 <code>reviewer</code> · 🔬 <code>researcher</code> · 🏗️ <code>architect</code> · ✍️ <code>writer</code> · 🐛 <code>debugger</code> · 🧪 <code>tester</code></sub>
    </td>
    <td width="50%" valign="top">
      <h3>📦 Packs</h3>
      <sub>Harness packs are <strong>context bundles</strong> (repos, IDs, conventions per client/project). Toolkit packs are reusable capabilities. See <a href="docs/PACKS.md">docs/PACKS.md</a>.</sub>
      <br><br>
      <sub><code>agent-toolkit workspace load packs/my-client.yaml</code></sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>⏳ DevCompanion Queue</h3>
      <sub>Background job queue for async tasks — code reviews, refactors, CI fixes, investigations. Jobs run in a separate agent session and leave artifacts.</sub>
      <br><br>
      <sub><code>agent-toolkit devcompanion queue my-project --template code-review</code></sub>
    </td>
    <td width="50%" valign="top">
      <h3>🧠 Persistent Memory</h3>
      <sub>Your AI remembers across sessions. <code>knowledge/</code> stores processes, learnings, todos, and patterns — indexed, searchable, and version-controlled.</sub>
      <br><br>
      <sub><code>agent-toolkit memory search "topic"</code></sub>
    </td>
  </tr>
</table>

---

## 📁 Structure

```text
agentic-harness/
├── AGENTS.md              # AI orchestration instructions (main config)
├── CLAUDE.md              # Symlink → AGENTS.md (opencode/Cursor)
├── GEMINI.md              # Symlink → AGENTS.md (Gemini CLI)
├── bin/
│   └── workspace-context  # Thin wrapper → agent-toolkit workspace context
├── docs/                  # Guides, references, and methodology
├── knowledge/             # Persistent AI memory (learnings, todos, patterns)
├── personas/              # Workspace persona selections (from Toolkit catalog)
├── people/                # Durable collaborators (one JSON per Person; roster stays empty until human review)
├── packs/                 # Workspace context bundles per client/project
├── profiles/              # Session profiles: pack + persona + skills
├── schemas/               # JSON Schema validation for context surfaces
├── templates/
│   ├── jobs/              # Job templates for agent-toolkit devcompanion
│   └── loops/             # Loop templates (daily-triage, ci-sweeper, …)
├── static/                # Banner and architecture diagrams
├── projects/              # Symlinks to repos (local, gitignored)
└── repos/                 # Cloned repos (local, gitignored)
```

Runtime CLIs come from **agent-toolkit**: `agent-toolkit workspace` · `memory` · `loop` · `devcompanion` · `project`.

---

## Architecture

<div align="center">
<img src="static/architecture.svg" alt="agentic-harness architecture: context, harness, and loop stages powered by agent-toolkit" width="96%">
</div>

Full component reference and Mermaid diagrams: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## Docs

| Guide | Description |
|-------|-------------|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Component architecture and data flow |
| [`docs/SETUP.md`](docs/SETUP.md) | Initial setup and AI tool configuration |
| [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) | The agentic harness philosophy (Stages 0–3) |
| [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md) | Task routing and skill usage patterns |
| [`docs/LOOPS.md`](docs/LOOPS.md) | Loop engineering reference and anti-patterns |
| [`docs/PERSONAS.md`](docs/PERSONAS.md) | Work mode personas lifecycle |
| [`docs/PACKS.md`](docs/PACKS.md) | Workspace context bundles (vs Toolkit capability packs) |
| [`docs/PROJECTS.md`](docs/PROJECTS.md) | Managing repos and symlinks |
| [`docs/DEVCOMPANION.md`](docs/DEVCOMPANION.md) | Background job queue guide |
| [`docs/KNOWLEDGE.md`](docs/KNOWLEDGE.md) | Knowledge base usage |
| [`docs/PERSONAS.md`](docs/PERSONAS.md) | Persona catalog and lifecycle (workspace selections) |
| [`docs/PEOPLE.md`](docs/PEOPLE.md) | Durable People (identity model, schema rules, gaps) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to extend and contribute |

---

## Personal DX Stack

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Infrastructure Layer</strong><br>
      <sub>Machine provisioning — chezmoi, shell, packages, and day-to-day ergonomics. The baseline your other layers run on.</sub>
      <br><br>
      <a href="https://github.com/ulises-jeremias/dotfiles"><code>ulises-jeremias/dotfiles</code></a>
      · <a href="https://github.com/ulises-jeremias/agentic-workstation"><code>agentic-workstation</code></a>
    </td>
    <td width="34%" valign="top">
      <strong>Capability Layer</strong><br>
      <sub>Reusable capabilities — skills, agents, loop/queue CLIs, profiles, MCP. Ships the runtime that workspaces consume.</sub>
      <br><br>
      <a href="https://github.com/ulises-jeremias/agent-toolkit"><code>agent-toolkit</code></a>
    </td>
    <td width="33%" valign="top">
      <strong>Workspace Layer</strong><br>
      <sub><strong>agentic-harness</strong> — the persistent reference workspace: memory, indexed repos, persona selections, context bundles, and loop state.</sub>
      <br><br>
      <a href="https://github.com/ulises-jeremias/agentic-harness"><code>agentic-harness</code></a>
    </td>
  </tr>
</table>

Together, these layers form a personal workspace system that optimizes setup, context switching, AI-assisted delivery, and daily workflow automation. The harness is the **reference workspace** — clone it, make it yours.

---

## ✅ Validation

```bash
# Verify setup
agent-toolkit project list          # shows indexed repos
agent-toolkit memory todo         # shows pending items
agent-toolkit workspace context     # session state snapshot

# Queue a test job
agent-toolkit devcompanion queue my-project --template code-review
agent-toolkit devcompanion run-once --no-llm
```

---

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| `agent-toolkit project: command not found` | Run `chmod +x ./bin/*` and ensure `agent-toolkit` is installed |
| DevCompanion: "No LLM provider" | Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` |
| Pending jobs stuck | Run `agent-toolkit devcompanion status` |
| Skills not loading | Check your AI tool's skill pack configuration |

---

<div align="center">

**⭐ Star this repo** if you use it — it helps others discover it.

[Report a bug](https://github.com/ulises-jeremias/agentic-harness/issues/new) · [Request a feature](https://github.com/ulises-jeremias/agentic-harness/issues/new)

<sub>Built with ❤️ for AI-assisted software delivery</sub>

</div>

## 👥 Contributors

<a href="https://github.com/ulises-jeremias/agentic-harness/contributors">
  <img alt="Contributors" src="https://contrib.rocks/image?repo=ulises-jeremias/agentic-harness"/>
</a>

Made with [contributors-img](https://contrib.rocks).
