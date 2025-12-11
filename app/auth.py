# app/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app import database, models

# -----------------------------
# CONFIGURATION
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------
# DB DEPENDENCY
# -----------------------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# PASSWORD HASHING
# -----------------------------
def hash_password(password: str) -> str:
    # bcrypt n'accepte pas plus de 72 bytes → on tronque par sécurité
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

# -----------------------------
# TOKEN (SIMPLIFIÉ pour tests)
# -----------------------------
def decode_token(token: str) -> int:
    """
    Fake decode POUR TEST.
    Plus tard → remplacer par un vrai JWT.
    """
    return 1  # on simule user_id = 1

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_token(token)

    user = db.query(models.Utilisateur).filter(models.Utilisateur.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur invalide"
        )

    return user

# -----------------------------
# ROLE CHECK
# -----------------------------
def require_magasin(user: models.Utilisateur = Depends(get_current_user)):
    if user.role != "magasin":
        raise HTTPException(
            status_code=403,
            detail="Accès refusé : rôle 'magasin' requis"
        )
    return user
