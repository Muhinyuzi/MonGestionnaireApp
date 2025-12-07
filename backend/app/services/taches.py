from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import os, shutil
from datetime import datetime

from app.models.tache import Tache
from app.models.commentaire import Commentaire
from app.models.utilisateur import Utilisateur
from app.models.fichier import FichierTache
from app.schemas.schemas import CommentaireCreate, CommentaireOut

from app.services.some_ai_module import generate_summary

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==========================================================
#                     CRÉATION DE TÂCHE
# ==========================================================
def create_tache_service(
    titre, contenu, auteur_id, equipe, priorite, categorie, fichiers, db: Session, current_user: Utilisateur
):
    final_auteur_id = auteur_id or current_user.id

    tache = Tache(
        titre=titre,
        contenu=contenu,
        equipe=equipe or current_user.equipe,
        auteur_id=final_auteur_id,
        priorite=priorite,
        categorie=categorie,
        status="en_attente"   # 👈 nouvelle logique
    )

    db.add(tache)
    db.commit()
    db.refresh(tache)

    # ---------------- FICHIERS ----------------
    if fichiers:
        for f in fichiers:
            filename = f.filename.replace("\\", "/").split("/")[-1]
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(f.file, buffer)

            new_file = FichierTache(
                nom_fichier=filename,
                chemin=file_path,
                tache_id=tache.id
            )
            db.add(new_file)

        db.commit()
        db.refresh(tache)

    return tache


# ==========================================================
#                     LISTE FILTRÉE
# ==========================================================
def list_taches_service(
    search,
    author,
    assign_to,
    sort,
    page,
    limit,
    db: Session,
    current_user: Utilisateur
):
    # Admin = voit tout
    if current_user.type == "admin":
        query = db.query(Tache)
    else:
        # User normal = voit uniquement ses tâches assignées
        query = db.query(Tache).filter(Tache.assign_to_id == current_user.id)

    # Si l’admin filtre par utilisateur assigné
    if assign_to:
        query = query.filter(Tache.assign_to_id == assign_to)

    # Recherche
    if search:
        query = query.filter(
            Tache.titre.ilike(f"%{search}%") |
            Tache.contenu.ilike(f"%{search}%")
        )

    # Filtre auteur (admin only)
    if author and current_user.type == "admin":
        query = query.join(Tache.auteur).filter(
            Utilisateur.nom.ilike(f"%{author}%")
        )

    # Tri
    if sort == "date_asc":
        query = query.order_by(Tache.created_at.asc())
    else:
        query = query.order_by(Tache.created_at.desc())

    total = query.count()

    taches = (
        query.options(
            joinedload(Tache.auteur),
            joinedload(Tache.assign_to),
            joinedload(Tache.fichiers)
        )
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "taches": taches
    }


# ==========================================================
#                     DÉTAIL TÂCHE
# ==========================================================
def get_tache_detail_service(tache_id: int, db: Session):
    tache = (
        db.query(Tache)
        .options(
            joinedload(Tache.commentaires),
            joinedload(Tache.auteur),
            joinedload(Tache.assign_to),
            joinedload(Tache.fichiers)
        )
        .filter(Tache.id == tache_id)
        .first()
    )

    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    # ---------------- RESUME IA AUTOMATIQUE ----------------
    if not tache.resume_ia and tache.contenu and len(tache.contenu) > 100:
        try:
            tache.resume_ia = generate_summary(tache.contenu)
            db.commit()
        except Exception:
            db.rollback()

    # ---------------- Compteur de vues ----------------
    tache.nb_vues = (tache.nb_vues or 0) + 1
    db.commit()

    db.refresh(tache)
    return tache


# ==========================================================
#                     UPDATE TÂCHE
# ==========================================================
async def update_tache_service(tache_id, titre, contenu, equipe, categorie, priorite, fichiers, db: Session):
    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    tache.titre = titre
    tache.contenu = contenu
    tache.equipe = equipe or tache.equipe
    tache.categorie = categorie or tache.categorie
    tache.priorite = priorite or tache.priorite

    # ---------------- AJOUT FICHIERS ----------------
    for f in fichiers:
        file_location = f"uploads/{f.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await f.read())

        new_file = FichierTache(
            nom_fichier=f.filename,
            chemin=file_location,
            tache_id=tache.id
        )
        db.add(new_file)

    db.commit()
    db.refresh(tache)
    return tache


# ==========================================================
#                     DELETE TÂCHE
# ==========================================================
def delete_tache_service(tache_id: int, db: Session):
    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    db.delete(tache)
    db.commit()

    return None


# ==========================================================
#                     LIKE TÂCHE
# ==========================================================
def like_tache_service(tache_id: int, db: Session):
    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    tache.likes = (tache.likes or 0) + 1
    db.commit()
    db.refresh(tache)

    return {"likes": tache.likes}


# ==========================================================
#                     COMMENTAIRES
# ==========================================================
def get_commentaires_service(tache_id: int, db: Session):
    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    return tache.commentaires


def add_commentaire_service(tache_id: int, commentaire: CommentaireCreate, db: Session):
    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    auteur = db.query(Utilisateur).filter(Utilisateur.id == commentaire.auteur_id).first()
    if not auteur:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")

    new_comment = Commentaire(
        contenu=commentaire.contenu,
        auteur_id=commentaire.auteur_id,
        tache_id=tache_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return CommentaireOut.model_validate(new_comment)


# ==========================================================
#                     DELETE FICHIER
# ==========================================================
def delete_file_service(file_id: int, db: Session):
    fichier = db.query(FichierTache).filter(FichierTache.id == file_id).first()
    if not fichier:
        raise HTTPException(status_code=404, detail="Fichier non trouvé")

    if os.path.exists(fichier.chemin):
        os.remove(fichier.chemin)

    db.delete(fichier)
    db.commit()

    return {"detail": "Fichier supprimé avec succès"}
