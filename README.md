# 📘 MonGestionnaireApp

**MonGestionnaireApp** est une application web **full-stack moderne** dédiée à la **gestion des employés et des tâches**.  
Elle est conçue avec une architecture professionnelle, sécurisée et prête pour la production, en respectant des standards utilisés en entreprise.

Ce projet sert de **projet portfolio** et démontre mes compétences en **backend**, **frontend**, **sécurité**, ainsi que les bases **DevOps** (Docker, environnements, déploiement).

---

## 🌐 Démo en ligne (Render)

- ✅ **Démo (Frontend)** : https://mongestionnaireapp-1.onrender.com  
- ✅ **API (Backend)** : https://mongestionnaireapp.onrender.com  
- ✅ **Swagger / Docs API** : https://mongestionnaireapp.onrender.com/docs  

### 🔑 Comptes de démonstration
| Rôle        | Email               | Mot de passe |
|------------|---------------------|--------------|
| Admin      | alice@example.com   | alice123     |
| Employé    | bob@example.com     | bob12345     |
| Technicien | charlie@example.com | charl123     |

> ⚠️ Note : le service Render peut se mettre en veille. Le premier chargement peut prendre quelques secondes.

---

## 🎯 Objectifs du projet

- Démontrer des compétences **Full-Stack professionnelles**
- Appliquer les **bonnes pratiques backend et frontend**
- Gérer des environnements **dev / demo / prod**
- Proposer une application **déployable en production**
- Servir de **projet portfolio** pour le marché canadien

---

## 🚀 Fonctionnalités principales

### 🔐 Authentification & Sécurité
- Authentification sécurisée via **JWT (OAuth2)**
- Activation de compte
- Changement et réinitialisation de mot de passe
- Gestion des rôles (**Admin / Employé / Technicien**)
- Protection des routes (Backend & Frontend)
- **RBAC** – contrôle d’accès par rôle

### 👥 Gestion des utilisateurs
- Création, modification et suppression d’utilisateurs
- Attribution des rôles
- Profils utilisateurs détaillés
- Activation / désactivation de comptes
- Liste paginée et filtrée

### 📝 Gestion des tâches
- Création et modification des tâches (**Admin uniquement**)
- Assignation des tâches aux employés
- Accès limité aux tâches assignées
- Statuts :
  - `en_attente`
  - `active`
  - `fermee`
- Catégories et priorités
- Historique des mises à jour
- Compteurs de vues et de likes

### 💬 Commentaires & Fichiers
- Commentaires liés aux tâches
- Upload de fichiers
- Suppression sécurisée
- Relations claires :
  - Utilisateurs ↔ Tâches
  - Tâches ↔ Commentaires
  - Tâches ↔ Fichiers

### 📄 Expérience utilisateur
- Pagination
- Recherche
- Filtres avancés
- Interface responsive (**Angular SPA**)
- Navigation fluide

---

## 📧 Notifications Email (activation / welcome / reset)

✅ Les notifications email sont **implémentées dans le backend** (emails de bienvenue, activation de compte, réinitialisation de mot de passe).

⚠️ **Dans la démo Render**, l’envoi d’emails peut être **désactivé / non fonctionnel** à cause des restrictions réseau (SMTP sortant) sur certains hébergeurs.

✅ En local (ou en production avec un fournisseur email adapté), la fonctionnalité fonctionne via :
- **SMTP** (ex: Gmail + App Password)
- ou un fournisseur transactionnel via **API** (Brevo, Mailgun, SendGrid, etc.)

---

## 🧱 Architecture du projet

MonGestionnaireApp/
├── backend/
│ ├── app/
│ │ ├── routers/ # Routes FastAPI
│ │ ├── models/ # Modèles SQLAlchemy
│ │ ├── schemas/ # Schémas Pydantic
│ │ ├── services/ # Logique métier
│ │ ├── auth/ # JWT & sécurité
│ │ ├── tests/ # Tests Pytest
│ │ └── main.py
│ ├── Dockerfile
│ └── requirements.txt
│
├── frontend/
│ ├── src/ # Application Angular
│ ├── Dockerfile
│ ├── angular.json
│ └── nginx.conf
│
├── docker-compose.yml
├── .env.example
└── README.md

yaml
Copier le code

---

## 🛠️ Stack technique

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT
- Pytest

### Frontend
- Angular
- TypeScript
- HTML / CSS
- RxJS

### DevOps & Qualité
- Docker
- Docker Compose
- Architecture modulaire
- Environnements séparés (dev / demo / prod)

---

## 🐳 Lancer le projet avec Docker (recommandé)

### ✅ Prérequis
- Docker
- Docker Compose

### ▶️ Installation

```bash
git clone https://github.com/Muhinyuzi/MonGestionnaireApp.git
cd MonGestionnaireApp
cp .env.example .env
docker-compose up --build
🌐 Accès en local
Frontend : http://localhost:4200

Backend API : http://localhost:8000

Swagger API Docs : http://localhost:8000/docs

🌱 Seed – Données de démonstration
Pour générer une base de données de démonstration :

bash
Copier le code
docker-compose exec backend python -m app.db_create
Le seed génère automatiquement :

utilisateurs

tâches assignées

fichiers

commentaires

🧪 Tests automatisés (Backend)
bash
Copier le code
cd backend
pytest
Tests couverts :

Authentification

Utilisateurs

Tâches

Commentaires

Permissions & rôles

Cas d’erreurs (401, 403, 404, 422)

🔄 CI/CD (prévu)
Architecture compatible CI/CD

Tests automatisés avec Pytest

Base de données isolée pour les tests

Pipeline GitHub Actions prévu (tests à chaque push / pull request)

🔐 Gestion des rôles (RBAC)
Rôle	Droits principaux
Admin	Gestion utilisateurs & tâches
Employé	Consultation de ses tâches
Technicien	Consultation de ses tâches

➡️ Séparation claire des responsabilités, conforme aux pratiques professionnelles.

👤 Auteur
Jean Claude Muhinyuzi
📍 Québec, Canada
💼 Développement logiciel & télécommunications
🔗 GitHub : https://github.com/Muhinyuzi

🚀 Améliorations possibles
Dashboard & statistiques

Logs & monitoring

Déploiement cloud avancé (Fly.io / AWS)

IA : résumé automatique des tâches

Mise en place CI/CD GitHub Actions