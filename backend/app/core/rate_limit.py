import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status

from app.core.config import settings

_requests_by_ip: dict[str, deque[float]] = defaultdict(deque)


def rate_limit(request: Request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    window_start = now - settings.RATE_LIMIT_WINDOW_SECONDS
    entries = _requests_by_ip[client_ip]

    while entries and entries[0] < window_start:
        entries.popleft()

    if len(entries) >= settings.RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas requisições. Tente novamente em instantes.",
        )

    entries.append(now)


def reset_rate_limit_state() -> None:
    _requests_by_ip.clear()
