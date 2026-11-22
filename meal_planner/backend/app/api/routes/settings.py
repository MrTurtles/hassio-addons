from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.api.deps import AccessDep, SessionDep
from app.schemas.settings import SettingsRead, SettingsUpdate
from app.services.households import read_settings, update_settings

router = APIRouter(prefix="/api/v1", tags=["settings"])


@router.get("/settings", dependencies=[AccessDep], response_model=SettingsRead)
def get_settings(session: Session = SessionDep) -> SettingsRead:
    return read_settings(session)


@router.patch("/settings", dependencies=[AccessDep], response_model=SettingsRead)
def patch_settings(payload: SettingsUpdate, session: Session = SessionDep) -> SettingsRead:
    return update_settings(session, payload)
