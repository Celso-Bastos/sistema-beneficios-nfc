from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_returns_running_and_security_headers() -> None:
    response = client.get("/", headers={"X-Request-ID": "test-request-id"})

    assert response.status_code == 200
    assert response.json()["status"] == "running"
    assert response.headers["X-Request-ID"] == "test-request-id"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["Cache-Control"] == "no-store"


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "sistema-beneficios-nfc-api",
        "version": "0.1.0",
    }


def test_detailed_health_has_api_database_version_and_timestamp() -> None:
    response = client.get("/health/detailed")

    assert response.status_code == 200
    payload = response.json()
    assert payload["api"]["service"] == "sistema-beneficios-nfc-api"
    assert payload["api"]["version"] == "0.1.0"
    assert "status" in payload["database"]
    assert "timestamp" in payload
