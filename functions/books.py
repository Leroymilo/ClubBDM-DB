from db_init import *

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