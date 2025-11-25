import jwt

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.core.constants import JWT_SECRET, JWT_ALGORITHM
from app.core.database import session_local
from app.auth.models import User
from app.roles.models import RolePermission, UserRole, Permission

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db() -> Session:
    db = session_local()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    """Encripta contraseña con bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verifica contraseña en texto plano contra hash."""
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_minutes: int = 1440):
    """Crea un JWT con expiración (default: 24 horas)."""
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Decodifica JWT y obtiene el usuario actual."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(401, "Token inválido")

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expirado")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Token inválido")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    user.permissions = get_user_permissions(db, user.id)

    return user

def get_user_permissions(db: Session, user_id: int):
    """Retorna una lista de permisos del usuario."""
    return [
        rp.permission.name
        for rp in db.query(RolePermission)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .join(Permission)
        .filter(UserRole.user_id == user_id)
        .all()
    ]

def require_permission(permission: str):
    """Decorator para proteger endpoints según permisos."""
    def decorator(user=Depends(get_current_user)):
        if permission not in user.permissions:
            raise HTTPException(403, f"No tienes permiso: {permission}")
        return user
    return decorator