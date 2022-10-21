from db_init import *

def select(filter_: Union[None, Tuple[str]] = None) -> np.array :
    base_query = """
        SELECT member_name,
            mail,
            tel,
            IF(loan_c IS NULL, "0", loan_c) || "/" || max_loans,
            loan_length || " jours",
            bail,
            IF(status_BDM IS NULL, "", status_BDM),
            IF(status_ALIR IS NULL, "", status_ALIR),
            last_loan,
            IF(archived, "Oui", "Non"),
            comment
        FROM Members
        LEFT JOIN (
            SELECT member_id, COUNT(*) AS loan_c
            FROM Loans
            WHERE NOT archived
            GROUP BY member_id
        ) USING (member_id)
    """

    if filter_ is None :
        cursor.execute(base_query)
    
    elif filter_[0] == "Name" :
        cursor.execute(base_query + f"""
            WHERE member_name LIKE "%{filter_[1]}%"
        """)
    
    elif filter_[0] == "Status" :
        cursor.execute(base_query + f"""
            WHERE status_BDM LIKE "%{filter_[1]}%"
            OR status_ALIR LIKE "%{filter_[1]}%"
        """)
    
    return np.asarray(cursor.fetchall())

def add(name: str, mail: str, tel: str, max_loans: int, loan_len: int,
    bail: float, BDM: str, ALIR: str, comment: str) :

    cursor.execute(f"""--sql
        SELECT member_id FROM Members
        WHERE member_name LIKE "{name}"
    ;""")
    if cursor.fetchall() != [] :
        return 1
    
    cursor.execute(f"""--sql
        INSERT INTO Members (
            member_name, mail, tel,
            max_loans, loan_length, bail,
            status_BDM, status_ALIR,
            comment
        ) VALUES (
            "{name}", "{mail}", "{tel}",
            {max_loans}, {loan_len}, {bail},
            "{BDM}", "{ALIR}",
            "{comment}"
        )
    ;""")

    db.commit()
    return 0

def get_item_data(item_name: str) :
    cursor.execute(f"""--sql
        SELECT member_id, mail, tel, bail,
            status_BDM, status_ALIR, comment
        FROM Members
        WHERE member_name = "{item_name}"
    ;""")
    values = cursor.fetchone()
    keys = ("id", "mail", "tel", "bail", "BDM", "ALIR", "comment")

    return {keys[i]: values[i] for i in range(7)}

def edit(member_id: int, name: str, mail: str, tel: str, max_loans: int,
    loan_len: int, bail: float, BDM: str, ALIR: str, comment: str) :

    pass