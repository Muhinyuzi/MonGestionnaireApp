from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, UploadFile, BackgroundTasks, status
from fastapi.responses import FileResponse
from app.models.utilisateur import Utilisateur
from app.models.tache import Tache
from app.schemas.schemas import (
    UtilisateurOut,
    UtilisateurDetailOut,
    TacheOut
)
from app.emails import send_activation_email, send_registration_email
from app.config import settings
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os, shutil

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Répertoire avatars
AVATAR_DIR = "uploads/avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)


# ======================================================
# 🔹 UTILITAIRES
# ======================================================
def _is_admin(user):
    """Retourne True si user est admin, compatible ORM/dict."""
    if not user:
        return False
    user_type = getattr(user, "type", None) or (user.get("type") if isinstance(user, dict) else None)
    return (user_type or "").lower() == "admin"


def _user_id(user):
    """Retourne l’ID utilisateur, compatible dict/ORM."""
    return getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)


# ======================================================
# 🔸 CRÉATION UTILISATEUR
# ======================================================
def create_user_service(user_data, db: Session, current_user, background_tasks: BackgroundTasks):

    if not _is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les administrateurs peuvent créer des utilisateurs."
        )

    if db.query(Utilisateur).filter(Utilisateur.email == user_data.email).first():
        raise HTTPException(
            status_code=400,
            detail="Un utilisateur avec cet email existe déjà."
        )

    hashed_password = pwd_context.hash(user_data.mot_de_passe or "changeme123")

    new_user = Utilisateur(
        nom=user_data.nom,
        email=user_data.email,
        mot_de_passe=hashed_password,
        equipe=user_data.equipe,
        type=user_data.type or "user",
        poste=user_data.poste,
        telephone=user_data.telephone,
        adresse=user_data.adresse,
        date_embauche=user_data.date_embauche,
        is_active=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # ------ Token activation ------
    token = jwt.encode(
        {
            "sub": new_user.email,
            "type": "activation",
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        },
        settings.JWT_SECRET,
        algorithm="HS256"
    )

    # ------ Emails ------
    try:
        background_tasks.add_task(
            send_registration_email,
            new_user.email,
            new_user.nom,
            user_data.mot_de_passe or "changeme123"
        )

        background_tasks.add_task(
            send_activation_email,
            new_user.email,
            new_user.nom,
            token
        )
    except Exception as e:
        print(f"⚠️ Email error: {e}")

    return UtilisateurOut.model_validate(new_user)


# ======================================================
# 🔸 LISTER UTILISATEURS
# ======================================================
def list_users_service(nom, email, equipe, type_, sort, page, limit, db: Session, current_user):

    if not _is_admin(current_user):
        raise HTTPException(status_code=403, detail="Action réservée aux administrateurs.")

    query = db.query(Utilisateur)

    if nom:
        query = query.filter(Utilisateur.nom.ilike(f"%{nom}%"))
    if email:
        query = query.filter(Utilisateur.email.ilike(f"%{email}%"))
    if equipe:
        query = query.filter(Utilisateur.equipe.ilike(f"%{equipe}%"))
    if type_:
        query = query.filter(Utilisateur.type.ilike(f"%{type_}%"))

    # Tri
    if sort == "nom_desc":
        query = query.order_by(Utilisateur.nom.desc())
    elif sort == "date_asc":
        query = query.order_by(Utilisateur.date)
    elif sort == "date_desc":
        query = query.order_by(Utilisateur.date.desc())
    else:
        query = query.order_by(Utilisateur.nom.asc())

    total = query.count()

    users = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "users": [UtilisateurOut.model_validate(u) for u in users],
    }


