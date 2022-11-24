import wx
import wx.dataview
import pandas as pd

from db_init import *
from backup import backup_db

from gen_classes.main_app import MainWindow

import functions.books as books
import functions.series as series
import functions.members as members
import functions.loans as loans

from functions.inventory import read_xlsx, write_db, read_db, write_xlsx

from linked_classes.book import Book
from linked_classes.series import Series
from linked_classes.author_add import Author
from linked_classes.editor_add import Editor
from linked_classes.member import Member
from linked_classes.loan import Loan
from linked_classes.loan_end import LoanEnd
from linked_classes.pwd_ask import Pwd

filters = {
    "Books" : ["Series", "Author", "Editor"],
    "Series" : ["Name", "Type", "Category", "Author", "Editor"],
    "Members" : ["Name", "Status"],
    "Loans" : ["Member", "Book"]
}

notebook_pages = ["Books", "Series", "Members", "Loans", "SQL", "Inventory"]

selectors = {
    "Books" : books.select,
    "Series" : series.select,
    "Members" : members.select,
    "Loans" : loans.select
}

sub_frames = {
    "Books" : Book,
    "Series" : Series,
    "Authors" : Author,
    "Editors" : Editor,
    "Members" : Member,
    "Loans" : Loan
}

class Main(MainWindow) :
    def __init__(self, parent) :
        backup_db(db_name)
        self.sql_locked = True
        super().__init__(parent)
        self.default_text = self.help_text.GetLabel()

        self.dataViews = {
            "Books" : self.book_display,
            "Series" : self.series_display,
            "Members" : self.member_display,
            "Loans" : self.loan_display
        }

        self.searchCols = {
            "Books" : self.book_search_col,
            "Series" : self.series_search_col,
            "Members" : self.member_search_col,
            "Loans" : self.loan_search_col,
        }
        
        self.searchVals = {
            "Books" : self.book_search_val,
            "Series" : self.series_search_val,
            "Members" : self.member_search_val,
            "Loans" : self.loan_search_val,
        }

        self.archive = {
            "Members": self.member_archive_toggle,
            "Loans": self.loan_archive_toggle
        }
        
        self.notebook.SetSelection(0)
        self.sub_frames = {}
        self.update_table(tab = notebook_pages[self.notebook.GetSelection()])
        self.replace_button.SetName("replace")
        self.append_button.SetName("append")

    def update_table(self, tab: str, filter_: tuple[str] | None = None) :
        dataView = self.dataViews[tab]
        dataView.DeleteAllItems()

        if tab in {"Members", "Loans"} :
            table = selectors[tab](filter_, self.archive[tab].GetValue())
        else :
            table = selectors[tab](filter_)
        
        if tab == "Books" :
            self.nbr_book.SetLabel(f"Nombre de livres : {len(table)}")
        
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

        if tab == "Members" :
            self.member_col_9.SetHidden(1 - self.member_col_9.IsHidden())
            self.member_col_10.SetHidden(1 - self.member_col_10.IsHidden())
        
        elif tab == "Loans" :
            self.loan_col_5.SetHidden(1 - self.loan_col_5.IsHidden())
            self.loan_col_4.SetWidth(80)    #The un-hidden columns appears out of the window without this
            self.loan_col_3.SetWidth(80)
        
        self.update_table(tab)
    
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
        sub_frame: wx.Frame = sub_frames[tab](self, id_)
        self.sub_frames[id_] = (tab, sub_frame)
        sub_frame.Show()
        sub_frame.SetFocus()
    
    def edit(self, event: wx.dataview.DataViewEvent) :
        tab = notebook_pages[self.notebook.GetSelection()]
        dvlc = self.dataViews[tab]

        if tab == "Loans" :
            archived = dvlc.GetValue(dvlc.GetSelectedRow(), 4) != "None"
            # Beware : the 4 is the index aùong VISIBLE columns.
            # You'll need to change it if you add other columns before this one.
            # There seem to be no way to get the number of visible columns.
            
            if self.loan_archive_toggle.GetValue() and archived :
                self.display("Vous ne pouvez pas modifier un emprunt déjà rendu.")
                return
            item_id = (
                dvlc.GetValue(dvlc.GetSelectedRow(), 0),
                dvlc.GetValue(dvlc.GetSelectedRow(), 1)
            )
        else :
            item_id = dvlc.GetValue(dvlc.GetSelectedRow(), 0)
        
        id_ = max(self.sub_frames.keys(), default=0) + 1
        sub_frame: wx.Frame = sub_frames[tab](self, id_, item_id)
        self.sub_frames[id_] = (tab, sub_frame)
        sub_frame.Show()
        sub_frame.SetFocus()
    
    def update_data(self, tab: str) :
        if tab == notebook_pages[self.notebook.GetSelection()] :
            self.search_table(None)
        
        to_update = {
            "Members": "Loans",
            "Books": "Loans",
            "Series": "Books",
            "Authors": "Series",
            "Editors": "Series",
            "Loans": "Loans"
        }

        for type_, sub_frame in self.sub_frames.values() :
            if type_ == to_update[tab] :
                sub_frame.update_data(tab)
            
    def end_loan(self, event) :
        row = self.loan_display.GetSelectedRow()
        dvlc = self.dataViews["Loans"]

        if row == wx.NOT_FOUND :
            self.display("Sélectionnez un emprunt à terminer d'abord.")
            return
            
        member_name = dvlc.GetValue(dvlc.GetSelectedRow(), 0)
        book_id = dvlc.GetValue(dvlc.GetSelectedRow(), 1)
        
        dlg = LoanEnd(self)
        if dlg.ShowModal() :
            loans.end(member_name, book_id)
            self.update_data("Loans")
            self.update_table("Loans")
    
    def read_inv(self, event: wx.Event) :
        
        directory: str = self.read_file_picker.GetPath()
        directory = directory.strip()

        if directory == "" or not directory.endswith(".xlsx"):
            self.display("Choisissez un fichier excel valide à importer.")
            return
        
        button: wx.Button = event.GetEventObject()
        replace = False
        if button.GetName() == "replace" :
            replace = True
        
        self.display("Lecture de l'excel...")

        errcode, data = read_xlsx(directory)

        if errcode :
            sheet_name, miss_cols = data
            self.display(f"Colonnes {', '.join(miss_cols)} manquantes dans la feuille {sheet_name}.")
            return
    
        self.display("Écriture des données...")

        errcode = write_db(data, replace)

        self.display("Données enregistrées!")

    def gen_inv(self, event) :

        directory: str = self.write_txt.GetValue()
        directory = directory.strip()

        if directory == "" :
            self.display("Donnez un nom au fichier à générer.")
            return
        
        if not directory.endswith(".xlsx") :
            directory += ".xlsx"
        
        try :
            pd.ExcelWriter(directory)
        except OSError :
            self.display("Le nom de fichier à générer est invalide.")
            return
        
        self.display("Génération de l'inventaire...")
        write_xlsx(directory, read_db())
        self.display("Inventaire généré!")

    def display(self, text: str) :
        self.help_text.SetLabel(text)
        self.help_timer.Start()
        self.timer_tick = 0
    
    def test_timer(self, event) :
        if self.timer_tick >= 500 :
            self.help_text.SetLabel(self.default_text)
            self.help_timer.Stop()
        else :
            self.timer_tick += 1

    def end_process(self, event) :
        self.help_timer.Stop()
    
    def on_activate(self, event):
        for _, sub_frame in self.sub_frames.values() :
            if sub_frame is not None :
                sub_frame.Show()
        
    def on_iconize(self, event):
        for _, sub_frame in self.sub_frames.values() :
            if sub_frame is not None :
                sub_frame.Hide()