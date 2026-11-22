from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MEALPLANNER_", extra="ignore")

    env: str = "production"
    data_dir: Path = Path("/data")
    static_dir: Path = Path("/opt/meal-planner/static")
    integration_token: str | None = None
    database_filename: str = "mealplanner.db"
    api_version: int = 1
    alembic_ini: Path = Field(default=BACKEND_ROOT / "alembic.ini")

    @property
    def database_path(self) -> Path:
        return self.data_dir / "database" / self.database_filename

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.database_path.resolve().as_posix()}"

    @property
    def token_path(self) -> Path:
        return self.data_dir / "secrets" / "integration_token"

    @property
    def backup_dir(self) -> Path:
        return self.data_dir / "backups"


@lru_cache
def get_settings() -> Settings:
    return Settings()