# ======================================================
# 🔸 DÉTAIL UTILISATEUR
# ======================================================
def get_user_detail_service(user_id: int, db: Session, current_user):

    current_id = _user_id(current_user)

    if not _is_admin(current_user) and current_id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé.")

    user = db.query(Utilisateur).options(
        joinedload(Utilisateur.taches),             # tâches créées
        joinedload(Utilisateur.commentaires)        # commentaires écrits
    ).filter(Utilisateur.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    # TÂCHES assignées à cet utilisateur
    assignations = (
        db.query(Tache)
        .options(joinedload(Tache.auteur), joinedload(Tache.fichiers))
        .filter(Tache.assign_to_id == user_id)
        .all()
    )

    user_out = UtilisateurDetailOut.model_validate(user)
    user_out.assignations = [TacheOut.model_validate(t) for t in assignations]

    return user_out


# ======================================================
# 🔸 UPDATE UTILISATEUR
# ======================================================
def update_user_service(user_id: int, updated_data, db: Session, current_user):

    current_id = _user_id(current_user)

    # Admin ou lui-même
    if not _is_admin(current_user) and current_id != user_id:
        raise HTTPException(status_code=403, detail="Action non autorisée.")

    user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    # Compatible dict + Pydantic
    if hasattr(updated_data, "model_dump"):
        data = updated_data.model_dump(exclude_unset=True)
    else:
        data = updated_data  # dict direct dans tes tests

    # Empêcher duplication email
    if "email" in data:
        exists = db.query(Utilisateur).filter(
            Utilisateur.email == data["email"],
            Utilisateur.id != user_id
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email déjà utilisé.")

    # Mise à jour simple
    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

# ======================================================
# 🔸 SUPPRESSION UTILISATEUR
# ======================================================
def delete_user_service(user_id: int, db: Session, current_user):

    if not _is_admin(current_user):
        raise HTTPException(status_code=403, detail="Action réservée aux administrateurs.")

    user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    db.delete(user)
    db.commit()
    return {"message": "Utilisateur supprimé avec succès."}


# ======================================================
# 🔸 UPLOAD AVATAR
# ======================================================
async def upload_avatar_service(user_id: int, file: UploadFile, db: Session):

    user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    ext = file.filename.split(".")[-1].lower()
    allowed = {"png", "jpg", "jpeg", "gif"}

    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Format non autorisé.")

    contents = await file.read()

    if len(contents) > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 2 Mo).")

    filename = f"user_{user_id}.{ext}"
    path = os.path.join(AVATAR_DIR, filename)

    with open(path, "wb") as f:
        f.write(contents)

    user.avatar_url = f"http://127.0.0.1:8000/uploads/avatars/{filename}"

    db.commit()
    db.refresh(user)

    return {"avatar_url": user.avatar_url}


# ======================================================
# 🔸 GET AVATAR
# ======================================================
async def get_avatar_service(user_id: int, db: Session):

    user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()

    if not user or not user.avatar_url:
        raise HTTPException(status_code=404, detail="Avatar non trouvé.")

    path = user.avatar_url.replace("http://127.0.0.1:8000/", "")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fichier introuvable.")

    return FileResponse(path)


# ======================================================
# 🔸 ASSIGNATION TÂCHE
# ======================================================
def assign_tache_to_user_service(user_id: int, tache_id: int, current_user, db: Session):

    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    old_assign = tache.assign_to_id

    # Nouvelle logique : devient ACTIVE
    tache.assign_to_id = user_id
    tache.status = "active"
    tache.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(tache)

    return {
        "detail": "Tâche assignée",
        "tache_id": tache_id,
        "old_assign": old_assign,
        "new_assign": user_id,
        "status": tache.status
    }


# ======================================================
# 🔸 DÉSASSIGNATION TÂCHE
# ======================================================
def unassign_tache_from_user_service(tache_id: int, current_user, db: Session):

    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    old_assign = tache.assign_to_id

    tache.assign_to_id = None
    tache.status = "en_attente"
    tache.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(tache)

    return {
        "detail": "Tâche désassignée",
        "tache_id": tache_id,
        "old_assign": old_assign,
        "new_assign": None,
        "status": tache.status
    }


# ======================================================
# 🔸 FERMETURE TÂCHE
# ======================================================
def close_tache_service(tache_id: int, current_user, db: Session):

    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    tache.status = "fermee"
    tache.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(tache)

    return {
        "detail": "Tâche fermée",
        "tache_id": tache_id,
        "status": "fermee"
    }
