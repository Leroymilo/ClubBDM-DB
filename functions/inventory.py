from db_init import *
import pandas as pd
from datetime import date

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

    return data

def write_db(data: dict[str, pd.DataFrame], replace = False) -> None :
    pass

def read_db() -> dict[str, pd.DataFrame] :
    data = {
        "categories" : pd.read_sql_query("""--sql
            SELECT cat_id AS code,
                   cat_name AS `désignation`
            FROM Categories
        ;"""),
        "authors" : pd.read_sql_query("""--sql
            SELECT auth_name AS nom
            FROM Authors
        ;"""),
        "editors" : pd.read_sql_query("""--sql
            SELECT edit_name AS nom
            FROM Editors
        ;"""),
        "series" : pd.read_sql_query("""--sql
            SELECT series_id AS identifiant,
                   series_name AS nom,
                   book_type AS type,
                   cat_name AS catégorie,
                   auths AS auteurs,
                   edits AS editors
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
        ;"""),
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
        ;"""),
        "members": pd.read_sql_query("""--sql
            SELECT member_name AS nom,
                   mail, tel,
                   status_BDM AS statut,
                   bail AS caution,
                   comment AS commentaire
            FROM Members
        ;"""),
        "loans": pd.read_sql_query("""--sql
            SELECT member_name AS `nom membre`,
                   book_id AS `cotation livre`
            FROM Loans
            JOIN Members
                USING (member_id)
        ;""")
    }

    return data

def write_xlsx(directory: str, data: dict[str, pd.DataFrame]) -> None :
    Sheet_names = {
        "categories": "Catégories",
        "series": "Séries",
        "books": "Livres",
        "members": "Membres",
        "loans": "Loans",
        "authors": "Auteurs",
        "editors": "Éditeurs"
    }

    writer = pd.ExcelWriter(directory, engine='xlsxwriter')

    for table in Sheet_names :
        sh_name = Sheet_names[table]
        data[table].to_excel(
            excel_writer=writer,
            sheet_name=sh_name,
            index=False
        )