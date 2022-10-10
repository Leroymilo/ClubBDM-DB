from db_init import *
import numpy as np

cursor.execute("INSERT INTO Categories VALUES (1, 'Fantasy')")
cursor.execute("INSERT INTO Categories VALUES (2, 'Science-Fiction')")
cursor.execute("""--sql
INSERT INTO Series VALUES (
    "BRSRK",
    "Berserk",
    "manga"
    1
);""")

for i in range(501) :
    cursor.execute(f"""
    --sql
    INSERT INTO Books VALUES (
        "01BRSRK{str(i).rjust(3, '0')}01",
        "Berserk vol.{i}",
        "BRSRK",
        {i}, 1,
        TRUE, 9,
        '2022-10-10', ""
    )
    ;
    """)
db.commit()

tables = ["Categories", "Series", "Books", "Users", "Loans", "Authors", "Srs-Auth", "Editors", "Srs-Edit"]

for table_name in tables[:-4] :
    cursor.execute(f"""--sql
    SELECT * FROM {table_name};""")
    print("Table :", table_name)
    print(np.array(cursor.fetchall()))
    print()