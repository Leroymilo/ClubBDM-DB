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

def add(id: str, name: str, b_type: str, cat: str,
    auth_ids: list[int], edit_ids: list[int]) :

    cursor.execute(f"""--sql
        SELECT series_id FROM Series
        WHERE series_id = "{id}"
    ;""")
    if cursor.fetchall() != [] :
        return 1
    
    cursor.execute(f"""--sql
        SELECT series_name FROM Series
        WHERE series_name LIKE "{name}"
    ;""")
    if cursor.fetchall() != [] :
        return 2
    
    cursor.execute(f"""--sql
    INSERT INTO Series VALUES (
        '{id}', "{name}", '{b_type}', {cat}
    )
    ;""")
    
    for auth_id in auth_ids :
        cursor.execute(f"""--sql
            INSERT INTO `Srs-Auth` VALUES ('{id}', {auth_id})
        ;""")
    
    for edit_id in edit_ids :
        cursor.execute(f"""--sql
            INSERT INTO `Srs-Edit` VALUES ('{id}', {edit_id})
        ;""")

    db.commit()
    return 0

def get_item_data(series_id: str) :
    cursor.execute(f"""--sql
        SELECT series_name, book_type, cat_name
        FROM Series
        JOIN Categories
            ON book_category = cat_id
        WHERE series_id = "{series_id}"
    ;""")
    values = cursor.fetchone()
    keys = ("series_name", "book_type", "book_cat")

    cursor.execute(f"""--sql
        SELECT auth_name
        FROM Authors
        JOIN `Srs-Auth` USING (auth_id)
        WHERE series_id = "{series_id}"
    ;""")
    authors = tuple(auth for auth, in cursor.fetchall())

    cursor.execute(f"""--sql
        SELECT edit_name
        FROM Editors
        JOIN `Srs-Edit` USING (edit_id)
        WHERE series_id = "{series_id}"
    ;""")
    editors = tuple(edit for edit, in cursor.fetchall())

    cursor.execute(f"""--sql
        SELECT book_id FROM Books
        WHERE series_id = "{series_id}"
    ;""")
    has_books = (cursor.fetchall() != [])

    return {keys[i]: values[i] for i in range(3)} |\
        {"authors": authors, "editors": editors, "has_books": has_books}

def edit(id: str, name: str, b_type: str, cat: str,
    auth_ids: list[int], edit_ids: list[int]) :
    
    cursor.execute(f"""--sql
        SELECT series_name FROM Series
        WHERE series_name LIKE "{name}"
        AND series_id != "{id}"
    ;""")
    if cursor.fetchall() != [] :
        return 1
    
    cursor.execute(f"""--sql
    UPDATE Series
    SET
        series_name = "{name}",
        book_type = '{b_type}',
        book_category = {cat}
    WHERE series_id = "{id}"
    ;""")
    
    cursor.execute(f"""--sql
        DELETE FROM `Srs-Auth`
        WHERE series_id = "{id}"
    ;""")
    for auth_id in auth_ids :
        cursor.execute(f"""--sql
            INSERT INTO `Srs-Auth` VALUES ('{id}', {auth_id})
        ;""")
    
    cursor.execute(f"""--sql
        DELETE FROM `Srs-Edit`
        WHERE series_id = "{id}"
    ;""")
    for edit_id in edit_ids :
        cursor.execute(f"""--sql
            INSERT INTO `Srs-Edit` VALUES ('{id}', {edit_id})
        ;""")

    db.commit()
    return 0