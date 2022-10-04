from db_init import *
import numpy as np

Tables = ["Categories", "Series", "Books", "Users", "Loans", "Authors", "Srs-Auth", "Editors", "Srs-Edit"]

def add(table_name: str, vector: list) :
    cursor.execute(f"SELECT * FROM `{table_name}`;")
    table = cursor.fetchall()
    if tuple(vector) in table :
        return False
    
    for i in range(len(vector)) :
        if type(vector[i]) == str :
            vector[i] = "'" + vector[i] + "'"
        elif type(vector[i]) == bool :
            vector[i] = ["FALSE", "TRUE"][vector[i]]
        else :
            vector[i] = str(vector[i])
    
    cursor.execute(f"INSERT INTO `{table_name}` VALUES ({', '.join(vector)});")
    db.commit()
    return True

add("Series", ["BRSRK", "Berserk", "manga", 1])
add("Books", ["01BRSRK00201", "Berserk Vol2", "BRSRK", 2, 1, True, 10, "2022-10-04", ""])
add("Books", ["01BRSRK00301", "Berserk Vol3", "BRSRK", 3, 1, True, 10, "2022-10-04", ""])
add("Books", ["01BRSRK00401", "Berserk Vol4", "BRSRK", 4, 1, True, 10, "2022-10-04", ""])

for table_name in Tables :
    print("Table", table_name, ":")
    cursor.execute(f"SELECT * FROM `{table_name}`")
    print(np.array(cursor.fetchall()))
    print()

db.commit()

db.close()