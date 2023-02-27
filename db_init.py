import mysql.connector as mysql
import numpy as np

db_name = "BDMANGA"
HOST = "51.77.231.57"

class SingletonMeta(type) :

    _instances = {}

    def __call__(cls, *args, **kwargs) :
        if cls not in cls._instances :
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Connector(metaclass=SingletonMeta) :
    def __init__(self, user: str = None, pwd: str = None) -> None:
        if user is None or pwd is None :
            return
    
        self.user = user

        print("Connecting...")
        self.db = mysql.connect(host=HOST, database=db_name, user=user, password=pwd)
        print("Connected to:", self.db.get_server_info())
        self.cursor = self.db.cursor()
    
    def execute(self, query: str) :
        self.cursor.execute(query)
    
    def fetchall(self) :
        return self.cursor.fetchall()
    
    def commit(self) :
        self.db.commit()
    
    def close(self) :
        self.db.close()

db = Connector()
cursor = db