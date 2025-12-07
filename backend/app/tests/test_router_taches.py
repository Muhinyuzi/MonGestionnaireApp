# app/tests/test_router_taches.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# -----------------------------------------------------------------
# ✅ TEST CREATE TACHE
# -----------------------------------------------------------------
def test_create_tache_router(create_test_user):
    data = {
        "titre": "Tache Test",
        "contenu": "Contenu Test",
        "auteur_id": create_test_user["id"],
        "equipe": "Dev",
        "priorite": "haute",
        "categorie": "info"
    }
    r = client.post("/taches/", json=data)
    assert r.status_code == 200
    assert r.json()["titre"] == "Tache Test"


# -----------------------------------------------------------------
# ✅ TEST LIST TACHES
# -----------------------------------------------------------------
def test_list_taches_router(client, create_test_user):
    # initial
    r0 = client.get("/taches/")
    initial_total = r0.json()["total"]

    payload = {
        "titre": "Tache test",
        "contenu": "Contenu",
        "auteur_id": create_test_user["id"]
    }

    client.post("/taches/", json=payload)

    r = client.get("/taches/")
    assert r.status_code == 200
    assert r.json()["total"] == initial_total + 1


# -----------------------------------------------------------------
# ✅ TEST DETAIL
# -----------------------------------------------------------------
def test_get_tache_detail_router(create_test_user):
    create = client.post("/taches/", json={"titre": "A", "contenu": "B", "auteur_id": create_test_user["id"]})
    tache_id = create.json()["id"]

    r = client.get(f"/taches/{tache_id}")
    assert r.status_code == 200
    assert r.json()["id"] == tache_id


# -----------------------------------------------------------------
# ✅ TEST LIKE TACHE
# -----------------------------------------------------------------
def test_like_tache_router(create_test_user):
    create = client.post("/taches/", json={"titre": "L", "contenu": "c", "auteur_id": create_test_user["id"]})
    tache_id = create.json()["id"]

    r = client.post(f"/taches/{tache_id}/like")
    assert r.status_code == 200
    assert r.json()["likes"] == 1


# -----------------------------------------------------------------
# ✅ TEST COMMENTAIRES
# -----------------------------------------------------------------
def test_add_commentaire_router(create_test_user):
    create = client.post("/taches/", json={"titre": "C", "contenu": "text", "auteur_id": create_test_user["id"]})
    tache_id = create.json()["id"]

    commentaire = {"contenu": "Salut", "auteur_id": create_test_user["id"]}
    r = client.post(f"/taches/{tache_id}/commentaires", json=commentaire)

    assert r.status_code == 200
    assert r.json()["contenu"] == "Salut"


def test_get_commentaires_router(create_test_user):
    create = client.post("/taches/", json={"titre": "C", "contenu": "text", "auteur_id": create_test_user["id"]})
    tache_id = create.json()["id"]

    client.post(
        f"/taches/{tache_id}/commentaires",
        json={"contenu": "Test", "auteur_id": create_test_user["id"]}
    )

    r = client.get(f"/taches/{tache_id}/commentaires")
    assert r.status_code == 200
    assert len(r.json()) == 1


# -----------------------------------------------------------------
# ✅ TEST DELETE TACHE
# -----------------------------------------------------------------
def test_delete_tache_router(create_test_user):
    create = client.post("/taches/", json={"titre": "D", "contenu": "z", "auteur_id": create_test_user["id"]})
    tache_id = create.json()["id"]

    r = client.delete(f"/taches/{tache_id}")
    assert r.status_code in (200, 204)


def test_create_tache_missing_title(client, create_test_user):
    payload = {
        "contenu": "Test no title",
        "auteur_id": create_test_user["id"]
    }
    r = client.post("/taches/", json=payload)
    assert r.status_code == 422


def test_get_tache_not_found(client):
    r = client.get("/taches/999")
    assert r.status_code == 404
