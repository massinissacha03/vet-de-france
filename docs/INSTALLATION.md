# Installation et Configuration

## Guide d'installation détaillé

### 1. Prérequis

Avant de commencer, assurez-vous d'avoir :
- Python 3.8 ou supérieur
- PostgreSQL 12 ou supérieur
- pip (gestionnaire de paquets Python)
- git

### 2. Clonage du projet

```bash
git clone <url-du-repo>
cd vetdefrance
```

### 3. Configuration de l'environnement virtuel

**Linux/Mac :**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Installation des dépendances

```bash
pip install -r requirements.txt
```

Si vous rencontrez des problèmes avec WeasyPrint, installez les dépendances système :

**Ubuntu/Debian :**
```bash
sudo apt-get install python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**Mac :**
```bash
brew install cairo pango gdk-pixbuf libffi
```

### 5. Configuration de PostgreSQL

**Créer la base de données :**
```bash
# Se connecter à PostgreSQL
psql -U postgres

# Dans psql
CREATE DATABASE vetdefrance;
\q
```

**Importer le schéma :**
```bash
psql -U postgres -d vetdefrance -f database/bddvet.sql
```

### 6. Configuration des variables d'environnement

```bash
# Copier le fichier exemple
cp .env.example .env
```

Éditer le fichier `.env` :
```env
SECRET_KEY=generer_une_cle_secrete_aleatoire
DB_NAME=vetdefrance
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe_postgres
```

### 7. Lancement de l'application

**Linux/Mac :**
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

**Windows :**
```bash
python main.py
```

### 8. Accès à l'application

Ouvrez votre navigateur et accédez à :
```
http://localhost:5000
```

## Comptes de test

Utilisez ces comptes pour tester l'application :

**Vétérinaires :**
- Email : jean.dupont@vetparis.fr  
  Mot de passe : dupont123

- Email : sophie.martin@vetparis.fr  
  Mot de passe : martin456

**Propriétaires :**
- Créez un compte via l'interface de création de compte propriétaire

## Résolution de problèmes

### Erreur de connexion à la base de données
- Vérifiez que PostgreSQL est démarré
- Vérifiez les credentials dans le fichier `.env`
- Vérifiez que la base de données existe

### Erreur WeasyPrint
- Installez les dépendances système listées ci-dessus
- Redémarrez votre terminal après installation

### Port 5000 déjà utilisé
Modifiez le port dans `main.py` :
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changez le port ici
```
