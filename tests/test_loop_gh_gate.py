"""Tests for bin/loop-gh-gate hard autonomy gate."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest


BIN_DIR = Path(__file__).resolve().parent.parent / "bin"
GATE = BIN_DIR / "loop-gh-gate"


def _load_gate():
    import runpy
    return runpy.run_path(str(GATE))


@pytest.fixture
def gate():
    return _load_gate()


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["pr", "merge", "250", "--repo", "o/r", "--squash"], "merge"),
        (["pr", "close", "12", "--repo", "o/r"], "close"),
        (["pr", "comment", "1", "--body", "hi"], "comment"),
        (["issue", "edit", "5", "--add-assignee", "bob"], "assign"),
        (["pr", "edit", "3", "--add-label", "bug"], "label"),
        (["pr", "review", "3", "--approve"], "approve"),
        (["pr", "list", "--repo", "o/r"], None),
        (["api", "repos/o/r/pulls/1"], None),
        (["api", "-X", "POST", "repos/o/r/issues/1/comments"], "comment"),
    ],
)
def test_classify_gh_argv(gate, argv, expected) -> None:
    action, _meta = gate["classify_gh_argv"](argv)
    assert action == expected


def test_evaluate_tier_rules(gate) -> None:
    assert gate["evaluate_action"]("merge", tier="L1", allowlist=["merge"], deny=[])[0] is False
    assert gate["evaluate_action"]("merge", tier="L2", allowlist=["merge"], deny=[])[0] is False
    assert gate["evaluate_action"]("comment", tier="L2", allowlist=["comment"], deny=[])[0] is True
    assert gate["evaluate_action"]("merge", tier="L3", allowlist=["merge"], deny=[])[0] is True
    assert gate["evaluate_action"]("merge", tier="L3", allowlist=["merge"], deny=["merge"])[0] is False
    assert gate["evaluate_action"]("comment", tier="L3", allowlist=["merge"], deny=[])[0] is False


def test_merge_requires_receipt(gate, tmp_path: Path) -> None:
    run = tmp_path / "run"
    run.mkdir()
    env = gate["install_gh_shim"](
        run,
        tier="L3",
        allowlist=["merge", "close"],
        deny=["push"],
        verifier="test-verifier",
        gate_script=GATE,
    )
    for key, value in env.items():
        if key.startswith("LOOP_GATE_") or key == "PATH":
            os.environ[key] = value

    ok, reason, action, _meta = gate["check_command"](
        ["pr", "merge", "9", "--repo", "acme/demo"],
    )
    assert action == "merge"
    assert ok is False
    assert "receipt" in reason

    receipt = {
        "action": "merge",
        "repo": "acme/demo",
        "number": 9,
        "approved": True,
        "verifier": "test-verifier",
        "rationale": "CI green dependabot",
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    (run / "verifier-receipts" / "m9.json").write_text(json.dumps(receipt), encoding="utf-8")

    ok, reason, action, _meta = gate["check_command"](
        ["pr", "merge", "9", "--repo", "acme/demo"],
    )
    assert ok is True


def test_shim_denies_with_exit_78(gate, tmp_path: Path) -> None:
    run = tmp_path / "run"
    run.mkdir()
    env = gate["install_gh_shim"](
        run,
        tier="L1",
        allowlist=[],
        deny=["merge", "close", "comment"],
        verifier="",
        gate_script=GATE,
    )
    shim = run / ".gate" / "bin" / "gh"
    result = subprocess.run(
        [str(shim), "pr", "merge", "1", "--repo", "o/r"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 78
    assert "DENIED" in result.stderr
    denials = (run / "gate-denials.jsonl").read_text(encoding="utf-8")
    assert "merge" in denials


def test_help_mentions_force() -> None:
    result = subprocess.run(
        [sys.executable, str(BIN_DIR / "loop"), "help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--force" in result.stdout
