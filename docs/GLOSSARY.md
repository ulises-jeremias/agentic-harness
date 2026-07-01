# Glossary

Shared terminology for the AI Workspace + agentic-workstation ecosystem.

## A

**agent**
: An AI-driven subprocess managed by the orchestrator. Agents have specialized roles (code review, security, planning) and are listed in `AGENTS.md`. Agents may be deployed as skills or as standalone processes.

**AGENTS.md**
: Root-level file that instructs the AI tool (Claude Code, opencode, Cursor) on how to behave in this workspace. The primary agent contract. Also called CLAUDE.md, GEMINI.md depending on the tool — symlinked to AGENTS.md for portability.

**agentic-harness**
: The running instance — a git repository at `~/.agentic-harness` containing knowledge, packs, personas, loops, and workspace CLIs. Layer 2 in the three-layer harness model.

## C

**context pack**
: See *pack*.

## D

**agentic-workstation**
: The portable workstation baseline — a chezmoi-managed repository at `~/.local/share/agentic-workstation` providing AI skills, agents, CLI helpers, and MCP templates. Layer 1 in the three-layer model.

## G

**glossary**
: This file. A shared vocabulary that both agentic-harness and agentic-workstation reference to ensure consistent terminology across docs, code, and agent instructions.

## H

**harness**
: The three-layer architecture (infrastructure → running instance → application repos) that makes AI-assisted delivery repeatable and auditable. Layers: L1 (agentic-workstation workstation), L2 (agentic-harness running instance), L3 (client repos).

## K

**knowledge base**
: The `knowledge/` directory in agentic-harness. Structured markdown files organized by type (skills, processes, learnings, todos) that persist across sessions. The loop's "memory."

## L

**loop**
: A recurring AI-driven process with durable state, safety gates, and cost budgets. Managed by `bin/loop`. Each loop has a LOOP.md definition, STATE.md state, and `runs/` directory with trace artifacts.

**loop run**
: A single execution of a loop. Creates a run directory with trace.jsonl, plan.md, and any output artifacts. Encoded as `runs/<run-id>/`.

**loop closure**
: The process of extracting learnings and decisions from a completed loop run and writing them back to the knowledge base. Ensures the loop improves over time.

## M

**MCP**
: Model Context Protocol — a standard for AI tools to interact with external systems (filesystem, GitHub, databases). agentic-workstation ships MCP templates.

## P

**pack**
: A YAML file in `packs/` that bundles context for a specific client, project, or domain. Loaded by `workspace-context load packs/<name>.yaml`. Can be composable with profiles.

**persona**
: A work mode defined by a markdown file in `personas/`. Each persona declares allow/deny action lists, output format, and handoff rules. Activated by `workspace-context use-persona <name>`.

**profile**
: A composable configuration that bundles a pack + persona. Listed by `workspace-context profiles` and loaded with `workspace-context load --profile <name>`.

## R

**runner**
: The agentic-workstation dev companion runner — a background process that executes loop jobs. Invoked by `bin/loop run` when available. Falls back to skeleton mode without agentic-workstation.

## S

**skill**
: A self-contained AI instruction bundle with `SKILL.md` (human-readable) and `skill.json` (manifest). Skills are the unit of distribution in agentic-workstation. They declare capabilities, boundaries, triggers, dependencies, and compatibility.

**skill catalog**
: `skill-catalog.yaml` — the agentic-workstation orchestration metadata file that maps skills to domains, responsibilities, roles, and dependency graph.

**snapshot**
: The output of `workspace-context` — a machine-readable summary of the current session state including active persona, loaded pack, spec hash, and persona constraints.

## T

**trace**
: A JSONL file at `runs/<run-id>/trace.jsonl` that records every event during a loop run (run_start, worktree_created, decision, run_end, etc.). Used for audit and loop closure.

## W

**worktree**
: A detached git checkout created by `bin/loop run` to execute work on a clean copy of the workspace. Automatically removed after the run completes or is cancelled.

**workspace-context**
: The session snapshot CLI at `bin/workspace-context`. Prints active state, loads packs/personas/profiles, validates schemas, and manages persona handoffs.
