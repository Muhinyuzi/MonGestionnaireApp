import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import engine
from app.config import settings

# ✅ Seed sécurisé (demo uniquement)
from app.db_create import seed

# Routers globaux
from app.routers import activation, reset_password

# Routers métier
from app.routers import (
    utilisateurs,
    taches,
    commentaires,
    login,
    router_password_change,
    techniciens,
)

# ======================================================
# ⚙ ENV
# ======================================================
ENV = os.getenv("ENV", "dev")       # dev | demo | prod
TESTING = os.getenv("TESTING") == "1"

port = int(os.getenv("PORT", 8000))

# ======================================================
# 🚀 APP
# ======================================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Tâches & Gestion Utilisateurs",
    version="1.0.0",
)

# ======================================================
# 🔁 STARTUP EVENTS
# ======================================================
@app.on_event("startup")
def startup_event():
    if TESTING:
        print("🧪 Startup skipped (TEST mode)")
        return

    print(f"🚀 Application boot — ENV={ENV}")

    # ✅ Seed automatique UNIQUEMENT en demo
    if ENV == "demo":
        seed()


# ======================================================
# 🌍 CORS
# ======================================================
app.add_middleware(
    CORSMiddleware,
    #allow_origins=settings.CORS_ORIGINS,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "https://mongestionnaireapp-1.onrender.com",   # 🌐 FRONT Render
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# 📦 STATIC FILES
# ======================================================
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# ======================================================
# 🏠 ROOT
# ======================================================
@app.get("/")
def root():
    return {"message": "Bienvenue sur l’API Tâches & Gestion Utilisateurs 🚀"}


# ======================================================
# 🔗 ROUTERS
# ======================================================
app.include_router(router_password_change.router)
app.include_router(activation.router)
app.include_router(reset_password.router)
app.include_router(login.router)

app.include_router(utilisateurs.router, prefix="/utilisateurs", tags=["Utilisateurs"])
app.include_router(taches.router, prefix="/taches", tags=["Tâches"])
app.include_router(commentaires.router, prefix="/commentaires", tags=["Commentaires"])
app.include_router(techniciens.router, prefix="/techniciens", tags=["Techniciens"])


# ======================================================
# ▶ LOCAL DEV
# ======================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=True)
