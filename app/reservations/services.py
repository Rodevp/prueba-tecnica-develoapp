from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_
from app.reservations.models import Reservation
from app.fields.models import Field
import datetime

def validate_availability(
    db: Session,
    field_id: int,
    start_time: datetime.datetime,
    end_time: datetime.datetime
):
    """
    Valida si existe una reserva que se cruce con las fechas dadas.
    (start < end_time AND end > start_time) → conflicto
    """
    conflict = db.query(Reservation).filter(
        Reservation.field_id == field_id,
        Reservation.status == "active",
        and_(
            Reservation.start_time < end_time,
            Reservation.end_time > start_time
        )
    ).first()

    if conflict:
        raise HTTPException(
            status_code=400,
            detail="La cancha ya está reservada en ese horario"
        )

def create_reservation(db: Session, user_id: int, data):
    field = db.query(Field).filter(Field.id == data.field_id).first()
    if not field:
        raise HTTPException(404, "La cancha no existe")

    if data.end_time <= data.start_time:
        raise HTTPException(400, "La hora final debe ser mayor a la inicial")

    validate_availability(db, data.field_id, data.start_time, data.end_time)

    reservation = Reservation(
        user_id=user_id,
        field_id=data.field_id,
        start_time=data.start_time,
        end_time=data.end_time,
        status="active"
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation

def list_user_reservations(db: Session, user_id: int):
    return (
        db.query(Reservation)
        .filter(Reservation.user_id == user_id)
        .order_by(Reservation.start_time.desc())
        .all()
    )

def list_all_reservations(db: Session):
    return (
        db.query(Reservation)
        .order_by(Reservation.start_time.desc())
        .all()
    )

def cancel_reservation(db: Session, user_id: int, reservation_id: int):
    reservation = (
        db.query(Reservation)
        .filter(
            Reservation.id == reservation_id,
            Reservation.user_id == user_id
        )
        .first()
    )

    if not reservation:
        raise HTTPException(404, "Reserva no encontrada")

    if reservation.status == "cancelled":
        raise HTTPException(400, "La reserva ya está cancelada")

    reservation.status = "cancelled"
    db.commit()

    return {"message": "Reserva cancelada con éxito"}
