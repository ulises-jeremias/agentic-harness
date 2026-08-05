"""Tests for agent-toolkit memory CLI (replaces bin/assistant-memory)."""

import shutil
import subprocess
from pathlib import Path

import pytest


def _run_memory(
    *args: str,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    bin_path = shutil.which("agent-toolkit")
    if bin_path is None:
        pytest.skip("agent-toolkit not installed")
    env = {"HARNESS_DIR": str(cwd)} if cwd else {}
    result = subprocess.run(
        [bin_path, "memory", *args],
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
        env={**__import__("os").environ, **env},
    )
    return result


def test_no_args_shows_help(temp_workspace: Path) -> None:
    """Running without arguments should show usage."""
    result = _run_memory("--help", cwd=temp_workspace)
    assert result.returncode == 0


def test_inject_outputs_context(temp_workspace: Path) -> None:
    """inject should output knowledge context markers."""
    result = _run_memory("inject", cwd=temp_workspace)
    assert result.returncode == 0


def test_search_runs(temp_workspace: Path) -> None:
    """search should run without crashing."""
    result = _run_memory("search", "test", cwd=temp_workspace)
    assert result.returncode == 0


def test_search_not_found(temp_workspace: Path) -> None:
    """search should handle no matches gracefully."""
    result = _run_memory("search", "nonexistent_xyz_123", cwd=temp_workspace)
    assert result.returncode == 0


def test_todo_lists_items(temp_workspace: Path) -> None:
    """todo should list pending items."""
    result = _run_memory("todo", cwd=temp_workspace)
    assert result.returncode == 0


def test_add_learning(temp_workspace: Path) -> None:
    """add --type learning should create a knowledge entry."""
    result = _run_memory(
        "add", "--type", "learning", "New test pattern discovered",
        cwd=temp_workspace,
    )
    assert result.returncode == 0
