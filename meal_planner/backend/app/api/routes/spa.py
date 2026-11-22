from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from starlette.requests import Request

from app.api.deps import TrustedDep
from app.core.config import Settings
from app.core.errors import ApiError
from app.core.storage import base_href_from_ingress

router = APIRouter(tags=["ui"], dependencies=[TrustedDep])


@router.get("/", include_in_schema=False, response_model=None)
@router.get("/{full_path:path}", include_in_schema=False, response_model=None)
def frontend(request: Request, full_path: str = "") -> FileResponse | HTMLResponse:
    settings: Settings = request.app.state.settings
    static_file = _safe_file(settings.static_dir, full_path)
    if static_file is not None:
        return FileResponse(static_file)
    index = settings.static_dir / "index.html"
    if not index.is_file():
        raise ApiError(404, "not_found", "Pagina niet gevonden.")
    base_href = base_href_from_ingress(request.headers.get("x-ingress-path"))
    html = index.read_text(encoding="utf-8").replace("__INGRESS_BASE_HREF__", base_href)
    return HTMLResponse(html)


def _safe_file(static_dir: Path, full_path: str) -> Path | None:
    if not full_path or full_path.endswith("/"):
        return None
    root = static_dir.resolve()
    candidate = (root / full_path).resolve()
    if not candidate.is_file():
        return None
    if candidate != root and root not in candidate.parents:
        return None
    return candidate
