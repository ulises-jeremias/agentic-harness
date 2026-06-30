# Personas

> Work mode definitions that constrain AI behavior in a session.

---

## What are Personas?

Personas define **what the AI does** (not who it is). They are constraint sets:

- `implementer` — write code, bias toward action
- `reviewer` — analyze and report, no changes
- `researcher` — explore and summarize, no implementation
- `architect` — design and tradeoffs, no code
- `writer` — documentation and prose only

Activating a persona prevents scope creep. If you want a review, you don't want the AI to also start refactoring.

---

## Available Personas

| Persona | Constraint | Best for |
|---------|-----------|----------|
| `implementer` | Write code, no long analysis | Feature work, fixes |
| `reviewer` | Read and report, no changes | Code review, audits |
| `researcher` | Explore only, no implementation | Discovery, R&D |
| `architect` | Design and options, no code | System design, ADRs |
| `writer` | Docs only, no code | READMEs, runbooks, ADRs |

---

## Usage

### Activate a persona

```bash
./bin/workspace-context use-persona reviewer
```

This writes `.active-persona` to the workspace root, which `workspace-context` snapshots at session start.

### Persona enforcement

When a persona is active, `workspace-context` emits a `<persona-constraints>`
block in the session snapshot with the persona's allow/deny lists, output
format, and handoff rules:

```xml
<persona-constraints>
    persona: implementer
    allow: [read, write, commit, run_commands, create_pr]
    deny: [design]
    output_format: code
    handoffs:
      - when: "task requires architectural decisions"
        to: architect
      - when: "result needs review"
        to: reviewer
</persona-constraints>
```

The AI tool **must respect this block** — it defines the operational
boundaries for the current session.

### List available personas

```bash
./bin/workspace-context personas
```

### Deactivate

```bash
rm .active-persona
```

### In a conversation

You can also just say: *"Use the reviewer persona for this task"* — the AI reads the persona file and applies its constraints.

---

## Creating a Custom Persona

```bash
cat > personas/my-persona.md << 'EOF'
# My Persona

> One-line description of what this persona does.

---

## Constraints

- **Do**: ...
- **Do not**: ...

## Behavior

- ...

## Output Format

- ...

## Handoffs

- When X happens → switch to `other-persona`
EOF
```

---

## Persona Design Principles

1. **Constraints first** — define what the AI must NOT do, not just what it should do
2. **No identity framing** — avoid "you are a senior engineer" — use "analyze and report, no changes"
3. **Clear handoffs** — define when to switch personas or delegate to subagents
4. **Output format** — specify what good output looks like
