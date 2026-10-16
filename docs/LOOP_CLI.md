# Agent Toolkit loop CLI

Agent Toolkit is the canonical loop implementation. This page keeps the
workspace's quick reference short; use the installed CLI's `--help` and the
[upstream loop guide](https://github.com/ulises-jeremias/agent-toolkit/blob/main/docs/LOOPS.md)
as the authority for version-specific behavior.

```bash
agent-toolkit loop help
agent-toolkit loop templates
agent-toolkit loop list
agent-toolkit loop status [name]
agent-toolkit loop cost <name>
agent-toolkit loop audit [name]
```

Create a loop from a bundled template, then inspect the generated
`loops/<name>/loop.yaml` before any execution:

```bash
agent-toolkit loop init <template> --name <name>
```

Run only after reviewing the definition, target scope, tier, budget and
allowlist. To ensure no LLM runner is invoked, use `--no-llm`; it selects the
skeleton runner and does not submit prompts to a model:

```bash
agent-toolkit loop run <name> --no-llm
```

Preview scheduling without installing a timer:

```bash
agent-toolkit loop schedule <name> --dry-run
```

Scheduling creates a recurring local systemd/launchd job (or a GitHub Actions
workflow when explicitly selected). Review the generated command and intended
frequency before applying it. Do not assume a scheduled run is harmless: the
loop's own allowlist and verifier still govern each iteration.

The current command surface includes `init`, `run`, `list`, `status`, `audit`,
`cost`, `schedule`, `sync`, `templates`, and `help`. Flags vary by subcommand
and toolkit version, so query the installed binary rather than relying on
older examples in this reference workspace.
