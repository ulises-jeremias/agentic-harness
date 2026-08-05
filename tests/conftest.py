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
def harness_bin_dir() -> Path:
    """Path to the real harness bin/ directory."""
    return Path(__file__).resolve().parent.parent / "bin"
