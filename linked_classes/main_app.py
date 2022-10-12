import wx
from db_init import *

from gen_classes.main_app import MainWindow

import functions.books as books
import functions.series as series
import functions.users as users
import functions.loans as loans

filters = {
    "Books" : ["Series", "Author", "Editor"],
    "Series" : ["Name", "Type", "Category", "Author", "Editor"],
    "Users" : ["Name", "Status"],
    "Loans" : ["User", "Book"]
}

notebook_pages = ["Books", "Series", "Users", "Loans", "SQL"]

selecters = {
    "Books" : books.select,
    "Series" : series.select,
    "Users" : users.select,
    "Loans" : loans.select
}

class Main(MainWindow) :
    def __init__(self, parent) :
        super().__init__(parent)
        self.notebook.SetSelection(0)

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
        
        tab = notebook_pages[self.notebook.GetSelection()]
        self.update_table(tab = tab)
        self.Show()
    
    def update_table(self, tab: str, filter_: Union[None, Tuple[str]] = None) :
        
        dataView = self.dataViews[tab]
        dataView.DeleteAllItems()
        table = selecters[tab](filter_)
        for line in table :
            dataView.AppendItem(list(map(str,line)))

    def search_table(self, event: wx.Event):
        search_ctrl: wx.TextCtrl = event.GetEventObject()
        tab = self.searchVals[search_ctrl]

        filter_val = search_ctrl.GetValue()
        if filter_val.strip() == "" :
            filter_ = None
        else :
            filter_col = filters[tab][self.searchCols[tab].GetSelection()]
            filter_ = (filter_col, filter_val)
        self.update_table(tab, filter_=filter_)
    
    def load_display(self, event: wx.Event):
        tab = notebook_pages[self.notebook.GetSelection()]
        # print(tab)
        if tab in selecters :
            self.update_table(tab)