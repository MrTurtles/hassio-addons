"""Generic single-database configuration."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app

INGRESS = {"X-MealPlanner-Channel": "ingress"}
TOKEN = "test-token-value"


@pytest.fixture
def app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    monkeypatch.setenv("MEALPLANNER_ENV", "production")
    monkeypatch.setenv("MEALPLANNER_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("MEALPLANNER_INTEGRATION_TOKEN", TOKEN)
    monkeypatch.setenv("MEALPLANNER_STATIC_DIR", str(tmp_path / "static"))
    get_settings.cache_clear()
    application = create_app(get_settings())
    return application


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
