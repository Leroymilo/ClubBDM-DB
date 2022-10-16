from db_init import *

def select(filter_: Union[None, Tuple[str]] = None) -> np.array :
    authors = """
        SELECT series_id, CONCAT('; ', auth_name) AS auths
        FROM Authors
        NATURAL JOIN `Srs-Auth`
        GROUP BY series_id
    """

    editors = """
        SELECT series_id, CONCAT('; ', edit_name) AS edits
        FROM Editors
        NATURAL JOIN `Srs-Edit`
        GROUP BY series_id
    """

    base_query = """
        SELECT series_id,
            series_name,
            book_type,
            cat_name,
            auths,
            edits
        FROM Series
    """

    if filter_ is None :
        cursor.execute(base_query + f"""
            NATURAL JOIN ({authors})
            NATURAL JOIN ({editors})
            JOIN Categories
                ON book_category = cat_id
        ;""")
    
    elif filter_[0] == "Name" :
        cursor.execute(base_query + f"""
            NATURAL JOIN ({authors})
            NATURAL JOIN ({editors})
            JOIN Categories
                ON book_category = cat_id
            WHERE series_name LIKE '%{filter_[1]}%'
        ;""")
    
    elif filter_[0] == "Type" :
        cursor.execute(base_query + f"""
            NATURAL JOIN ({authors})
            NATURAL JOIN ({editors})
            JOIN Categories
                ON book_category = cat_id
            WHERE book_type = '{filter_[1].lower().strip()}'
        ;""")
    
    elif filter_[0] == "Category" :
        cursor.execute(base_query + f"""
            NATURAL JOIN ({authors})
            NATURAL JOIN ({editors})
            JOIN Categories
                ON book_category = cat_id
            WHERE cat_name LIKE '%{filter_[1]}%'
        ;""")
    
    else :
        if filter_[0] == "Author" :
            authors = f"""
                SELECT series_id, CONCAT('; ', auth_name) AS auths
                FROM (
                    SELECT * FROM Authors
                    WHERE auth_name LIKE '%{filter_[1]}%'
                )
                NATURAL JOIN `Srs-Auth`
                GROUP BY series_id
            """
        
        elif filter_[0] == "Editor" :
            editors = f"""
                SELECT series_id, CONCAT('; ', edit_name) AS edits
                FROM (
                    SELECT * FROM Editors
                    WHERE edit_name LIKE '%{filter_[1]}%'
                )
                NATURAL JOIN `Srs-Edit`
                GROUP BY series_id
            """

        cursor.execute(base_query + f"""
            NATURAL JOIN ({authors})
            NATURAL JOIN ({editors})
            JOIN Categories
                ON book_category = cat_id
        ;""")
    
    return np.asarray(cursor.fetchall())

def get_categories() :
    cursor.execute("""--sql
        SELECT cat_id, cat_name FROM Categories
    ;""")

    return {el[1]: el[0] for el in cursor.fetchall()}

def get_auths() :
    cursor.execute("""--sql
        SELECT auth_id, auth_name FROM Authors
    ;""")

    return {el[1]: el[0] for el in cursor.fetchall()}

def get_edits() :
    cursor.execute("""--sql
        SELECT edit_id, edit_name FROM Editors
    ;""")

    return {el[1]: el[0] for el in cursor.fetchall()}