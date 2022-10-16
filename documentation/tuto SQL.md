# Tutoriel de l'onglet "Requêtes SQL" de l'application BD-Manga

## Recommandations :

- N'utilisez cet onglet que si vous savez écrire des requêtes SQL.
- Ne lancez qu'une requête à la fois.

## Informations supplémentaires :

- La structure de la base de données sous forme de requêtes SQL est disponible [ici](https://github.com/Leroymilo/ClubBDM-DB/blob/main/documentation/structure%20db.md) pour plus de détails.
- Si vous écrivez plusieurs requêtes séparées par des `;`, elles seront toutes executées mais seul le dernier `SELECT` sera affiché.
- Les requêtes de modification sont protégées par un mot de passe.
- Les requêtes passent par la librairie python-SQL par défaut `sqlite3` pour éviter des problèmes de màj, mais cette librairie ne supporte pas toutes les fonctions SQL habituelles, voici celles qui ont été réimplémentées :
    - `REGEXP(item, expression)`
    - `LPAD(item, filler, width)`
    - `IF(condition, if_true, if_false)`
    - `CONCATWS(separator, *args)`
    - `CONCAT(separator, attribute)` (aggrégat, donc à utiliser avec GROUP BY)

### Exemple de l'aggrégat CONCAT :
```sql
SELECT series_name, CONCAT('; ', auth_name) AS authors
FROM Authors
NATURAL JOIN Series
NATURAL JOIN `Srs-Auth`
GROUP BY series_id
```
Renvoi (échantillon) :

|series_name|authors|
|:-------:|:----:|
|"Berserk"|"Kentaro Miura"|
|"Requiem Chevalier Vampire"|"Pat Mills; Olivier Ledroit"|
|"The Walking Dead"|"Robert Kirkman; Charlie Adlard; Tony Moore; Stefano Gaudiano; Cliff Rathburn"|
|"Dragon Ball"|"Akira Toriyama"|