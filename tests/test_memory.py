import os
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).parent.parent
BIN_PATH = REPO_ROOT / "bin" / "assistant-memory"


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
    """Run the assistant-memory CLI against an isolated workspace."""
    return subprocess.run(
        [sys.executable, str(BIN_PATH), *args],
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
    assert "Added learning" in result.stdout

    content = (workspace / "knowledge" / "learnings" / "general.md").read_text()
    assert "test learning" in content


def test_search(workspace: Path):
    """Test searching for an entry without relying on test order."""
    run_memory_command(["add", "--type", "learning", "test learning"], workspace)
    result = run_memory_command(["search", "test"], workspace)
    assert result.returncode == 0
    assert "test learning" in result.stdout


def test_review_stale(workspace: Path):
    """Test reviewing stale entries."""
    result = run_memory_command(["review", "--stale"], workspace)
    assert result.returncode == 0


def test_inject(workspace: Path):
    """Test injecting the knowledge base."""
    result = run_memory_command(["inject"], workspace)
    assert result.returncode == 0


def test_add_duplicate(workspace: Path):
    """Test adding a duplicate entry."""
    run_memory_command(["add", "--type", "learning", "duplicate entry"], workspace)
    result = run_memory_command(
        ["add", "--type", "learning", "duplicate entry"], workspace
    )
    assert result.returncode == 0
    content = (workspace / "knowledge" / "learnings" / "general.md").read_text()
    assert content.count("duplicate entry") == 2


def test_add_with_special_characters(workspace: Path):
    """Test adding an entry with special characters."""
    special_string = "!@#$%^&*()_+-=[]{};':\",./<>?`~"
    result = run_memory_command(
        ["add", "--type", "learning", special_string], workspace
    )
    assert result.returncode == 0
    content = (workspace / "knowledge" / "learnings" / "general.md").read_text()
    assert special_string in content


def test_empty_knowledge_base(tmp_path: Path):
    """Test commands against an empty (non-existent) knowledge directory."""
    result = run_memory_command(["search", "nonexistent"], tmp_path)
    assert result.returncode == 0


def test_add_todo(workspace: Path):
    """Test adding a todo entry."""
    result = run_memory_command(
        ["add", "--type", "todo", "fix the CI pipeline"], workspace
    )
    assert result.returncode == 0
    assert "Added todo" in result.stdout

    content = (workspace / "knowledge" / "todos" / "pending.md").read_text()
    assert "fix the CI pipeline" in content


def test_inject_output_format(workspace: Path):
    """Test inject output contains expected structure."""
    result = run_memory_command(["inject"], workspace)
    assert result.returncode == 0
    assert len(result.stdout) > 0


def test_search_no_results(workspace: Path):
    """Test search with no matching results returns cleanly."""
    result = run_memory_command(["search", "zzzz_nonexistent_query_zzzz"], workspace)
    assert result.returncode == 0


def test_review_stale_output(workspace: Path):
    """Test review --stale output format."""
    result = run_memory_command(["review", "--stale"], workspace)
    assert result.returncode == 0


def test_add_process(workspace: Path):
    """Test adding a process entry."""
    result = run_memory_command(
        ["add", "--type", "process", "deploy to production"], workspace
    )
    assert result.returncode == 0
    assert "Added process" in result.stdout

    content = (workspace / "knowledge" / "processes" / "general.md").read_text()
    assert "deploy to production" in content
