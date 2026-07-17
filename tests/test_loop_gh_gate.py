"""Tests for bin/loop-gh-gate hard autonomy gate."""

from __future__ import annotations

import json
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


@pytest.fixture
def fake_gh(tmp_path: Path) -> Path:
    """A stub real `gh` binary so install_gh_shim never depends on host PATH."""
    path = tmp_path / "real-gh"
    path.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    path.chmod(0o755)
    return path


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["pr", "merge", "250", "--repo", "o/r", "--squash"], "merge"),
        (["pr", "close", "12", "--repo", "o/r"], "close"),
        (["pr", "comment", "1", "--body", "hi"], "comment"),
        (["pr", "create", "--title", "x", "--body", "y"], "push"),
        (["pr", "edit", "3", "--title", "new"], "push"),
        (["issue", "edit", "5", "--add-assignee", "bob"], "assign"),
        (["issue", "edit", "5", "--state", "closed"], "close"),
        (["issue", "create", "--title", "x"], "push"),
        (["pr", "edit", "3", "--add-label", "bug"], "label"),
        (["pr", "review", "3", "--approve"], "approve"),
        (["pr", "list", "--repo", "o/r"], None),
        (["api", "repos/o/r/pulls/1"], None),
        (["api", "-X", "POST", "repos/o/r/issues/1/comments"], "comment"),
        (["api", "-f", "body=hi", "repos/o/r/issues/1/comments"], "comment"),
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


def test_merge_requires_receipt(gate, tmp_path: Path, fake_gh: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    run = tmp_path / "run"
    run.mkdir()
    env = gate["install_gh_shim"](
        run,
        tier="L3",
        allowlist=["merge", "close"],
        deny=["push"],
        verifier="test-verifier",
        gate_script=GATE,
        real_gh=str(fake_gh),
    )
    for key, value in env.items():
        if key.startswith("LOOP_GATE_") or key == "PATH":
            monkeypatch.setenv(key, value)

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


def test_receipt_hmac_required_when_secret_set(
    gate, tmp_path: Path, fake_gh: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run = tmp_path / "run"
    run.mkdir()
    secret = "test-secret"
    monkeypatch.setenv("LOOP_GATE_RECEIPT_SECRET", secret)
    env = gate["install_gh_shim"](
        run,
        tier="L3",
        allowlist=["merge"],
        deny=[],
        verifier="test-verifier",
        gate_script=GATE,
        real_gh=str(fake_gh),
    )
    for key, value in env.items():
        if key.startswith("LOOP_GATE_") or key == "PATH":
            monkeypatch.setenv(key, value)

    receipt = {
        "action": "merge",
        "repo": "acme/demo",
        "number": 9,
        "approved": True,
        "verifier": "test-verifier",
        "rationale": "ok",
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    (run / "verifier-receipts" / "m9.json").write_text(json.dumps(receipt), encoding="utf-8")
    ok, _reason, _action, _meta = gate["check_command"](
        ["pr", "merge", "9", "--repo", "acme/demo"],
    )
    assert ok is False  # missing sig

    receipt["sig"] = gate["sign_receipt"](receipt, secret)
    (run / "verifier-receipts" / "m9.json").write_text(json.dumps(receipt), encoding="utf-8")
    ok, _reason, _action, _meta = gate["check_command"](
        ["pr", "merge", "9", "--repo", "acme/demo"],
    )
    assert ok is True


def test_redact_argv(gate) -> None:
    redacted = gate["redact_argv"](
        ["pr", "comment", "1", "--body", "secret text", "-H", "Authorization: token"]
    )
    assert "secret text" not in redacted
    assert "Authorization: token" not in redacted
    assert "<redacted>" in redacted


def test_shim_denies_with_exit_78(
    gate, tmp_path: Path, fake_gh: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run = tmp_path / "run"
    run.mkdir()
    env = gate["install_gh_shim"](
        run,
        tier="L1",
        allowlist=[],
        deny=["merge", "close", "comment"],
        verifier="",
        gate_script=GATE,
        real_gh=str(fake_gh),
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
