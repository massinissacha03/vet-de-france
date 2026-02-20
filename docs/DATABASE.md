# Architecture de la Base de Données

## Schéma relationnel

```
┌────────────────┐         ┌─────────────┐         ┌──────────────┐
│    centre      │         │   employes  │         │    propri    │
├────────────────┤         ├─────────────┤         ├──────────────┤
│ PK idcentre    │◄────────│ FK idcentre │         │ PK idpro     │
│    nomcentre   │         │ PK mat      │         │    nom       │
│    codepost    │         │    nom      │         │    prenom    │
│    adresse     │         │    prenom   │         │    mail      │
│    tel         │         │    adresse  │         │    tel       │
└────────────────┘         │    tel      │         │    adresse   │
        │                  │    naissance│         └──────────────┘
        │                  │    numsec   │                │
        │                  │    login    │                │
        └──────────┐       │    mdp      │                │
                   │       └─────────────┘                │
                   │              │                       │
                   │              │                       │
                   ▼              ▼                       ▼
              ┌──────────────────────────────────────────────┐
              │                 animal                       │
              ├──────────────────────────────────────────────┤
              │ PK ida                                       │
              │    nom                                       │
              │    espece                                    │
              │    age                                       │
              │    sexe                                      │
              │    signedist (signes distinctifs)            │
              │ FK idpro (propriétaire)                      │
              └──────────────────────────────────────────────┘
                        │                  │
                        │                  │
            ┌───────────┴────────┐    ┌────┴──────────┐
            │                    │    │               │
            ▼                    ▼    ▼               ▼
      ┌──────────┐         ┌──────────┐        ┌──────────┐
      │ inscrit  │         │  opere   │        │ordonnance│
      ├──────────┤         ├──────────┤        ├──────────┤
      │ FK ida   │         │ FK ida   │        │ FK ida   │
      │ FK idcent│         │ FK mat   │        │ numordo  │
      │ dateins  │         │ datesoin │        │ details  │
      └──────────┘         │ nature   │        │ date     │
                           │historique│        └──────────┘
                           └──────────┘
```

## Description des tables

### centre
Table des centres vétérinaires partenaires.

| Colonne    | Type         | Contraintes | Description                  |
|------------|--------------|-------------|------------------------------|
| idcentre   | INTEGER      | PK          | Identifiant unique du centre |
| nomcentre  | VARCHAR(200) | NOT NULL    | Nom du centre               |
| codepost   | INTEGER      | NOT NULL    | Code postal                 |
| adresse    | VARCHAR(200) | NOT NULL    | Adresse complète            |
| tel        | VARCHAR(200) |             | Numéro de téléphone         |

### employes
Table des vétérinaires employés dans les centres.

| Colonne    | Type         | Contraintes        | Description                  |
|------------|--------------|--------------------|------------------------------|
| mat        | INTEGER      | PK                 | Matricule de l'employé      |
| nom        | VARCHAR(50)  | NOT NULL           | Nom de famille              |
| prenom     | VARCHAR(50)  | NOT NULL           | Prénom                      |
| adresse    | VARCHAR(200) | NOT NULL           | Adresse du domicile         |
| tel        | VARCHAR(15)  | NOT NULL           | Téléphone personnel         |
| naissance  | DATE         | NOT NULL           | Date de naissance           |
| numsec     | VARCHAR(50)  | NOT NULL, UNIQUE   | Numéro de sécurité sociale  |
| login      | VARCHAR(50)  | NOT NULL, UNIQUE   | Login de connexion          |
| mdp        | VARCHAR(255) | NOT NULL           | Mot de passe hashé          |
| idcentre   | INTEGER      | FK → centre        | Centre d'affectation        |

### propri (propriétaires)
Table des propriétaires d'animaux.

| Colonne | Type         | Contraintes | Description              |
|---------|--------------|-------------|--------------------------|
| idpro   | VARCHAR(10)  | PK          | ID unique (P + 9 chiffres)|
| nom     | VARCHAR(50)  | NOT NULL    | Nom de famille           |
| prenom  | VARCHAR(50)  | NOT NULL    | Prénom                   |
| mail    | VARCHAR(100) | NOT NULL    | Email                    |
| tel     | VARCHAR(15)  | NOT NULL    | Téléphone                |
| adresse | VARCHAR(200) |             | Adresse du domicile      |

### animal
Table des animaux enregistrés.

| Colonne   | Type         | Contraintes  | Description              |
|-----------|--------------|--------------|--------------------------|
| ida       | INTEGER      | PK           | Identifiant unique       |
| nom       | VARCHAR(50)  | NOT NULL     | Nom de l'animal          |
| espece    | VARCHAR(50)  | NOT NULL     | Espèce (chien, chat...)  |
| age       | INTEGER      |              | Âge en années            |
| sexe      | VARCHAR(10)  |              | Sexe (M/F)               |
| signedist | VARCHAR(200) |              | Signes distinctifs       |
| idpro     | VARCHAR(10)  | FK → propri  | Propriétaire             |

