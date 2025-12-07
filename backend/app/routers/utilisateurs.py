# app/routers/utilisateurs.py

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.utilisateur import Utilisateur
from app.schemas.schemas import (
    UtilisateurCreate,
    UtilisateurOut,
    UtilisateurDetailOut,
    PaginatedUsers,
    UtilisateurUpdate,
)
from app.auth import get_current_user

from app.services.utilisateurs import (
    create_user_service,
    list_users_service,
    get_user_detail_service,
    update_user_service,
    delete_user_service,
    upload_avatar_service,
    get_avatar_service,

    # 👇 nouveaux services adaptés aux TACHES
    assign_tache_to_user_service,
    unassign_tache_from_user_service,
    close_tache_service,
)

router = APIRouter()

# ---------------- CREATE ----------------
@router.post("/", response_model=dict)
def create_user(
    user: UtilisateurCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    new_user = create_user_service(user, db, current_user, background_tasks)
    return {"status": "success", "data": new_user}


# ---------------- LIST ----------------
@router.get("/", response_model=dict)
def list_users(
    nom: str = Query("", description="Filtrer par nom"),
    email: str = Query("", description="Filtrer par email"),
    equipe: str = Query("", description="Filtrer par équipe"),
    type_: str = Query("", alias="type", description="Filtrer par type"),
    sort: str = Query("nom_asc", description="nom_asc, nom_desc, date_asc, date_desc"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    data = list_users_service(nom, email, equipe, type_, sort, page, limit, db, current_user)
    return {"status": "success", "data": data}


# ---------------- DETAIL ----------------
@router.get("/{user_id}", response_model=dict)
def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    user = get_user_detail_service(user_id, db, current_user)
    return {"status": "success", "data": user}


# ---------------- UPDATE ----------------
@router.put("/{user_id}", response_model=dict)
def update_user(
    user_id: int,
    updated: UtilisateurUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    updated_user = update_user_service(user_id, updated, db, current_user)

    return {
        "status": "success",
        "data": UtilisateurOut.model_validate(updated_user).model_dump()
    }


# ---------------- DELETE ----------------
@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    delete_user_service(user_id, db, current_user)
    return {"status": "success", "data": {"message": "Utilisateur supprimé avec succès"}}


# ---------------- UPLOAD AVATAR ----------------
@router.post("/{user_id}/avatar", response_model=dict)
async def upload_avatar(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    data = await upload_avatar_service(user_id, file, db)
    return {"status": "success", "data": data}


# ---------------- GET AVATAR ----------------
@router.get("/{user_id}/avatar")
async def get_avatar(
    user_id: int,
    db: Session = Depends(get_db),
):
    return await get_avatar_service(user_id, db)


# ===========================================================
#            🎯  GESTION DES TÂCHES PAR UTILISATEUR
# ===========================================================

# ------------ ASSIGNER UNE TÂCHE ----------------
@router.post("/{user_id}/assign-tache/{tache_id}", response_model=dict)
def assign_tache_to_user(
    user_id: int,
    tache_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    data = assign_tache_to_user_service(user_id, tache_id, current_user, db)
    return {"status": "success", "data": data}


# ------------ DÉSASSIGNER UNE TÂCHE ----------------
@router.post("/{user_id}/unassign-tache/{tache_id}", response_model=dict)
def unassign_tache_from_user(
    user_id: int,
    tache_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    data = unassign_tache_from_user_service(user_id, tache_id, current_user, db)
    return {"status": "success", "data": data}


# ------------ FERMER UNE TÂCHE --------------------
@router.post("/{user_id}/close-tache/{tache_id}", response_model=dict)
def close_tache(
    user_id: int,
    tache_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    data = close_tache_service(tache_id, current_user, db)
    return {"status": "success", "data": data}
