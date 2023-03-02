from db_init import *
from db_reset import reset

import re
import pandas as pd
from datetime import date, datetime
import time as t


Cols = {
    "series": {"identifiant", "nom", "type", "catégorie", "auteurs", "éditeurs"},
    "books": {
        "nom", "identifiant série",
        "numéro de volume", "numéro d'exemplaire", "disponible",
        "condition", "date d'ajout", "commentaire"
    },
    "members": {"nom", "mail", "tel", "statut", "caution", "commentaire"},
    "loans": {"nom membre", "cotation livre", "date", "retour"}
}

Sheets = {
    "series": "Séries",
    "books": "Livres",
    "members": "Membres",
    "loans": "Emprunts",
}

bad_chars = {'"', ';'}
mail_pattern = "^\w+([\.-]?\w+)*@\w+([-]?\w+)*(\.\w{2,3})+$"
tel_pattern = "^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
BDM_Status = {"Membre", "Membre actif", "Membre +", "Membre actif +", "Bureau", "Non-membre"}
today = date.today().strftime("%Y-%m-%d")


def parse_date(date_: str | date | datetime | pd.Timestamp,
        default = today) -> str :
    if type(date_) == pd.Timestamp :
        date_: datetime = date_.date()
    if type(date_) in {date, datetime} :
        return date_.strftime("%Y-%m-%d")
    if (type(date_) == str and date_ == "") or pd.isnull(date_) :
        return default
    if type(date_) == str :
        return date_
    return None

def parse_tel(tel: str | float) :
    if type(tel) == float :
        try :
            tel = round(tel)
        except ValueError :
            return ""
    if type(tel) == int :
        tel = str(tel)
    
    if len(tel) == 10 and tel[0] == '0' :
        tel = tel[1:]
    if len(tel) == 9 :
        return "+33" + tel
    
    if len(tel) == 11 :
        return '+' + tel
    return tel

def parse_max_loans(statut: str, caution: int) -> int :
    if statut in {"Membre +", "Membre actif +"} :
        return caution//8
    elif statut == "Bureau" :
        return 20
    else :
        return 0

def parse_status(status: str) -> str :
    if status in BDM_Status :
        return status
    return None


