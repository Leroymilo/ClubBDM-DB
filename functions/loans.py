from datetime import timedelta, date

from db_init import *

def select(filter_: tuple[str] | None = None) -> np.array :
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

    return {el for el, in cursor.fetchall()}

def add(member_id: int, book_id: str) :
    cursor.execute(f"""--sql
        UPDATE Books
        SET available = FALSE
        WHERE book_id = "{book_id}"
    ;""")

    cursor.execute(f"""--sql
        UPDATE Members
        SET last_loan = DATE(), archived = FALSE
        WHERE member_id = "{member_id}"
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

def get_item_data(item_id: tuple[str]) :
    cursor.execute(f"""--sql
        SELECT loan_id, member_id, loan_start, late_return
        FROM Loans JOIN Members USING (member_id)
        WHERE member_name = "{item_id[0]}"
        AND book_id = "{item_id[1]}"
        AND NOT Loans.archived
    ;""")
    values = cursor.fetchone()
    keys = ("loan_id", "member_id", "loan_start", "due_date")

    return {keys[i]: values[i] for i in range(4)}

def edit(item_id: int, member_id: int, book_id: str) :
    cursor.execute(f"""--sql
        SELECT book_id
        FROM Loans WHERE loan_id = {item_id}
    ;""")
    old_book_id, = cursor.fetchone()

    if old_book_id != book_id :
        cursor.execute(f"""--sql
            UPDATE Books
            SET available = TRUE
            WHERE book_id = "{old_book_id}"
        ;""")
        cursor.execute(f"""--sql
            UPDATE Books
            SET available = FALSE
            WHERE book_id = "{book_id}"
        ;""")
    
    cursor.execute(f"""--sql
        UPDATE Loans
        SET member_id = {member_id}, book_id = "{book_id}"
        WHERE loan_id = {item_id}
    ;""")

    db.commit()
    return 0

def end(member_name: str, book_id: str) :
    cursor.execute(f"SELECT member_id FROM Members WHERE member_name = \"{member_name}\"")
    member_id, = cursor.fetchone()

    cursor.execute("""--sql
        UPDATE Loans
        SET loan_return = DATE(), archived = TRUE
        WHERE member_id = "{member_id}"
        AND book_id = "{book_id}"
        AND archived = False
    ;""")

    cursor.execute(f"""--sql
        UPDATE Books
        SET available = TRUE
        WHERE book_id = "{book_id}"
    ;""")

    cursor.execute(f"""--sql
        UPDATE Members
        SET last_loan = DATE(), archived = FALSE
        WHERE member_id = "{member_id}"
    ;""")

    db.commit()
    return 0