import io
import pytest
from fastapi import HTTPException, UploadFile
from app.tests.conftest import TestingSessionLocal
from app.models.utilisateur import Utilisateur
from app.models.tache import Tache
from app.models.fichier import FichierTache
from app.models.commentaire import Commentaire
from app.schemas.schemas import CommentaireCreate
from app.services.taches import (
    create_tache_service,
    list_taches_service,
    get_tache_detail_service,
    update_tache_service,
    delete_tache_service,
    like_tache_service,
    get_commentaires_service,
    add_commentaire_service,
    delete_file_service
)

# =========================================================
# 🔧 Fake utilisateur
# =========================================================
class FakeUser:
    id = 1
    equipe = "Dev"
    type = "admin"

fake_user = FakeUser()


# =========================================================
# 🔧 DB fixture
# =========================================================
@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    yield db
    db.rollback()
    db.close()


# =========================================================
# 🔹 CREATE TÂCHE
# =========================================================
def test_create_tache_service(db_session):
    user = Utilisateur(nom="Jean", email="jean@test.com", mot_de_passe="123", type="admin")
    db_session.add(user)
    db_session.commit()

    t = create_tache_service(
        titre="T1",
        contenu="Contenu",
        auteur_id=user.id,
        equipe="Dev",
        priorite="haute",
        categorie="info",
        fichiers=None,
        db=db_session,
        current_user=user
    )

    assert t.id is not None
    assert t.status == "en_attente"


def test_create_tache_with_files(tmp_path, db_session):
    # créer utilisateur
    user = Utilisateur(nom="Leo", email="leo@test.com", mot_de_passe="123", type="admin")
    db_session.add(user)
    db_session.commit()

    # simulate upload file
    fake_file = UploadFile(filename="doc.txt", file=io.BytesIO(b"hello"))

    tache = create_tache_service(
        "Titre",
        "Contenu",
        user.id,
        "Dev",
        "haute",
        "info",
        fichiers=[fake_file],
        db=db_session,
        current_user=user
    )

    assert len(tache.fichiers) == 1


# =========================================================
# 🔹 LIST TÂCHES
# =========================================================
def test_list_taches_service(db_session):
    # préparer
    for i in range(3):
        t = Tache(titre=f"T{i}", contenu="X", auteur_id=1, equipe="Dev")
        db_session.add(t)
    db_session.commit()

    user = FakeUser()

    res = list_taches_service(
        search=None,
        author=None,
        sort="date_desc",
        page=1,
        limit=10,
        db=db_session,
        current_user=user
    )

    assert res["total"] >= 3
    assert len(res["taches"]) >= 3


def test_list_taches_search(db_session):
    t = Tache(titre="Install Fibre", contenu="Travail urgent", auteur_id=1, equipe="Dev")
    db_session.add(t)
    db_session.commit()

    res = list_taches_service(
        search="fibre",
        author=None,
        sort="date_desc",
        page=1,
        limit=10,
        db=db_session,
        current_user=fake_user
    )

    assert res["total"] == 1
    assert "Install Fibre" in res["taches"][0].titre


# =========================================================
# 🔹 DÉTAIL TÂCHE
# =========================================================
def test_get_tache_detail_ok(db_session):
    t = Tache(titre="T", contenu="X" * 200, auteur_id=1, equipe="Dev")
    db_session.add(t)
    db_session.commit()

    res = get_tache_detail_service(t.id, db_session)
    assert res.id == t.id
    assert res.nb_vues == 1


def test_get_tache_detail_not_found(db_session):
    with pytest.raises(HTTPException):
        get_tache_detail_service(9999, db_session)


# =========================================================
# 🔹 UPDATE TÂCHE
# =========================================================
@pytest.mark.asyncio
async def test_update_tache_ok(db_session):
    t = Tache(titre="Ancien", contenu="B", auteur_id=1, equipe="Dev")
    db_session.add(t)
    db_session.commit()

    res = await update_tache_service(
        t.id,
        titre="Nouveau",
        contenu="Contenu",
        equipe="Tech",
        categorie="urgent",
        priorite="haute",
        fichiers=[],
        db=db_session
    )

    assert res.titre == "Nouveau"
    assert res.equipe == "Tech"


@pytest.mark.asyncio
async def test_update_tache_not_found(db_session):
    with pytest.raises(HTTPException):
        await update_tache_service(9999, "A", "B", "Dev", "cat", "prio", [], db_session)


# =========================================================
# 🔹 DELETE TÂCHE
# =========================================================
def test_delete_tache_service(db_session):
    t = Tache(titre="Supprimer", contenu="xx", auteur_id=1, equipe="Dev")
    db_session.add(t)
    db_session.commit()

    delete_tache_service(t.id, db_session)

    assert db_session.query(Tache).count() == 0


def test_delete_tache_not_found(db_session):
    with pytest.raises(HTTPException):
        delete_tache_service(9999, db_session)


# =========================================================
# 🔹 LIKE TÂCHE
# =========================================================
def test_like_tache_service(db_session):
    t = Tache(titre="Like", contenu="aaa", auteur_id=1, equipe="Dev")
    db_session.add(t)
    db_session.commit()

    res = like_tache_service(t.id, db_session)

    assert res["likes"] == 1


def test_like_tache_not_found(db_session):
    with pytest.raises(HTTPException):
        like_tache_service(9999, db_session)


# =========================================================
# 🔹 COMMENTAIRES
# =========================================================
def test_add_commentaire_ok(db_session):
    u = Utilisateur(nom="Bob", email="bob@test.com", mot_de_passe="123", type="user")
    t = Tache(titre="T", contenu="C", auteur_id=1, equipe="Dev")
    db_session.add_all([u, t])
    db_session.commit()

    c = CommentaireCreate(contenu="Salut", auteur_id=u.id)

    res = add_commentaire_service(t.id, c, db_session)

    assert res.contenu == "Salut"
    assert res.auteur_id == u.id


def test_add_commentaire_tache_not_found(db_session):
    c = CommentaireCreate(contenu="X", auteur_id=1)
    with pytest.raises(HTTPException):
        add_commentaire_service(9999, c, db_session)


def test_add_commentaire_author_not_found(db_session):
    t = Tache(titre="T", contenu="X", auteur_id=1, equipe="Dev")
    db_session.add(t)
    db_session.commit()

    c = CommentaireCreate(contenu="X", auteur_id=9999)

    with pytest.raises(HTTPException):
        add_commentaire_service(t.id, c, db_session)


def test_get_commentaires_service(db_session):
    u = Utilisateur(nom="Tom", email="tom@test.com", mot_de_passe="123", type="user")
    t = Tache(titre="T", contenu="C", auteur_id=1, equipe="Dev")
    c = Commentaire(contenu="OK", auteur_id=1, tache_id=1)

    db_session.add_all([u, t, c])
    db_session.commit()

    res = get_commentaires_service(t.id, db_session)

    assert len(res) == 1


# =========================================================
# 🔹 DELETE FILE
# =========================================================
def test_delete_file_service(db_session, tmp_path):
    # créer fichier physique
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(b"abc")

    f = FichierTache(
        nom_fichier="test.txt",
        chemin=str(file_path),
        tache_id=1
    )
    db_session.add(f)
    db_session.commit()

    res = delete_file_service(f.id, db_session)

    assert res["detail"] == "Fichier supprimé avec succès"
    assert not file_path.exists()


def test_delete_file_not_found(db_session):
    with pytest.raises(HTTPException):
        delete_file_service(9999, db_session)
