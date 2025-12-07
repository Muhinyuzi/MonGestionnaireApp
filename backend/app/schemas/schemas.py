from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Generic, TypeVar
from datetime import datetime
from pydantic.generics import GenericModel

# ======================================================
# CONFIG GLOBALE — Pydantic v2+
# ======================================================
BaseModel.model_config = {"from_attributes": True}

# ======================================================
# UTILISATEUR (Employé)
# ======================================================
class UtilisateurBase(BaseModel):
    nom: str
    email: EmailStr

    equipe: Optional[str] = "Aucune"
    type: Optional[str] = "user"

    poste: Optional[str] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None
    date_embauche: Optional[datetime] = None


class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: Optional[str] = None


class UtilisateurUpdate(BaseModel):
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
    mot_de_passe: Optional[str] = None
    equipe: Optional[str] = None
    type: Optional[str] = None
    poste: Optional[str] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None
    date_embauche: Optional[datetime] = None
    avatar_url: Optional[str] = None


class UtilisateurOut(UtilisateurBase):
    id: int
    date: Optional[datetime]
    avatar_url: Optional[str] = None
    is_active: bool = False


class UtilisateurDetailOut(UtilisateurOut):
    taches: List["TacheOut"] = []
    commentaires: List["CommentaireOut"] = []
    assignations: List["TacheOut"] = []


# ======================================================
# FICHIERS TÂCHES
# ======================================================
class FichierTacheBase(BaseModel):
    nom_fichier: str
    chemin: str


class FichierTacheOut(FichierTacheBase):
    id: int
    tache_id: int


# ======================================================
# TÂCHES
# ======================================================
class TacheBase(BaseModel):
    titre: str
    contenu: str
    equipe: Optional[str] = None
    categorie: Optional[str] = None
    priorite: Optional[str] = "Moyenne"
    resume_ia: Optional[str] = None

    # 🔥 CHAMP STATUT OFFICIEL
    status: str = Field(default="en_attente", description="Statut : en_attente, active, fermee")


class TacheCreate(TacheBase):
    auteur_id: Optional[int] = None
    assign_to_id: Optional[int] = None


class TacheOut(TacheBase):
    id: int
    likes: int
    nb_vues: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    auteur: Optional[UtilisateurOut] = None
    assign_to: Optional[UtilisateurOut] = None

    fichiers: Optional[List[FichierTacheOut]] = []


class TacheDetailOut(TacheOut):
    commentaires: List["CommentaireOut"] = []


class TachesResponse(BaseModel):
    total: int
    page: int
    limit: int
    taches: List[TacheOut]


# ======================================================
# COMMENTAIRES
# ======================================================
class CommentaireBase(BaseModel):
    contenu: str


class CommentaireCreate(CommentaireBase):
    auteur_id: Optional[int] = None
    tache_id: Optional[int] = None


class CommentaireOut(CommentaireBase):
    id: int
    date: datetime
    auteur_id: int
    tache_id: int

    auteur: Optional[UtilisateurOut] = None
    tache: Optional[TacheOut] = None


# ======================================================
# EMAIL
# ======================================================
class EmailRequest(BaseModel):
    email: EmailStr


# ======================================================
# RÉFÉRENCES CIRCULAIRES
# ======================================================
UtilisateurDetailOut.model_rebuild()
TacheOut.model_rebuild()
TacheDetailOut.model_rebuild()
CommentaireOut.model_rebuild()
FichierTacheOut.model_rebuild()


# ======================================================
# RÉPONSE GÉNÉRIQUE
# ======================================================
T = TypeVar("T")


class ResponseModel(GenericModel, Generic[T]):
    status: str = Field(..., example="success")
    data: Optional[T] = None


class PaginatedUsers(BaseModel):
    total: int
    page: int
    limit: int
    users: List[UtilisateurOut]
