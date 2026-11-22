from fastapi import FastAPI
from fastapi.testclient import TestClient

from tests.conftest import INGRESS, TOKEN


def test_settings_require_a_channel(client: TestClient) -> None:
    response = client.get("/api/v1/settings")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_ingress_channel_can_read_settings(client: TestClient) -> None:
    response = client.get("/api/v1/settings", headers=INGRESS)
    assert response.status_code == 200
    assert response.json()["default_servings"] == 2


def test_internal_channel_requires_the_token(client: TestClient) -> None:
    rejected = client.get("/api/v1/settings", headers={"X-MealPlanner-Channel": "internal"})
    assert rejected.status_code == 401
    assert TOKEN not in rejected.text

    accepted = client.get(
        "/api/v1/settings",
        headers={"X-MealPlanner-Channel": "internal", "Authorization": f"Bearer {TOKEN}"},
    )
    assert accepted.status_code == 200


def test_wrong_token_is_rejected(client: TestClient) -> None:
    response = client.get(
        "/api/v1/settings",
        headers={"X-MealPlanner-Channel": "internal", "Authorization": "Bearer other-token"},
    )
    assert response.status_code == 401
    assert "other-token" not in response.text


def test_development_channel_is_rejected_in_production(client: TestClient) -> None:
    response = client.get("/api/v1/settings", headers={"X-MealPlanner-Channel": "development"})
    assert response.status_code == 403


def test_untrusted_peer_is_rejected(app: FastAPI) -> None:
    with TestClient(app, client=("192.0.2.8", 40000)) as outsider:
        health = outsider.get("/api/v1/health")
        settings = outsider.get("/api/v1/settings", headers=INGRESS)
    assert health.status_code == 403
    assert settings.status_code == 403
