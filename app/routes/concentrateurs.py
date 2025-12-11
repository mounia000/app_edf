from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, auth  # importer auth pour la sécurité
from typing import Optional, List
from fastapi import Query

router = APIRouter(prefix="/concentrateurs", tags=["concentrateurs"])

# ---------------- DB ----------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- POST : créer un concentrateur ----------------
@router.post("/", response_model=schemas.ConcentrateurOut)
def create_concentrateur(conc: schemas.ConcentrateurCreate, db: Session = Depends(get_db)):
    return crud.create_concentrateur(db, conc)

# ---------------- GET : lister tous les concentrateurs ----------------
@router.get("/", response_model=List[schemas.ConcentrateurOut])
def list_concentrateurs(db: Session = Depends(get_db)):
    return crud.get_concentrateurs(db)

# ---------------- GET : recherche ----------------
@router.get("/search", response_model=List[schemas.ConcentrateurOut])
def search_concentrateurs(
    numero_serie: Optional[str] = Query(None, description="Numéro de série exact ou partiel"),
    statut: Optional[str] = Query(None, description="Filtrer par statut"),
    emplacement: Optional[str] = Query(None, description="Filtrer par emplacement"),
    db: Session = Depends(get_db)
):
    query = db.query(crud.models.Concentrateur)
    
    if numero_serie:
        query = query.filter(crud.models.Concentrateur.numero_serie.ilike(f"%{numero_serie}%"))
    if statut:
        query = query.filter(crud.models.Concentrateur.statut == statut)
    if emplacement:
        query = query.filter(crud.models.Concentrateur.emplacement.ilike(f"%{emplacement}%"))
    
    return query.all()

# ---------------- GET : scan par numéro de série (magasin seulement) ----------------
@router.get("/scan/{numero_serie}", response_model=schemas.ConcentrateurOut)
def scan_concentrateur(
    numero_serie: str,
    db: Session = Depends(get_db),
    user: auth.models.Utilisateur = Depends(auth.require_magasin)  # protection rôle magasin
):
    conc = db.query(crud.models.Concentrateur).filter_by(numero_serie=numero_serie).first()
    if not conc:
        raise HTTPException(status_code=404, detail="Concentrateur non trouvé")
    return conc

# ---------------- GET : détails par ID ----------------
@router.get("/{conc_id}", response_model=schemas.ConcentrateurOut)
def get_concentrateur(conc_id: int, db: Session = Depends(get_db)):
    conc = crud.get_concentrateur(db, conc_id)
    if not conc:
        raise HTTPException(status_code=404, detail="Concentrateur non trouvé")
    return conc
