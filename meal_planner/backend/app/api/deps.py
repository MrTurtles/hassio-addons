from collections.abc import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.security import AccessContext, require_access, require_trusted_peer


def get_session(request: Request) -> Iterator[Session]:
    session = request.app.state.session_factory()
    try:
        yield session
    finally:
        session.close()


def trusted_peer(request: Request) -> None:
    require_trusted_peer(request)


def access_context(request: Request) -> AccessContext:
    return require_access(request)


SessionDep = Depends(get_session)
TrustedDep = Depends(trusted_peer)
AccessDep = Depends(access_context)
