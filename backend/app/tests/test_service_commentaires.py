# app/tests/test_service_commentaires.py

import pytest
from app.tests.conftest import TestingSessionLocal
from app.models.tache import Tache
from app.models.utilisateur import Utilisateur
from app.schemas.schemas import CommentaireCreate
from app.services.commentaires import add_commentaire_service, get_commentaires_service


@pytest.fixture
def db():
    db = TestingSessionLocal()

    # --- Création utilisateur ---
    user = Utilisateur(
        nom="Alice",
        email="alice@test.com",
        mot_de_passe="12345678",
        type="admin",
        equipe="Dev"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # --- Création TÂCHE ---
    tache = Tache(
        titre="Tâche test",
        contenu="Contenu test",
        auteur_id=user.id,
        equipe="Dev"
    )
    db.add(tache)
    db.commit()
    db.refresh(tache)

    yield db
    db.close()


# -------------------------------------------------------------------------
# ✅ TEST ADD COMMENTAIRE
# -------------------------------------------------------------------------
def test_add_commentaire_service(db):
    """Test ajout de commentaire sur une tâche"""

    tache = db.query(Tache).first()
    user = db.query(Utilisateur).first()

    data = CommentaireCreate(
        contenu="Super tâche !",
        auteur_id=user.id,
        tache_id=tache.id
    )

    commentaire = add_commentaire_service(tache.id, data, db)

    assert commentaire.contenu == "Super tâche !"
    assert commentaire.auteur_id == user.id
    assert commentaire.tache_id == tache.id


# -------------------------------------------------------------------------
# ✅ TEST GET COMMENTAIRES
# -------------------------------------------------------------------------
def test_get_commentaires(db):
    """Test récupération des commentaires"""

    tache = db.query(Tache).first()
    user = db.query(Utilisateur).first()

    data = CommentaireCreate(
        contenu="Très bien",
        auteur_id=user.id,
        tache_id=tache.id
    )

    add_commentaire_service(tache.id, data, db)

    commentaires = get_commentaires_service(tache.id, db)

    assert len(commentaires) == 1
    assert commentaires[0].contenu == "Très bien"
