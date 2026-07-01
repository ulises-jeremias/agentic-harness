# ADR 0002: Coordinate rename with agentic-workstation

**Status**: Accepted

## Context

ADR 0001 decided to rename this repository from `agentic-harness` to `agentic-harness`. That ADR was accepted but never executed, pending coordination with the companion workstation repository (`agentic-workstation`, now renamed to `agentic-workstation` via its ADR-010).

The three-layer architecture (ADR-007 in agentic-workstation) defines:

| Layer | Purpose | Repo |
|-------|---------|------|
| L1 — Workstation Baseline | Tooling, skills, agents, CLI helpers | `agentic-workstation` |
| L2 — Running Instance | Session state, knowledge, packs, loops | `agentic-harness` (this repo) |
| L3 — Application | Client project repos | Per-client |

Both renames must happen in tandem to avoid a staggered migration period where cross-references (documentation, the `dots-harness-knowledge-sync` skill, CI workflows) point to outdated URLs.

## Decision

1. **Reaffirm ADR 0001**: Rename this repo from `agentic-harness` to `agentic-harness`, with GitHub description "Portable agentic harness — context, memory, and loops for AI coding agents."
2. **Coordinate execution**: This rename executes immediately after `agentic-workstation` → `agentic-workstation` is complete.
3. **Cross-repo skill**: Rename `dots-ai-workspace-knowledge-sync` to `dots-harness-knowledge-sync` to reflect both new repo names.
4. **Environment variables**: Rename `HARNESS_*` env vars (e.g., `HARNESS_RUNNER_DIR`) to `HARNESS_*` equivalents.
5. **Local paths**: The personal instance at `~/.agentic-harness/` is a separate fork (`my-agentic-harness`) with `agentic-harness` as upstream. Only the remote URL needs updating — the local directory name stays `~/.agentic-harness/`.

## Consequences

### Positive

- Cohesive naming across L1 (`agentic-workstation`) and L2 (`agentic-harness`)
- Cross-repo skill name is no longer disonant
- Single coordinated migration window minimizes disruption

### Negative

- Migration cost: updating ~48 references in this repo plus cross-references
- Personal `~/.agentic-harness` clone needs remote update
- Env var renames (`HARNESS_*` → `HARNESS_*`) may require shell config updates
