#!/bin/bash
# script pour lancer l'appli VetDeFrance

echo "Démarrage de VetDeFrance..."

# se placer dans le dossier racine du projet
cd "$(dirname "$0")/.."

# vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "Erreur : environnement virtuel non trouvé"
    echo "Lancez : python3 -m venv venv"
    exit 1
fi

# activer l'environnement virtuel
source venv/bin/activate

# vérifier si .env existe
if [ ! -f ".env" ]; then
    echo "Attention : fichier .env non trouvé"
    echo "Copiez .env.example vers .env et configurez-le"
fi

# lancer Flask
echo "Application disponible sur http://localhost:5000"
python main.py
