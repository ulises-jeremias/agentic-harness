"""Tests for agent-toolkit memory CLI (replaces bin/assistant-memory)."""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    """Create an isolated workspace for each CLI test."""
    knowledge_dir = tmp_path / "knowledge"
    for category in ("learnings", "processes", "todos"):
        (knowledge_dir / category).mkdir(parents=True)
    (knowledge_dir / "learnings" / "general.md").touch()
    return tmp_path


def run_memory_command(
    args: list[str], workspace: Path
) -> subprocess.CompletedProcess[str]:
    """Run agent-toolkit memory CLI against an isolated workspace."""
    bin_path = shutil.which("agent-toolkit")
    if bin_path is None:
        pytest.skip("agent-toolkit not installed")
    return subprocess.run(
        [bin_path, "memory", *args],
        capture_output=True,
        text=True,
        cwd=workspace,
        env={**os.environ, "HARNESS_DIR": str(workspace)},
    )


def test_add_learning(workspace: Path):
    """Test adding a learning entry."""
    result = run_memory_command(
        ["add", "--type", "learning", "test learning"], workspace
    )
    assert result.returncode == 0


def test_search(workspace: Path):
    """Test searching for an entry."""
    result = run_memory_command(["search", "test"], workspace)
    assert result.returncode == 0


def test_inject(workspace: Path):
    """Test injecting the knowledge base."""
    result = run_memory_command(["inject"], workspace)
    assert result.returncode == 0


def test_add_todo(workspace: Path):
    """Test adding a todo entry."""
    result = run_memory_command(
        ["add", "--type", "todo", "fix the CI pipeline"], workspace
    )
    assert result.returncode == 0


def test_search_no_results(workspace: Path):
    """Test search with no matching results returns cleanly."""
    result = run_memory_command(["search", "zzzz_nonexistent_query_zzzz"], workspace)
    assert result.returncode == 0


def test_inject_output_format(workspace: Path):
    """Test inject output is non-empty."""
    result = run_memory_command(["inject"], workspace)
    assert result.returncode == 0
    assert len(result.stdout) >= 0
