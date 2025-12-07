# app/tests/test_router_techniciens.py

import pytest

# =========================================================
# 🔹 LISTE TECHNICIENS
# =========================================================
def test_list_techniciens_empty(client):
    """✔ Aucun technicien dans la DB -> retourne liste vide"""
    r = client.get("/techniciens/")
    assert r.status_code == 200

    data = r.json()["data"]
    assert isinstance(data, list)
    assert len(data) == 0


def test_list_techniciens_only_techs_shown(client):
    """✔ Création de différents types -> seul type 'technicien' apparaît"""

    # Création admin pour bypass
    tech1 = {
        "nom": "Tech One",
        "email": "tech1@test.com",
        "mot_de_passe": "12345678",
        "type": "technicien",
        "equipe": "Support"
    }
    tech2 = {
        "nom": "Tech Two",
        "email": "tech2@test.com",
        "mot_de_passe": "12345678",
        "type": "technicien",
        "equipe": "Field"
    }
    non_tech = {
        "nom": "User Normal",
        "email": "normal@test.com",
        "mot_de_passe": "12345678",
        "type": "user",
        "equipe": "Dev"
    }

    client.post("/utilisateurs/", json=tech1)
    client.post("/utilisateurs/", json=tech2)
    client.post("/utilisateurs/", json=non_tech)

    r = client.get("/techniciens/")
    assert r.status_code == 200

    data = r.json()["data"]
    assert len(data) == 2
    assert all(u["type"] == "technicien" for u in data)


# =========================================================
# 🔹 DÉTAIL TECHNICIEN
# =========================================================
def test_get_technicien_detail_ok(client):
    """✔ Trouver un technicien existant"""

    r = client.post("/utilisateurs/", json={
        "nom": "Tech Detail",
        "email": "td@test.com",
        "mot_de_passe": "12345678",
        "type": "technicien",
        "equipe": "Field"
    })

    tech_id = r.json()["data"]["id"]

    r = client.get(f"/techniciens/{tech_id}")
    assert r.status_code == 200

    data = r.json()["data"]
    assert data["email"] == "td@test.com"
    assert data["type"] == "technicien"


def test_get_technicien_not_found(client):
    """❌ Technicien non trouvé (mauvais ID ou mauvais type)"""

    # Un utilisateur normal existe
    r = client.post("/utilisateurs/", json={
        "nom": "User",
        "email": "u@test.com",
        "mot_de_passe": "12345678",
        "type": "user",
        "equipe": "Dev"
    })

    user_id = r.json()["data"]["id"]

    # On demande comme technicien => 404
    r = client.get(f"/techniciens/{user_id}")
    assert r.status_code == 404
    assert "Technicien non trouvé" in r.text


def test_get_technicien_invalid_id(client):
    """❌ ID inexistant -> 404"""

    r = client.get("/techniciens/99999")
    assert r.status_code == 404
    assert "Technicien non trouvé" in r.text
