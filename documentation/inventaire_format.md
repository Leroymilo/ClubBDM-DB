# Instruction de mise-en-forme d'un inventaire pour l'import de données

Pour que l'application lise correctement un fichier excel de données à importer, ce fichier doit suivre un format assez strict.</br>
Pour avoir un exemple avec au moins les feuilles et les colonnes du fichier excel, il suffit de générer un inventaire avec l'application, mais la structure et les règles à respecter sont rappelées ci-dessous.</br>
Les guillemets `"` sont interdits das les champs de texte (les apostrophes sont autorisés). Vous pouvez les remplacer par ce charactère : `”`.

## Structure :
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

## Règles :

### Catégories
2 catégories ne peuvent pas avoir le même code ou la même désignation.</br>
Le code doit être compris entre 0 et 99 (inclus).

### Séries
L'identifiant doit être composé d'exactement 5 charactères alphanumériques (alphabétiques de préférence).</br>
Le type doit être un de ces 4 : "`bd`", "`comics`", "`manga`" ou "`roman`".</br>
La catégorie doit correspondre **exactement** à la désignation d'une catégorie de l'onglet `Catégories`.</br>
Les auteurs (et éditeurs) doivent être séparés par des points-virgules `;` et les noms doivent correspondre **exactement** aux noms de l'onglet `Auteurs` (respectivement, aux noms de l'onglet `Éditeurs`).

### Livres
La cotation n'est pas nécessaire : elle sera recalculée en fonction des autres colonnes de toute façon.</br>
L'identifiant de la série doit correspondre **exactement** à un identifiant de l'onglet `Séries`.</br>
Le numéro de volume est compris entre 0 et 999 (inclus).</br>
Le numéro de duplicata est compris entre 0 et 99 (inclus).</br>
La disponibilité doit être remprésentée par `Oui` ou `Non`.</br>
La condition est une note d'état comprise entre 1 et 10 (inclus), 10 étant un ouvrage neuf et 1 un ouvrage extrêmement abimé.</br>
La date d'ajout doit être au format Année(4 charactères)/Mois/Jour, exemple : `2022/11/15`. Si Excel reconnait la date ça doit marcher aussi, mais on est jamais sûr avec Excel...</br>

### Membres
Le statut doit être un des suivants : "`Membre`", "`Membre actif`", "`Membre +`", "`Membre actif +`" ou "`Bureau`".</br>
La caution est en euros.</br>
Il doit y avoir au moins un contact de rempli : mail ou tel.

### Emprunts
L'import des emprunts n'a pas été implémenté comme le système n'est pas actuellement en place. Il sera à faire dans la fonction `write_db` du script `functions/inventory.py`.

### Auteurs et Éditeurs
Les noms ne doivent pas contenir de point-virgule `;`.