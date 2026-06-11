from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.core import rate_limit as rate_limit_module
from app.core.rate_limit import rate_limit, reset_rate_limit_state
from app.main import app


def test_unhandled_errors_return_sanitized_payload() -> None:
    test_client = TestClient(app, raise_server_exceptions=False)

    @app.get("/__test_unhandled_error")
    def fail_for_test() -> None:
        raise RuntimeError("internal secret")

    response = test_client.get("/__test_unhandled_error")

    assert response.status_code == 500
    assert response.json() == {"error": True, "message": "Erro interno"}
    assert "X-Request-ID" in response.headers


def test_rate_limit_blocks_after_configured_threshold() -> None:
    reset_rate_limit_state()
    original_requests = rate_limit_module.settings.RATE_LIMIT_REQUESTS
    original_window = rate_limit_module.settings.RATE_LIMIT_WINDOW_SECONDS
    rate_limit_module.settings.RATE_LIMIT_REQUESTS = 1
    rate_limit_module.settings.RATE_LIMIT_WINDOW_SECONDS = 60

    request = SimpleNamespace(client=SimpleNamespace(host="127.0.0.9"))

    try:
        rate_limit(request)
        with pytest.raises(HTTPException) as exc_info:
            rate_limit(request)
    finally:
        rate_limit_module.settings.RATE_LIMIT_REQUESTS = original_requests
        rate_limit_module.settings.RATE_LIMIT_WINDOW_SECONDS = original_window
        reset_rate_limit_state()

    assert exc_info.value.status_code == 429
