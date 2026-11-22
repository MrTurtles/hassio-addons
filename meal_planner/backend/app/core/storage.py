import re
import secrets
import sqlite3
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.services.households import seed_household

_INGRESS_PATH = re.compile(r"^/[A-Za-z0-9._/-]*$")


def prepare_storage(settings: Settings, session_factory: sessionmaker[Session]) -> None:
    for path in (
        settings.data_dir / "database",
        settings.data_dir / "images",
        settings.backup_dir,
        settings.data_dir / "logs",
        settings.data_dir / "secrets",
    ):
        path.mkdir(parents=True, exist_ok=True)
    ensure_token(settings)
    upgrade_database(settings)
    with session_factory() as session:
        seed_household(session)


def ensure_token(settings: Settings) -> None:
    if settings.integration_token or settings.token_path.is_file():
        return
    token = secrets.token_urlsafe(32)
    settings.token_path.write_text(token + "\n", encoding="utf-8")
    try:
        settings.token_path.chmod(0o600)
    except OSError:
        return


def upgrade_database(settings: Settings) -> None:
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    config = alembic_config(settings)
    if settings.database_path.exists() and migration_pending(settings, config):
        destination = settings.backup_dir / f"pre-migrate-{settings.database_path.stem}.db"
        backup_sqlite(settings.database_path, destination)
    command.upgrade(config, "head")


def alembic_config(settings: Settings) -> Config:
    config = Config(str(settings.alembic_ini))
    config.set_main_option("script_location", str(settings.alembic_ini.parent / "migrations"))
    config.set_main_option("sqlalchemy.url", settings.database_url)
    return config


def migration_pending(settings: Settings, config: Config) -> bool:
    script = ScriptDirectory.from_config(config)
    heads = set(script.get_heads())
    with sqlite3.connect(settings.database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        if "alembic_version" not in tables:
            return True
        current = {row[0] for row in connection.execute("SELECT version_num FROM alembic_version")}
    return current != heads


def backup_sqlite(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(source) as src, sqlite3.connect(destination) as dst:
        src.backup(dst)


def base_href_from_ingress(header: str | None) -> str:
    if not header:
        return "/"
    value = header.strip()
    if not _INGRESS_PATH.fullmatch(value) or ".." in value.split("/"):
        return "/"
    if value != "/" and value.endswith("/"):
        value = value[:-1]
    if value == "/":
        return "/"
    return f"{value}/"
