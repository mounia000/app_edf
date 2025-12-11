from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

# ------------------ Utilisateur ------------------
class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "bo", "magasin", "labo", "admin"

# ------------------ Concentrateur ------------------
class Concentrateur(Base):
    __tablename__ = "concentrateurs"
    id = Column(Integer, primary_key=True, index=True)
    numero_serie = Column(String, unique=True, nullable=False)
    statut = Column(String, nullable=False)  # "en_transit", "en_stock", "posé", "HS", "à_tester"
    emplacement = Column(String, nullable=False)  # "Magasin", "BO Nord", etc.
    poste_pose = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    actions = relationship("Action", back_populates="concentrateur")

# ------------------ Action ------------------
class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    concentrateur_id = Column(Integer, ForeignKey("concentrateurs.id"))
    type_action = Column(String, nullable=False)  # "réception", "pose", "dépose", "transfert", "test", "HS"
    date_action = Column(DateTime(timezone=True), server_default=func.now())
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    emplacement = Column(String, nullable=True)
    commentaire = Column(String, nullable=True)

    concentrateur = relationship("Concentrateur", back_populates="actions")
