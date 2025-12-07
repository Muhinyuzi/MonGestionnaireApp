# app/services/commentaires.py

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.commentaire import Commentaire
from app.models.tache import Tache
from app.models.utilisateur import Utilisateur
from app.schemas.schemas import CommentaireCreate, CommentaireOut


# ==========================================================
#                AJOUTER UN COMMENTAIRE SUR TÂCHE
# ==========================================================
def add_commentaire_service(tache_id: int, commentaire: CommentaireCreate, db: Session):
    # 1️⃣ Vérifier si l'auteur existe (respect tests)
    auteur = db.query(Utilisateur).filter(Utilisateur.id == commentaire.auteur_id).first()
    if not auteur:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")

    # 2️⃣ Vérifier si la tâche existe
    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    # 3️⃣ Créer le commentaire
    new_comment = Commentaire(
        contenu=commentaire.contenu,
        auteur_id=commentaire.auteur_id,
        tache_id=tache_id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return CommentaireOut.model_validate(new_comment)


# ==========================================================
#                OBTENIR COMMENTAIRES D'UNE TÂCHE
# ==========================================================
def get_commentaires_service(tache_id: int, db: Session):
    commentaires = (
        db.query(Commentaire)
        .filter(Commentaire.tache_id == tache_id)
        .order_by(Commentaire.id.asc())
        .all()
    )

    return [CommentaireOut.model_validate(c) for c in commentaires]
