# Changelog

All notable changes to agentic-harness are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

> [!NOTE]
> For commit-level detail, see the [commit history](https://github.com/ulises-jeremias/agentic-harness/commits/main).

---

<!-- markdownlint-disable MD024 -->
## [Unreleased]

### Added

- Hard autonomy gate (`bin/loop-gh-gate`): PATH-first `gh` shim during `loop run` that enforces tier/allowlist/deny and requires verifier receipts for merge/close (exit code 78 on denial)
- `loop run --force` bypasses `max_runs_per_day` budget
- Runner prompt now loads `request.md`, injects a HARD autonomy contract, and persists `prompt.md` per run
- STATE.md pending/escalations are preserved across runs; list items with `#` are quoted
- Loop starter templates (daily-triage, issue-triage, pr-babysitter) document silent-ops style and `per_page=50` scanning lessons from production OSS loops

### Fixed

- Loop hard gate follow-up (CodeRabbit on #166): fail-closed gate install, stricter `gh` mutation classification, redacted audit argv, HMAC receipt binding, always-quoted STATE strings, docs/workshop fence fixes

- `bin/loop` no longer wiped `pending`/`escalations` after every run
- ISO timestamps in STATE.md parsed as datetime by PyYAML no longer crash the budget gate
- Duplicate `_try_opencode_runner` definition removed

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

<!-- markdownlint-enable MD024 -->

---

[1.0.0]: https://github.com/ulises-jeremias/agentic-harness/releases/tag/v1.0.0
[0.4.0]: https://github.com/ulises-jeremias/agentic-harness/releases/tag/v0.4.0
[0.3.0]: https://github.com/ulises-jeremias/agentic-harness/releases/tag/v0.3.0
[0.2.0]: https://github.com/ulises-jeremias/agentic-harness/releases/tag/v0.2.0
