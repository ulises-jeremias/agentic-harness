# Security Model — agentic-harness

> How the harness handles secrets, credentials, and sensitive context across all layers.

---

## Credential Storage

### Environment variables

API keys and tokens are stored in `~/.config/agentic-workstation/env.d/<client>.env` and loaded via `dots-loadenv` (from agentic-workstation). These files are:

- **Outside the harness repository** — never git-tracked
- **Sourced at session start** — loaded into shell environment only
- **Per-client** — isolated per engagement to prevent cross-contamination

Example env file (`~/.config/agentic-workstation/env.d/acme.env`):

```bash

export ANTHROPIC_API_KEY="sk-ant-..."
export JIRA_API_TOKEN="..."
export JIRA_EMAIL="dev@acme.com"
export JIRA_URL="https://acme.atlassian.net"

```

### `.gitignore` protections

The harness `.gitignore` prevents accidental credential commits:

| Pattern | Protects |
|---------|----------|
| `.env` / `.env.*` | Local environment files |
| `env.d/` | Agentic-workstation env directory |
| `*.log` / `*.tmp` | Temporary files that may contain session data |
| `repos/` / `projects/` | Cloned repositories (may contain their own secrets) |
| `*.key` / `*.pem` / `*.p12` | Private keys and certificates |
| `credentials*` | Any file with "credentials" in the name |

### Credential boundaries

Never reference credentials in:

- `knowledge/` entries — the AI may repeat them
- `packs/*.yaml` — packs may be shared between environments
- `personas/*.md` — personas are loaded into AI context
- Job descriptions passed to `devcompanion queue`

Always use environment variable names (e.g., `$JIRA_API_TOKEN`) in context files.

---

## Knowledge Hygiene

### What belongs in knowledge/

| Safe to store | Avoid storing |
|---------------|---------------|
| Code patterns and conventions | API keys and tokens |
| Process workflows | Password hashes or secrets |
| Bug workarounds and gotchas | Personal identifiable information (PII) |
| Tool configuration preferences | Proprietary business logic (without client approval) |
| Project-specific naming rules | Internal URLs with credentials in query strings |

### Knowledge review checklist

Before committing knowledge entries, verify:

- [ ] Contains no credentials, tokens, or API keys
- [ ] Contains no PII (names, emails, phone numbers from client systems)
- [ ] References environment variables, not literal secrets
- [ ] Describes patterns, not proprietary algorithms
- [ ] Would be safe to share with a new team member

---

## Persona Guardrails

Personas constrain what the AI can do. Each persona declares:

```yaml

allow:

  - read_files
  - search_code
deny:

  - execute_commands
  - write_files
  - network_access
handoff:
  trigger: "when task requires implementation"
  target: "implementer"

```

### How guardrails prevent data exposure

| Persona | Read files | Execute commands | Write files | API calls |
|----------|-----------|-----------------|-------------|-----------|
| Researcher | Yes | No | No | No |
| Reviewer | Yes | No | No | No |
| Implementer | Yes | Yes | Yes | Limited |
| Architect | Yes | No | Yes (docs only) | No |

The `researcher` and `reviewer` personas have **no execution capability** — they cannot run commands that might leak data or make destructive changes.

---

## LLM Isolation

### Per-pack LLM policies

Each pack can declare an LLM policy:

```yaml

llm:
  allowlist:

    - anthropic
  deny list:

    - openai
  strict: true

```

When a pack with strict LLM policy is active:

1. The harness enforces the policy for all AI operations
2. `devcompanion` jobs respect the policy
3. Cross-client contamination is prevented — Acme's data never goes to Startup X's provider

### Audit trail

All `devcompanion` jobs log LLM policy decisions to `~/.local/share/agentic-workstation/dev-companion/logs/llm-audit.log`:

```json

{
  "job_id": "abc123",
  "pack": "acme-corp",
  "policy": "anthropic-only",
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "timestamp": "2026-07-03T14:00:00Z"
}

```

---

## Loop Safety

### Tier system

| Tier | Writes | PRs | Comments | Risk |
|------|-------|-----|----------|------|
| L1 | None | No | No | Safe: read-only report |
| L2 | Draft only | Draft only | Draft only | Guarded: human approval required |
| L3 | Yes | Yes | Yes | Automated: requires maker/checker pattern |

### Exit conditions as safety net

Every loop declares exit conditions that stop execution:

```yaml

exit:

  - condition: "cost_exceeds 5.00"
    action: "pause"

  - condition: "error_rate > 0.1"
    action: "stop"

  - condition: "consecutive_failures > 3"
    action: "stop_and_alert"

```

### Loop credential isolation

Loops never have direct access to the harness's environment variables. They inherit the shell environment at run time, so schedule loops with explicit environment:

```bash

# systemd service file
[Service]
EnvironmentFile=%h/.config/agentic-workstation/env.d/acme.env
ExecStart=%h/.ai-workspace/bin/loop run daily-triage

```

---

## Threat Model

### What an attacker with harness access could do

| Access level | Risk | Mitigation |
|-------------|------|-----------|
| Read `knowledge/` | Learn project patterns and processes | Knowledge hygiene checklist (above) |
| Read `packs/` | Discover repo URLs and project IDs | Don't put secrets in packs |
| Execute `bin/loop` | Run autonomous loops with your credentials | Loop tier system prevents destructive L3 loops |
| Execute `bin/devcompanion` | Queue jobs that consume API tokens | LLM policy per pack prevents unauthorized provider use |
| Write to `knowledge/` | Inject malicious patterns into future sessions | Review knowledge entries before committing |

### What the harness CANNOT protect against

- **Compromised host machine**: If an attacker has shell access, they can read env vars directly
- **Malicious AI tool extensions**: Plugins/extensions that exfiltrate data outside the harness
- **Social engineering**: The harness can't prevent you from sharing secrets in chat
- **Zero-day exploits in AI tool CLIs**: The harness doesn't sandbox the AI tool process

---

## Responsible Disclosure

If you discover a security vulnerability in agentic-harness:

1. Do not open a public issue
2. Report via [GitHub private vulnerability reporting](https://github.com/ulises-jeremias/agentic-harness/security/advisories/new)
3. Include: affected component, reproduction steps, impact assessment
