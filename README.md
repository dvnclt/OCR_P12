# Epic Events CRM

Epic Events CRM est une application de gestion des clients, contrats et événements. Ce projet est conçu pour permettre aux utilisateurs de gérer efficacement les données liées aux clients, contrats et événements, tout en respectant les permissions et rôles des utilisateurs.

## Technologies Utilisées

- **Python** : Langage principal.
- **SQLAlchemy** : ORM pour interagir avec la base de données PostgreSQL.
- **Click** : Framework pour créer des interfaces en ligne de commande.
- **JWT** : Authentification sécurisée.
- **Argon2** : Hachage des mots de passe.
- **dotenv** : Gestion des variables d'environnement.
- **Sentry** : Journalisation des erreurs.

## Fonctionnalités

- **Gestion des utilisateurs** :
  - Création, lecture, mise à jour et suppression des utilisateurs.
  - Gestion des rôles et permissions (Gestion, Commercial, Support).

- **Gestion des clients** :
  - Création, lecture, mise à jour et suppression des clients.
  - Validation des emails et numéros de téléphone.

- **Gestion des contrats** :
  - Création, lecture, mise à jour et suppression des contrats.
  - Suivi des paiements (montant total, payé, restant dû).
  - Association des contrats aux clients.

- **Gestion des événements** :
  - Création, lecture, mise à jour et suppression des événements.
  - Association des événements aux contrats et clients.
  - Gestion des participants, dates, lieux et notes.

- **Authentification et permissions** :
  - Authentification via JWT.
  - Vérification des permissions pour chaque action.
  - Gestion des rôles et permissions via un système relationnel.

## Structure du Projet

Le projet est organisé comme suit :

```
epic_events_crm/
├── commands/          # Commandes CLI pour gérer les utilisateurs, clients, contrats et événements.
├── config/            # Configuration de l'application.
├── models/            # Modèles SQLAlchemy pour les tables de la base de données.
├── repositories/      # Repositories pour interagir avec la base de données.
├── services/          # Services pour la logique métier.
├── utils/             # Utilitaires pour l'authentification, validation, etc.
├── main.py            # Initialise les tables dans la db.
└── cli.py             # Point d'entrée principal pour les commandes CLI.
```

## Installation

### Prérequis

