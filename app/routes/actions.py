from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/actions", tags=["actions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ActionOut)
def create_action(action: schemas.ActionCreate, db: Session = Depends(get_db)):
    return crud.create_action(db, action)

@router.get("/concentrateur/{conc_id}", response_model=list[schemas.ActionOut])
def get_actions(conc_id: int, db: Session = Depends(get_db)):
    return crud.get_actions_by_concentrateur(db, conc_id)
