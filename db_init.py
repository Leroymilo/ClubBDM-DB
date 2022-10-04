from sqlite3 import *
import re

def regexp(expr: str, item: str) :
    reg = re.compile(expr)
    return reg.search(item) is not None

def lpad(item, char: str, nb: int) :
    return str(item).rjust(nb, char)

db = connect("temp.sql")
cursor = db.cursor()
db.create_function("REGEXP", 2, regexp)
db.create_function("LPAD", 3, lpad)