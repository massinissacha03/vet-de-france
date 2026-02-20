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

## Base de données

Le projet utilise PostgreSQL avec 7 tables principales :

### Tables
- **employes** : Vétérinaires des centres (login, mdp hashé, nom, prénom, centre)
- **propri** : Propriétaires d'animaux (id unique P+9 chiffres, nom, prénom, mdp hashé)
- **animal** : Animaux enregistrés (numéro, nom, espèce, race, date de naissance, etc.)
- **centre** : Centres vétérinaires partenaires (code postal, nom, adresse)
- **inscrit** : Relation employés-centres
- **opere** : Relation centres-animaux
- **ordonnance** : Soins et consultations (date, description, ordonnance)

### Relations
- Un employé peut travailler dans plusieurs centres
- Un animal appartient à un propriétaire
- Un animal peut être suivi par plusieurs centres
- Un animal a plusieurs ordonnances/soins

## Routes principales

### Routes publiques
- `GET /` ou `/accueil` : Page d'accueil, choix employé/propriétaire
- `GET /invite` : Page d'invitation générale

### Routes employés (vétérinaires)
- `GET/POST /emp` : Connexion vétérinaire
- `GET /pageemp` : Tableau de bord vétérinaire
- `GET/POST /ajout_animal` : Enregistrer un nouvel animal
- `GET /ficheanimalemp/<numero>` : Fiche détaillée d'un animal
- `POST /ajout_soin/<numero>` : Ajouter un soin/consultation
- `GET /pdf/<numero>` : Générer la fiche PDF
- `GET/POST /infocentre` : Annuaire des centres

### Routes propriétaires
- `GET/POST /propconnex` : Connexion propriétaire
- `GET/POST /creation_proprietaire` : Créer un compte propriétaire
- `GET /pageprop` : Tableau de bord propriétaire
- `GET /ficheanimal/<numero>` : Voir la fiche de son animal
- `GET/POST /modifications/<numero>` : Modifier les infos de l'animal
- `GET /fichepdf/<numero>` : Télécharger le PDF

### Déconnexion
- `GET /deconnexion` : Déconnexion (vétérinaire ou propriétaire)

## Guide de test

### Scénario 1 : Vétérinaire - Enregistrer un nouvel animal

1. Accéder à http://localhost:5000
2. Choisir "Employé"
3. Se connecter avec : `jean.dupont@vetparis.fr` / `dupont123`
4. Cliquer sur "Ajouter un animal"
5. Remplir le formulaire :
   - Numéro d'identification (unique)
   - Nom de l'animal
   - Espèce, race, sexe
   - Date de naissance
   - Tatouage/puce
   - Propriétaire (sélectionner dans la liste)
6. Soumettre le formulaire

### Scénario 2 : Vétérinaire - Ajouter un soin

1. Se connecter en tant que vétérinaire
2. Cliquer sur un animal dans la liste
3. Dans la fiche de l'animal, descendre à "Ajouter un soin"
4. Remplir :
   - Date du soin
   - Description de la consultation
   - Ordonnance (médicaments prescrits)
5. Soumettre

### Scénario 3 : Propriétaire - Créer un compte et consulter son animal

1. Sur la page d'accueil, choisir "Propriétaire"
2. Cliquer sur "Créer un compte"
3. Remplir : nom, prénom, téléphone, adresse, mot de passe
4. Un identifiant unique (P + 9 chiffres) est généré automatiquement
5. Se connecter avec l'identifiant et le mot de passe
6. Voir les animaux associés à ce propriétaire
7. Cliquer sur un animal pour voir son historique médical complet

### Scénario 4 : Générer une fiche PDF

1. Se connecter (vétérinaire ou propriétaire)
2. Accéder à la fiche d'un animal
3. Cliquer sur "Télécharger PDF" ou "Générer fiche PDF"
4. Le PDF contient :
   - Informations de l'animal
   - Historique complet des soins
   - Coordonnées du propriétaire
   - Logo et informations du centre

### Scénario 5 : Consulter l'annuaire des centres

1. Se connecter en tant que vétérinaire
2. Accéder à "Annuaire des centres"
3. Rechercher par code postal et nom de centre
4. Voir la liste des centres avec leurs informations

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

## Problèmes courants

### Erreur "ModuleNotFoundError: No module named 'psycopg2'"
**Solution :** Utilisez le Python de votre environnement virtuel
```bash
./venv/bin/python3 main.py
# au lieu de
python3 main.py
```

### Erreur "Port 5000 is in use"
**Solution :** Un autre processus Flask est déjà en cours
```bash
# Arrêter tous les processus Flask
pkill -f "python.*main.py"
# Relancer
./venv/bin/python3 main.py
```

### Erreur de connexion à PostgreSQL
**Solution :** Vérifiez votre fichier .env
- Le service PostgreSQL doit être démarré
- Les identifiants DB_USER et DB_PASSWORD doivent être corrects
- La base de données DB_NAME doit exister

### Problème de génération PDF
**Solution :** Vérifiez que WeasyPrint et pydyf sont bien installés
```bash
./venv/bin/pip install WeasyPrint==62.3 pydyf==0.11.0
```

## Architecture applicative

### Flux de données

**Vétérinaire :**
```
Connexion → Vérification mot de passe hashé → Session créée → Accès tableau de bord
→ Actions : Ajouter animal / Ajouter soin / Consulter fiches / Générer PDF
```

**Propriétaire :**
```
Création compte → Génération ID unique → Connexion → Session → Consultation uniquement
→ Actions : Voir animaux / Voir historique soins / Télécharger PDF / Modifier infos
```

### Sécurité

- **Mots de passe** : Hashés avec Flask-Bcrypt (bcrypt)
- **Sessions** : Gestion côté serveur avec Flask session
- **Variables sensibles** : Stockées dans .env (jamais versionné)
- **Accès** : Routes protégées par vérification de session

### Génération PDF

Le système utilise WeasyPrint pour convertir un template HTML en PDF :
1. Récupération des données depuis PostgreSQL
2. Injection dans le template `fichepdf.html`
3. Conversion HTML → PDF avec mise en page CSS
4. Téléchargement direct pour l'utilisateur

## Note

Projet développé dans un cadre pédagogique - Université Gustave Eiffel

