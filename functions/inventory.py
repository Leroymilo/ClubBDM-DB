from db_init import *
import pandas as pd
from datetime import date

def read_xlsx(directory: str) -> dict[str, pd.DataFrame] :
    data = {
        "categories" : pd.read_excel(directory, sheet_name="Catégories"),
        "authors" : pd.read_excel(directory, sheet_name="Auteurs"),
        "editors" : pd.read_excel(directory, sheet_name="Éditeurs"),
        "series" : pd.read_excel(directory, sheet_name="Séries"),
        "books" : pd.read_excel(directory, sheet_name="Livres"),
        "members": pd.read_excel(directory, sheet_name="Membres"),
    }

    return data

def write_db(data: dict[str, pd.DataFrame]) -> None :
    pass

def read_db() -> dict[str, pd.DataFrame] :
    pass

def write_xlsx(directory: str, data: dict[str, pd.DataFrame]) -> None :
    pass