# Instruction de mise-en-forme d'un inventaire pour l'import de données

Pour que l'application lise correctement un fichier excel de données à importer, ce fichier doit suivre un format assez strict.</br>
Pour avoir un exemple avec au moins les colonnes et les feuilles du fichier excel, il suffit de générer un inventaire avec l'application, mais la structure et les règles à respecter sont rappelées ci-dessous.

## Structure :
- Catégories
    - code
    - désignation
- Séries
    - identifiant
    - nom
    - type
    - catégorie
    - auteurs
    - éditeurs
- Livres
    - cotation (facultative, recalculée en interne)
    - nom
    - identifiant série
    - numéro de volume
    - numéro de duplicata
    - disponible
    - condition
    - date d'ajout
    - commentaire
- Membres
    - nom
    - mail
    - tel
    - statut
    - caution
    - commentaire
- Emprunts (pas pris en compte dans l'import)
    - nom membre
    - cotation livre
- Auteurs
    - nom
- Éditeurs
    - nom

## Règles :

# 