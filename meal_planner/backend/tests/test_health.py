from fastapi.testclient import TestClient


def test_health_is_available_without_channel(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "api_version": 1}


def test_health_hides_secrets(client: TestClient) -> None:
    body = response_text(client.get("/api/v1/health"))
    assert "test-token-value" not in body
    assert "integration_token" not in body


def response_text(response) -> str:  # type: ignore[no-untyped-def]
    return response.text
