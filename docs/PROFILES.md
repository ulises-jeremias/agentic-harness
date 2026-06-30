# Session Profiles

> Composable profiles that bundle a pack, persona, and optional skills into a
> single loadable unit — one command to set up a full session context.

---

## Concept

A **profile** replaces the two-step "load pack + use persona" flow with a
single command:

```bash
# Before profiles
workspace-context load packs/oss.yaml
workspace-context use-persona implementer

# With profiles
workspace-context load --profile oss-contrib
```

Profiles are YAML files in `profiles/*.yaml` that declare:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✓ | Kebab-case identifier (matches filename) |
| `description` | | One-line summary |
| `persona` | | Persona to activate |
| `pack` | | Pack name to load |
| `skills` | | Extra skill names to note |
| `loops` | | Loop names to associate |

---

## Usage

```bash
# List available profiles
workspace-context profiles

# Load a profile (activates pack + persona together)
workspace-context load --profile <name>
```

---

## Creating a profile

```yaml
# profiles/my-client.yaml
name: my-client
description: Delivery sessions for Acme Corp
pack: acme          # loads packs/acme.yaml
persona: implementer
skills:
  - github-cli-workflow
  - clickup-cli
loops:
  - pr-babysitter
```

Validate the profile:

```bash
# Profile YAML is validated by check-yaml pre-commit hook automatically
pre-commit run check-yaml --files profiles/my-client.yaml
```

---

## Persona transition log

Every time you switch personas (via `workspace-context use-persona`), the
transition is appended to `.persona-history`:

```text
2026-06-30T10:00:00Z transition: reviewer → implementer
```

`.persona-history` is gitignored (it contains machine-local session state).

---

## Bundled profiles

| Profile | Persona | Pack | Description |
|---------|---------|------|-------------|
| `oss-contrib` | implementer | — | OSS contribution sessions (fork → PR) |

---

## Schema

Profile files are validated against `schemas/profile.schema.json`.

```json
{
  "name": "my-profile",
  "description": "...",
  "persona": "implementer",
  "pack": "my-pack",
  "skills": ["github-cli-workflow"],
  "loops": ["pr-babysitter"]
}
```

See `schemas/profile.schema.json` for the full schema.
