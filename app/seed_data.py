from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Utilisateur, Concentrateur, Action
from werkzeug.security import generate_password_hash
from datetime import datetime

db: Session = SessionLocal()

# ------------------ Utilisateurs ------------------
utilisateurs_initiaux = [
    {"nom": "Dupont", "prenom": "Jean", "email": "bo@edf.fr", "role": "bo"},
    {"nom": "Martin", "prenom": "Claire", "email": "magasin@edf.fr", "role": "magasin"},
    {"nom": "Durand", "prenom": "Luc", "email": "labo@edf.fr", "role": "labo"},
    {"nom": "Admin", "prenom": "Admin", "email": "admin@edf.fr", "role": "admin"}
]

utilisateurs_obj = {}
for u in utilisateurs_initiaux:
    existing = db.query(Utilisateur).filter_by(email=u["email"]).first()
    if not existing:
        user = Utilisateur(
            nom=u["nom"],
            prenom=u["prenom"],
            email=u["email"],
            mot_de_passe=generate_password_hash("Base2026"),
            role=u["role"]
        )
        db.add(user)
        db.flush()  # pour récupérer l'ID
        utilisateurs_obj[u["email"]] = user
    else:
        utilisateurs_obj[u["email"]] = existing

# ------------------ Concentrateurs ------------------
concentrateurs_initiaux = [
    {"numero_serie": "KB71O205687", "statut": "en_transit", "emplacement": "Magasin", "poste_pose": None},
    {"numero_serie": "KB71O205688", "statut": "en_stock", "emplacement": "BO Nord", "poste_pose": None},
    {"numero_serie": "KB71O205689", "statut": "posé", "emplacement": "BO Centre", "poste_pose": "Poste A"},
    {"numero_serie": "KB71O205690", "statut": "à_tester", "emplacement": "Labo", "poste_pose": None},
]

concentrateurs_obj = {}
for c in concentrateurs_initiaux:
    existing = db.query(Concentrateur).filter_by(numero_serie=c["numero_serie"]).first()
    if not existing:
        conc = Concentrateur(
            numero_serie=c["numero_serie"],
            statut=c["statut"],
            emplacement=c["emplacement"],
            poste_pose=c["poste_pose"]
        )
        db.add(conc)
        db.flush()
        concentrateurs_obj[c["numero_serie"]] = conc
    else:
        concentrateurs_obj[c["numero_serie"]] = existing

# ------------------ Actions ------------------
actions_initiaux = [
    {"concentrateur": "KB71O205687", "type_action": "réception", "utilisateur": "magasin@edf.fr", "emplacement": "Magasin", "commentaire": "Réception initiale"},
    {"concentrateur": "KB71O205688", "type_action": "transfert", "utilisateur": "bo@edf.fr", "emplacement": "BO Nord", "commentaire": "Transfert vers BO Nord"},
    {"concentrateur": "KB71O205689", "type_action": "pose", "utilisateur": "bo@edf.fr", "emplacement": "Poste A", "commentaire": "Installation poste A"},
    {"concentrateur": "KB71O205690", "type_action": "test", "utilisateur": "labo@edf.fr", "emplacement": "Labo", "commentaire": "Test labo"},
]

for a in actions_initiaux:
    conc = concentrateurs_obj[a["concentrateur"]]
    user = utilisateurs_obj[a["utilisateur"]]
    existing = db.query(Action).filter_by(concentrateur_id=conc.id, type_action=a["type_action"]).first()
    if not existing:
        action = Action(
            concentrateur_id=conc.id,
            type_action=a["type_action"],
            utilisateur_id=user.id,
            emplacement=a["emplacement"],
            commentaire=a["commentaire"]
        )
        db.add(action)

# ------------------ Commit final ------------------
db.commit()
db.close()

print("Seed data inséré : utilisateurs, concentrateurs et actions !")
