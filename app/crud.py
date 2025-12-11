# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import hash_password
from sqlalchemy.exc import SQLAlchemyError

# ------------------
# UTILISATEURS
# ------------------
'''
def create_utilisateur(db: Session, utilisateur: schemas.UtilisateurCreate):
    db_user = models.Utilisateur(
        nom=utilisateur.nom,
        prenom=utilisateur.prenom,
        email=utilisateur.email,
        mot_de_passe=hash_password(utilisateur.mot_de_passe),  # hashed !
        role=utilisateur.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
'''


def create_utilisateur(db: Session, utilisateur: schemas.UtilisateurCreate):
    try:
        db_user = models.Utilisateur(
            nom=utilisateur.nom,
            prenom=utilisateur.prenom,
            email=utilisateur.email,
            mot_de_passe=hash_password(utilisateur.mot_de_passe),  # hashed !
            role=utilisateur.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        print("ERREUR DB:", e)
        raise


def get_utilisateurs(db: Session):
    return db.query(models.Utilisateur).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()

# ------------------
# CONCENTRATEURS
# ------------------
def create_concentrateur(db: Session, concentrateur: schemas.ConcentrateurCreate):
    db_conc = models.Concentrateur(
        numero_serie=concentrateur.numero_serie,
        statut=concentrateur.statut,
        emplacement=concentrateur.emplacement,
        poste_pose=concentrateur.poste_pose
    )
    db.add(db_conc)
    db.commit()
    db.refresh(db_conc)
    return db_conc

def get_concentrateurs(db: Session):
    return db.query(models.Concentrateur).all()

def get_concentrateur(db: Session, conc_id: int):
    return db.query(models.Concentrateur).filter(models.Concentrateur.id == conc_id).first()

# ------------------
# ACTIONS
# ------------------
def create_action(db: Session, action: schemas.ActionCreate):
    db_act = models.Action(
        concentrateur_id=action.concentrateur_id,
        type_action=action.type_action,
        utilisateur_id=action.utilisateur_id,
        emplacement=action.emplacement,
        commentaire=action.commentaire
    )
    db.add(db_act)
    db.commit()
    db.refresh(db_act)
    return db_act

def get_actions_by_concentrateur(db: Session, conc_id: int):
    return db.query(models.Action).filter(models.Action.concentrateur_id == conc_id).all()
