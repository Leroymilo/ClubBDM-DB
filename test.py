from db_init import *
import numpy as np

# import db_reset

# cursor.execute("INSERT INTO Categories VALUES (1, 'Fantasy')")
# cursor.execute("INSERT INTO Categories VALUES (2, 'Science-Fiction')")
# cursor.execute("""--sql
# INSERT INTO Series VALUES (
#     "BRSRK",
#     "Berserk",
#     "manga",
#     1
# );""")

# for i in range(1, 501) :
#     cursor.execute(f"""
#     --sql
#     INSERT INTO Books VALUES (
#         "01BRSRK{str(i).rjust(3, '0')}01",
#         "Berserk vol.{i}",
#         "BRSRK",
#         {i}, 1,
#         TRUE, {i%10+1},
#         '2022-10-10', ""
#     )
#     ;
#     """)
# db.commit()

tables = ["Categories", "Series", "Books", "Users", "Loans", "Authors", "Srs-Auth", "Editors", "Srs-Edit"]

# for table_name in tables :
#     cursor.execute(f"""--sql
#     SELECT * FROM `{table_name}`;""")
#     print("Table :", table_name)
#     print(np.array(cursor.fetchall()))
#     print()

cursor.execute("""--sql
INSERT INTO Users VALUES (
    1, 'Adriaan Lecorché', 'adriaanboxmail@gmail.com',
    '0642280338', 10, 90, 20, NULL,
    'Secrétaire Général', NULL, FALSE, ""
)
;""")
cursor.execute("""--sql
INSERT INTO Users VALUES (
    2, 'Ethan', 'ethan@insa-lyon.fr',
    '06XXXXXXXX', 2, 30, 20, NULL,
    'Trésorier', NULL, FALSE, ""
)
;""")
cursor.execute("""--sql
INSERT INTO Loans VALUES (
    1, 1, '01BRSRK01201', '05/10/2022',
    '5/01/2023', NULL, False
)
;""")
db.commit()

db.close()