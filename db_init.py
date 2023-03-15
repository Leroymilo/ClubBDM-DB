import mysql.connector as mysql
import numpy as np
import sys

db_name = "BDMANGA"
HOST = "51.77.231.57"

class Connector :
    def __init__(self, user: str = None, pwd: str = None) -> None:
        if user is None or pwd is None :
            return
    
        self.user = user

        print("Connecting...")
        self.db = mysql.connect(host=HOST, database=db_name, user=user, password=pwd)
        print("Connected to:", self.db.get_server_info())
        self.cursor = self.db.cursor()
    
    def execute(self, query: str) :
        try :
            self.cursor.execute(query)
        except mysql.errors.IntegrityError as e :
            print("query :")
            print(query)
            raise e
    
    def fetchall(self) :
        return self.cursor.fetchall()
    
    def fetchone(self) :
        return self.cursor.fetchone()
    
    def commit(self) :
        self.db.commit()
    
    def close(self) :
        self.db.close()

db = Connector()
cursor = db