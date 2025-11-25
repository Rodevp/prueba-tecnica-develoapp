from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.roles.models import Role, Permission, RolePermission, UserRole
from app.auth.models import User

def create_role(db: Session, name: str):
    """Crear un rol nuevo."""
    existing = db.query(Role).filter(Role.name == name).first()
    if existing:
        raise HTTPException(400, "El rol ya existe")

    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def list_roles(db: Session):
    """Retornar todos los roles."""
    return db.query(Role).all()

def delete_role(db: Session, role_id: int):
    """Eliminar un rol."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(404, "Rol no encontrado")

    db.delete(role)
    db.commit()
    return {"message": "Rol eliminado"}

def create_permission(db: Session, name: str):
    """Crear un permiso."""
    existing = db.query(Permission).filter(Permission.name == name).first()
    if existing:
        raise HTTPException(400, "El permiso ya existe")

    perm = Permission(name=name)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm

def list_permissions(db: Session):
    """Retornar todos los permisos."""
    return db.query(Permission).all()

def assign_permission_to_role(db: Session, role_id: int, permission_name: str):
    """Asigna un permiso a un rol."""
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(404, "Rol no encontrado")

    permission = db.query(Permission).filter(Permission.name == permission_name).first()

    if not permission:
        # si no existe el permiso, lo creamos
        permission = Permission(name=permission_name)
        db.add(permission)
        db.commit()
        db.refresh(permission)

    # verificar si ya está asignado
    exists = db.query(RolePermission).filter(
        RolePermission.role_id == role_id,
        RolePermission.permission_id == permission.id
    ).first()

    if exists:
        raise HTTPException(400, "El rol ya tiene este permiso asignado")

    rp = RolePermission(role_id=role.id, permission_id=permission.id)
    db.add(rp)
    db.commit()

    return {"message": f"Permiso '{permission_name}' asignado al rol '{role.name}'"}


def assign_role_to_user(db: Session, user_id: int, role_id: int):
    """Asigna un rol a un usuario."""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(404, "Rol no encontrado")

    exists = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role_id
    ).first()

    if exists:
        raise HTTPException(400, "El usuario ya tiene ese rol")

    ur = UserRole(user_id=user.id, role_id=role.id)
    db.add(ur)
    db.commit()

    return {"message": f"Rol '{role.name}' asignado al usuario '{user.email}'"}


def get_user_permissions(db: Session, user_id: int):
    """Retorna una lista de permisos del usuario."""

    permissions = db.query(Permission.name).join(
        RolePermission, Permission.id == RolePermission.permission_id
    ).join(
        UserRole, UserRole.role_id == RolePermission.role_id
    ).filter(
        UserRole.user_id == user_id
    ).all()

    return [p[0] for p in permissions]


def user_has_permission(db: Session, user_id: int, permission_name: str) -> bool:
    """Verifica si un usuario tiene un permiso específico."""

    return db.query(RolePermission).join(
        UserRole, UserRole.role_id == RolePermission.role_id
    ).join(
        Permission, Permission.id == RolePermission.permission_id
    ).filter(
        UserRole.user_id == user_id,
        Permission.name == permission_name
    ).first() is not None