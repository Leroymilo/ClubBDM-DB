from datetime import timedelta, date

from db_init import *

def select(filter_: Union[None, Tuple[str]] = None) -> np.array :
    base_query = """
        SELECT member_name,
            book_id,
            loan_start,
            late_return,
            loan_return
        FROM Loans
        JOIN Members USING (member_id)
    """

    if filter_ is None :
        cursor.execute(base_query)
    
    elif filter_[0] == "Member" :
        cursor.execute(base_query + f"""
            WHERE member_name LIKE "%{filter_[1]}%"
        """)
    
    elif filter_[0] == "Book" :
        cursor.execute(base_query + f"""
            WHERE book_id LIKE "%{filter_[1]}%"
        """)
    
    return np.asarray(cursor.fetchall())

def get_members() :
    cursor.execute("""--sql
        SELECT member_id, member_name
        FROM Members
        LEFT JOIN (
            SELECT member_id, COUNT(*) as nb_loans
            FROM Loans
            GROUP BY member_id
        ) USING (member_id)
        WHERE nb_loans IS NULL
        OR max_loans > nb_loans
    ;""")

    return {el[1]: el[0] for el in cursor.fetchall()}

def get_books() :
    cursor.execute("""--sql
        SELECT book_id
        FROM Books
        WHERE available
    ;""")

    return [el for el, in cursor.fetchall()]

def add(member_id: int, book_id: str) :
    cursor.execute(f"""--sql
        UPDATE Books
        SET available = FALSE
        WHERE book_id = "{book_id}"
    ;""")

    cursor.execute(f"""--sql
        SELECT loan_length FROM Members
        WHERE member_id = {member_id}
    ;""")
    loan_length, = cursor.fetchone()
    start = date.today()
    end = start + timedelta(days=loan_length)

    cursor.execute(f"""--sql
        INSERT INTO Loans (
            member_id, book_id, loan_start, late_return
        ) VALUES (
            {member_id}, "{book_id}", "{start.strftime('%Y/%m/%d')}", "{end.strftime('%Y/%m/%d')}"
        )
    ;""")

    db.commit()
    return 0

def get_item_data() :
    pass

def edit(item_id: int, member_id: int, book_id: str) :
    pass