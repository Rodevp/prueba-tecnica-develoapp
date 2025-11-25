from sqlalchemy.orm import Session
from sqlalchemy import func
from app.reservations.models import Reservation
from app.fields.models import Field
from app.auth.models import User

def get_stats(db: Session):
    """
    Retorna un conjunto de estadísticas para el dashboard administrativo.
    Incluye:
        - Reservas por cancha
        - Total reservas activas
        - Total reservas canceladas
        - Total de reservas
        - Total de usuarios
    """

    reservation_per_field = (
        db.query(Field.name, func.count(Reservation.id))
        .join(Reservation, Field.id == Reservation.field_id)
        .group_by(Field.name)
        .all()
    )

    actives = (
        db.query(func.count(Reservation.id))
        .filter(Reservation.status == "active")
        .scalar()
    )

    cancels = (
        db.query(func.count(Reservation.id))
        .filter(Reservation.status == "cancelled")
        .scalar()
    )

    total_reservations = (
        db.query(func.count(Reservation.id))
        .scalar()
    )

    total_users = (
        db.query(func.count(User.id))
        .scalar()
    )

    return {
        "reservation_per_field": [
            {"field": name, "total": total}
            for name, total in reservation_per_field
        ],
        "reservations": {
            "actives": actives,
            "cancels": cancels,
            "total": total_reservations,
        },
        "users": {
            "total": total_users
        }
    }
