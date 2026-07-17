# Methodology — From Prompting to Loops

> How this workspace is designed and why it works.

---

## The Discipline Stack

Three disciplines layer on top of each other to take you from "typing prompts" to "designing autonomous AI processes":

| Layer | Question | What it does |
|-------|----------|-------------|
| **Context engineering** | What does the agent *know* before it acts? | Schemas, packs, personas, knowledge base |
| **Harness engineering** | What *scaffolds and observes* the agent? | Routing, telemetry, contracts, sub-agent dispatch |
| **Loop engineering** | How does work *repeat autonomously*? | Schedulers, STATE/LOOP spine, maker/checker, cost budgets |

Each layer builds on the one below. You can use context engineering alone; to get loops, you need all three.

---

## Layer 0 — The Ralph Loop Foundation

> *Named after Geoffrey Huntley's "RALPH" model — [ghuntley.com/loop](https://ghuntley.com/loop/)*

Everything builds on the Ralph Loop — a four-phase feedback cycle:

```text
┌─────────────────────────────────────────────────────────┐
│                      Ralph Loop                          │
│                                                          │
│  Backing Specs  →  Context Engineering                   │
│       ↑                   ↓                              │
│  Fix the Loop  ←  Persistent Memory                      │
└─────────────────────────────────────────────────────────┘
```

1. **Backing Specs** (`AGENTS.md`) — the invariant that doesn't change session-to-session
2. **Context Engineering** — inject the right information at the right time
3. **Persistent Memory** (`knowledge/`) — what we learned carries forward
4. **Fix the Loop** — specs and knowledge improve over time

The Ralph Loop turns each session into a training run for the next one.

---

## Layer 1 — Context Engineering

> *What does the agent know before it acts?*

Context engineering is the practice of giving the agent exactly the right information — no more, no less — so it can act correctly without asking.

### Surfaces

| Surface | What it provides | Where |
|---------|-----------------|-------|
| `AGENTS.md` | Orchestration rules, routing table, skill list | Repo root |
| `packs/*.yaml` | Project-specific context: repos, IDs, conventions | `packs/` |
| `personas/*.md` | Behavioral constraints: allow/deny/handoffs | `personas/` |
| `profiles/*.yaml` | Composable sessions: pack + persona + skills | `profiles/` |
| `knowledge/` | Persistent cross-session memory | `knowledge/` |

### Rules for good context engineering

1. **Validate every surface** — use `workspace-context validate` to catch schema violations before they confuse the agent
2. **Tag knowledge entries** — `tags`, `project`, `created`, `stale_after` let you filter at retrieval time
3. **Keep personas narrow** — a reviewer persona that can accidentally commit is a safety hazard
4. **Load before you work** — `workspace-context load --profile <name>` is one command to prime the session

---

## Layer 2 — Harness Engineering

> *What scaffolds and observes the agent during the run?*

The harness is the scaffolding that wraps the agent: routing, telemetry, contracts, sub-agent dispatch. It makes the agent's behavior observable and reproducible.

### Components

| Component | Role |
|-----------|------|
| `AGENTS.md` routing table | Dispatch the right skill or sub-agent per task type |
| `workspace-context` snapshot | Record the spec hash and active pack at session start |
| Job templates (`templates/jobs/`) | Declared contract: inputs, outputs, exit criteria |
| `devcompanion` job queue | Background work with artifact output |
| Schema validation CI | Catch malformed context before it reaches the agent |

### The AGENTS.md spec hash

Every session records which version of `AGENTS.md` it ran under:

```text
Spec       : AGENTS.md@ca723537e215
```

When you update `AGENTS.md`, the hash changes. Mismatches indicate that a session ran on a stale spec.

---

## Layer 3 — Loop Engineering

> *How does work repeat autonomously?*
> "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."
> — Peter Steinberger

A **loop** is a recurring goal: you define a purpose and the AI iterates — with sub-agents, verification, and external state — until the goal is met or the loop decides to hand off to you.

### The 6 parts of a loop

| Part | Role |
|------|------|
| **Automation / Scheduling** | When does the loop fire? (cron, timer, trigger) |
| **Worktree isolation** | Each run gets its own git worktree |
| **Skills** | Reusable task prompts (from `agentic-workstation`) |
| **Plugins / Connectors** | MCP and CLI reach (GitHub, ClickUp, CI) |
| **Sub-agents** | Maker (implementer) + Checker (verifier receipt / skill) |
| **Memory / State spine** | `LOOP.md` (intent) + `STATE.md` (current state) |
| **Hard gate** | `bin/loop-gh-gate` wraps `gh` during runs (allowlist/deny/receipts) |

### Rollout tiers

Always start at L1. Graduate to L3 only with a proven allowlist.

| Tier | Autonomy | When |
|------|----------|------|
| **L1** | Report-only | Exploring a new loop pattern |
| **L2** | Assisted (allowlisted mutations) | Actions verified; humans still own merge |
| **L3** | Unattended on allowlist | High-confidence, narrow scope + hard gate |

### Quick start

```bash
# Scaffold from a reference pattern
./bin/loop init daily-triage

# Run once to see what it would do (L1 = report only)
./bin/loop run daily-triage

# Review the output
cat loops/daily-triage/runs/<id>/report.md

# Check cost so far
./bin/loop audit daily-triage
```

See [docs/LOOPS.md](LOOPS.md) for the full reference.

---

## Glossary

| Term | Definition |
|------|-----------|
| **backing spec** | `AGENTS.md` — the invariant orchestration instructions |
| **pack** | `packs/*.yaml` — project/client context bundle |
| **persona** | `personas/*.md` — behavioral constraint (allow/deny/handoffs) |
| **profile** | `profiles/*.yaml` — pack + persona + skills composition |
| **knowledge** | `knowledge/` — persistent cross-session memory |
| **harness** | Scaffolding that wraps an agent (routing, contracts, telemetry) |
| **loop** | Recurring autonomous process with STATE/LOOP spine |
| **loop tier** | L1 (report) / L2 (PR-gated) / L3 (unattended on allowlist) |
| **maker** | Implementer sub-agent in a loop |
| **checker/verifier** | Verifier sub-agent in a loop; signs off before writes |
| **worktree** | Isolated git working tree created per loop run |
| **exit condition** | DSL signal that ends a loop iteration (goal_met, budget_exhausted, …) |

---

## Workflow Lifecycle

```text
Session Start
    │
    ▼
1. AI reads AGENTS.md (spec hash recorded)
    │
    ▼
2. Load pack or profile
    ./bin/workspace-context load --profile oss-contrib
    │
    ▼
3. Prime context
    ./bin/workspace-context         # state snapshot
    ./bin/assistant-memory inject   # knowledge dump
    │
    ▼
4. Work (discover → delegate → implement)
    │
    ▼
5. Save
    ./bin/assistant-memory add --type learning "..."
    │
    ▼
Session End
    │
    ▼
Loop runs autonomously between sessions (if configured)
```

---

## Key Commands

```bash
# Context
./bin/workspace-context validate          # check schema violations
./bin/workspace-context load --profile oss-contrib
./bin/assistant-memory search --tag oss "deploy"
./bin/assistant-memory review --stale     # check decayed entries

# Loops
./bin/loop init daily-triage              # scaffold from template
./bin/loop run daily-triage              # one iteration
./bin/loop status                        # all loops at a glance
./bin/loop audit                         # cost and success rate
./bin/loop cost daily-triage             # estimate per run

# Background work (one-shot)
./bin/devcompanion queue my-project --template code-review
./bin/devcompanion run-once
```
