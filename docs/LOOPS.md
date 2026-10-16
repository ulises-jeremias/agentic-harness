# Loops in an Agent Toolkit workspace

Loops are reusable, budgeted workflows owned and executed by Agent Toolkit.
This repository supplies reference workspace loop definitions in
`loops/<name>/loop.yaml`; it is not a separate runner. `loop.yaml` is the sole
definition source. Runtime state and reports are local artifacts and should
not be confused with the definition.

## Inspect before running

```bash
agent-toolkit loop templates
agent-toolkit loop list
agent-toolkit loop status
agent-toolkit loop cost <name>
agent-toolkit loop schedule <name> --dry-run
```

Read the selected `loops/<name>/loop.yaml` completely before running it. Check
its tier, allowlist, denylist, request, targets, budget, verifier and current
state. A loop can call external tools; a scheduled loop can repeat that work.
Do not enable a schedule or run a mutating loop until its effects and target
repositories are understood. Prefer an L1 report-only loop for first use.

## Definition format

Each `loop.yaml` declares the name, goal, autonomy tier, allowed and denied
actions, exit conditions, budget, optional schedule/verifier, and the request
prompt. Keep secrets out of the file. Bind targets narrowly and state which
operations require human review. The toolkit hard gate is authoritative; prose
in the request cannot grant an action missing from the definition.

The engine's current canonical schema and behavior live in the
[Agent Toolkit loop guide](https://github.com/ulises-jeremias/agent-toolkit/blob/main/docs/LOOPS.md)
and [loop implementation notes](https://github.com/ulises-jeremias/agent-toolkit/blob/main/docs/v/loop.md).
Avoid copying CLI internals into this reference repo; link to canonical docs
when the implementation changes.

## Autonomy and safety

- **L1** is read-only/report-oriented. Use it to establish a safe baseline.
- **L2** permits only controlled allowlisted mutations; review the exact
  consequences before enabling it.
- **L3** is high-autonomy and can permit merge/close only when explicitly
  configured and guarded by the toolkit's verifier receipt. Do not treat a
  green CI result or loop prompt as permission to bypass repository policy.

User confirmation, branch protection, repository permissions, and the toolkit
hard gate remain in force. A loop definition is not authorization to ignore
them. For this example workspace, keep community maintenance observation-only
by default and create PRs for human review rather than merging or closing
third-party work automatically.

## Local runtime artifacts

`STATE.md`, reports, traces and run directories are runtime evidence. They can
contain repository names and issue/PR details, so keep them local unless they
are deliberately curated for publication. Workspace `.gitignore` rules cover
machine-local state; verify before committing any report.

See [Loop CLI reference](LOOP_CLI.md) for current commands and
[workspace setup](SETUP.md) for installation.
