📘 MonGestionnaireApp

MonGestionnaireApp est une application web full-stack moderne de gestion des employés et des tâches.
Elle est conçue avec une architecture professionnelle, sécurisée, testée, dockerisée et prête pour la production.

Ce projet sert de projet portfolio et démontre ma maîtrise du backend, frontend, sécurité, DevOps et CI/CD, selon des standards utilisés en entreprise.

🚀 Fonctionnalités principales
🔐 Authentification & Sécurité

Authentification JWT (login sécurisé)

Activation de compte

Changement et réinitialisation de mot de passe

Gestion des rôles (Admin / Employé / Technicien)

Protection des routes (Backend + Frontend)

Accès contrôlé par rôle (RBAC)

👥 Gestion des utilisateurs

Création, modification et suppression d’utilisateurs

Attribution des rôles

Profils utilisateurs détaillés

Activation / désactivation de comptes

Visualisation des activités

📝 Gestion des tâches

Création et modification de tâches (Admin uniquement)

Assignation des tâches aux employés

Les employés ne voient que les tâches qui leur sont assignées

Statuts de tâches :

en_attente

active

fermee

Catégories et priorités

Historique des mises à jour

Compteur de vues et likes

💬 Commentaires & Fichiers

Commentaires liés aux tâches

Upload de fichiers

Suppression sécurisée des fichiers

Relations :

Utilisateurs ↔ Tâches

Tâches ↔ Commentaires

Tâches ↔ Fichiers

📄 Expérience utilisateur

Pagination

Recherche

Filtres avancés

Interface responsive (Angular)

Navigation fluide SPA

🧱 Architecture du projet
MonGestionnaireApp/
├── backend/
│   ├── app/
│   │   ├── routers/           # Routes FastAPI
│   │   ├── models/        # Modèles SQLAlchemy
│   │   ├── schemas/       # Schémas Pydantic
│   │   ├── services/      # Logique métier
│   │   ├── auth/          # JWT / Sécurité
│   │   ├── tests/         # Tests Pytest
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── angular.json
│   └── nginx.conf
│
├── docker-compose.yml
├── .env.example
└── README.md

🛠️ Stack technique
Backend

Python 3.11

FastAPI

SQLAlchemy

PostgreSQL

Pydantic

JWT

Pytest

Frontend

Angular

TypeScript

HTML / CSS

RxJS

DevOps & Qualité

Docker

Docker Compose

GitHub Actions (CI/CD)

Tests automatisés

Architecture modulaire

🐳 Lancer le projet avec Docker (recommandé)
✅ Prérequis

Docker

Docker Compose

▶️ Installation
git clone https://github.com/Muhinyuzi/MonGestionnaireApp.git
cd MonGestionnaireApp
cp .env.example .env
docker-compose up --build

🌐 Accès

Frontend : http://localhost:4200

Backend API : http://localhost:8000

Swagger API Docs : http://localhost:8000/docs

🌱 Seed (données de démonstration)

Pour générer une base propre avec des données de test :

docker-compose exec backend python -m app.db_create

Comptes de test
Rôle	Email	Mot de passe
Admin	alice@example.com
	alice123
Employé	bob@example.com
	bob12345
Technicien	charlie@example.com
	charl123

Le seed crée automatiquement :

utilisateurs

tâches assignées

fichiers

commentaires

🧪 Tests automatisés (Backend)
cd backend
pytest


Tests couverts :

Authentification

Utilisateurs

Tâches

Commentaires

Permissions & rôles

Cas d’erreurs (401, 403, 404, 422)

🔄 CI/CD (GitHub Actions)

Pipeline CI intégré :

Lancement automatique des tests à chaque push / PR

Base PostgreSQL isolée pour les tests

Validation du backend

🔐 Gestion des rôles (RBAC)
Rôle	Droits
Admin	Gère utilisateurs et tâches
Employé	Consulte ses tâches assignées
Technicien	Consulte ses tâches assignées

➡️ Séparation claire des responsabilités, conforme aux pratiques professionnelles.

📦 Base de données

PostgreSQL

Schéma relationnel normalisé

Contraintes d’intégrité

Relations claires entre entités

Seed reproductible

🎯 Objectifs du projet

✅ Démontrer des compétences Full-Stack

✅ Appliquer les bonnes pratiques professionnelles

✅ Être déployable en production

✅ Servir de projet portfolio pour le marché canadien

👤 Auteur

Jean Claude Muhinyuzi
📍 Québec, Canada
💼 Développement logiciel & télécommunications
🔗 GitHub : https://github.com/Muhinyuzi

✅ Améliorations possibles

Notifications email

Dashboard & statistiques

Logs & monitoring

Déploiement cloud (Render, Fly.io, AWS)

IA : résumé automatique des tâches