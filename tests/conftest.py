"""Shared fixtures for harness CLI tests."""

import os
import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_workspace() -> Path:
    """Create a temporary workspace directory mimicking the harness structure."""
    tmp = Path(tempfile.mkdtemp(prefix="harness-test-"))
    (tmp / "loops").mkdir()
    (tmp / "templates" / "loops").mkdir(parents=True)
    (tmp / "knowledge" / "learnings").mkdir(parents=True)
    (tmp / "knowledge" / "processes").mkdir(parents=True)
    (tmp / "knowledge" / "todos").mkdir(parents=True)
    (tmp / "packs").mkdir()
    (tmp / "personas").mkdir()
    (tmp / "schemas").mkdir()
    (tmp / "templates" / "jobs").mkdir(parents=True)

    # Create a minimal knowledge entry
    (tmp / "knowledge" / "learnings" / "general.md").write_text(
        "---\ntype: learning\ndate: 2026-07-01\n---\n\n# Test Learning\n\nThis is a test pattern.\n",
        encoding="utf-8",
    )
    (tmp / "knowledge" / "README.md").write_text(
        "# Knowledge Base\n\nTest knowledge base.\n", encoding="utf-8",
    )

    yield tmp

    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def temp_workspace_with_loop(temp_workspace: Path) -> Path:
    """Create a workspace with a sample loop initialized."""
    loop_dir = temp_workspace / "loops" / "test-loop"
    loop_dir.mkdir()

    (loop_dir / "LOOP.md").write_text(
        """---
name: test-loop
description: "Test loop for automated tests"
tier: L1
cadence: 1d
allowlist: []
deny:
  - merge
  - close
  - push
exit_conditions:
  - goal_met
  - budget_exhausted
budget:
  max_tokens: 1000
  max_runs_per_day: 1
  max_wall_seconds: 60
request: |
  Test loop — do nothing.
---
""",
        encoding="utf-8",
    )

    (loop_dir / "STATE.md").write_text(
        """---
loop: test-loop
last_run: "2026-07-01T09:00:00Z"
last_exit_code: 0
total_runs: 1
successful_runs: 1
failed_runs: 0
total_tokens: 100
total_cost: 0.01
---
""",
        encoding="utf-8",
    )

    # Create a template
    template_dir = temp_workspace / "templates" / "loops"
    (template_dir / "test-template.yaml").write_text(
        """name: test-template
description: "Test template"
tier: L1
cadence: 1d
budget:
  max_tokens: 1000
  max_runs_per_day: 1
  max_wall_seconds: 60
request: "Test loop"
""",
        encoding="utf-8",
    )

    return temp_workspace


@pytest.fixture
def harness_bin_dir() -> Path:
    """Path to the real harness bin/ directory."""
    return Path(__file__).resolve().parent.parent / "bin"
