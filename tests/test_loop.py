"""Tests for bin/loop CLI."""

import subprocess
import sys
from pathlib import Path

import pytest


BIN_DIR = Path(__file__).resolve().parent.parent / "bin"


def _run_loop(
    *args: str,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(BIN_DIR / "loop"), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else str(BIN_DIR.parent),
    )
    return result


def test_help() -> None:
    """--help should show usage with init, run, status, audit, cost, sync."""
    result = _run_loop("help")
    assert result.returncode == 0
    assert "init" in result.stdout
    assert "run" in result.stdout
    assert "status" in result.stdout
    assert "audit" in result.stdout
    assert "cost" in result.stdout


def test_no_args_shows_help() -> None:
    """No arguments should show usage."""
    result = _run_loop()
    assert result.returncode == 0
    assert "loop" in result.stdout.lower()


def test_status_no_loops(temp_workspace: Path) -> None:
    """status should work with empty loops directory."""
    result = _run_loop("status", cwd=temp_workspace)
    assert result.returncode == 0


def test_audit_missing_loop(temp_workspace: Path) -> None:
    """audit on non-existent loop should handle gracefully (returns 0)."""
    result = _run_loop("audit", "nonexistent", cwd=temp_workspace)
    assert result.returncode == 0


def test_cost_missing_loop(temp_workspace: Path) -> None:
    """cost on non-existent loop shows unknown estimate (returns 0)."""
    result = _run_loop("cost", "nonexistent", cwd=temp_workspace)
    assert result.returncode == 0


def test_templates_list() -> None:
    """templates should list real templates."""
    result = _run_loop("templates")
    assert result.returncode == 0
    # Should include at least one of the bundled templates
    assert "daily-triage" in result.stdout or "pr-babysitter" in result.stdout


def test_unknown_command() -> None:
    """Unknown commands should return error code 1."""
    result = _run_loop("nonexistent_command_xyz")
    assert result.returncode == 1


def test_init_missing_template(temp_workspace: Path) -> None:
    """init with non-existent template should fail gracefully."""
    result = _run_loop(
        "init", "nonexistent", "--template", "nonexistent",
        cwd=temp_workspace,
    )
    assert result.returncode != 0


def test_run_missing_loop(temp_workspace: Path) -> None:
    """run on non-existent loop should fail gracefully."""
    result = _run_loop("run", "nonexistent", cwd=temp_workspace)
    assert result.returncode != 0


def test_sync_no_loops(temp_workspace: Path) -> None:
    """sync with no loops should succeed."""
    result = _run_loop("sync", cwd=temp_workspace)
    assert result.returncode == 0
