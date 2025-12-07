from __future__ import annotations
from datetime import datetime, timedelta
import os
import random

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from passlib.context import CryptContext

from app.db import engine, Base
from app.models.utilisateur import Utilisateur
from app.models.tache import Tache
from app.models.commentaire import Commentaire
from app.models.fichier import FichierTache

# ======================================================
# ⚙ CONFIG
# ======================================================

ENV = os.getenv("ENV", "dev")  # dev | demo | prod

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ======================================================
# 🔍 CHECK DB VIDE
# ======================================================
def is_db_empty(session) -> bool:
    return session.query(Utilisateur).count() == 0


# ======================================================
# 🔄 RESET SCHEMA (DEV / DEMO UNIQUEMENT)
# ======================================================
def reset_schema():
    print("💣 RESETTING PostgreSQL PUBLIC SCHEMA...")

    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))

    print("🧹 PostgreSQL schema cleaned successfully.")

    Base.metadata.create_all(bind=engine)
    print("🏗️ SQLAlchemy models recreated successfully.")


# ======================================================
# 🌱 SEED DATA (IDEMPOTENT & SAFE)
# ======================================================
def seed():
    print(f"🌱 ENV = {ENV}")

    if ENV == "prod":
        raise RuntimeError("❌ Seed interdit en production")

    with SessionLocal() as session:

        # ✅ DB déjà initialisée → on sort
        if not is_db_empty(session):
            print("✅ Base déjà initialisée — seed ignoré")
            return

        # ✅ Reset autorisé uniquement en dev / demo
        if ENV in ("dev", "demo"):
            reset_schema()
        else:
            raise RuntimeError("❌ Environnement non autorisé pour le seed")

        # ======================================================
        # 1️⃣ UTILISATEURS
        # ======================================================
        users_data = [
            {
                "nom": "Alice",
                "email": "alice@example.com",
                "mot_de_passe": "alice123",
                "type": "admin",
                "equipe": "Dev",
                "poste": "Chef de projet",
                "telephone": "514-123-4567",
                "adresse": "123 rue Sainte-Catherine, Montréal",
                "date_embauche": datetime(2023, 1, 10),
                "is_active": True,
            },
            {
                "nom": "Bob",
                "email": "bob@example.com",
                "mot_de_passe": "bob12345",
                "type": "user",
                "equipe": "QA",
                "poste": "Testeur QA",
                "telephone": "438-987-6543",
                "adresse": "55 boul. René-Lévesque, Laval",
                "date_embauche": datetime(2022, 5, 22),
                "is_active": True,
            },
            {
                "nom": "Charlie",
                "email": "charlie@example.com",
                "mot_de_passe": "charl123",
                "type": "technicien",
                "equipe": "Support",
                "poste": "Tech Terrain",
                "telephone": "450-888-9999",
                "adresse": "88 avenue du Parc, Longueuil",
                "date_embauche": datetime(2021, 8, 30),
                "is_active": True,
            },
        ]

        users = []
        for u in users_data:
            avatar_num = random.randint(1, 80)

            user = Utilisateur(
                nom=u["nom"],
                email=u["email"],
                mot_de_passe=hash_password(u["mot_de_passe"]),
                type=u["type"],
                equipe=u["equipe"],
                poste=u["poste"],
                telephone=u["telephone"],
                adresse=u["adresse"],
                date_embauche=u["date_embauche"],
                avatar_url=f"https://i.pravatar.cc/150?img={avatar_num}",
                is_active=u["is_active"],
            )
            session.add(user)
            users.append(user)

        session.commit()
        print(f"✅ {len(users)} utilisateurs créés")

        # ======================================================
        # 2️⃣ TÂCHES — 0 pour admin, 5 par employé
        # ======================================================
        now = datetime.utcnow()
        taches = []

        for user in users:
            if user.type == "admin":
                continue

            for i in range(5 if ENV == "dev" else 3):
                tache = Tache(
                    titre=f"Tâche automatique {i + 1} pour {user.nom}",
                    contenu=f"Contenu auto-généré pour {user.nom}.",
                    equipe=user.equipe,
                    auteur_id=user.id,
                    assign_to_id=user.id,
                    status=random.choice(["en_attente", "active"]),
                    created_at=now - timedelta(days=random.randint(0, 10)),
                    updated_at=now,
                    nb_vues=random.randint(0, 200),
                    likes=random.randint(0, 20),
                    categorie=random.choice(["Urgent", "Normal", "Info"]),
                    priorite=random.choice(["Haute", "Moyenne", "Basse"]),
                )
                session.add(tache)
                taches.append(tache)

        session.commit()
        print(f"✅ {len(taches)} tâches générées")

        # ======================================================
        # 3️⃣ FICHIERS (DEV / DEMO)
        # ======================================================
        fichiers = []
        for tache in taches:
            for j in range(random.randint(0, 2)):
                filename = f"{tache.titre.replace(' ', '_')}_file{j + 1}.txt"
                filepath = os.path.join(UPLOAD_DIR, filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"Contenu du fichier {j + 1} pour {tache.titre}")

                fichier = FichierTache(
                    nom_fichier=filename,
                    chemin=filepath,
                    tache_id=tache.id,
                )
                session.add(fichier)
                fichiers.append(fichier)

        session.commit()
        print(f"✅ {len(fichiers)} fichiers ajoutés")

        # ======================================================
        # 4️⃣ COMMENTAIRES
        # ======================================================
        commentaires = []
        for tache in taches:
            for _ in range(random.randint(0, 2)):
                com = Commentaire(
                    contenu=f"Commentaire automatique sur {tache.titre}",
                    auteur_id=random.choice(users).id,
                    tache_id=tache.id,
                    date=tache.created_at + timedelta(hours=random.randint(0, 6)),
                )
                session.add(com)
                commentaires.append(com)

        session.commit()
        print(f"✅ {len(commentaires)} commentaires créés")

        print("🎉 SEEDING TERMINÉ AVEC SUCCÈS 🎉")


# ======================================================
# ▶ EXECUTION DIRECTE (DEV LOCAL)
# ======================================================
if __name__ == "__main__" and os.getenv("TESTING") != "1":
    seed()
    print("🚀 Base de données initialisée !")