- Python 3.13 ou supérieur
- PostgreSQL
- [Poetry](https://python-poetry.org/) pour la gestion des dépendances

### Étapes

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/dvnclt/OCR_P12.git
   cd epic-events-crm
   ```

2. Installez les dépendances avec Poetry :
   ```bash
   poetry install
   ```

3. Configurez les variables d'environnement :
   - Créez un fichier `.env` à la racine du projet.
   - Ajoutez-y la clé secrète et les informations de connexion à la base de données :
     ```
     SECRET=your_secret_key
     ```

4. Initialisez la base de données :
   ```bash
   python epic_events_crm/main.py
   ```

## Utilisation

### Commandes CLI

Le projet utilise `Click` pour exécuter des commandes via une interface en ligne de commande. Voici les commandes disponibles pour chaque entité :

#### **Création superuser (admin)**
- Création du compte admin :
  ```bash
  python cli.py admin
  ```
- Informations par défaut de admin
  ```bash
  user : admin
  password : admin
  email : admin

#### **Authentification**
- Connexion :
  ```bash
  python cli.py login
  ```
- Déconnexion :
  ```bash
  python cli.py logout
  ```

#### **Gestion des utilisateurs**
- Créer un utilisateur :
  ```bash
  python cli.py user create
  ```
- Lire un utilisateur :
  ```bash
  python cli.py user get
  ```
- Mettre à jour un utilisateur :
  ```bash
  python cli.py user update
  ```
- Supprimer un utilisateur :
  ```bash
  python cli.py user delete
  ```

#### **Gestion des clients**
- Créer un client :
  ```bash
  python cli.py client create
  ```
- Lire un client :
  ```bash
  python cli.py client get
  ```
- Mettre à jour un client :
  ```bash
  python cli.py client update
  ```
- Supprimer un client :
  ```bash
  python cli.py client delete
  ```

#### **Gestion des contrats**
- Créer un contrat :
  ```bash
  python cli.py contract create
  ```
- Lire un contrat :
  ```bash
  python cli.py contract get all,
                             id,
                             user,
                             client,
                             remaining_amount,
                             status
  ```
- Mettre à jour un contrat :
  ```bash
  python cli.py contract update
  ```
- Supprimer un contrat :
  ```bash
  python cli.py contract delete
  ```

#### **Gestion des événements**
- Créer un événement :
  ```bash
  python cli.py event create
  ```
- Lire un événement :
  ```bash
  python cli.py event get all,
                          id,
                          contract,
                          user,
                          client,
                          start_date,
                          end_date,
                          no_user
  ```
- Mettre à jour un événement :
  ```bash
  python cli.py event update
  ```
- Supprimer un événement :
  ```bash
  python cli.py event delete
  ```

## Permissions et Rôles

Description des rôles et permissions

### **Rôles et Permissions**

#### **Admin**
L'administrateur a toutes les permissions sur toutes les entités :
- **Utilisateurs** : Créer, Lire, Mettre à jour, Supprimer.
- **Clients** : Créer, Lire, Mettre à jour, Supprimer.
- **Contrats** : Créer, Lire, Mettre à jour, Supprimer.
- **Événements** : Créer, Lire, Mettre à jour, Supprimer.

### **Gestion**
Le rôle "gestion" a des permissions étendues, mais limitées par rapport à l'admin :
- **Utilisateurs** : Créer, Lire, Mettre à jour, Supprimer.
- **Clients** : Lire.
- **Contrats** : Créer, Lire, Mettre à jour.
- **Événements** : Lire, Mettre à jour.

### **Commercial**
Le rôle "commercial" est principalement axé sur les clients et les événements :
- **Utilisateurs** : Lire.
- **Clients** : Créer, Lire, Mettre à jour (si responsable du client).
- **Contrats** : Lire.
- **Événements** : Créer (si responsable du client), Lire.

### **Support**
Le rôle "support" est axé sur la lecture et la mise à jour des événements :
- **Utilisateurs** : Lire.
- **Clients** : Lire.
- **Contrats** : Lire.
- **Événements** : Lire, Mettre à jour (si responsable de l'événement).

---

## **Résumé des Permissions par Entité**

| **Permission**       | **Admin** | **Gestion** | **Commercial** | **Support** |
|-----------------------|-----------|-------------|----------------|-------------|
| Créer utilisateur     | ✅         | ✅           | ❌              | ❌           |
| Lire utilisateur      | ✅         | ✅           | ✅              | ✅           |
| Mettre à jour utilisateur | ✅     | ✅           | ❌              | ❌           |
| Supprimer utilisateur | ✅         | ✅           | ❌              | ❌           |
| Créer client          | ✅         | ❌           | ✅              | ❌           |
| Lire client           | ✅         | ✅           | ✅              | ✅           |
| Mettre à jour client  | ✅         | ❌           | ✅ (si responsable) | ❌       |
| Supprimer client      | ✅         | ❌           | ❌              | ❌           |
| Créer contrat         | ✅         | ✅           | ❌              | ❌           |
| Lire contrat          | ✅         | ✅           | ✅              | ✅           |
| Mettre à jour contrat | ✅         | ✅           | ❌              | ❌           |
| Supprimer contrat     | ✅         | ❌           | ❌              | ❌           |
| Créer événement       | ✅         | ❌           | ✅ (si responsable) | ❌       |
| Lire événement        | ✅         | ✅           | ✅              | ✅           |
| Mettre à jour événement | ✅       | ✅           | ❌              | ✅ (si responsable) |
| Supprimer événement   | ✅         | ❌           | ❌              | ❌           |

---

