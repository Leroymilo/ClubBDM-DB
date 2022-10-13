import wx
import wx.dataview
import pandas as pd

from db_init import *

from gen_classes.main_app import MainWindow

import functions.books as books
import functions.series as series
import functions.users as users
import functions.loans as loans

from linked_classes.book_add import Book

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
    "Series" : None,
    "Users" : None,
    "Loans" : None
}

class Main(MainWindow) :
    def __init__(self, parent) :
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
            self.book_search_val : "Books",
            self.series_search_val : "Series",
            self.user_search_val : "Users",
            self.loan_search_val : "Loans",
        }
        
        self.notebook.SetSelection(0)
        self.sub_frames = []
        tab = notebook_pages[self.notebook.GetSelection()]
        self.update_table(tab = tab)
        self.Show()

    def update_table(self, tab: str, filter_: Union[None, Tuple[str]] = None) :
        
        dataView = self.dataViews[tab]
        dataView.DeleteAllItems()
        table = selectors[tab](filter_)
        for line in table :
            dataView.AppendItem(list(map(str,line)))

    def search_table(self, event: wx.Event) :
        search_ctrl: wx.TextCtrl = event.GetEventObject()
        tab = self.searchVals[search_ctrl]

        filter_val = search_ctrl.GetValue()
        if filter_val.strip() == "" :
            filter_ = None
        else :
            filter_col = filters[tab][self.searchCols[tab].GetSelection()]
            filter_ = (filter_col, filter_val)
        self.update_table(tab, filter_=filter_)
    
    def load_display(self, event: wx.Event) :
        tab = notebook_pages[self.notebook.GetSelection()]
        # print(tab)
        if tab in selectors :
            self.update_table(tab)
    
    def toggle_archived(self, event: wx.Event) :
        tab = notebook_pages[self.notebook.GetSelection()]

        if tab == "Users" :
            self.user_col_7.SetHidden(1 - self.user_col_7.IsHidden())
            self.user_col_8.SetHidden(1 - self.user_col_8.IsHidden())
        
        elif tab == "Loans" :
            self.loan_col_5.SetHidden(1 - self.loan_col_5.IsHidden())
            self.loan_col_4.SetWidth(80)    #The un-hidden column appears out of the window without this
    
    def run_query(self, event: wx.Event) :
        queries = self.query_text.GetValue().split(';\n')

        for query in queries :
            if query.upper().startswith("SELECT") :
                df = pd.read_sql(query, db)
        
        col_names = df.columns
        table = df.to_numpy(dtype=str, na_value="None")
        self.query_result.ClearColumns()
        self.query_result.DeleteAllItems()
        for col in col_names :
            self.query_result.AppendTextColumn(col, flags=wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE)
        for line in table :
            self.query_result.AppendItem(list(map(str,line)))

    def add(self, event: wx.Event) :
        tab = notebook_pages[self.notebook.GetSelection()]
        sub_frame = adders[tab](self)