from sqlite3 import *
import re
from typing import Union, Tuple
import numpy as np

db_name = "dbBDM"

def regexp(expr: str, item: str) :
    reg = re.compile(expr)
    return reg.search(item) is not None

def lpad(item, char: str, nb: int) :
    return str(item).rjust(nb, char)

def if_(condition: bool, if_true, if_false) :
    if condition :
        return if_true
    return if_false

def concat(sep: str, *list_) :
    return sep.join(map(str, list_))

class ConcatAgg :
    def __init__(self) :
        self.values = []
        self.sep = ""
    
    def step(self, sep: str, value) :
        self.sep = sep
        self.values.append(str(value))
    
    def finalize(self) :
        return self.sep.join(self.values)

db = connect(db_name + ".sql")
cursor = db.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
db.create_function("REGEXP", 2, regexp)
db.create_function("LPAD", 3, lpad)
db.create_function("IF", 3, if_)
db.create_function("CONCATWS", -1, concat)
db.create_aggregate("CONCAT", 2, ConcatAgg)
