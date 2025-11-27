from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import session_local
from app.core.utilitys import require_permission
from app.roles.services import (
    create_role,
    list_roles,
    delete_role,
    list_permissions,
    assign_role_to_user,
    assign_permission_to_role
)
from app.roles.schema import RoleCreate, AssingRole

router = APIRouter(
    prefix="/roles",
    tags=["Roles & Permissions"]
)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    dependencies=[Depends(require_permission("roles:create"))]
)
def route_create_role(
    data: RoleCreate,
    db: Session = Depends(get_db)
):
    return create_role(db, data.name)

@router.get(
    "/",
    dependencies=[Depends(require_permission("roles:view"))]
)
def route_list_roles(
    db: Session = Depends(get_db)
):
    return list_roles(db)

@router.delete(
    "/{role_id}",
    dependencies=[Depends(require_permission("roles:delete"))]
)
def route_delete_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    return delete_role(db, role_id)


@router.get(
    "/permissions",
    dependencies=[Depends(require_permission("permissions:view"))]
)
def route_list_permissions(
    db: Session = Depends(get_db)
):
    return list_permissions(db)

@router.post(
    "/{role_id}/permissions",
    dependencies=[Depends(require_permission("permissions:assign"))]
)
def route_assign_permission(
    role_id: int,
    data: RoleCreate,
    db: Session = Depends(get_db)
):
    return assign_permission_to_role(db, role_id, data.permissions)

@router.post(
    "/assign-role",
    dependencies=[Depends(require_permission("roles:assign"))]
)
def route_assign_role_to_user(
    data: AssingRole,
    db: Session = Depends(get_db)
):
    return assign_role_to_user(db, data.user_id, data.role_id)
