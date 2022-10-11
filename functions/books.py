from db_init import *

def select(filter: Union[None, Tuple[str]] = None) -> np.array :
    if filter is None :
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
    
    elif filter[0] == "series" :
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
            WHERE series_name LIKE '%{filter[1]}%'
        ) USING (series_id)
        ;""")
    
    elif filter[0] == "author" :
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
            JOIN `Srs-Auth`
            JOIN (
                SELECT auth_id
                FROM Authors
                WHERE auth_name LIKE '%{filter[1]}%'
            )
        ) USING (series_id)
        ;""")
    
    return cursor.fetchall()
