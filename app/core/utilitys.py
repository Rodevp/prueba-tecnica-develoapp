import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.core.constants import JWT_SECRET, JWT_ALGORITHM
from app.core.database import session_local
from app.auth.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
http_bearer = HTTPBearer()

def get_db() -> Session:
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    plain = plain[:72]
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_minutes: int = 1440):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
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

    user.permissions = [p.name for p in user.role.permissions]

    return user


def require_permission(permission: str):
    def decorator(user=Depends(get_current_user)):
        if permission not in user.permissions:
            raise HTTPException(403, f"No tienes permiso: {permission}")
        return user
    return decorator
