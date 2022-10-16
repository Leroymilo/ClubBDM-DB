import wx

from gen_classes.series_add import SeriesWindow

from functions.series import get_categories, get_auths, get_edits

class Series (SeriesWindow) :
    def __init__(self, parent, id_: int) :
        super().__init__(parent)
        self.id_ = id_
        self.cat_dict = get_categories()
        self.book_cat_choice.SetItems(list(self.cat_dict.keys()))
        self.timer_tick = 0

        self.auth_choices = []
        self.auth_sizer = self.scroll_auth.GetSizer()
        self.auth_dict = get_auths()
        self.add_auth_ch()

        self.edit_choices = []
        self.edit_sizer = self.scroll_edit.GetSizer()
        self.edit_dict = get_edits()
        self.add_edit_ch()
    
    def add_auth_ch(self) :
        new_choice = wx.Choice(
            self.scroll_auth, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            [""] + list(self.auth_dict.keys()), wx.CB_SORT )
        new_choice.Select(0)
        self.auth_sizer.Add( new_choice, 0, wx.ALL|wx.EXPAND, 5 )
        new_choice.Bind(wx.EVT_CHOICE, self.auth_selected)
    
    def auth_selected(self, event: wx.Event) :
        print("Selection :", event.GetEventObject().GetSelection())
    
    def add_edit_ch(self) :
        new_choice = wx.Choice(
            self.scroll_edit, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            [""] + list(self.edit_dict.keys()), wx.CB_SORT )
        new_choice.Select(0)
        self.edit_sizer.Add( new_choice, 0, wx.ALL|wx.EXPAND, 5 )
    
    def add_series(self, event) :
        if self.book_cat_choice.GetSelection() == -1 :
            self.display("Sélectionnez une catégorie littéraire.")
            return
        
        if self.book_type_choice.GetSelection() == 0 :
            self.display("Sélectionnez un type de livres.")
            return
        
        series_id = self.series_id_txt.GetValue().strip(' ')
        if not series_id.isalnum() :
            self.display("Le code de la série doit être alpha-numérique.")
        if len(series_id) != 5 :
            self.display("Le code de la série doit être composé de 5 charactères")
    
        series_name = self.series_name_txt.GetValue().strip(' ')
        if series_name == "" :
            self.display("Le nom de la série ne peut pas être vide.")
        


    def display(self, text: str) :
        self.help_text.SetLabel(text)
        self.help_timer.Start()
        self.timer_tick = 0
    
    def test_timer(self, event) :
        if self.timer_tick == 500 :
            self.help_text.SetLabel("")
            self.help_timer.Stop()
        else :
            self.timer_tick += 1

    def end_process(self, event) :
        self.help_timer.Stop()
        self.Parent.sub_frames[self.id_] = None
        self.Parent.clean_sub_frames()
        self.Destroy()