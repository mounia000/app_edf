# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Import des routers depuis le dossier routes
from app.routes.utilisateurs import router as utilisateurs_router
from app.routes.concentrateurs import router as concentrateurs_router
from app.routes.actions import router as actions_router

# Import du reste
from app import auth, schemas, database

# Créer l'application FastAPI
app = FastAPI(title="EDF CPL Backend")

# Inclure les routes
app.include_router(utilisateurs_router)
app.include_router(concentrateurs_router)
app.include_router(actions_router)

# Route test pour vérifier que le backend est actif
@app.get("/")
def home():
    return {"message": "Backend FastAPI actif 🚀"}

# Route LOGIN
@app.post("/login", response_model=schemas.TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(auth.get_db)
):
    # Chercher l'utilisateur par email
    user = db.query(auth.models.Utilisateur).filter(auth.models.Utilisateur.email == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.mot_de_passe):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    # Pour l'instant, le token est juste l'id de l'utilisateur
    return {"access_token": str(user.id), "token_type": "bearer"}
