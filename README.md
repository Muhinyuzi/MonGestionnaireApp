📋 Gestion des Tâches & Employés

Application web full-stack professionnelle permettant la gestion des utilisateurs et des tâches avec rôles, assignation, sécurité et pagination.
Ce projet démontre une architecture moderne backend / frontend prête pour un environnement professionnel.

🎯 Objectifs du projet

Centraliser la gestion des tâches d’une organisation

Mettre en place un système de rôles (admin / employé)

Assigner des tâches aux employés

Garantir la sécurité des accès et des données

Proposer une application claire, maintenable et testée

🧱 Architecture générale

Frontend : Angular (SPA)

Backend : FastAPI (API REST)

Base de données : PostgreSQL

ORM : SQLAlchemy

Authentification : JWT

Tests backend : Pytest

Frontend (Angular)
   ↓ HTTP REST
Backend (FastAPI)
   ↓ ORM
PostgreSQL

⚙️ Stack technique
Backend

Python 3.11

FastAPI

SQLAlchemy

Pydantic v2

JWT (authentification sécurisée)

Pytest (tests automatisés)

Frontend

Angular

TypeScript

HTML / CSS

HttpClient

Gestion des rôles côté UI

Base de données

PostgreSQL

Seed automatisé (script de réinitialisation complète)

🔐 Gestion des rôles
👑 Administrateur

Créer des tâches

Assigner des tâches aux employés

Voir toutes les tâches

Filtrer par auteur

Accéder aux détails complets

👤 Employé

Voir uniquement les tâches qui lui sont assignées

Accéder au détail d’une tâche

Ajouter des commentaires

Consulter les fichiers liés

✅ Fonctionnalités principales
📌 Tâches

Création / consultation / suppression

Assignation à un employé

Catégorie & priorité

Statut (en_attente, active, fermée)

Pagination & tri

Recherche texte

👥 Utilisateurs

Authentification JWT

Rôles (admin / employé)

Équipes

Compte actif / inactif

📎 Fichiers

Upload de fichiers liés aux tâches

Suppression sécurisée

💬 Commentaires

Commentaires associés aux tâches

Historique par tâche

🧪 Tests

Tests unitaires et fonctionnels du backend

Base de données isolée en mode test

Vérification des routes critiques (CRUD, auth, permissions)

🚀 Installation & exécution
1️⃣ Backend
cd backend
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt

2️⃣ Variables d’environnement

Créer un fichier .env :

DATABASE_URL=postgresql://user:password@localhost:5432/mongestionnaire
JWT_SECRET=supersecretkey

3️⃣ Initialiser la base de données

⚠️ Réinitialise complètement PostgreSQL

python -m app.db_create

4️⃣ Lancer l’API
uvicorn app.main:app --reload


API disponible sur :
👉 http://127.0.0.1:8000

5️⃣ Frontend
cd frontend
npm install
ng serve


Application disponible sur :
👉 http://localhost:4200

👨‍💻 Auteur

Jean Claude Muhinyuzi
Développeur Full-Stack (Python / FastAPI / Angular)
📍 Québec, Canada

Projet réalisé dans un contexte professionnel et de portfolio, avec une attention particulière portée à l’architecture, à la sécurité et à la maintenabilité.

📈 Évolutions possibles

Résumé automatique des tâches par IA

Recherche intelligente

Notifications email

Déploiement cloud (Railway / Render / VPS)

💡 Ce projet démontre ma capacité à concevoir et livrer une application complète, structurée et prête pour un environnement professionnel.