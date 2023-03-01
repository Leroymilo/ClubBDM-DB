from db_init import *

def add(name: str) :
    cursor.execute(f"""-- sql
        SELECT auth_id FROM Authors
        WHERE auth_name LIKE "{name}"
    ;""")
    if cursor.fetchall() != [] :
        return 1
    
    cursor.execute(f"""-- sql
        INSERT INTO Authors (auth_name) VALUES ("{name}")
    ;""")
    db.commit()
    return 0