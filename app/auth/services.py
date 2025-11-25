from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.auth.models import User, PasswordReset
from app.core.utilitys import hash_password, verify_password, create_access_token
import uuid
import datetime

def register_user(db: Session, data):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(400, "El correo ya está registrado")

    user = User(
        email=data.email,
        full_name=data.full_name,
        password=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, data):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Credenciales inválidas")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def request_password_reset(db: Session, email: str):
    """Genera un token para restablecer contraseña."""
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(404, "No existe un usuario con ese correo")

    token = str(uuid.uuid4())
    expires = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    reset = PasswordReset(
        user_id=user.id,
        token=token,
        expires_at=expires
    )

    db.add(reset)
    db.commit()

    return {
        "message": "Token generado",
        "token": token
    }


def reset_password(db: Session, token: str, new_password: str):
    reset = (
        db.query(PasswordReset)
        .filter(PasswordReset.token == token)
        .first()
    )

    if not reset:
        raise HTTPException(404, "Token inválido")

    if reset.expires_at < datetime.datetime.utcnow():
        raise HTTPException(400, "El token ya expiró")

    user = db.query(User).filter(User.id == reset.user_id).first()
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    user.password = hash_password(new_password)
    db.commit()

    return {"message": "Contraseña actualizada con éxito"}
