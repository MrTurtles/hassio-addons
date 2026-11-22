from fastapi.testclient import TestClient

from tests.conftest import INGRESS


def test_default_household_is_dutch_and_metric(client: TestClient) -> None:
    body = client.get("/api/v1/settings", headers=INGRESS).json()
    assert body["name"] == "Huishouden"
    assert body["timezone"] == "Europe/Amsterdam"
    assert body["locale"] == "nl"
    assert body["unit_system"] == "metric"
    assert body["week_starts_on"] == 1
    assert body["subtract_pantry"] is True
    assert body["auto_consume_pantry"] is False


def test_settings_can_be_updated(client: TestClient) -> None:
    response = client.patch(
        "/api/v1/settings",
        headers=INGRESS,
        json={"name": "  Thuis  ", "default_servings": 3, "auto_consume_pantry": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Thuis"
    assert body["default_servings"] == 3
    assert body["auto_consume_pantry"] is True
    assert body["timezone"] == "Europe/Amsterdam"


def test_known_timezone_is_kept(client: TestClient) -> None:
    response = client.patch(
        "/api/v1/settings",
        headers=INGRESS,
        json={"timezone": "Europe/Amsterdam"},
    )
    assert response.status_code == 200
    assert response.json()["timezone"] == "Europe/Amsterdam"
    response = client.patch(
        "/api/v1/settings",
        headers=INGRESS,
        json={"timezone": "Niet/EenZone"},
    )
    assert response.status_code == 422
    assert response.json()["error"] == {
        "code": "validation_error",
        "message": "Onbekende tijdzone.",
    }


def test_invalid_servings_are_rejected(client: TestClient) -> None:
    response = client.patch(
        "/api/v1/settings",
        headers=INGRESS,
        json={"default_servings": 0},
    )
    assert response.status_code == 422
    assert "tussen 1 en 24" in response.json()["error"]["message"]


def test_fixed_fields_cannot_be_overwritten(client: TestClient) -> None:
    response = client.patch(
        "/api/v1/settings",
        headers=INGRESS,
        json={"locale": "en"},
    )
    assert response.status_code == 422
