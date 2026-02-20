# Guide de contribution

Merci de votre intérêt pour contribuer à VetDeFrance !

## Comment contribuer

### Signaler un bug

Si vous trouvez un bug :
1. Vérifiez qu'il n'a pas déjà été signalé dans les Issues
2. Créez une nouvelle Issue avec :
   - Une description claire du problème
   - Les étapes pour reproduire le bug
   - Le comportement attendu vs le comportement observé
   - Votre environnement (OS, version Python, etc.)

### Proposer une fonctionnalité

Pour proposer une nouvelle fonctionnalité :
1. Ouvrez une Issue avec le tag "enhancement"
2. Décrivez clairement la fonctionnalité et son utilité
3. Attendez les retours avant de commencer le développement

### Soumettre du code

1. **Fork le projet**
2. **Créez une branche** : `git checkout -b feature/ma-fonctionnalite`
3. **Committez vos changements** : `git commit -m 'Ajout de ma fonctionnalité'`
4. **Push vers la branche** : `git push origin feature/ma-fonctionnalite`
5. **Ouvrez une Pull Request**

## Standards de code

### Python
- Suivre la PEP 8
- Utiliser des noms de variables explicites
- Commenter le code complexe
- Tester les modifications

### HTML/CSS
- Indentation : 4 espaces
- Noms de classes en kebab-case
- Utiliser les variables CSS du thème

### SQL
- Mots-clés en MAJUSCULES
- Indentation cohérente
- Noms de tables/colonnes en minuscule

## Structure des commits

Format des messages de commit :
```
type: description courte

Description détaillée si nécessaire
```

Types possibles :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage du code
- `refactor`: Refactoring
- `test`: Ajout de tests

Exemples :
```
feat: ajout recherche animaux par propriétaire

fix: correction génération PDF pour animaux sans soins

docs: mise à jour README installation
```

## Tests

Avant de soumettre :
- Testez votre code localement
- Vérifiez qu'il n'y a pas d'erreurs dans la console
- Testez sur différents navigateurs si possible

## Questions ?

N'hésitez pas à ouvrir une Issue pour poser vos questions !
