import mysql.connector as mysql
import numpy as np

db_name = "BDMANGA"

HOST = "51.77.231.57"
USER = "admin"
PASSWORD = "limploseur3000"
print("Connecting...")
db = mysql.connect(host=HOST, database=db_name, user=USER, password=PASSWORD)
print("Connected to:", db.get_server_info())
cursor = db.cursor()