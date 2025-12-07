# app/tests/test_router_commentaires.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_add_commentaire_router_success(client, create_test_user):
    # Créer une tache
    tache = client.post(
        "/taches/",
        json={
            "titre": "T",
            "contenu": "C",
            "auteur_id": create_test_user["id"]
        }
    ).json()

    tache_id = tache["id"]

    r = client.post(
        f"/taches/{tache_id}/commentaires",
        json={"contenu": "Hello", "auteur_id": create_test_user["id"]}
    )

    assert r.status_code == 200
    assert r.json()["contenu"] == "Hello"


def test_add_commentaire_router_tache_not_found():
    r = client.post(
        "/taches/999/commentaires",
        json={"contenu": "Hello", "auteur_id": 1}
    )
    assert r.status_code == 404


def test_add_commentaire_router_author_not_found(client, create_test_user):
    # Créer une tache
    tache = client.post(
        "/taches/",
        json={
            "titre": "T",
            "contenu": "C",
            "auteur_id": create_test_user["id"]
        }
    ).json()

    tache_id = tache["id"]

    r = client.post(
        f"/taches/{tache_id}/commentaires",
        json={"contenu": "Hello", "auteur_id": 999}
    )

    assert r.status_code == 404
