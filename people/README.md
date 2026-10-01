# People

Durable collaborators for this workspace. A Person is a character you have
chosen and reviewed, not a running session and not an agent definition.

Create one JSON file per person:

```json
{
  "spec": "agent-toolkit/person@1",
  "id": "reviewer-name",
  "name": "Reviewer Name",
  "role": "reviewer",
  "goal": "Review code changes with care.",
  "archived": false
}
```

Validate with: `python3 scripts/validate-people.py --workspace .`

Optional role preferences live in `people/bindings.yaml`. Schemas are mirrored
from the agent-toolkit contract; see `schemas/people-contracts.lock.json`.
