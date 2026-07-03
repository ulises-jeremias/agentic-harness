# Multi-Client Setup Tutorial — agentic-harness

> How to manage multiple clients, repos, and tools with isolated context and LLM policies.

**Time to complete**: ~30 minutes
**Prerequisites**: Completed "Your First PR" tutorial, multiple client projects

---

## Scenario

You're a freelancer or agency developer managing 3 clients:

| Client | Repos | Ticketing | LLM Policy |
|--------|-------|-----------|------------|
| Acme Corp | `acme/backend`, `acme/frontend` | Jira (ACME) | Anthropic only |
| Startup X | `startupx/api` | ClickUp (space 123) | Any provider |
| Agency Y (internal) | `agency/tooling` | GitHub Issues | OpenCode |

Each client has different tools, credentials, and compliance requirements. The harness keeps them isolated.

---

## Setup

### Step 1: Configure per-client credentials

Create env files for each client:

```bash
mkdir -p ~/.config/agentic-workstation/env.d
```

**`~/.config/agentic-workstation/env.d/acme.env`**:

```bash
export ANTHROPIC_API_KEY="sk-ant-acme-..."
export JIRA_API_TOKEN="..."
export JIRA_EMAIL="dev@acme.com"
export JIRA_URL="https://acme.atlassian.net"
```

**`~/.config/agentic-workstation/env.d/startupx.env`**:

```bash
export OPENAI_API_KEY="sk-startupx-..."
export CLICKUP_API_TOKEN="pk_..."
export CLICKUP_TEAM_ID="..."
```

**`~/.config/agentic-workstation/env.d/agency.env`**:

```bash
# Uses default gh auth — no extra env needed
```

### Step 2: Clone client repos

```bash
# Acme repos
./bin/project-indexer clone acme-corp/backend
./bin/project-indexer clone acme-corp/frontend

# Startup X repo
./bin/project-indexer clone startupx/api

# Agency repo (already local)
./bin/project-indexer link ~/projects/agency-tooling agency/tooling
```

Verify:

```bash
./bin/project-indexer list
```

```text
projects/
├── acme-backend -> repos/github.com/acme-corp/backend
├── acme-frontend -> repos/github.com/acme-corp/frontend
├── startupx-api -> repos/github.com/startupx/api
└── agency-tooling -> repos/github.com/agency/tooling
```

### Step 3: Create per-client packs

**`packs/acme-corp.yaml`**:

```yaml
name: acme-corp
repos:
  - name: backend
    path: projects/acme-backend
    primary: true
  - name: frontend
    path: projects/acme-frontend
conventions:
  commits: conventional-commits
  branch: feat/ACME-123-description
  language: python
  framework: fastapi
tools:
  ticketing: jira
  jira_project: ACME
  jira_url: "${JIRA_URL}"
llm:
  allowlist:
    - anthropic
  strict: true
env_file: acme.env
```

**`packs/startup-x.yaml`**:

```yaml
name: startup-x
repos:
  - name: api
    path: projects/startupx-api
    primary: true
conventions:
  commits: conventional-commits
  branch: feature/description
  language: typescript
  framework: express
tools:
  ticketing: clickup
  clickup_space: "123"
  clickup_team: "${CLICKUP_TEAM_ID}"
llm:
  allowlist:
    - anthropic
    - openai
  strict: false
env_file: startupx.env
```

**`packs/agency.yaml`**:

```yaml
name: agency
repos:
  - name: tooling
    path: projects/agency-tooling
    primary: true
conventions:
  commits: conventional-commits
  branch: feat/description
  language: python
tools:
  ticketing: github
env_file: agency.env
```

---

## Daily Workflow

### Morning: Acme Corp

```bash
# Load Acme credentials
source ~/.config/agentic-workstation/env.d/acme.env

# Load Acme context
./bin/workspace-context load --pack packs/acme-corp.yaml

# Verify
./bin/workspace-context
```

Expected output:

```text
Active pack: acme-corp
Repos: backend (primary), frontend
LLM policy: anthropic only (strict)
Ticketing: Jira (ACME)
```

Start your AI tool. Tell it:

```text
Load workspace context. Check Jira for my assigned ACME tasks.
```

The AI uses the Jira skill with ACME project context — it won't accidentally query Startup X's ClickUp.