### inscrit
Table de liaison : animaux inscrits dans les centres.

| Colonne  | Type    | Contraintes    | Description                    |
|----------|---------|----------------|--------------------------------|
| ida      | INTEGER | FK → animal    | Animal inscrit                 |
| idcentre | INTEGER | FK → centre    | Centre d'inscription           |
| dateins  | DATE    | NOT NULL       | Date d'inscription             |
| -        | -       | PK (ida, idcentre) | Clé primaire composite    |

### opere
Table des soins et interventions sur les animaux.

| Colonne    | Type          | Contraintes   | Description                  |
|------------|---------------|---------------|------------------------------|
| ida        | INTEGER       | FK → animal   | Animal concerné              |
| mat        | INTEGER       | FK → employes | Vétérinaire                  |
| datesoin   | DATE          | NOT NULL      | Date du soin                 |
| nature     | VARCHAR(200)  | NOT NULL      | Type de soin                 |
| historique | TEXT          |               | Détails du soin              |
| -          | -             | PK (ida, mat, datesoin) | Clé primaire composite |

### ordonnance
Table des ordonnances (actuellement non utilisée dans l'application).

| Colonne  | Type         | Contraintes | Description                 |
|----------|--------------|-------------|-----------------------------|
| ida      | INTEGER      | FK → animal | Animal concerné             |
| numordo  | INTEGER      | NOT NULL    | Numéro d'ordonnance         |
| details  | TEXT         |             | Contenu de l'ordonnance     |
| date     | DATE         |             | Date de prescription        |
| -        | -            | PK (ida, numordo) | Clé primaire composite |

## Relations

### 1 à N (One-to-Many)
- **centre → employes** : Un centre peut avoir plusieurs employés
- **centre → inscrit** : Un centre peut avoir plusieurs animaux inscrits
- **propri → animal** : Un propriétaire peut avoir plusieurs animaux
- **animal → opere** : Un animal peut avoir plusieurs soins
- **animal → ordonnance** : Un animal peut avoir plusieurs ordonnances
- **employes → opere** : Un vétérinaire peut effectuer plusieurs soins

### N à N (Many-to-Many)
- **animal ↔ centre** (via inscrit) : Un animal peut être inscrit dans plusieurs centres, un centre peut avoir plusieurs animaux
- **animal ↔ employes** (via opere) : Un animal peut être soigné par plusieurs vétérinaires, un vétérinaire peut soigner plusieurs animaux

## Contraintes d'intégrité

### Clés étrangères avec CASCADE
```sql
-- Suppression d'un centre → supprime ses employés
FOREIGN KEY (idcentre) REFERENCES centre(idcentre) ON DELETE CASCADE

-- Suppression d'un animal → supprime ses soins
FOREIGN KEY (ida) REFERENCES animal(ida) ON DELETE CASCADE

-- Suppression d'un propriétaire → supprime ses animaux
FOREIGN KEY (idpro) REFERENCES propri(idpro) ON DELETE CASCADE
```

### Contraintes d'unicité
- `employes.numsec` : Numéro de sécurité sociale unique
- `employes.login` : Login unique pour l'authentification
- Clés primaires composites pour éviter les doublons dans les tables de jonction

## Index recommandés

Pour améliorer les performances :
```sql
CREATE INDEX idx_animal_idpro ON animal(idpro);
CREATE INDEX idx_opere_ida ON opere(ida);
CREATE INDEX idx_opere_mat ON opere(mat);
CREATE INDEX idx_inscrit_ida ON inscrit(ida);
CREATE INDEX idx_inscrit_idcentre ON inscrit(idcentre);
CREATE INDEX idx_employes_login ON employes(login);
```

## Exemples de requêtes

### Trouver tous les animaux d'un centre
```sql
SELECT a.* 
FROM animal a
JOIN inscrit i ON a.ida = i.ida
WHERE i.idcentre = 1;
```

### Historique des soins d'un animal
```sql
SELECT o.datesoin, o.nature, o.historique, e.nom, e.prenom
FROM opere o
JOIN employes e ON o.mat = e.mat
WHERE o.ida = 1
ORDER BY o.datesoin DESC;
```

### Animaux d'un propriétaire
```sql
SELECT a.* 
FROM animal a
WHERE a.idpro = 'P123456789';
```

### Vétérinaires d'un centre
```sql
SELECT e.nom, e.prenom, e.tel
FROM employes e
WHERE e.idcentre = 1;
```
