# Performance & Scaling — agentic-harness

> Practical limits, token costs, and scaling recommendations for solo devs, small teams, and agencies.

---

## Repo Scale

### Recommended limits

| Profile | Max repos | Reasoning |
|---------|-----------|-----------|
| Solo developer | 10-20 | Comfortable for one person's active projects |
| Small team (3-5) | 20-50 | Each member has their own harness instance |
| Agency (10+ clients) | 50-100 | Use packs to load only active client repos |

### When to use project-indexer vs manual cloning

Use `project-indexer` when:
- You clone repos frequently
- You want automatic symlink management in `projects/`
- You're setting up a new harness instance

Clone manually when:
- You need custom clone options (shallow, single-branch)
- The repo requires SSH key selection per host
- You want to control the exact local path

### Large monorepo impact

Monorepos (>1GB, >10K files) don't directly impact harness performance since the harness doesn't index file contents. However:

- **workspace-context** reads project metadata only (not file contents)
- **project-indexer** clones once, manages symlinks thereafter
- **AI tools** may be slow indexing large repos; this is a tool issue, not a harness issue

---

## Knowledge Scale

### Token budget

`assistant-memory inject` outputs all knowledge entries to stdout. The AI tool reads this as context. Budget accordingly:

| Context window | Max knowledge entries | Total tokens |
|---------------|----------------------|-------------|
| 200K (Claude 3.5/4) | 50-100 | ~50K-100K for knowledge |
| 128K (GPT-4o) | 30-60 | ~30K-60K for knowledge |
| 32K (older models) | 10-20 | ~10K-20K for knowledge |

**Rule of thumb**: Keep knowledge entries under 50% of your context window. The other 50% is for AGENTS.md, pack context, and the actual task.

### Knowledge growth management

| Strategy | When to use |
|----------|------------|
| Archive stale entries | Entry > 90 days old and not referenced in last 10 sessions |
| Delete duplicates | Multiple entries describing the same pattern |
| Split large entries | Single entry > 5K characters |
| Use `search` instead of `inject` | Knowledge base > 50 entries |
| Filter by tag/category | Context window limited |

### Storage impact

Knowledge entries are plain Markdown files. Size estimates:

| Entries | Disk space | Git repo size |
|---------|-----------|---------------|
| 10 | ~50KB | ~200KB |
| 50 | ~250KB | ~1MB |
| 100 | ~500KB | ~2MB |
| 500 | ~2.5MB | ~10MB |

Git handles this well — knowledge is text, so delta compression is efficient.

---

## Loop Costs

### Cost formula

```
cost_per_run = (input_tokens × input_price) + (output_tokens × output_price)

monthly_cost = cost_per_run × runs_per_day × 30
```

### Example costs (Claude Sonnet 4, May 2026 pricing)

| Loop | Tier | Tokens/run | Runs/day | Monthly cost |
|------|------|-----------|----------|-------------|
| Daily issue triage | L1 | ~5K | 1 | ~$0.50 |
| PR babysitter (5 PRs) | L2 | ~15K | 4 | ~$6.00 |
| CI sweeper (3 repos) | L3 | ~30K | 12 | ~$36.00 |
| Dependency sweeper (5 repos) | L3 | ~40K | 1 | ~$4.00 |
| Changelog drafter | L2 | ~8K | 1 | ~$0.80 |

### Cost optimization

1. **Use smaller models for L1 loops**: L1 loops don't need reasoning — use Haiku or Flash
2. **Batch work**: Run PR reviews once every 4 hours, not on every commit
3. **Cache results**: If STATE.md hasn't changed since last run, skip with exit condition
4. **Use max_tokens limits**: Cap output tokens per loop to prevent runaway costs
5. **Monitor with `bin/loop cost`**: Review monthly and adjust

### Cost monitoring

```bash
# Per-loop cost estimate
bin/loop cost daily-triage --monthly

# Audit all loops
bin/loop audit --summary

# Set cost alert
bin/loop cost daily-triage --alert 5.00  # Alert if monthly exceeds $5
```

---

## Pack & Profile Scale

### Recommended limits

| Surface | Max recommended | Why |
|---------|----------------|-----|
| Active packs | 1 at a time | Context switching is explicit |
| Pack file size | 500KB | YAML parsing performance |
| Personas | 5-10 | Cognitive overhead for each |
| Profiles | 5-10 | Each is a pack + persona combo |
| Repos per pack | 5-10 | Loading too many repos dilutes focus |

### Context snapshot size

`workspace-context` generates a snapshot of all loaded context. Snapshot size grows with:

- Number of active repos (each adds project metadata)
- Knowledge base size (`inject` adds all entries)
- Persona complexity (larger allow/deny lists)

Typical snapshot: **5-15KB** for a solo dev setup. Agency setups with 10 repos and 50 knowledge entries: **30-50KB**.

---

## Tool-Specific Limits

| AI tool | Context limit | Best for |
|---------|-------------|----------|
| Claude Code (Sonnet 4) | 200K | Full harness with large knowledge base |
| opencode (GPT-4o) | 128K | Medium knowledge base, focused tasks |
| Cursor | 128K | Interactive development, smaller knowledge |
| GitHub Copilot | 32K (inline) | Light context, single-task focus |
| Gemini CLI (2.5 Pro) | 1M | Largest knowledge bases, multi-repo |

---

## Scaling Checklist

### For solo developers
- [ ] Keep knowledge/ under 50 entries
- [ ] Archive stale entries monthly
- [ ] Use 3-5 personas max
- [ ] Run loops on schedule, not continuously

### For small teams (3-5)
- [ ] Each member forks their own harness
- [ ] Share packs via the project repo (not knowledge/)
- [ ] Document team-wide conventions in AGENTS.md
- [ ] One member runs L2+ loops (not everyone)

### For agencies (10+ clients)
- [ ] One pack per client
- [ ] Per-client LLM policies (strict mode)
- [ ] Per-client env.d/ files
- [ ] Audit knowledge/ weekly for cross-client contamination
- [ ] Rotate loop contexts with workspace-context load
