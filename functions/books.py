from db_init import *

def select(filter_: Union[None, Tuple[str]] = None) -> np.array :
    if filter_ is None :
        cursor.execute("""--sql
        SELECT book_id,
               book_name,
               vol_nb,
               series_name,
               condition,
               available,
               added_on,
               comment
        FROM Books
        JOIN Series USING (series_id)
        ;""")
    
    elif filter_[0] == "Series" :
        cursor.execute(f"""--sql
        SELECT book_id,
               book_name,
               vol_nb,
               series_name,
               condition,
               available,
               added_on,
               comment
        FROM Books
        JOIN (
            SELECT series_id, series_name
            FROM Series
            WHERE series_name LIKE '%{filter_[1]}%'
        ) USING (series_id)
        ;""")
    
    elif filter_[0] == "Author" :
        cursor.execute(f"""--sql
        SELECT book_id,
               book_name,
               vol_nb,
               series_name,
               condition,
               available,
               added_on,
               comment
        FROM Books
        JOIN (
            SELECT series_id, series_name
            FROM Series
            NATURAL JOIN `Srs-Auth`
            NATURAL JOIN (
                SELECT auth_id
                FROM Authors
                WHERE auth_name LIKE '%{filter_[1]}%'
            )
        ) USING (series_id)
        ;""")
    
    elif filter_[0] == "Editor" :
        cursor.execute(f"""--sql
        SELECT book_id,
               book_name,
               vol_nb,
               series_name,
               condition,
               available,
               added_on,
               comment
        FROM Books
        JOIN (
            SELECT series_id, series_name
            FROM Series
            NATURAL JOIN `Srs-Edit`
            NATURAL JOIN (
                SELECT edit_id
                FROM Editors
                WHERE edit_name LIKE '%{filter_[1]}%'
            )
        ) USING (series_id)
        ;""")
    
    return cursor.fetchall()
