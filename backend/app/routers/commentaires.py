from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.schemas import CommentaireCreate, CommentaireOut
from app.services.commentaires import add_commentaire_service
from app.models.utilisateur import Utilisateur
from app.models.tache import Tache
from app.auth import get_current_user

router = APIRouter()

@router.post("/taches/{tache_id}/commentaires", response_model=CommentaireOut)
def add_commentaire(
    tache_id: int,
    commentaire: CommentaireCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):

    # Déterminer automatiquement l'auteur si non fourni
    auteur_id = commentaire.auteur_id if commentaire.auteur_id else current_user.id

    # Construire le commentaire avec tache_id
    data = CommentaireCreate(
        contenu=commentaire.contenu,
        auteur_id=auteur_id,
        note_id=tache_id    # 👈 Tu dois renommer plus tard en "tache_id" dans ton schema
    )

    return add_commentaire_service(tache_id, data, db)
