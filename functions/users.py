from db_init import *

def select(filter_: Union[None, Tuple[str]] = None) -> np.array :
    base_query = """
        SELECT user_name,
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
        FROM Users
        LEFT JOIN (
            SELECT user_id, COUNT(*) AS loan_c
            FROM Loans
            WHERE NOT archived
            GROUP BY user_id
        ) USING (user_id)
    """

    if filter_ is None :
        cursor.execute(base_query)
    
    elif filter_[0] == "Name" :
        cursor.execute(base_query + f"""
            WHERE user_name LIKE "%{filter_[1]}%"
        """)
    
    elif filter_[0] == "Status" :
        cursor.execute(base_query + f"""
            WHERE status_BDM LIKE "%{filter_[1]}%"
            OR status_ALIR LIKE "%{filter_[1]}%"
        """)
    
    return np.asarray(cursor.fetchall())