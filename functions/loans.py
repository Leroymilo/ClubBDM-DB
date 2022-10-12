from db_init import *

def select(filter_: Union[None, Tuple[str]] = None) -> np.array :
    base_query = """
        SELECT user_name,
            book_id,
            loan_start,
            late_return,
            loan_return
        FROM Loans
        JOIN Users USING (user_id)
    """

    if filter_ is None :
        cursor.execute(base_query)
    
    elif filter_[0] == "User" :
        cursor.execute(base_query + f"""
            WHERE user_name LIKE "%{filter_[1]}%"
        """)
    
    elif filter_[0] == "Book" :
        cursor.execute(base_query + f"""
            WHERE book_id LIKE "%{filter_[1]}%"
        """)
    
    return np.asarray(cursor.fetchall())