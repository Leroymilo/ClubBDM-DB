from db_init import *
import pandas as pd
from datetime import date

import db_reset #Cleans database

categories = pd.read_excel("Inventaire.xlsx", sheet_name="Catégories")
authors = pd.read_excel("Inventaire.xlsx", sheet_name="Auteurs")
editors = pd.read_excel("Inventaire.xlsx", sheet_name="Éditeurs")
series = pd.read_excel("Inventaire.xlsx", sheet_name="Séries")
books = pd.read_excel("Inventaire.xlsx", sheet_name="Livres")

series.fillna("NULL", inplace=True)
books.fillna("NULL", inplace=True)

cat_dict = {}
for _, line in categories.iterrows() :
    cat_dict[line.désignation] = line.code
    cursor.execute(f"""--sql
        INSERT INTO Categories VALUES (
            {line.code},
            "{line.désignation}"
        )
    ;""")

for _, line in authors.iterrows() :
    cursor.execute(f"""--sql
        INSERT INTO Authors (auth_name) VALUES ("{line.nom}")
    ;""")

for _, line in editors.iterrows() :
    cursor.execute(f"""--sql
        INSERT INTO Editors (edit_name) VALUES ("{line.nom}")
    ;""")

srs_cat_dict = {}
for _, line in series.iterrows() :
    cursor.execute(f"""--sql
        INSERT INTO Series VALUES (
            "{line.identifiant}",
            "{line.nom}",
            "{line.type}",
            {cat_dict[line.catégorie]}
        )
    ;""")

    srs_cat_dict[line.identifiant] = cat_dict[line.catégorie]

    for auth in line.auteurs.split(";") :
        auth = auth.strip().lstrip()
        if auth != "NULL" :
            cursor.execute(f"""SELECT auth_id FROM Authors WHERE auth_name = "{auth}";""")
            auth_id, = cursor.fetchone()
            cursor.execute(f"""--sql
                INSERT INTO `Srs-Auth` VALUES (
                    "{line.identifiant}", {auth_id}
                )
            ;""")

    for edit in line.éditeurs.split(";") :
        edit = edit.strip().lstrip()
        if edit != "NULL" :
            cursor.execute(f"""SELECT edit_id FROM Editors WHERE edit_name = "{edit}";""")
            edit_id, = cursor.fetchone()
            cursor.execute(f"""--sql
                INSERT INTO `Srs-Edit` VALUES (
                    "{line.identifiant}", {edit_id}
                )
            ;""")

for _, line in books.iterrows() :
    srs_id = line["identifiant série"]
    cat_id = str(srs_cat_dict[srs_id])
    vol_nb = str(line["numéro de volume"])
    dup_nb = str(line["numéro de duplicata"])

    new_id = cat_id.rjust(2, '0') + srs_id + \
        vol_nb.rjust(3, '0') + dup_nb.rjust(2, '0')
    
    today = date.today().strftime("%Y/%m/%d")
    
    cursor.execute(f"""--sql
        INSERT INTO Books (
            book_id,
            book_name,
            series_id,
            vol_nb,
            dup_nb,
            added_on,
            condition,
            comment
        ) VALUES (
            "{new_id}",
            "{line.nom}",
            "{srs_id}",
            {vol_nb},
            {dup_nb},
            "{today}",
            {line.condition},
            "{line.commentaire}"
        )
    ;""")

db.commit()
print("Excel imported")
db.close()