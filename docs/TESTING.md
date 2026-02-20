# Guide de Test

## Comptes de test

Le fichier `database/bddvet.sql` contient des données de test pour faciliter le développement et les tests.

### Comptes Vétérinaires

| Login | Mot de passe | Centre |
|-------|--------------|--------|
| `vet1` | `password123` | VetDeFrance Paris |
| `vet2` | `password123` | VetDeFrance Lyon |

### Comptes Propriétaires

Pour se connecter en tant que propriétaire, vous avez besoin de :
- Email du propriétaire
- Numéro de téléphone
- ID de l'animal

**Exemple de compte propriétaire :**
- **Email** : `dupont.jean@example.com`
- **Téléphone** : `0612345678`
- **ID Animal** : `1` (Rex, un Labrador)

**Autre propriétaire :**
- **Email** : `martin.sophie@example.com`
- **Téléphone** : `0687654321`
- **ID Animal** : `2` (Whiskers, un Chat)

## Scénarios de test

### Test 1 : Connexion Vétérinaire
1. Aller sur `/emp`
2. Login : `vet1`
3. Mot de passe : `password123`
4. Vérifier l'accès à la page `/pageemp`

### Test 2 : Ajout d'un animal
1. Se connecter en tant que vétérinaire
2. Cliquer sur "Nouvel animal"
3. Remplir le formulaire
4. Vérifier que l'animal apparaît dans la liste

### Test 3 : Ajout d'un soin
1. Se connecter en tant que vétérinaire
2. Cliquer sur un animal
3. Ajouter un soin
4. Vérifier qu'il apparaît dans l'historique

### Test 4 : Connexion Propriétaire
1. Aller sur `/connexionprop`
2. Utiliser les identifiants ci-dessus
3. Vérifier l'accès à la page `/pageprop`

### Test 5 : Génération PDF
1. Se connecter en tant que propriétaire
2. Cliquer sur "Télécharger PDF"
3. Vérifier que le PDF contient toutes les informations

### Test 6 : Création de compte propriétaire
1. Aller sur la page d'accueil
2. Cliquer sur "Créer un compte propriétaire"
3. Remplir le formulaire
4. Vérifier la génération de l'ID (format P + 9 chiffres)

### Test 7 : Modification d'animal
1. Se connecter en tant que propriétaire
2. Aller sur "Modifier les informations"
3. Changer le nom ou l'âge
4. Vérifier la mise à jour

## Tests de sécurité

### Test d'accès non autorisé
- Essayer d'accéder à `/pageemp` sans être connecté
- Devrait rediriger vers `/emp`

### Test de mot de passe incorrect
- Se connecter avec un mauvais mot de passe
- Devrait afficher une erreur

### Test de déconnexion
- Se connecter et cliquer sur "Se déconnecter"
- Vérifier la redirection vers l'accueil

## États de la base de données

Après avoir exécuté `database/bddvet.sql`, vous aurez :
- 2 centres vétérinaires
- 2 vétérinaires
- 2 propriétaires
- 2 animaux avec historique de soins
- Plusieurs enregistrements de soins

## Réinitialiser les données

Pour réinitialiser la base de données :

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Supprimer et recréer la base
DROP DATABASE bddvet;
CREATE DATABASE bddvet;
\q

# Réimporter les données
psql -U postgres -d bddvet -f database/bddvet.sql
```

## Tests automatisés

Pour implémenter des tests automatisés (non inclus actuellement), considérez :
- **pytest** : Framework de test Python
- **Flask-Testing** : Extension pour tester les applications Flask
- **Selenium** : Tests end-to-end du navigateur

Exemple de structure de test :
```
tests/
  ├── test_auth.py
  ├── test_routes.py
  ├── test_pdf.py
  └── test_database.py
```
