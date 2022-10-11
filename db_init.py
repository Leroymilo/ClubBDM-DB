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

def if_(condition: bool, if_true, if_false) :
    if condition :
        return if_true
    return if_false

db = connect(db_name + ".sql")
cursor = db.cursor()
db.create_function("REGEXP", 2, regexp)
db.create_function("LPAD", 3, lpad)
db.create_function("IF", 3, if_)
