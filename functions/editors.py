from db_init import *

def add(name: str) :
    cursor.execute(f"""-- sql
        SELECT edit_id FROM Editors
        WHERE edit_name LIKE "{name}"
    ;""")
    if cursor.fetchall() != [] :
        return 1
    
    cursor.execute(f"""-- sql
        INSERT INTO Editors (edit_name) VALUES ("{name}")
    ;""")
    db.commit()
    return 0