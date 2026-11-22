import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.core.database import create_sqlite_engine
from app.core.storage import base_href_from_ingress, prepare_storage, upgrade_database
from app.services.households import household_count
from tests.conftest import INGRESS


def test_restart_keeps_one_household_and_skips_backup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MEALPLANNER_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("MEALPLANNER_INTEGRATION_TOKEN", "test-token-value")
    get_settings.cache_clear()
    settings = get_settings()
    engine = create_sqlite_engine(settings)
    factory = sessionmaker(bind=engine)
    prepare_storage(settings, factory)
    prepare_storage(settings, factory)
    with factory() as session:
        assert household_count(session) == 1
    assert list(settings.backup_dir.glob("*.db")) == []
    engine.dispose()


def test_pending_migration_creates_a_backup_before_upgrade(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MEALPLANNER_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("MEALPLANNER_INTEGRATION_TOKEN", "test-token-value")
    get_settings.cache_clear()
    settings = get_settings()
    engine = create_sqlite_engine(settings)
    factory = sessionmaker(bind=engine)
    prepare_storage(settings, factory)
    with sqlite3.connect(settings.database_path) as connection:
        connection.execute("DELETE FROM alembic_version")

    seen: list[int] = []

    def fake_upgrade(_config: object, _revision: str) -> None:
        seen.append(len(list(settings.backup_dir.glob("*.db"))))

    monkeypatch.setattr("app.core.storage.command.upgrade", fake_upgrade)
    upgrade_database(settings)
    assert seen == [1]
    engine.dispose()


def test_token_file_is_created_when_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MEALPLANNER_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("MEALPLANNER_INTEGRATION_TOKEN", raising=False)
    get_settings.cache_clear()
    settings = get_settings()
    engine = create_sqlite_engine(settings)
    factory = sessionmaker(bind=engine)
    prepare_storage(settings, factory)
    token = settings.token_path.read_text(encoding="utf-8").strip()
    assert len(token) >= 32
    engine.dispose()


def test_ingress_path_is_sanitized() -> None:
    assert base_href_from_ingress("/api/hassio_ingress/Ab12/") == "/api/hassio_ingress/Ab12/"
    assert base_href_from_ingress("/") == "/"
    assert base_href_from_ingress("/api/../etc") == "/"
    assert base_href_from_ingress("<script>") == "/"
    assert base_href_from_ingress(None) == "/"


def test_index_receives_the_ingress_base(client: TestClient, tmp_path: Path) -> None:
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "index.html").write_text(
        "<!doctype html><base href=\"__INGRESS_BASE_HREF__\"><p>Maaltijdplanner</p>",
        encoding="utf-8",
    )
    response = client.get(
        "/",
        headers={**INGRESS, "X-Ingress-Path": "/api/hassio_ingress/Ab12"},
    )
    assert response.status_code == 200
    assert '<base href="/api/hassio_ingress/Ab12/">' in response.text
    assert "__INGRESS_BASE_HREF__" not in response.text


def test_api_is_not_replaced_by_the_frontend(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.headers["content-type"].startswith("application/json")
