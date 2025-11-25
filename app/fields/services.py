from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.fields.models import Field

def create_field(db: Session, data):
    existing = db.query(Field).filter(Field.name == data.name).first()
    if existing:
        raise HTTPException(400, "Ya existe una cancha con ese nombre")

    field = Field(
        name=data.name,
        location=data.location,
        capacity=data.capacity,
        price_per_hour=data.price_per_hour,
    )

    db.add(field)
    db.commit()
    db.refresh(field)

    return field

def list_fields(db: Session):
    return db.query(Field).order_by(Field.name.asc()).all()

def get_field(db: Session, field_id: int):
    field = db.query(Field).filter(Field.id == field_id).first()
    if not field:
        raise HTTPException(404, "Cancha no encontrada")
    return field

def update_field(db: Session, field_id: int, data):
    field = get_field(db, field_id)

    for key, value in data.dict(exclude_none=True).items():
        setattr(field, key, value)

    db.commit()
    db.refresh(field)

    return field

def delete_field(db: Session, field_id: int):
    field = get_field(db, field_id)

    db.delete(field)
    db.commit()

    return {"message": "Cancha eliminada con éxito"}
