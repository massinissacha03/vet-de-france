# Guide de Déploiement

## Options de déploiement

### Option 1 : Heroku

1. **Installer Heroku CLI**
```bash
# Voir https://devcenter.heroku.com/articles/heroku-cli
```

2. **Créer un fichier Procfile**
```
web: gunicorn main:app
```

3. **Ajouter gunicorn aux dépendances**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

4. **Déployer**
```bash
heroku login
heroku create votre-app-vet
heroku addons:create heroku-postgresql:mini
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
git push heroku main
```

5. **Initialiser la base de données**
```bash
heroku pg:psql < database/bddvet.sql
```

### Option 2 : Render

1. **Créer un compte sur render.com**

2. **Créer un fichier render.yaml**
```yaml
services:
  - type: web
    name: vetdefrance
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn main:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      
databases:
  - name: vetdb
    databaseName: bddvet
    user: postgres
```

3. **Connecter le repo GitHub et déployer**

### Option 3 : VPS (DigitalOcean, Linode, etc.)

1. **Installer les dépendances système**
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx
```

2. **Cloner et configurer l'application**
```bash
git clone votre-repo
cd pj
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn
```

3. **Configurer PostgreSQL**
```bash
sudo -u postgres createdb bddvet
sudo -u postgres psql bddvet < database/bddvet.sql
```

4. **Créer un fichier systemd**
```ini
# /etc/systemd/system/vetdefrance.service
[Unit]
Description=VetDeFrance Flask App
After=network.target

[Service]
User=www-data
WorkingDirectory=/chemin/vers/pj
Environment="PATH=/chemin/vers/pj/venv/bin"
ExecStart=/chemin/vers/pj/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 main:app

[Install]
WantedBy=multi-user.target
```

5. **Configurer Nginx**
```nginx
# /etc/nginx/sites-available/vetdefrance
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /chemin/vers/pj/static;
    }
}
```

6. **Activer et démarrer**
```bash
sudo systemctl enable vetdefrance
sudo systemctl start vetdefrance
sudo ln -s /etc/nginx/sites-available/vetdefrance /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### Option 4 : Docker

1. **Créer un Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

2. **Créer un docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_NAME=bddvet
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - SECRET_KEY=votre-cle-secrete
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=bddvet
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/bddvet.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  postgres_data:
```

3. **Déployer**
```bash
docker-compose up -d
```

## Variables d'environnement en production

Assurez-vous de définir :
- `SECRET_KEY` : Clé secrète unique (utilisez `python -c 'import secrets; print(secrets.token_hex(32))'`)
- `DB_HOST` : Hôte de la base de données
- `DB_NAME` : Nom de la base
- `DB_USER` : Utilisateur PostgreSQL
- `DB_PASSWORD` : Mot de passe PostgreSQL
- `DB_PORT` : Port PostgreSQL (5432 par défaut)

## Checklist avant déploiement

- [ ] Générer une nouvelle `SECRET_KEY`
- [ ] Configurer les variables d'environnement
- [ ] Tester la connexion à la base de données
- [ ] Désactiver le mode debug Flask (par défaut désactivé)
- [ ] Vérifier que `.env` est dans `.gitignore`
- [ ] Importer les données initiales
- [ ] Tester tous les endpoints
- [ ] Configurer HTTPS (Let's Encrypt recommandé)
- [ ] Configurer les sauvegardes de la base de données

## Sécurité en production

1. **HTTPS obligatoire**
   - Utiliser Let's Encrypt pour un certificat gratuit
   - Forcer la redirection HTTP → HTTPS

2. **Limiter les requêtes**
   - Implémenter Flask-Limiter pour éviter les abus

3. **Sauvegardes régulières**
   - Sauvegarder PostgreSQL quotidiennement
   - Stocker les sauvegardes hors serveur

4. **Monitoring**
   - Utiliser des outils comme Sentry pour le tracking d'erreurs
   - Surveiller les performances avec New Relic ou Datadog

5. **Mises à jour**
   - Maintenir les dépendances à jour
   - Suivre les alertes de sécurité

## Support

Pour plus d'informations sur le déploiement, consultez :
- Documentation Flask : https://flask.palletsprojects.com/en/latest/deploying/
- Documentation PostgreSQL : https://www.postgresql.org/docs/
- Gunicorn : https://docs.gunicorn.org/
