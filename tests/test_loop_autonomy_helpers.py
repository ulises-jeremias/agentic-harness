"""Tests for STATE.md / request.md autonomy helpers in bin/loop."""

from __future__ import annotations

import runpy
from pathlib import Path

import pytest


BIN_DIR = Path(__file__).resolve().parent.parent / "bin"
LOOP = BIN_DIR / "loop"


@pytest.fixture
def loop_ns():
    return runpy.run_path(str(LOOP))


def test_parse_state_md_reads_state_not_loop(loop_ns, tmp_path: Path) -> None:
    loop_dir = tmp_path / "loops" / "demo"
    loop_dir.mkdir(parents=True)
    (loop_dir / "LOOP.md").write_text(
        "---\nname: demo\ntier: L1\nallowlist: []\n---\n\n# Loop\n",
        encoding="utf-8",
    )
    (loop_dir / "STATE.md").write_text(
        '---\nlast_run: "2026-07-16T12:00:00Z"\npending:\n'
        '  - "owner/repo#12 — waiting on CI"\nescalations: []\n---\n',
        encoding="utf-8",
    )
    state = loop_ns["parse_state_md"](loop_dir)
    last = state.get("last_run")
    assert last is not None
    assert "2026-07-16" in str(last)
    # pending may be list
    pending = state.get("pending") or []
    assert any("owner/repo#12" in str(p) for p in pending)
    assert "tier" not in state  # must not have read LOOP.md


def test_write_state_md_quotes_hash(loop_ns, tmp_path: Path) -> None:
    loop_dir = tmp_path / "loops" / "demo"
    loop_dir.mkdir(parents=True)
    loop_ns["write_state_md"](
        loop_dir,
        {
            "last_run": "2026-07-16T12:00:00Z",
            "last_run_status": "completed",
            "pending": ["nanlabs/backend-reference#136 - isort"],
            "escalations": [],
        },
    )
    text = (loop_dir / "STATE.md").read_text(encoding="utf-8")
    assert "nanlabs/backend-reference#136" in text
    assert text.split("pending:")[1].splitlines()[1].strip().startswith("- \"")
    # Round-trip must keep the PR number (not truncate at #)
    loaded = loop_ns["parse_state_md"](loop_dir)
    pending = loaded.get("pending") or []
    assert any("#136" in str(p) for p in pending)


def test_load_request_body_prefers_request_md(loop_ns, tmp_path: Path) -> None:
    loop_dir = tmp_path / "loops" / "demo"
    loop_dir.mkdir(parents=True)
    (loop_dir / "LOOP.md").write_text(
        "---\nname: demo\ntier: L1\ngoal: From frontmatter\n---\n",
        encoding="utf-8",
    )
    (loop_dir / "request.md").write_text(
        "You are the detailed request from request.md.\n",
        encoding="utf-8",
    )
    meta = loop_ns["parse_loop_md"](loop_dir)
    body = loop_ns["_load_request_body"](loop_dir, meta, "demo")
    assert "request.md" in body or "detailed request" in body


def test_build_runner_prompt_includes_autonomy_contract(loop_ns, tmp_path: Path) -> None:
    loop_dir = tmp_path / "loops" / "demo"
    loop_dir.mkdir(parents=True)
    (loop_dir / "LOOP.md").write_text(
        "---\nname: demo\ntier: L3\nallowlist:\n  - merge\n"
        "deny:\n  - push\nverifier: test-verifier\ngoal: Merge safe deps\n---\n",
        encoding="utf-8",
    )
    (loop_dir / "request.md").write_text("Do the work.\n", encoding="utf-8")
    (loop_dir / "STATE.md").write_text(
        "---\npending: []\nescalations: []\n---\n",
        encoding="utf-8",
    )
    meta = loop_ns["parse_loop_md"](loop_dir)
    prompt = loop_ns["_build_runner_prompt"](loop_dir, meta, "demo", loop_dir / "runs" / "x")
    assert "Autonomy contract" in prompt
    assert "HARD" in prompt
    assert "merge" in prompt
    assert "Do the work." in prompt
