from db_init import *
from db_reset import reset

import pandas as pd
from datetime import date, datetime, timedelta
import time as t

bad_chars = {'"', ';'}

Cols = {
    "categories": {"code", "désignation"},
    "series": {"identifiant", "nom", "type", "catégorie", "auteurs", "éditeurs"},
    "books": {
        "nom", "identifiant série",
        "numéro de volume", "numéro de duplicata", "disponible",
        "condition", "date d'ajout", "commentaire"
    },
    "members": {"nom", "mail", "tel", "statut", "caution", "commentaire"},
    "loans": {"nom membre", "cotation livre", "date", "retour"},
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

BDM_Status = {"Membre", "Membre actif", "Membre +", "Membre actif +", "Bureau"}
today = date.today().strftime("%Y/%m/%d")

def parse_date(date_: str | date | datetime | pd.Timestamp,
        default = '"' + today + '"') -> str :
    if type(date_) == pd.Timestamp :
        date_: datetime = date_.date()
    if type(date_) in {date, datetime} :
        return '"' + date_.strftime("%Y/%m/%d") + '"'
    if (type(date_) == str and date_ == "") or pd.isnull(date_) :
        return default
    return '"' + date_ + '"'

def parse_max_loans(line: pd.Series) -> int :
    if line.statut in {"Membre +", "Membre actif +"} :
        return line.caution//8
    elif line.statut == "Bureau" :
        return 20
    else :
        return 0

def parse_status(status: str) -> str :
    if status in BDM_Status :
        return status
    return "Non-membre"


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
    on_error = "IGNORE"
    if replace :
        reset(db, db_name, cursor)
        on_error = "REPLACE"

    logs = []

    t0 = t.time()
    print("started writing")

    # Categories :
    cat_dict = {}
    if not replace :
        cursor.execute("SELECT ")

    if data["categories"].shape[0] > 0 :
        categories = data["series"]["catégorie"].apply(str.lower).unique()

        values = []
        for nb, cat in enumerate(categories) :
            bad = False
            for char in bad_chars :
                if char in cat :
                    logs.append(f"Forbidden character in category {cat} : {char}")
                    bad = True
            
            if bad :
                continue

            cat_dict[cat] = nb
            values.append(f"({nb}, \"{cat}\")")
        cursor.execute(f"""-- sql
            INSERT {on_error}
            INTO Categories
            VALUES ({"), (".join(
                f'{line.code}, "{line.désignation}"'
                for _, line in data["categories"].iterrows()
            )})
        ;""")

        print(f"Categories took {round(t.time()-t0, 3)}s")
    t0 = t.time()

    # Authors :
    query = f"""-- sql
            INSERT {on_error}
            INTO Authors (auth_name)
            VALUES ({"), (".join(
                f'"{line.nom}"'
                for _, line in data["authors"].iterrows()
            )})
        ;"""
    if data["authors"].shape[0] > 0 :
        cursor.execute(query)

        print(f"Authors took {round(t.time()-t0, 3)}s")
    t0 = t.time()

    # Editors :
    if data["editors"].shape[0] > 0 :
        cursor.execute(f"""-- sql
            INSERT {on_error}
            INTO Editors (edit_name)
            VALUES ({"), (".join(
                f'"{line.nom}"'
                for _, line in data["editors"].iterrows()
            )})
        ;""")

        print(f"Editors took {round(t.time()-t0, 3)}s")
    t0 = t.time()

    # Series :
    if data["series"].shape[0] > 0 :
        cursor.execute(f"""-- sql
            INSERT {on_error}
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
        # print(auth_dict)
        cursor.execute(f"""-- sql
            INSERT {on_error}
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
        cursor.execute(f"""-- sql
            INSERT {on_error}
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
    if data["books"].shape[0] > 0 :
        srs_cat_dict = {
            line.identifiant : cat_dict[line.catégorie]
            for _, line in data["series"].iterrows()
        }

        data["books"].rename(columns={
                "identifiant série": "srs",
                "numéro de volume": "vol",
                "numéro de duplicata": "dup",
                "date d'ajout": "date"
            }, inplace=True)
        
        data["books"].fillna(value="", inplace=True)

        cursor.execute(f"""-- sql
            INSERT {on_error}
            INTO Books
            VALUES ({"), (".join(
                '"' + str(srs_cat_dict[line.srs]).rjust(2, '0') + line.srs +
                str(line.vol).rjust(3, '0') + str(line.dup).rjust(2, '0') +
                f'''", "{line.nom}", "{line.srs}", {line.vol}, {line.dup},
                {line.disponible.lower() == "oui"}, {line.condition},
                {parse_date(line.date)},
                "{line.commentaire}"'''
                for _, line in data["books"].iterrows()
            )})
        ;""")

        print(f"Books took {round(t.time()-t0, 3)}s")
    t0 = t.time()

    # Members
    if data["members"].shape[0] > 0 :
        cursor.execute(f"""-- sql
            INSERT {on_error}
            INTO Members (
                member_name, mail, tel,
                max_loans, loan_length, bail,
                status_BDM, status_ALIR,
                comment
            ) VALUES ({"), (".join(
                f'''"{line.nom}", "{line.mail}", "{line.tel}",
                {parse_max_loans(line)}, 30, {line.caution},
                "{parse_status(line.statut)}", "Non-Membre",
                "{line.commentaire}"
                '''
                for _, line in data["members"].iterrows()
            )})
        ;""")
        print(f"Members took {round(t.time()-t0, 3)}s")
    t0 = t.time()

    # Loans
    if data["loans"].shape[0] > 0 :
        cursor.execute("SELECT member_id, member_name FROM Members;")
        user_dict = {
            name: code
            for code, name in cursor.fetchall()
        }

        cursor.execute(f"""-- sql
            INSERT {on_error}
            INTO Loans (
                member_id, book_id,
                loan_start,
                loan_return,
                archived
            ) VALUES ({"), (".join(
                f'''{user_dict[line['nom membre']]},
                "{line['cotation livre']}",
                {parse_date(line.date)},
                {parse_date(line.retour, default='NULL')},
                {not pd.isnull(line.retour)}'''
                for _, line in data["loans"].iterrows()
            )})
        ;""")
        print(f"Loans took {round(t.time()-t0, 3)}s")
    
    db.commit()


def read_db() -> dict[str, pd.DataFrame] :
    data = {
        "categories" : pd.read_sql_query("""-- sql
            SELECT cat_id AS code,
                   cat_name AS `désignation`
            FROM Categories
        ;""", db),
        "authors" : pd.read_sql_query("""-- sql
            SELECT auth_name AS nom
            FROM Authors
        ;""", db),
        "editors" : pd.read_sql_query("""-- sql
            SELECT edit_name AS nom
            FROM Editors
        ;""", db),
        "series" : pd.read_sql_query("""-- sql
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
                SELECT series_id, GROUP_CONCAT(auth_name SEPARATOR '; ') AS auths
                FROM Authors
                NATURAL JOIN `Srs-Auth`
                GROUP BY series_id
            )
            NATURAL JOIN (
                SELECT series_id, GROUP_CONCAT(edit_name SEPARATOR '; ') AS edits
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
                   book_id AS `cotation livre`,
                   loan_start AS `date`,
                   loan_return AS `retour`
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