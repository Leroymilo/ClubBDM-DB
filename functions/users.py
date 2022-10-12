from db_init import *

archived = False

def select(filter_: Union[None, Tuple[str]] = None) -> np.array :
    base_query = """--sql
        SELECT user_name,
            mail,
            tel,
            loan_c || '/' || max_loans,
            loan_length || " jours",
            "BDM : " || status_BDM || ";" || "ALIR : " || status_ALIR,
            comment
        FROM Users
        NATURAL JOIN (
            SELECT user_id, COUNT(*) AS loan_c
            FROM Loans
            WHERE NOT archived
            GROUP BY user_id
        )
    ;"""

    cursor.execute(base_query)
    return np.asarray(cursor.fetchall())