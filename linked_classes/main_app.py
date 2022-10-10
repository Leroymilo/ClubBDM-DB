import wx
from db_init import *
from gen_classes.main_app import MainWindow

tables = ["Categories", "Series", "Books", "Users", "Loans", "Authors", "Srs-Auth", "Editors", "Srs-Edit"]

def get_cols(table_name: str) :
    cursor.execute(f"""--sql
        PRAGMA table_info(`{table_name}`);""")
    cols = cursor.fetchall()
    return [col[1] for col in cols]

columns = {table_name: get_cols(table_name) for table_name in tables}
print(columns)

class Main(MainWindow) :
    def __init__(self, parent) :
        super().__init__(parent)
        self.update_books()
        self.Show()
    
    def update_books(self) :
        self.book_display.DeleteAllItems()
        cursor.execute("""
        --sql
        SELECT book_id, book_name, vol_nb, series_name, condition, available, added_on, comment
        FROM Books
        JOIN Series USING (series_id)
        ;
        """)
        for line in cursor.fetchall() :
            self.book_display.AppendItem(list(map(str,line)))

    def update_users(self) :
        pass

    def update_loans(self) :
        pass