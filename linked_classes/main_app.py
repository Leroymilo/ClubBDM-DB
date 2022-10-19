import wx
import wx.dataview
import pandas as pd

from db_init import *
from backup import backup_db

from gen_classes.main_app import MainWindow

import functions.books as books
import functions.series as series
import functions.users as users
import functions.loans as loans

from linked_classes.book_add import Book
from linked_classes.series_add import Series
from linked_classes.author_add import Author
from linked_classes.editor_add import Editor
from linked_classes.pwd_ask import Pwd

filters = {
    "Books" : ["Series", "Author", "Editor"],
    "Series" : ["Name", "Type", "Category", "Author", "Editor"],
    "Users" : ["Name", "Status"],
    "Loans" : ["User", "Book"]
}

notebook_pages = ["Books", "Series", "Users", "Loans", "SQL"]

selectors = {
    "Books" : books.select,
    "Series" : series.select,
    "Users" : users.select,
    "Loans" : loans.select
}

adders = {
    "Books" : Book,
    "Series" : Series,
    "Authors" : Author,
    "Editors" : Editor,
    "Users" : None,
    "Loans" : None
}

class Main(MainWindow) :
    def __init__(self, parent) :
        backup_db(db_name)
        self.sql_locked = True
        super().__init__(parent)

        self.dataViews = {
            "Books" : self.book_display,
            "Series" : self.series_display,
            "Users" : self.user_display,
            "Loans" : self.loan_display
        }

        self.searchCols = {
            "Books" : self.book_search_col,
            "Series" : self.series_search_col,
            "Users" : self.user_search_col,
            "Loans" : self.loan_search_col,
        }
        
        self.searchVals = {
            "Books" : self.book_search_val,
            "Series" : self.series_search_val,
            "Users" : self.user_search_val,
            "Loans" : self.loan_search_val,
        }
        
        self.notebook.SetSelection(0)
        self.sub_frames = {}
        self.update_table(tab = notebook_pages[self.notebook.GetSelection()])

    def update_table(self, tab: str, filter_: Union[None, Tuple[str]] = None) :
        dataView = self.dataViews[tab]
        dataView.DeleteAllItems()
        table = selectors[tab](filter_)
        for line in table :
            dataView.AppendItem(list(map(str,line)))

    def search_table(self, event) :
        tab = notebook_pages[self.notebook.GetSelection()]

        search_ctrl = self.searchVals[tab]
        filter_val = search_ctrl.GetValue()
        if filter_val.strip() == "" :
            filter_ = None
        else :
            filter_col = filters[tab][self.searchCols[tab].GetSelection()]
            filter_ = (filter_col, filter_val)
        self.update_table(tab, filter_=filter_)
    
    def load_display(self, event: wx.Event) :
        tab = notebook_pages[self.notebook.GetSelection()]
        if tab in selectors :
            self.update_table(tab)
    
    def toggle_archived(self, event: wx.Event) :
        tab = notebook_pages[self.notebook.GetSelection()]

        if tab == "Users" :
            self.user_col_9.SetHidden(1 - self.user_col_9.IsHidden())
            self.user_col_10.SetHidden(1 - self.user_col_10.IsHidden())
        
        elif tab == "Loans" :
            self.loan_col_5.SetHidden(1 - self.loan_col_5.IsHidden())
            self.loan_col_4.SetWidth(80)    #The un-hidden column appears out of the window without this
    
    def run_query(self, event: wx.Event) :
        queries = self.query_text.GetValue().split(';\n')

        df = pd.DataFrame()

        tried_pwd = False
        backed_up = False
        for query in queries :            
            if not query.upper().startswith("SELECT") and self.sql_locked :
                if tried_pwd :
                    continue
            
                if not backed_up :
                    backup_db(db_name)
                    backed_up = True

                pwd_dlg = Pwd(self)
                if pwd_dlg.ShowModal() == 1 :
                    self.sql_locked = False
                else :
                    continue
            
            self.help_text.SetLabel("Requête en cours d'execution...")
            try :
                df = pd.read_sql(query, db)
            except TypeError :
                self.help_text.SetLabel("La requête n'a pas de résultat")
                db.commit()
            except pd.errors.DatabaseError as er:
                self.help_text.SetLabel("Erreur dans la requête : {0}".format(er))
        
        self.query_result.ClearColumns()
        self.query_result.DeleteAllItems()
        if df.shape == (0, 0) :
            return
        self.help_text.SetLabel(f"Dimensions du résultat : {df.shape}")
        col_names = df.columns
        table = df.to_numpy(dtype=str, na_value="None")
        for col in col_names :
            self.query_result.AppendTextColumn(col, flags=wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE)
        for line in table :
            self.query_result.AppendItem(list(map(str,line)))

    def add(self, event=None, tab: str=None) :
        if tab is None :
            tab = notebook_pages[self.notebook.GetSelection()]
        id_ = max(self.sub_frames.keys(), default=0) + 1
        sub_frame: wx.Frame = adders[tab](self, id_)
        self.sub_frames[id_] = sub_frame
        sub_frame.Show()
        sub_frame.SetFocus()
    
    def on_activate(self, event):
        for sub_frame in self.sub_frames.values() :
            if sub_frame is not None :
                sub_frame.Show()
        
    def on_iconize(self, event):
        for sub_frame in self.sub_frames.values() :
            if sub_frame is not None :
                sub_frame.Hide()