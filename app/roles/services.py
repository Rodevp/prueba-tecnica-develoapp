from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.roles.models import Role, Permission
from app.auth.models import User
from app.roles.models import Permission, Role

def create_role(db: Session, name: str):
    existing = db.query(Role).filter(Role.name == name).first()
    if existing:
        raise HTTPException(400, "El rol ya existe")

    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def list_roles(db: Session):
    return db.query(Role).all()


def delete_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(404, "Rol no encontrado")

    db.delete(role)
    db.commit()
    return {"message": "Rol eliminado"}


def create_permission(db: Session, role_id: int, name: str):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(404, "Rol no encontrado")

    perm = Permission(name=name, role_id=role_id)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm


def list_permissions(db: Session):
    return db.query(Permission).all()


def assign_role_to_user(db: Session, user_id: int, role_id: int):
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(404, "Rol no encontrado")

    user.role_id = role_id
    db.commit()

    return {"message": f"Rol '{role.name}' asignado al usuario '{user.email}'"}


def assign_permission_to_role(db: Session, role_id: int, permission_names: List[str]):

    print(permission_names)

    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(404, f"Rol con ID {role_id} no encontrado.")

    permissions_to_assign = db.query(Permission).filter(
        Permission.name.in_(permission_names)
    ).all()
    
    if not permissions_to_assign:
        if not permission_names:
            return {"message": f"No se proporcionaron permisos para el rol {role.name}."}
        else:
             raise HTTPException(404, "No se encontraron permisos válidos con esos nombres.")
    for permission in permissions_to_assign:
        permission.role_id = role_id
        db.add(permission)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail=f"Error de base de datos al asignar permisos: {str(e)}")

    assigned_count = len(permissions_to_assign)
    return {
        "message": f"Se reasignaron {assigned_count} permisos al rol '{role.name}' (ID: {role_id}).",
        "permissions_assigned": [p.name for p in permissions_to_assign]
    }