from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import session_local
from app.core.utilitys import require_permission
from app.fields.services import (
    create_field,
    list_fields,
    get_field,
    update_field,
    delete_field
)

router = APIRouter(
    prefix="/fields",
    tags=["Fields"]
)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    dependencies=[Depends(require_permission("fields:create"))]
)
def route_create_field(
    data,
    db: Session = Depends(get_db)
):
    return create_field(db, data)


@router.get("/")
def route_list_fields(
    db: Session = Depends(get_db)
):
    return list_fields(db)


@router.get("/{field_id}")
def route_get_field(
    field_id: int,
    db: Session = Depends(get_db)
):
    return get_field(db, field_id)


@router.put(
    "/{field_id}",
    dependencies=[Depends(require_permission("fields:update"))]
)
def route_update_field(
    field_id: int,
    data,
    db: Session = Depends(get_db)
):
    return update_field(db, field_id, data)

@router.delete(
    "/{field_id}",
    dependencies=[Depends(require_permission("fields:delete"))]
)
def route_delete_field(
    field_id: int,
    db: Session = Depends(get_db)
):
    return delete_field(db, field_id)
