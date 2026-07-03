# General Processes

> SAMPLE — Replace with your own process documentation.

## Feature Development Workflow

**Last updated**: 2026-07-03

### Standard flow

1. **Plan**: Use planner subagent to create implementation plan
2. **Branch**: `git checkout -b feat/JIRA-123-description`
3. **Implement**: Follow the plan, write code + tests
4. **Self-review**: Use code-reviewer subagent for initial review
5. **PR**: Push branch, create PR via github-cli-workflow skill
6. **Address feedback**: Iterate on review comments
7. **Merge**: Squash merge to main after approval
8. **Save**: Record learnings in knowledge base

### PR size guidelines

- Max 200 lines changed per PR
- If larger, split into stacked PRs
- Exceptions: generated code, large refactors with review agreement

## Release Process

**Last updated**: 2026-07-02

### Steps

1. Update CHANGELOG.md with new version section
2. Bump version in relevant config files
3. Create git tag: `git tag -a v1.2.0 -m "Release v1.2.0"`
4. Push tag: `git push origin v1.2.0`
5. CI builds and publishes artifacts
6. Create GitHub Release with changelog content
7. Announce in team channel

### Version scheme

Semantic versioning: MAJOR.MINOR.PATCH
- MAJOR: breaking changes
- MINOR: new features, backward compatible
- PATCH: bug fixes, backward compatible
