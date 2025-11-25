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
    data,
    db: Session = Depends(get_db)
):
    return register_user(db, data)


@router.post("/login")
def route_login(
    data,
    db: Session = Depends(get_db)
):
    return login_user(db, data)


@router.get("/me")
def route_me(
    current_user=Depends(get_current_user)
):
    return current_user


@router.post("/password/reset-request")
def route_password_reset_request(
    data,
    db: Session = Depends(get_db)
):
    return request_password_reset(db, data.email)


@router.post("/password/reset")
def route_reset_password(
    data,
    db: Session = Depends(get_db)
):
    return reset_password(db, data.token, data.new_password)
