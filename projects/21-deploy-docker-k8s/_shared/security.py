"""Middleware de segurança reusável para apps FastAPI do portfolio.

Aplica de uma vez:
- CORS restritivo (allow_origins explícito)
- Security headers (X-Content-Type-Options, X-Frame-Options, HSTS, Referrer-Policy)
- Rate limiting opcional (se ``slowapi`` estiver instalado)

Uso típico::

    from fastapi import FastAPI
    from projects._shared.security import apply_security

    app = FastAPI()
    apply_security(app, allow_origins=["https://meu-front.exemplo.com"])
"""
from __future__ import annotations

from collections.abc import Iterable


_DEFAULT_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}


def apply_security(
    app,
    allow_origins: Iterable[str] = ("http://localhost:3000",),
    allow_methods: Iterable[str] = ("GET", "POST", "DELETE"),
    rate_limit_per_minute: int | None = 60,
    extra_headers: dict[str, str] | None = None,
) -> None:
    """Aplica CORS + security headers + rate limit (se slowapi disponível)."""
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.requests import Request
    from starlette.responses import Response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(allow_origins),
        allow_methods=list(allow_methods),
        allow_credentials=False,
        allow_headers=["*"],
    )

    headers = {**_DEFAULT_HEADERS, **(extra_headers or {})}

    @app.middleware("http")
    async def _security_headers(request: Request, call_next) -> Response:
        response: Response = await call_next(request)
        for name, value in headers.items():
            response.headers.setdefault(name, value)
        return response

    if rate_limit_per_minute:
        try:
            from slowapi import Limiter
            from slowapi.errors import RateLimitExceeded
            from slowapi.middleware import SlowAPIMiddleware
            from slowapi.util import get_remote_address

            limiter = Limiter(
                key_func=get_remote_address,
                default_limits=[f"{rate_limit_per_minute}/minute"],
            )
            app.state.limiter = limiter
            app.add_middleware(SlowAPIMiddleware)

            @app.exception_handler(RateLimitExceeded)
            async def _rate_handler(_req, _exc):
                return Response(content="too many requests", status_code=429)
        except ImportError:
            # slowapi opcional; se não instalado, segue sem rate limiting.
            pass
