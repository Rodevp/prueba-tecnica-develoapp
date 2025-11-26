from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import session_local
from app.core.utilitys import get_current_user, require_permission
from app.reservations.services import (
    create_reservation,
    list_user_reservations,
    list_all_reservations,
    cancel_reservation
)
from app.reservations.schema import ReservationCreate

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def route_create_reservation(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_reservation(db, current_user.id, data)


@router.get("/my")
def route_my_reservations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return list_user_reservations(db, current_user.id)


@router.get(
    "/all",
    dependencies=[Depends(require_permission("reservations:view_all"))]
)
def route_list_all_reservations(
    db: Session = Depends(get_db)
):
    return list_all_reservations(db)


@router.delete("/{reservation_id}")
def route_cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return cancel_reservation(db, current_user.id, reservation_id)
