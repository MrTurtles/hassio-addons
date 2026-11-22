from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from app.api.routes import health, spa
from app.api.routes import settings as settings_routes
from app.core.config import Settings, get_settings
from app.core.database import create_sqlite_engine
from app.core.errors import register_exception_handlers
from app.core.storage import prepare_storage


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        engine = create_sqlite_engine(resolved)
        app.state.engine = engine
        app.state.session_factory = sessionmaker(
            bind=engine, autoflush=False, expire_on_commit=False
        )
        prepare_storage(resolved, app.state.session_factory)
        try:
            yield
        finally:
            engine.dispose()

    app = FastAPI(title="Meal Planner", version="0.1.0", lifespan=lifespan)
    app.state.settings = resolved
    register_exception_handlers(app)
    app.include_router(health.router)
    app.include_router(settings_routes.router)
    app.include_router(spa.router)
    return app


app = create_app()
