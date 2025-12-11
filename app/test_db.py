from app.database import Base, engine
from app.models import Utilisateur, Concentrateur, Action

# Crée toutes les tables
Base.metadata.create_all(bind=engine)
print("Connexion à la DB réussie et tables créées !")
