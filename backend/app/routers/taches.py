# app/api/v1/taches.py
from fastapi import APIRouter, Depends, Form, File, UploadFile, Query, Request, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.utilisateur import Utilisateur
from app.schemas.schemas import (
    TacheOut,
    TacheDetailOut,
    TachesResponse,
    CommentaireOut,
    CommentaireCreate,
    TacheCreate
)
from app.services.taches import (
    create_tache_service,
    list_taches_service,
    get_tache_detail_service,
    update_tache_service,
    delete_tache_service,
    like_tache_service,
    get_commentaires_service,
    add_commentaire_service,
    delete_file_service,
)
from app.auth import get_current_user

router = APIRouter()

# ---------------- CREATE ----------------
@router.post("/", response_model=TacheOut)
async def create_tache(
    request: Request,
    titre: Optional[str] = Form(None),
    contenu: Optional[str] = Form(None),
    auteur_id: Optional[int] = Form(None),
    equipe: Optional[str] = Form(None),
    priorite: Optional[str] = Form("moyenne"),
    categorie: Optional[str] = Form(None),
    fichiers: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    current_user_id = current_user.get("id") if isinstance(current_user, dict) else current_user.id
    current_user_team = current_user.get("equipe") if isinstance(current_user, dict) else current_user.equipe

    if request.headers.get("content-type", "").startswith("application/json"):
        data = await request.json()

        titre = data.get("titre", titre)
        contenu = data.get("contenu", contenu)

        if not titre or not contenu:
            raise HTTPException(status_code=422, detail="titre et contenu sont obligatoires")

        auteur_id = data.get("auteur_id", current_user_id)
        equipe = data.get("equipe", current_user_team)
        priorite = data.get("priorite", priorite)
        categorie = data.get("categorie", categorie)
        fichiers = None

    else:
        auteur_id = auteur_id or current_user_id
        equipe = equipe or current_user_team

        if not titre or not contenu:
            raise HTTPException(status_code=422, detail="titre et contenu sont obligatoires")

    return create_tache_service(
        titre, contenu, auteur_id, equipe, priorite, categorie, fichiers, db, current_user
    )


# ---------------- LIST ----------------
# ---------------- LIST ----------------
@router.get("/", response_model=TachesResponse)
def list_taches(
    search: str = Query("", description="Mot-clé"),
    author: str = Query("", description="Nom auteur"),
    assign_to: Optional[int] = Query(None, description="Filtrer les tâches assignées à un utilisateur"),  # 🔥 ajouté ici
    sort: str = Query("date_desc", description="date_asc ou date_desc"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    result = list_taches_service(
        search=search,
        author=author,
        assign_to=assign_to,  # 🔥 transmis au service
        sort=sort,
        page=page,
        limit=limit,
        db=db,
        current_user=current_user
    )

    return {
        "total": result["total"],
        "page": page,
        "limit": limit,
        "taches": result["taches"],
    }


# ---------------- DETAIL ----------------
@router.get("/{tache_id}", response_model=TacheDetailOut)
def get_tache_detail(tache_id: int, db: Session = Depends(get_db)):
    return get_tache_detail_service(tache_id, db)


# ---------------- UPDATE ----------------
@router.put("/{tache_id}", response_model=TacheOut)
async def update_tache(
    tache_id: int,
    titre: str = Form(...),
    contenu: str = Form(...),
    equipe: Optional[str] = Form(None),
    categorie: Optional[str] = Form(None),
    priorite: Optional[str] = Form(None),
    fichiers: List[UploadFile] = File([]),
    db: Session = Depends(get_db),
):
    return await update_tache_service(
        tache_id, titre, contenu, equipe, categorie, priorite, fichiers, db
    )


# ---------------- DELETE ----------------
@router.delete("/{tache_id}", status_code=204)
def delete_tache(tache_id: int, db: Session = Depends(get_db)):
    return delete_tache_service(tache_id, db)


# ---------------- LIKE ----------------
@router.post("/{tache_id}/like")
def like_tache(tache_id: int, db: Session = Depends(get_db)):
    return like_tache_service(tache_id, db)


# ---------------- COMMENTAIRES ----------------
@router.get("/{tache_id}/commentaires", response_model=List[CommentaireOut])
def get_commentaires(tache_id: int, db: Session = Depends(get_db)):
    return get_commentaires_service(tache_id, db)


@router.post("/{tache_id}/commentaires", response_model=CommentaireOut)
def add_commentaire(tache_id: int, commentaire: CommentaireCreate, db: Session = Depends(get_db)):
    return add_commentaire_service(tache_id, commentaire, db)


# ---------------- SUPPRESSION DE FICHIER ----------------
@router.delete("/fichiers/{file_id}", response_model=dict)
def delete_file(file_id: int, db: Session = Depends(get_db)):
    return delete_file_service(file_id, db)
