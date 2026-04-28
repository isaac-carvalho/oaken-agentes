"""Tests for project 15 — agente-codigo-sandbox."""
from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

import pytest


# --------------- extract_code (main.py) ---------------

def _extract_code(text: str) -> str:
    """Reimplementation to test without importing typer/docker deps."""
    import ast
    import re

    CODE_BLOCK = re.compile(r"```(?:python)?\s*(.+?)```", re.DOTALL)
    m = CODE_BLOCK.search(text)
    candidate = m.group(1).strip() if m else text.strip()
    try:
        ast.parse(candidate)
    except SyntaxError:
        return text.strip()
    return candidate


def test_extract_code_from_markdown():
    text = "Here is the code:\n```python\nprint('hello')\n```\nDone."
    assert _extract_code(text) == "print('hello')"


def test_extract_code_no_language_tag():
    text = "```\nx = 1 + 2\n```"
    assert _extract_code(text) == "x = 1 + 2"


def test_extract_code_plain_text_valid_python():
    text = "x = 42"
    assert _extract_code(text) == "x = 42"


def test_extract_code_multiline_block():
    text = "```python\ndef f(x):\n    return x * 2\n\nassert f(3) == 6\n```"
    code = _extract_code(text)
    assert "def f(x):" in code
    assert "assert f(3) == 6" in code


# --------------- sandbox._run_subprocess ---------------

from sandbox import _run_subprocess, run_in_docker


def test_run_subprocess_success():
    ok, out = _run_subprocess("print('OK')", timeout=5)
    assert ok is True
    assert "OK" in out


def test_run_subprocess_syntax_error():
    ok, out = _run_subprocess("if if if", timeout=5)
    assert ok is False
    assert "SyntaxError" in out


def test_run_subprocess_timeout():
    ok, out = _run_subprocess("import time; time.sleep(30)", timeout=1)
    assert ok is False
    assert out == "TIMEOUT"


def test_run_subprocess_runtime_error():
    ok, out = _run_subprocess("raise ValueError('boom')", timeout=5)
    assert ok is False
    assert "ValueError" in out


# --------------- run_in_docker fallback ---------------

def test_run_in_docker_falls_back_to_subprocess():
    """Without Docker, run_in_docker should fall back to subprocess."""
    ok, out = run_in_docker("print('hello from fallback')", timeout=5)
    assert ok is True
    assert "hello from fallback" in out


def test_run_in_docker_output_truncation():
    """Stderr output should be truncated to 4000 chars."""
    ok, out = _run_subprocess("import sys; sys.stderr.write('X' * 8000); sys.exit(1)", timeout=5)
    assert ok is False
    assert len(out) <= 4000
