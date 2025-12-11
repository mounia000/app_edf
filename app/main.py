from fastapi import FastAPI
from app.routes import utilisateurs, concentrateurs, actions

app = FastAPI(title="EDF CPL Backend")

# Inclure les routes
app.include_router(utilisateurs.router)
app.include_router(concentrateurs.router)
app.include_router(actions.router)

# Optionnel : une route test pour vérifier que le backend est actif
@app.get("/")
def home():
    return {"message": "Backend FastAPI actif 🚀"}