def read_xlsx(directory: str) -> dict[str, pd.DataFrame] :
    data = {
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


def write_db(data: dict[str, pd.DataFrame], replace = False) -> list[str] :
    if replace :
        reset()

    logs = []

    print("started writing")

    # Categories :
    
    logs.append("==Catégories==")

    if not replace :
        cursor.execute("SELECT cat_id, cat_name FROM Categories;")
        cat_dict = {name: id_ for id_, name in cursor.fetchall()}
        start = max(cat_dict.values()) + 1
    else :
        cat_dict = {}
        start = 1

    if data["series"].shape[0] > 0 :
        t0 = t.time()
        categories = data["series"]["catégorie"].apply(str.lower).unique()

        values = []
        for i, cat in enumerate(categories) :
            cat = cat.strip().lower()
            
            if cat == "" :
                continue

            if cat in cat_dict :
                continue

            bad = False
            for char in bad_chars :
                if char in cat :
                    logs.append(f"Charactère interdit pour la catégorie '{cat}' : {char} (ligne {i}).")
                    bad = True
            
            if bad :
                continue

            cat_dict[cat] = i+start
            values.append(f"({i+start}, \"{cat}\")")
        
        if values :
            cursor.execute(f"""-- sql
                INSERT
                INTO Categories
                VALUES {", ".join(values)};
            """)

        print(f"Categories took {round(t.time()-t0, 3)}s")

    # Authors :
    
    logs.append("==Auteurs==")

    if not replace :
        cursor.execute("SELECT auth_id, auth_name FROM Authors;")
        auth_dict = {name: id_ for id_, name in cursor.fetchall()}
        nb = max(cat_dict.values()) + 1
    else :
        auth_dict = {}
        nb = 1
    
    if data["series"].shape[0] > 0 :
        t0 = t.time()
        srs_authors = data["series"][["identifiant", "auteurs"]]

        srs_auth = {}
        values = []
        for _, line in srs_authors.iterrows() :
            if line["auteurs"].strip() == "" :
                continue

            authors = [author.strip() for author in line["auteurs"].split(";")]
            author_ids = []
            for author in authors :
                if author not in auth_dict :
                    auth_dict[author] = nb
                    values.append(f"({nb}, \"{author}\")")
                    nb += 1
                author_ids.append(auth_dict[author])
            srs_auth[line["identifiant"]] = author_ids.copy()

        if values :
            cursor.execute(f"""-- sql
                INSERT
                INTO Authors
                VALUES {", ".join(values)};
            """)

        print(f"Authors took {round(t.time()-t0, 3)}s")

    # Editors :
    
    logs.append("==Éditeurs==")

    if not replace :
        cursor.execute("SELECT edit_id, edit_name FROM Editors;")
        edit_dict = {name: id_ for id_, name in cursor.fetchall()}
        nb = max(cat_dict.values()) + 1
    else :
        edit_dict = {}
        nb = 1
    
    if data["series"].shape[0] > 0 :
        t0 = t.time()
        srs_editors = data["series"][["identifiant", "éditeurs"]]

        srs_edit = {}
        values = []
        for _, line in srs_editors.iterrows() :
            if line["éditeurs"].strip() == "" :
                continue

            editors = [editor.strip() for editor in line["éditeurs"].split(";")]
            editor_ids = []
            for editor in editors :
                if editor not in edit_dict :
                    edit_dict[editor] = nb
                    values.append(f"({nb}, \"{editor}\")")
                    nb += 1
                editor_ids.append(edit_dict[editor])
            srs_edit[line["identifiant"]] = editor_ids.copy()

        if values :
            cursor.execute(f"""-- sql
                INSERT
                INTO Editors
                VALUES {", ".join(values)};
            """)

        print(f"Editors took {round(t.time()-t0, 3)}s")

    # Series :
    
    logs.append("==Séries==")

    if not replace :
        cursor.execute("SELECT series_id, series_name FROM Series;")
        srs_ids = {id_: name for id_, name in cursor.fetchall()}
    else :
        srs_ids = {}
    
    if data["series"].shape[0] > 0 :
        t0 = t.time()

        values = []
        auth_values = []
        edit_values = []
        series_cat_dict = {}

        for i, line in data["series"].iterrows() :

            srs_id: str = line.identifiant.strip().upper()
            if len(srs_id) != 5 or not srs_id.isalnum() :
                logs.append(f"ID de la série '{line.nom}' invalide : {srs_id} (ligne {i}).")
                logs.append(f"Les IDs de séries doivent être uniques et composés de 5 lettres et/ou chiffres.")
                continue
                
            if srs_id in srs_ids.keys() :
                logs.append(f"ID de série '{srs_id}' déjà utilisé par '{srs_ids[srs_id]}', (ligne {i} ignorée).")
                continue

            srs_name = line.nom.strip()
            bad = False
            for char in bad_chars :
                if char in srs_name :
                    logs.append(f"Charactère interdit pour la série '{line.nom}' : {char} (ligne {i}).")
                    bad = True
            if bad :
                continue

            srs_type = line.type.strip().lower()
            if srs_type not in {"bd", "comics", "manga", "roman"} :
                logs.append(f"Type de livre de la série {line.nom} inconnu : {line.type} (ligne {i}).")
                continue

            srs_cat = line["catégorie"].strip().lower()
            if srs_cat not in cat_dict.keys() :
                logs.append(f"Catégorie de la série {line.nom} inconnu : {line['catégorie']} (ligne {i}).")
                continue
            srs_cat = cat_dict[srs_cat]
        
            values.append(f"(\"{srs_id}\", \"{srs_name}\", \"{srs_type}\", {srs_cat})")
            srs_ids[srs_id] = srs_name
            series_cat_dict[srs_id] = srs_cat

            if srs_id in srs_auth :
                for auth_id in srs_auth[srs_id] :
                    auth_values.append(f"(\"{srs_id}\", {auth_id})")

            if srs_id in srs_edit :
                for edit_id in srs_edit[srs_id] :
                    edit_values.append(f"(\"{srs_id}\", {edit_id})")
            
        if values :
            cursor.execute(f"""-- sql
                INSERT
                INTO Series
                VALUES {", ".join(values)};
            """)

        if auth_values :
            cursor.execute(f"""-- sql
                INSERT
                INTO `Srs-Auth`
                VALUES {", ".join(auth_values)};
            """)
        if edit_values :
            cursor.execute(f"""-- sql
                INSERT
                INTO `Srs-Edit`
                VALUES {", ".join(edit_values)};
            """)

        print(f"Series took {round(t.time()-t0, 3)}s")

    # Books
    
    logs.append("==Livres==")

    if not replace :
        cursor.execute("SELECT book_id, book_name FROM Books;")
        book_ids = {id_: name for id_, name in cursor.fetchall()}
    else :
        book_ids = {}

    if data["books"].shape[0] > 0 :
        t0 = t.time()

        data["books"].rename(columns={
                "identifiant série": "srs",
                "numéro de volume": "vol",
                "numéro d'exemplaire": "dup",
                "date d'ajout": "date"
            }, inplace=True)
        
        data["books"].fillna(value="", inplace=True)

        values = []

        for i, line in data["books"].iterrows() :
            book_srs = line.srs.strip().upper()
            if book_srs not in series_cat_dict :
                logs.append(f"Série du livre '{line.nom}' inconnue : {line.srs} (ligne {i}).")
                continue

            if line.vol <= 0 :
                logs.append(f"Numéro du livre '{line.vol}' négatif ou nul (ligne {i}).")
                continue
        
            if line.dup <= 0 :
                logs.append(f"Numéro d'exemplaire du livre '{line.vol}' négatif ou nul (ligne {i}).")
                continue

            book_id = str(series_cat_dict[line.srs]).rjust(2, '0')
            book_id += book_srs + str(line.vol).rjust(3, '0')
            book_id += str(line.dup).rjust(2, '0')

            if book_id in book_ids.keys() :
                logs.append(f"ID '{book_id}' (calculé pour le livre '{line.nom}') déjà utilisé par '{book_ids[book_id]}', (ligne {i} ignorée).")
                continue

            book_name = line.nom.strip()
            bad = False
            for char in bad_chars :
                if char in book_name :
                    logs.append(f"Charactère interdit pour le livre '{line.nom}' : {char} (ligne {i}).")
                    bad = True
            if bad :
                continue

            dispo = (line.disponible.strip().lower() == "oui")

            if not 0 < line.condition < 11 :
                logs.append(f"Condition du livre '{line.nom}' invalide (ligne {i}), ce doit être une note entre 1 et 10 compris.")
                continue

            add_date = parse_date(line.date)
            if add_date is None :
                logs.append(f"Format de date non reconnu ligne {i}, bonne chance avec Excel...")
                continue

            com = line.commentaire.strip()
            bad = False
            for char in bad_chars :
                if char in com :
                    logs.append(f"Charactère interdit dans le commentaire du livre '{line.nom}' : {char} (ligne {i}).")
                    bad = True
            if bad :
                continue
            
            value = f"(\"{book_id}\", \"{book_name}\", \"{book_srs}\", {line.vol}, "
            value += f"{line.dup}, {dispo}, {line.condition}, '{add_date}', \"{com}\")"
            values.append(value)
            book_ids[book_id] = book_name
        
        if values :
            cursor.execute(f"""-- sql
                INSERT
                INTO Books
                VALUES {", ".join(values)};
            """)

        print(f"Books took {round(t.time()-t0, 3)}s")

    # Members
    
    logs.append("==Membres==")

    if not replace :
        cursor.execute("SELECT member_id, member_name FROM Members;")
        member_names = {name: id_ for id_, name in cursor.fetchall()}
        nb = max(member_names.keys()) + 1
    else :
        member_names = {}
        nb = 1

    if data["members"].shape[0] > 0 :
        t0 = t.time()

        values = []

        for i, line in data["members"].iterrows() :

            name = line.nom.strip()
            bad = False
            for char in bad_chars :
                if char in name :
                    logs.append(f"Charactère interdit dans le nom '{line.nom}' : {char} (ligne {i}).")
                    bad = True
            if bad :
                continue

            if name in member_names.keys() :
                logs.append(f"Un membre du nom de '{name}' existe déjà (ligne {i} ignorée).")
                continue
            
            mail = line.mail.strip().lower()
            if not re.match(mail_pattern, mail) :
                logs.append(f"Adresse mail de '{line.nom}' invalide : {line.mail} (ligne {i}).")
                continue

            tel = parse_tel(line.tel).strip()
            if tel != "" and not re.match(tel_pattern, tel) :
                logs.append(f"Numéro de téléphone de '{line.nom}' invalide : {line.tel} (ligne {i}).")
                continue

            status_BDM = parse_status(line.statut.strip())
            if status_BDM is None :
                logs.append(f"Statut de '{line.nom}' invalide : '{line.statut}' (ligne {i}).")
                logs.append(f"Les statuts possibles sont : {', '.join(BDM_Status)}.")
                continue

            com = line.commentaire
            if type(com) != str :
                com = ""

            else :
                com = com.strip()
                bad = False
                for char in bad_chars :
                    if char in com :
                        logs.append(f"Charactère interdit dans le commentaire du membre '{line.nom}' : {char} (ligne {i}).")
                        bad = True
                if bad :
                    continue

            value = f"({nb}, \"{name}\", \"{mail}\", '{tel}', "
            value += f"{parse_max_loans(status_BDM, line.caution)}, 30, "
            value += f"{line.caution}, '{status_BDM}', 'Non-membre', \"{com}\")"
            values.append(value)
            member_names[name] = nb
            nb += 1

        if values :
            cursor.execute(f"""-- sql
                INSERT INTO Members (
                    member_id, member_name, mail, tel,
                    max_loans, loan_length, bail,
                    status_BDM, status_ALIR,
                    `comment`
                ) VALUES {", ".join(values)};
            """)

        print(f"Members took {round(t.time()-t0, 3)}s")

    # Loans
    
    logs.append("==Emprunts==")

    if data["loans"].shape[0] > 0 :
        t0 = t.time()

        values = []

        for i, line in data["loans"].iterrows() :
            mem_name = line["nom membre"]
            if mem_name not in member_names.keys() :
                logs.append(f"Le membre '{line['nom membre']}' n'existe pas (ligne {i}).")
                continue
            mem_id = member_names[mem_name]
            
            book_id = line["cotation livre"][2:]
            for cat_id in cat_dict.values() :
                full_book_id = str(cat_id).rjust(2, '0') + book_id
                if full_book_id in book_ids.keys() :
                    break
            else :
                logs.append(f"Le livre avec l'ID '{book_id}' n'existe pas (ligne {i}).")
                continue

            date_emp = parse_date(line.date)
            if date_emp is None :
                logs.append(f"Format de date d'emprunt non reconnu ligne {i}, bonne chance avec Excel...")
                continue

            date_retour = parse_date(line.retour, default="NULL")
            if date_retour is None :
                logs.append(f"Format de date de retour non reconnu ligne {i}, bonne chance avec Excel...")
                continue
            if date_retour != "NULL" :
                date_retour = '\'' + date_retour + '\''

            arch = (date_retour != "NULL")
            
            value = f"({mem_id}, '{full_book_id}', '{date_emp}', {date_retour}, {arch})"
            values.append(value)

        if values :
            cursor.execute(f"""-- sql
                INSERT INTO Loans (
                    member_id, book_id,
                    loan_start,
                    loan_return,
                    archived
                ) VALUES {", ".join(values)};
            """)

        print(f"Loans took {round(t.time()-t0, 3)}s")
    
    db.commit()

    logs.append("Fini !")

    return logs


def read_db() -> dict[str, pd.DataFrame] :
    data = {
        "series" : pd.read_sql_query("""-- sql
            SELECT series_id AS identifiant,
                   series_name AS nom,
                   book_type AS type,
                   cat_name AS catégorie,
                   auths AS auteurs,
                   edits AS éditeurs
            FROM Series AS ser
            JOIN Categories AS cat
                ON book_category = cat_id
            NATURAL JOIN (
                SELECT series_id, GROUP_CONCAT(auth_name SEPARATOR ', ') AS auths
                FROM Authors
                NATURAL JOIN `Srs-Auth`
                GROUP BY series_id
            ) AS auth
            NATURAL JOIN (
                SELECT series_id, GROUP_CONCAT(edit_name SEPARATOR ', ') AS edits
                FROM Editors
                NATURAL JOIN `Srs-Edit`
                GROUP BY series_id
            ) AS edit;""", db.db),
        "books" : pd.read_sql_query("""-- sql
            SELECT book_id AS `cotation (sera recalculée)`,
                   book_name AS nom,
                   series_id AS `identifiant série`,
                   vol_nb AS `numéro de volume`,
                   dup_nb AS `numéro d'exemplaire`,
                   IF(available, 'Oui', 'Non') AS `disponible`,
                   `condition`,
                   creation_date AS `date d'ajout`,
                   comment AS commentaire
            FROM Books
        ;""", db.db),
        "members": pd.read_sql_query("""-- sql
            SELECT member_name AS nom,
                   mail, tel,
                   status_BDM AS statut,
                   bail AS caution,
                   comment AS commentaire
            FROM Members
        ;""", db.db),
        "loans": pd.read_sql_query("""-- sql
            SELECT member_name AS `nom membre`,
                   book_id AS `cotation livre`,
                   loan_start AS `date`,
                   loan_return AS `retour`
            FROM Loans AS l
            JOIN Members AS m
                USING (member_id)
        ;""", db.db)
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