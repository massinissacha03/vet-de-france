# Documentation des Routes

## Routes publiques

### Page d'accueil
- **URL** : `/` ou `/accueil`
- **Méthodes** : GET, POST
- **Description** : Page d'accueil avec choix employé/propriétaire

### Annuaire des centres
- **URL** : `/invite`
- **Méthode** : GET
- **Description** : Liste de tous les centres vétérinaires

### Détails d'un centre
- **URL** : `/invite/<codepostale>/<nomcentre>`
- **Méthode** : GET
- **Description** : Informations détaillées sur un centre

## Routes Employés

### Connexion
- **URL** : `/emp`
- **Méthodes** : GET, POST
- **Description** : Formulaire de connexion pour les vétérinaires
- **POST params** : `login`, `mdp`

### Création de compte
- **URL** : `/creer`
- **Méthodes** : GET, POST
- **Description** : Inscription d'un nouvel employé
- **POST params** : `prenom`, `nom`, `adresse`, `tel`, `naissance`, `numsec`, `loginn`, `mdp`, `idcentre`

### Tableau de bord
- **URL** : `/pageemp`
- **Méthode** : GET
- **Auth** : Requise (session)
- **Description** : Page principale avec liste des animaux du centre

### Fiche animal (vétérinaire)
- **URL** : `/animal/<ida>`
- **Méthode** : GET
- **Auth** : Requise (session)
- **Description** : Détails complets d'un animal et ses soins

### Ajouter un animal
- **URL** : `/animal/ajouter`
- **Méthodes** : GET, POST
- **Auth** : Requise (session)
- **Description** : Enregistrer un nouvel animal
- **POST params** : `nom`, `espece`, `age`, `sexe`, `signedist`, `idpro`, `inscrire_centre`

### Ajouter un soin
- **URL** : `/soin/ajouter`
- **Méthode** : POST
- **Auth** : Requise (session)
- **Description** : Ajouter un soin à un animal
- **POST params** : `ida`, `nature`, `historique`

## Routes Propriétaires

### Connexion
- **URL** : `/connexionprop`
- **Méthodes** : GET, POST
- **Description** : Formulaire de connexion propriétaire
- **POST params** : `username` (email), `numero` (tel), `id_animal`

### Création de compte
- **URL** : `/creer/proprietaire`
- **Méthodes** : GET, POST
- **Description** : Inscription d'un nouveau propriétaire
- **POST params** : `nom`, `prenom`, `tel`, `mail`, `adresse`

### Tableau de bord
- **URL** : `/pageprop`
- **Méthode** : GET
- **Auth** : Requise (session)
- **Description** : Vue du propriétaire sur son animal

### Modifier l'animal
- **URL** : `/changer`
- **Méthodes** : GET, POST
- **Auth** : Requise (session)
- **Description** : Modifier les infos de l'animal
- **POST params** : `tochange` (nom|age|signedist), `valeur`

### Générer PDF
- **URL** : `/pdf`
- **Méthode** : GET
- **Auth** : Requise (session)
- **Description** : Télécharger la fiche médicale en PDF

## Route commune

### Déconnexion
- **URL** : `/deconnecter`
- **Méthode** : GET
- **Description** : Déconnexion (employé ou propriétaire)

## Sessions

Les sessions utilisent Flask session avec les clés suivantes :

### Session Employé
- `loginn` : Login de l'employé
- `mat` : Matricule
- `idcentre` : ID du centre

### Session Propriétaire
- `id` : ID du propriétaire
- `email` : Email
- `num` : Numéro de téléphone
- `ida` : ID de l'animal

## Codes de réponse

- **200** : Succès
- **302** : Redirection (notamment pour les redirections après login)
- **404** : Page non trouvée
- **500** : Erreur serveur
