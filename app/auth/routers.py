from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import session_local
from app.auth.services import (
    register_user,
    login_user,
    request_password_reset,
    reset_password
)
from app.core.utilitys import get_current_user
from app.auth.schema import UserCreate, UserLogin, PasswordResetRequest, PasswordResetConfirm


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def route_register(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(db, data)


@router.post("/login")
def route_login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user(db, data)


@router.post("/password/reset-request")
def route_password_reset_request(
    data: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    return request_password_reset(db, data.email)


@router.post("/password/reset")
def route_reset_password(
    data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    return reset_password(db, data.token, data.new_password)
