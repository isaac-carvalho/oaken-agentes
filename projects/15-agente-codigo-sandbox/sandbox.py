"""Execução de código Python em sandbox Docker (com fallback subprocess)."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def _run_subprocess(code: str, timeout: int) -> tuple[bool, str]:
    try:
        out = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if out.returncode == 0:
            return True, out.stdout
        return False, (out.stderr or out.stdout)[:4000]
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"


def run_in_docker(code: str, timeout: int = 10) -> tuple[bool, str]:
    """Tenta Docker. Se indisponível, usa subprocess."""
    try:
        import docker

        client = docker.from_env()
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(code)
            host_path = Path(f.name)
        try:
            log = client.containers.run(
                "python:3.12-slim",
                command=["python", "/work/script.py"],
                volumes={str(host_path.parent): {"bind": "/work", "mode": "ro"}},
                working_dir="/work",
                network_disabled=True,
                mem_limit="256m",
                detach=False,
                stderr=True,
                stdout=True,
                remove=True,
            )
            text = log.decode("utf-8", "replace")
            return True, text
        except Exception as e:
            return False, str(e)[:4000]
        finally:
            host_path.rename(host_path.with_suffix(".done.py"))
    except Exception:
        return _run_subprocess(code, timeout)
