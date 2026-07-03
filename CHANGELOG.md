# Changelog

All notable changes to agentic-harness are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

> [!NOTE]
> For commit-level detail, see the [commit history](https://github.com/ulises-jeremias/agentic-harness/commits/main).

---

## [1.0.0] — Stable

### Added

- Loop engineering with L1 (report-only), L2 (PR-gated), L3 (unattended) safety tiers
- 7 loop templates: daily-triage, issue-triage, pr-babysitter, ci-sweeper, dep-sweeper, changelog-drafter, post-merge-cleanup
- Dev companion background job queue with 5 templates: code-review, create-pr, fix-ci, investigate, refactor
- Project indexer with clone + symlink management (`bin/project-indexer`)
- Workspace context snapshot generation and validation (`bin/workspace-context`)
- Persona system with 5 work modes: implementer, reviewer, researcher, architect, writer
- Pack system for project context switching with YAML-based configuration
- Knowledge base with persistent cross-session AI memory (`knowledge/`)
- Session profiles combining pack + persona + skills (`profiles/`)
- JSON Schema validation for all context surfaces: packs, personas, knowledge, loops, jobs
- 3 example walkthroughs: solo-dev-daily-triage, pr-babysitter, oss-contribution
- Comprehensive documentation: 9 docs covering setup, methodology, workflows, loops, personas, packs, projects, devcompanion, and knowledge
- Multi-tool portability: symlinks for Claude Code, opencode, Cursor, Gemini CLI, GitHub Copilot
- Architecture diagram with Mermaid visualizations (`docs/ARCHITECTURE.md`)
- Full bin/loop CLI reference (`docs/LOOP_CLI.md`)
- FAQ page covering common questions and scenarios (`docs/FAQ.md`)
- Security model documentation (`docs/SECURITY.md`)
- Performance and scaling guidance (`docs/PERFORMANCE.md`)
- Migration guide for existing AI workflows (`docs/MIGRATION.md`)
- Tool-specific quick-start guides for all 5 supported AI tools (`docs/quickstarts/`)
- "Your First PR with agentic-harness" end-to-end tutorial (`docs/tutorials/FIRST_PR.md`)
- Multi-client setup tutorial for freelancers and agencies (`docs/tutorials/MULTI_CLIENT_SETUP.md`)
- Sample knowledge base with realistic entries demonstrating persistent memory
- .devcontainer/devcontainer.json for GitHub Codespaces onboarding
- LLM policy integration with agentic-workstation dev companion runner

### Changed

- Renamed from `ai-workspace` to `agentic-harness` (ADR-002)
- Renamed workspace-knowledge-sync skill to harness-knowledge-sync

## [0.4.0] — Observability

### Added

- Structured trace and telemetry primitives
- Loop closure audit trail
- Cost tracking per loop at Tier 1

### Changed

- Loop audit outputs now include cost accumulator
- STATE.md format extended with total_tokens and total_cost fields

## [0.3.0] — Loop Engine

### Added

- First-class loop primitives: init, run, status, audit, cost
- STATE/LOOP spine with exit condition DSL
- Maker/checker pattern for L2+ loops
- Loop template directory with 7 reusable templates
- systemd/launchd scheduler integration

### Changed

- Loop directory structure standardized: `loops/<name>/LOOP.md` + `STATE.md`
- Exit conditions moved from inline flags to LOOP.md YAML frontmatter

## [0.2.0] — Context Contracts

### Added

- JSON Schema validation for all context surfaces
- Pack schema with repo, convention, tool, and LLM policy definitions
- Persona frontmatter schema with allow/deny/handoff rules
- Knowledge entry schema for learnings and processes
- Loop result schema with exit codes and cost tracking
- Profile schema combining pack + persona + skills
- Pre-commit hooks for schema validation
- CI smoke tests for context validation

### Changed

- Pack format standardized: YAML with validated fields
- Persona format: Markdown with YAML frontmatter
- Knowledge entries: Frontmatter with type, date, and context fields

---

[1.0.0]: https://github.com/ulises-jeremias/agentic-harness/releases/tag/v1.0.0
[0.4.0]: https://github.com/ulises-jeremias/agentic-harness/releases/tag/v0.4.0
[0.3.0]: https://github.com/ulises-jeremias/agentic-harness/releases/tag/v0.3.0
[0.2.0]: https://github.com/ulises-jeremias/agentic-harness/releases/tag/v0.2.0
