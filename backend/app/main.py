import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db import Base, engine
from app.config import settings

# Routers globaux
from app.routers import activation
from app.routers import reset_password

# Routers groupés (ta structure est correcte)
from app.routers import utilisateurs, taches, commentaires, login, router_password_change, techniciens


# 🔧 Force le mode production
os.environ["TESTING"] = "0"

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Tâches & Gestion Utilisateurs",
    version="1.0.0",
)

IS_TEST = os.getenv("TESTING") == "1"

if IS_TEST:
    print("🧪 Startup skipped (TEST mode)")
else:
    print("🚀 Application boot — Production mode")
    Base.metadata.create_all(bind=engine)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "Bienvenue sur l’API Tâches & Gestion Utilisateurs 🚀"}


# ROUTERS
app.include_router(router_password_change.router)
app.include_router(activation.router)
app.include_router(reset_password.router)
app.include_router(login.router)

app.include_router(utilisateurs.router, prefix="/utilisateurs", tags=["Utilisateurs"])
app.include_router(taches.router, prefix="/taches", tags=["Tâches"])
app.include_router(commentaires.router, prefix="/commentaires", tags=["Commentaires"])
app.include_router(techniciens.router, prefix="/techniciens", tags=["Techniciens"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
