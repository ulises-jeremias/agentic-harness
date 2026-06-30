# ADR 0001: Rename repository from ai-workspace to agentic-harness

**Status**: Accepted

## Context

The repository was originally named `ai-workspace`, a generic descriptor that
does not differentiate the project from countless other "AI workspace" tools
and configurations. The project's core philosophy — documented in
`docs/METHODOLOGY.md` — is that of an **agentic harness**: a lightweight,
portable framework that provides context, memory, and orchestration loops for
AI coding agents. The term "harness" accurately conveys that the project
controls, constrains, and amplifies the agent rather than serving as a passive
workspace.

## Decision

1. Rename the GitHub repository from `ai-workspace` to `agentic-harness`.
2. Set the GitHub description to:
   > "Portable agentic harness — context, memory, and loops for AI coding
   > agents."
3. Provide a migration script (`scripts/rename-migrate.sh`) to help existing
   users update their local remotes.
4. Update all references throughout the codebase over time to reflect the new
   name.

## Consequences

### Positive

- Clearer project identity and differentiation from generic "AI workspace"
  repos.
- The name "agentic-harness" aligns with the methodology and terminology
  already used in the project's documentation.
- Improved discoverability for users looking specifically for agentic
  harness/orchestration tooling.

### Negative

- Existing local clones must update their remote URL. The migration script
  addresses this.
- Documentation and references across the web (issues, forks, stars) will
  continue to point to the old URL.
- Internal tooling and automation that depends on the repository path will
  need updating.
