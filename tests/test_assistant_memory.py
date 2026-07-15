"""Tests for bin/assistant-memory CLI."""

import subprocess
import sys
from pathlib import Path

import pytest


def _run_memory(
    *args: str,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    bin_path = Path(__file__).resolve().parent.parent / "bin" / "assistant-memory"
    test_env = {"HARNESS_DIR": str(cwd)} if cwd else {}
    result = subprocess.run(
        [sys.executable, str(bin_path), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
        env={**__import__("os").environ, **test_env},
    )
    return result


def test_no_args_shows_help(temp_workspace: Path) -> None:
    """Running without arguments should show usage."""
    result = _run_memory(cwd=temp_workspace)
    assert result.returncode == 0
    assert "Types for add:" in result.stdout


def test_inject_outputs_context(temp_workspace: Path) -> None:
    """inject should output knowledge context markers."""
    result = _run_memory("inject", cwd=temp_workspace)
    assert result.returncode == 0
    assert "assistant-memory inject" in result.stdout


def test_search_found(temp_workspace: Path) -> None:
    """search should find existing knowledge."""
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


def test_inject_after_add_contains_learning(temp_workspace: Path) -> None:
    """After adding a learning, inject should include it."""
    _run_memory("add", "--type", "learning", "UniquePatternXYZ123", cwd=temp_workspace)
    result = _run_memory("inject", cwd=temp_workspace)
    assert "UniquePatternXYZ123" in result.stdout
