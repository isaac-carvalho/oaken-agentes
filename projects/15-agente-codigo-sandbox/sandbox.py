"""Execução de código Python em sandbox Docker (com fallback subprocess opt-in).

⚠️  SEGURANÇA: o fallback subprocess executa código arbitrário no host. Por
padrão é desabilitado. Para habilitar (use só em ambiente descartável):
    export OAKEN_ALLOW_LOCAL_EXEC=1
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
import tempfile

log = logging.getLogger(__name__)
from pathlib import Path


class SandboxRefusedError(RuntimeError):
    """Levantado quando Docker não está disponível e fallback não foi autorizado."""


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
    """Executa código em container Docker isolado (network=none, ro, mem 256m).

    Se Docker não estiver disponível e ``OAKEN_ALLOW_LOCAL_EXEC=1`` estiver
    definida, faz fallback para subprocess local (apenas pra demo). Caso
    contrário levanta ``SandboxRefusedError``.
    """
    host_path: Path | None = None
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
                volumes={str(host_path): {"bind": "/work/script.py", "mode": "ro"}},
                working_dir="/work",
                network_disabled=True,
                mem_limit="256m",
                detach=False,
                stderr=True,
                stdout=True,
                remove=True,
                stop_signal="SIGKILL",
                timeout=timeout,
            )
            text = log.decode("utf-8", "replace")
            return True, text
        except Exception as e:
            return False, str(e)[:4000]
    except Exception:
        if os.environ.get("OAKEN_ALLOW_LOCAL_EXEC") != "1":
            raise SandboxRefusedError(
                "Docker indisponível e OAKEN_ALLOW_LOCAL_EXEC!=1. "
                "Por segurança, recuso executar código não-isolado. "
                "Para autorizar fallback subprocess (use SÓ em ambiente "
                "descartável): export OAKEN_ALLOW_LOCAL_EXEC=1"
            )
        return _run_subprocess(code, timeout)
    finally:
        if host_path is not None:
            host_path.unlink(missing_ok=True)
