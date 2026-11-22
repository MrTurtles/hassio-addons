from fastapi import APIRouter, Request

from app.api.deps import TrustedDep
from app.core.config import Settings

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", dependencies=[TrustedDep])
def health(request: Request) -> dict[str, str | int]:
    settings: Settings = request.app.state.settings
    return {"status": "ok", "api_version": settings.api_version}