### Midday: Startup X

```bash
# Switch credentials
source ~/.config/agentic-workstation/env.d/startupx.env

# Switch context
./bin/workspace-context load --pack packs/startup-x.yaml
```

The AI now sees Startup X's repos, ClickUp space, and TypeScript conventions. Acme's Jira context is gone.

### Afternoon: Agency (internal)

```bash
source ~/.config/agentic-workstation/env.d/agency.env
./bin/workspace-context load --pack packs/agency.yaml
```

---

## LLM Policy Enforcement

### Why per-client policies matter

Without LLM policies, the harness might:

- Send Acme's proprietary code to OpenAI (if Acme requires Anthropic only)
- Use the wrong API key for a client
- Mix Startup X's context with Acme's context

### Strict mode example

Acme's pack has `strict: true` and `allowlist: [anthropic]`. If `devcompanion` tries to use OpenAI:

```text
Error: policy_no_provider_available
Active pack 'acme-corp' requires Anthropic only.
Available providers: anthropic.
Requested: openai. Blocked by strict mode.
```

### Verifying policy

```bash
./bin/devcompanion llm-status
```

```text
Active pack: acme-corp
LLM policy: allowlist=[anthropic], strict=true
Active provider: anthropic (claude-sonnet-4-20250514)
Status: OK — requests will use Anthropic
```

---

## Loop Per Client

Each client gets their own loop directory:

```text
loops/
├── acme/
│   ├── daily-triage/
│   └── pr-babysitter/
├── startupx/
│   ├── daily-triage/
│   └── ci-sweeper/
└── agency/
    └── changelog-drafter/
```

### Scheduling per client

```bash
# Acme loops run in business hours (UTC-5)
./bin/loop schedule acme/daily-triage --cron "0 9 * * 1-5"
./bin/loop schedule acme/pr-babysitter --cron "0 */4 * * 1-5"

# Startup X runs 24/7 (global team)
./bin/loop schedule startupx/daily-triage --cron "0 8 * * *"
./bin/loop schedule startupx/ci-sweeper --cron "0 */2 * * *"

# Agency runs weekly
./bin/loop schedule agency/changelog-drafter --cron "0 9 * * 1"
```

Each loop must be configured to source the correct env file before execution. Edit the systemd service file:

```ini
[Service]
EnvironmentFile=%h/.config/agentic-workstation/env.d/acme.env
ExecStart=%h/.ai-workspace/bin/loop run acme/daily-triage
```

---

## Cost Tracking Per Client

```bash
# Per-client loop cost
./bin/loop cost acme/daily-triage --monthly
./bin/loop cost startupx/daily-triage --monthly

# All loops for one client
./bin/loop audit acme --summary

# Agency-wide total
for client in acme startupx agency; do
  echo "=== $client ==="
  ./bin/loop cost "$client" --monthly --summary
done
```

---

## Secrets Management

### What NEVER goes in packs

- API keys, tokens, passwords
- Client-specific URLs with credentials
- Internal IP addresses (if sensitive)

### What goes in env.d/ files

- API keys and tokens
- OAuth client secrets
- Service account credentials

### What goes in packs

- Repo URLs (public)
- Project IDs (Jira project key, ClickUp space ID)
- Conventions and preferences
- LLM provider preferences (not API keys)

### Security checklist

- [ ] env.d/ files are in `.gitignore`
- [ ] Packs reference `$VARIABLE` names, not literal values
- [ ] LLM audit log reviewed weekly for cross-client contamination
- [ ] Knowledge entries reviewed for client-specific PII before committing
- [ ] Each client has a unique env file (not sharing `default.env`)

---

## Troubleshooting

### "Wrong Jira project loaded"

Your pack's `jira_project` is incorrect, or you loaded the wrong pack. Verify:

```bash
./bin/workspace-context | grep jira
```

### "LLM policy blocks my provider"

The active pack restricts providers. Options:

1. Edit the pack's `llm.allowlist` to add your provider
2. Load a different pack without restrictions
3. Set `llm.strict: false` for development (not recommended for production)

### "Loop ran against the wrong client"

The loop's scheduled service doesn't source the right env file. Edit the systemd service file and add the correct `EnvironmentFile=` directive.
