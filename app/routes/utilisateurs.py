from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/utilisateurs", tags=["utilisateurs"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UtilisateurOut)
def create_utilisateur(utilisateur: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    return crud.create_utilisateur(db, utilisateur)

@router.get("/", response_model=list[schemas.UtilisateurOut])
def list_utilisateurs(db: Session = Depends(get_db)):
    return crud.get_utilisateurs(db)
