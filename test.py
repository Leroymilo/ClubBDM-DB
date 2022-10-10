from db_init import *
import numpy as np



tables = ["Categories", "Series", "Books", "Users", "Loans", "Authors", "Srs-Auth", "Editors", "Srs-Edit"]

for table_name in tables[:-4] :
    cursor.execute(f"--sql SELECT * FROM {table_name};")
    print("Table :", table_name)
    print(np.array(cursor.fetchall()))
    print()