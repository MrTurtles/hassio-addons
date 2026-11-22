import secrets
from dataclasses import dataclass

from starlette.requests import Request

from app.core.config import Settings
from app.core.errors import ApiError

TRUSTED_PEERS = frozenset({"127.0.0.1", "::1", "localhost", "testclient"})


@dataclass(frozen=True)
class AccessContext:
    channel: str
    user_id: str | None


def expected_token(settings: Settings) -> str | None:
    if settings.integration_token:
        return settings.integration_token
    path = settings.token_path
    if not path.is_file():
        return None
    token = path.read_text(encoding="utf-8").strip()
    return token or None


def require_trusted_peer(request: Request) -> None:
    host = request.client.host if request.client else ""
    if host not in TRUSTED_PEERS:
        raise ApiError(403, "forbidden", "Toegang geweigerd.")


def require_access(request: Request) -> AccessContext:
    require_trusted_peer(request)
    settings: Settings = request.app.state.settings
    channel = request.headers.get("x-mealplanner-channel", "")

    if channel == "ingress":
        user_id = request.headers.get("x-remote-user-id") or None
        return AccessContext(channel="ingress", user_id=user_id)

    if channel == "internal":
        provided = _bearer_token(request)
        expected = expected_token(settings)
        if not provided or not expected or not _matches(provided, expected):
            raise ApiError(401, "unauthorized", "Ongeldige toegangssleutel.")
        return AccessContext(channel="internal", user_id=None)

    if channel == "development" and settings.env == "development":
        return AccessContext(channel="development", user_id=None)

    raise ApiError(403, "forbidden", "Toegang geweigerd.")


def _bearer_token(request: Request) -> str | None:
    header = request.headers.get("authorization", "")
    scheme, _, value = header.partition(" ")
    if scheme.lower() != "bearer" or not value.strip():
        return None
    return value.strip()


def _matches(provided: str, expected: str) -> bool:
    try:
        return secrets.compare_digest(provided, expected)
    except (TypeError, ValueError):
        return False
