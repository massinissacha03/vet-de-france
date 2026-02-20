# VetDeFrance

Application web de gestion pour centres vétérinaires permettant le suivi des animaux et de leurs soins médicaux.

## Description

VetDeFrance est une application web développée dans le cadre d'un projet universitaire. Elle permet aux vétérinaires de gérer les dossiers des animaux de leur centre, et aux propriétaires de consulter l'historique des soins de leurs animaux.

## Fonctionnalités

### Pour les vétérinaires
- Connexion sécurisée avec mot de passe hashé
- Enregistrement de nouveaux animaux
- Ajout de soins et consultations
- Vue d'ensemble des animaux du centre
- Génération de fiches médicales PDF

### Pour les propriétaires
- Création de compte propriétaire
- Consultation du dossier médical de l'animal
- Modification des informations de l'animal
- Téléchargement de la fiche médicale en PDF

### Autres
- Annuaire des centres vétérinaires partenaires
- Gestion des sessions utilisateurs
- Interface responsive

## Installation

### Prérequis
- Python 3.8+
- PostgreSQL 12+

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd vetdefrance
```

2. **Créer un environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base (si nécessaire)
CREATE DATABASE vetdefrance;

# Importer le schéma et les données
\i database/bddvet.sql
```

5. **Configurer les variables d'environnement**
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env avec vos paramètres
nano .env
```

6. **Lancer l'application**
```bash
python main.py
# ou si vous avez des problèmes avec le venv
./venv/bin/python3 main.py
```

7. **Accéder à l'application**
```
http://localhost:5000
```

## Structure du projet

```
vetdefrance/
├── database/           # Scripts SQL
│   └── bddvet.sql     # Schéma et données de test
├── docs/              # Documentation
│   ├── INSTALLATION.md
│   ├── ROUTES.md
│   ├── TESTING.md
│   ├── DEPLOYMENT.md
│   ├── DATABASE.md
│   └── CONTRIBUTING.md
├── scripts/           # Scripts utilitaires
│   └── start.sh
├── static/            # Fichiers CSS, images
│   └── style.css
├── templates/         # Templates HTML
│   ├── accueil.html
│   ├── pageemp.html
│   ├── pageprop.html
│   └── ...
├── db.py              # Configuration PostgreSQL
├── main.py            # Application Flask principale
├── requirements.txt   # Dépendances Python
├── .env.example       # Exemple de configuration
├── .gitignore         # Fichiers ignorés par Git
└── README.md          # Documentation
```

## Documentation

Pour plus d'informations, consultez les guides dans le dossier `docs/` :

- **[INSTALLATION.md](docs/INSTALLATION.md)** - Guide d'installation détaillé
- **[ROUTES.md](docs/ROUTES.md)** - Documentation des routes
- **[TESTING.md](docs/TESTING.md)** - Guide de test avec comptes de test
- **[DATABASE.md](docs/DATABASE.md)** - Architecture de la base de données

## Configuration

### Fichier .env
```env
SECRET_KEY=votre_cle_secrete_aleatoire
DB_NAME=postgres
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
```

## Comptes de test

Des comptes de test sont disponibles dans le fichier `database/bddvet.sql` :

**Vétérinaires :**
- jean.dupont@vetparis.fr / dupont123
- sophie.martin@vetparis.fr / martin456
- pierre.leroy@vetlyon.fr / leroy789

**Propriétaires :**
- Créez un compte via l'interface web

## Technologies utilisées

- **Backend:** Flask 3.0
- **Base de données:** PostgreSQL
- **Frontend:** HTML5, CSS3
- **Sécurité:** Flask-Bcrypt
- **PDF:** WeasyPrint
- **Variables d'environnement:** python-dotenv

## Dépendances principales

```
Flask==3.0.0
psycopg2-binary==2.9.9
Flask-Bcrypt==1.0.1
WeasyPrint==62.3
python-dotenv==1.0.0
```

## Note

Projet développé dans un cadre pédagogique - 2024

