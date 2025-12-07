# app/routers/techniciens.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.utilisateur import Utilisateur
from app.schemas.schemas import UtilisateurOut
from app.auth import get_current_user

router = APIRouter()


# ---------------- LISTE TECHNICIENS ----------------
@router.get("/", response_model=dict)
def list_techniciens(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    techniciens = (
        db.query(Utilisateur)
        .filter(Utilisateur.type == "technicien")
        .order_by(Utilisateur.nom)
        .all()
    )

    # 🔥 Convertir en Pydantic
    return {
        "status": "success",
        "data": [UtilisateurOut.model_validate(t) for t in techniciens],
    }


# ---------------- DETAIL TECHNICIEN ----------------
@router.get("/{tech_id}", response_model=dict)
def get_technicien(
    tech_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    tech = (
        db.query(Utilisateur)
        .filter(Utilisateur.id == tech_id, Utilisateur.type == "technicien")
        .first()
    )

    if not tech:
        raise HTTPException(404, detail="Technicien non trouvé")

    # 🔥 Convertir en Pydantic
    return {
        "status": "success",
        "data": UtilisateurOut.model_validate(tech),
    }
