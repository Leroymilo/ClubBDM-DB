from sqlite3 import *
import re
from typing import Union, Tuple
import numpy as np

db_name = "temp"

def regexp(expr: str, item: str) :
    reg = re.compile(expr)
    return reg.search(item) is not None

def lpad(item, char: str, nb: int) :
    return str(item).rjust(nb, char)

db = connect(db_name + ".sql")
cursor = db.cursor()
db.create_function("REGEXP", 2, regexp)
db.create_function("LPAD", 3, lpad)
