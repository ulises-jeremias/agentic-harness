# People — durable collaborators, separate from runtime

This reference workspace mirrors Agent Toolkit's People contracts and provides
fictional examples. It does not implement a second People runtime. The current
Desktop supports roster CRUD, archive/restore, reviewed one-way
`munder-difflin/hire@1` import, and starting a Person as a real local PTY session.
Session resume across Desktop exit and full swarm-session identity/world
integration remain partial; see [current toolkit documentation](https://github.com/ulises-jeremias/agent-toolkit/blob/main/docs/PEOPLE.md).

The active `people/` roster is intentionally empty until a human configures
collaborators. Example declarations under `templates/people/` are validated
but are not configured People and never imply runtime activity.

## Identity model

| Concept | Canonical location | Meaning |
|---|---|---|
| Agent definition | Toolkit `agents/<name>/AGENT.md` | Reusable behavior and capability template |
| Person | Workspace `people/<id>.json` | Durable collaborator configuration and appearance |
| Agent session | Toolkit workspace `.agent-toolkit/sessions/` plus live Electron PTY | Runtime lifecycle evidence tied to a real process |
| Swarm role | Recipe/run | Temporary responsibility in one orchestration |
| Workspace persona | Workspace `personas/*.md` | Constraints for a work mode, not a person or agent definition |

A configured or archived Person is not a worker. The Desktop world may show a
Person only when a real session is live and associated with a registered
project. A swarm role binding currently selects launch preferences and records
the Person ID, but it does not yet create a canonical Person session, terminal
action, or World character for the swarm process.

## Data and validation

People declarations use `agent-toolkit/person@1`; optional role preferences
use `agent-toolkit/people-bindings@1`. This repository mirrors the canonical
schemas and validator under `schemas/` and `scripts/`. The mirror lock records
source revisions and SHA-256 digests. Update mirrors from the Agent Toolkit
repository and verify the lock before changing these files; do not hand-edit
the mirrored contracts.

Validate the examples and active roster offline:

```bash
python3 scripts/validate-people.py --workspace .
```

The validator rejects symlinked declarations, invalid or duplicate IDs,
duplicate keys, non-finite numeric values, oversized files, unknown fields and
tampered schema mirrors. It prints static diagnostics and does not echo
declaration contents. Templates are checked without being counted as active
People.

## Import boundary

The Munder adapter is one-way interoperability. Import opens a review flow and
requires an explicit save. Embedded commands are inert/ignored; importing
never spawns a session, installs arbitrary code, enables MCP, or establishes
live sync. Munder's registry is not an Agent Toolkit runtime source of truth.

## Swarm role resolution

Before start, Desktop can preview role bindings. An explicit Person selection
wins; saved workspace defaults and compatible People may be considered by the
backend; unmatched roles remain ephemeral. Runner/model preferences can inform
role launch configuration. The persisted role Person ID is currently an
adapter hint, not a canonical session identity. Swarms continue to work with
no configured People.

## Operational limits

- Person start creates a new local PTY session; it does not resume provider
  conversation history or keep the process alive after Desktop exits.
- `max_seconds` is enforced for local Person PTYs. Token/cost budgets and
  non-inherited isolation are disclosed as unsupported in that flow.
- Cursor and Muse open interactively without a submitted initial task until
  their runner-specific prompt contracts are verified.
- Swarm role processes are not yet exposed as Person sessions in Terminal or
  the semantic World.

For implementation evidence and the current feature ledger, use Agent
Toolkit's [People contract](https://github.com/ulises-jeremias/agent-toolkit/blob/main/docs/PEOPLE.md)
and [Desktop workflow ledger](https://github.com/ulises-jeremias/agent-toolkit/blob/main/docs/desktop/workflows.yaml).
