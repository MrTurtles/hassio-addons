from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.core.database import create_sqlite_engine
from app.core.storage import prepare_storage


def main() -> None:
    settings = get_settings()
    engine = create_sqlite_engine(settings)
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    try:
        prepare_storage(settings, factory)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
