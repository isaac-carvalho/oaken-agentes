"""Tests for project 20 — aiops-langfuse."""
from __future__ import annotations

import json
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import functions directly
import sys
sys.path.insert(0, str(Path(__file__).parent))


# --------------- quality_score ---------------

def _quality_score(text: str) -> float:
    """Copied from main.py to avoid heavy import chain."""
    if not text:
        return 0.0
    words = text.split()
    uniq = len(set(words)) / max(len(words), 1)
    length_ok = 1.0 if 20 <= len(words) <= 400 else 0.5
    return round(0.5 * uniq + 0.5 * length_ok, 3)


def test_quality_score_empty():
    assert _quality_score("") == 0.0


def test_quality_score_short_text():
    score = _quality_score("hello world")
    # 2 unique words / 2 total = 1.0 uniq, length_ok = 0.5 (< 20 words)
    assert score == round(0.5 * 1.0 + 0.5 * 0.5, 3)


def test_quality_score_repetitive():
    text = " ".join(["word"] * 50)
    score = _quality_score(text)
    # 1 unique / 50 total = 0.02, length_ok = 1.0
    assert score < 0.6


def test_quality_score_good_text():
    text = " ".join(f"palavra{i}" for i in range(30))
    score = _quality_score(text)
    # All unique, good length
    assert score > 0.9


def test_quality_score_boundary_20_words():
    text = " ".join(f"w{i}" for i in range(20))
    score = _quality_score(text)
    # length_ok = 1.0 (exactly 20)
    assert score == round(0.5 * 1.0 + 0.5 * 1.0, 3)


# --------------- LocalSink ---------------

def test_local_sink_trace_and_end(tmp_path):
    from main import LocalSink, SINK

    sink = LocalSink()
    # Patch SINK to tmp_path
    import main
    original = main.SINK
    main.SINK = tmp_path / "traces.jsonl"

    span = sink.trace(name="test_trace", input="hello")
    time.sleep(0.01)
    span.update(output="world")
    span.end()

    data = json.loads((tmp_path / "traces.jsonl").read_text().strip())
    assert data["name"] == "test_trace"
    assert data["output"] == "world"
    assert "latency_ms" in data
    assert "ts" in data

    main.SINK = original


def test_local_sink_flush():
    """flush() should not raise."""
    from main import LocalSink
    sink = LocalSink()
    sink.flush()  # no-op, should not raise
