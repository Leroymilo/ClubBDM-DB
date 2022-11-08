from db_init import *
import pandas as pd
from datetime import date
import time as t

Cols = {
    "categories": {"code", "désignation"},
    "series": {"identifiant", "nom", "type", "catégorie", "auteurs", "éditeurs"},
    "books": {
        "cotation", "nom", "identifiant série",
        "numéro de volume", "numéro de duplicata", "disponible",
        "condition", "date d'ajout", "commentaire"
    },
    "members": {"nom", "mail", "tel", "statut", "caution", "commentaire"},
    "loans": {"nom membre", "cotation livre"},
    "authors": {"nom"},
    "editors": {"nom"}
}

Sheets = {
    "categories": "Catégories",
    "series": "Séries",
    "books": "Livres",
    "members": "Membres",
    "loans": "Emprunts",
    "authors": "Auteurs",
    "editors": "Éditeurs"
}


def read_xlsx(directory: str) -> dict[str, pd.DataFrame] :
    data = {
        "categories" : pd.read_excel(directory, sheet_name="Catégories"),
        "authors" : pd.read_excel(directory, sheet_name="Auteurs"),
        "editors" : pd.read_excel(directory, sheet_name="Éditeurs"),
        "series" : pd.read_excel(directory, sheet_name="Séries"),
        "books" : pd.read_excel(directory, sheet_name="Livres"),
        "members": pd.read_excel(directory, sheet_name="Membres"),
        "loans": pd.read_excel(directory, sheet_name="Emprunts")
    }

    for table_name, table in data.items() :
        miss_cols = Cols[table_name].difference(set(table.columns.to_list()))
        if len(miss_cols) > 0 :
            return 1, (Sheets[table_name], miss_cols)

    return 0, data


def write_db(data: dict[str, pd.DataFrame], replace = False) -> None :
    if replace :
        import db_reset
    
    t0 = t.time()
    print("started writing")

    # Categories :
    cat_dict = {line.désignation: line.code for _, line in data["categories"].iterrows()}
    cursor.execute(f"""--sql
        INSERT OR IGNORE
        INTO Categories
        VALUES ({"), (".join(
            f'{line.code}, "{line.désignation}"'
            for _, line in data["categories"].iterrows()
        )})
    ;""")

    print(f"Categories took {round(t.time()-t0, 3)}s")
    t0 = t.time()

    # Authors :
    cursor.execute(f"""--sql
        INSERT OR IGNORE
        INTO Authors (auth_name)
        VALUES ({"), (".join(
            f'"{line.nom}"'
            for _, line in data["authors"].iterrows()
        )})
    ;""")

    print(f"Authors took {round(t.time()-t0, 3)}s")
    t0 = t.time()

    # Editors :
    cursor.execute(f"""--sql
        INSERT OR IGNORE
        INTO Editors (edit_name)
        VALUES ({"), (".join(
            f'"{line.nom}"'
            for _, line in data["editors"].iterrows()
        )})
    ;""")

    print(f"Editors took {round(t.time()-t0, 3)}s")
    t0 = t.time()

    # Series :
    cursor.execute(f"""--sql
        INSERT OR IGNORE
        INTO Series
        VALUES ({"), (".join(
            f'"{line.identifiant}", "{line.nom}", "{line.type}", {cat_dict[line.catégorie]}'
            for _, line in data["series"].iterrows()
        )})
    ;""")

    cursor.execute("SELECT * FROM Authors;")
    auth_dict = {
        name: code
        for code, name in cursor.fetchall()
    }
    cursor.execute(f"""--sql
        INSERT OR IGNORE
        INTO `Srs-Auth`
        VALUES ({"), (".join(
            "), (".join(
                f'"{line.identifiant}", {auth_dict[auth_name.strip()]}'
                for auth_name in line.auteurs.split(";")
            )
            for _, line in data["series"].iterrows()
        )})
    ;""")

    cursor.execute("SELECT * FROM Editors;")
    edit_dict = {
        name: code
        for code, name in cursor.fetchall()
    }
    cursor.execute(f"""--sql
        INSERT OR IGNORE
        INTO `Srs-Edit`
        VALUES ({"), (".join(
            "), (".join(
                f'"{line.identifiant}", {edit_dict[edit_name.strip()]}'
                for edit_name in line.éditeurs.split(";")
            )
            for _, line in data["series"].iterrows()
        )})
    ;""")

    print(f"Series took {round(t.time()-t0, 3)}s")
    t0 = t.time()

    # Books
    series_dict = {
        line.identifiant : cat_dict[line.catégorie]
        for _, line in data["series"].iterrows()
    }

    data["books"].loc[data["books"].cotation == ""]

    # cursor.execute(f"""--sql
    #     INSERT OR IGNORE
    #     INTO Books
    #     Values ({"), (".join(
    #         f'{line}'
    #         for _, line in data["books"].iterrows()
    #     )})
    # ;""")

    print(f"Books took {round(t.time()-t0, 3)}s")


def read_db() -> dict[str, pd.DataFrame] :
    data = {
        "categories" : pd.read_sql_query("""--sql
            SELECT cat_id AS code,
                   cat_name AS `désignation`
            FROM Categories
        ;""", db),
        "authors" : pd.read_sql_query("""--sql
            SELECT auth_name AS nom
            FROM Authors
        ;""", db),
        "editors" : pd.read_sql_query("""--sql
            SELECT edit_name AS nom
            FROM Editors
        ;""", db),
        "series" : pd.read_sql_query("""--sql
            SELECT series_id AS identifiant,
                   series_name AS nom,
                   book_type AS type,
                   cat_name AS catégorie,
                   auths AS auteurs,
                   edits AS éditeurs
            FROM Series
            JOIN Categories
                ON book_category = cat_id
            NATURAL JOIN (
                SELECT series_id, CONCAT('; ', auth_name) AS auths
                FROM Authors
                NATURAL JOIN `Srs-Auth`
                GROUP BY series_id
            )
            NATURAL JOIN (
                SELECT series_id, CONCAT('; ', edit_name) AS edits
                FROM Editors
                NATURAL JOIN `Srs-Edit`
                GROUP BY series_id
            )
        ;""", db),
        "books" : pd.read_sql_query("""--sql
            SELECT book_id AS `cotation (sera recalculée)`,
                   book_name AS nom,
                   series_id AS `identifiant série`,
                   vol_nb AS `numéro de volume`,
                   dup_nb AS `numéro de duplicata`,
                   IF(available, 'Oui', 'Non') AS `disponible`,
                   condition,
                   added_on AS `date d'ajout`,
                   comment AS commentaire
            FROM Books
        ;""", db),
        "members": pd.read_sql_query("""--sql
            SELECT member_name AS nom,
                   mail, tel,
                   status_BDM AS statut,
                   bail AS caution,
                   comment AS commentaire
            FROM Members
        ;""", db),
        "loans": pd.read_sql_query("""--sql
            SELECT member_name AS `nom membre`,
                   book_id AS `cotation livre`
            FROM Loans
            JOIN Members
                USING (member_id)
        ;""", db)
    }

    return data


def write_xlsx(directory: str, data: dict[str, pd.DataFrame]) -> None :
    writer = pd.ExcelWriter(directory, engine='xlsxwriter')

    for table in Sheets :
        data[table].to_excel(
            excel_writer=writer,
            sheet_name=Sheets[table],
            index=False
        )
    writer.close()