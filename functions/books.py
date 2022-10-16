from db_init import *
from datetime import date

def select(filter_: Union[None, Tuple[str]] = None) -> np.array :
    base_query = """
        SELECT book_id,
            book_name,
            series_name,
            LPAD(vol_nb, '0', 3),
            IF(
                condition IS NULL,
                '',
                LPAD(condition, '0', 2) || '/10'
            ),
            IF(available, 'Oui', 'Non'),
            IF(added_on IS NULL, '', added_on),
            comment
        FROM Books
    """

    if filter_ is None :
        cursor.execute(base_query + """
            NATURAL JOIN Series
        ;""")
    
    elif filter_[0] == "Series" :
        cursor.execute(base_query + f"""
            NATURAL JOIN (
                SELECT series_id, series_name
                FROM Series
                WHERE series_name LIKE '%{filter_[1]}%'
            )
        ;""")
    
    elif filter_[0] == "Author" :
        cursor.execute(base_query + f"""
            NATURAL JOIN (
                SELECT s.series_id, series_name
                FROM Series AS s
                NATURAL JOIN `Srs-Auth`
                NATURAL JOIN (
                    SELECT auth_id
                    FROM Authors
                    WHERE auth_name LIKE '%{filter_[1]}%'
                )
            )
        ;""")
    
    elif filter_[0] == "Editor" :
        cursor.execute(base_query + f"""
            NATURAL JOIN (
                SELECT s.series_id, series_name
                FROM Series AS s
                NATURAL JOIN `Srs-Edit`
                NATURAL JOIN (
                    SELECT edit_id
                    FROM Editors
                    WHERE edit_name LIKE '%{filter_[1]}%'
                )
            )
        ;""")
    
    return np.asarray(cursor.fetchall())

def get_series() :
    cursor.execute("""--sql
        SELECT series_id, series_name FROM Series
    ;""")

    return {el[1]: el[0] for el in cursor.fetchall()}

def add(series_id: str, vol_nb: int, cond: int, vol_name: str, comment: str) :
    cursor.execute(f"""--sql
        SELECT book_category FROM Series
        WHERE series_id = "{series_id}"
    ;""")
    cat_id, = cursor.fetchone()

    cursor.execute(f"""--sql
        SELECT COUNT(book_id) FROM Books
        WHERE series_id = "{series_id}"
        AND vol_nb = {vol_nb}
    ;""")
    dup_nb = cursor.fetchone()[0] + 1

    book_id = str(cat_id).rjust(2, '0') + series_id +\
        str(vol_nb).rjust(3, '0') + str(dup_nb).rjust(2, '0')

    cursor.execute(f"""--sql
    INSERT INTO Books (
        book_id, book_name, series_id, vol_nb,
        dup_nb, condition, added_on, comment
    ) Values (
        "{book_id}", "{vol_name}", "{series_id}", {vol_nb},
        {dup_nb}, {cond}, "{date.today().strftime("%Y-%m-%d")}", "{comment}"
    )
    ;""")
    db.commit()
    return book_id
