from pydantic import BaseModel
from typing import Optional

# ------------------ Utilisateur ------------------
class UtilisateurCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    mot_de_passe: str
    role: str  # "bo", "magasin", "labo", "admin"

class UtilisateurOut(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    role: str

    class Config:
        orm_mode = True

# ------------------ Concentrateur ------------------
class ConcentrateurCreate(BaseModel):
    numero_serie: str
    statut: str  # "en_transit", "en_stock", "posé", "HS", "à_tester"
    emplacement: Optional[str] = None
    poste_pose: Optional[str] = None

class ConcentrateurOut(BaseModel):
    id: int
    numero_serie: str
    statut: str
    emplacement: str
    poste_pose: Optional[str]

    class Config:
        orm_mode = True

# ------------------ Action ------------------
class ActionCreate(BaseModel):
    concentrateur_id: int
    type_action: str  # "réception", "pose", "dépose", "transfert", "test", "HS"
    utilisateur_id: int
    emplacement: Optional[str] = None
    commentaire: Optional[str] = None

class ActionOut(BaseModel):
    id: int
    concentrateur_id: int
    type_action: str
    utilisateur_id: int
    emplacement: Optional[str]
    commentaire: Optional[str]

    class Config:
        orm_mode = True
