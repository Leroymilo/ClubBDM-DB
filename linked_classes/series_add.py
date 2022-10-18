import wx

from gen_classes.series_add import SeriesWindow

from linked_classes.author_add import Author
from linked_classes.editor_add import Editor

from functions.series import get_categories, get_auths, get_edits, add

class Series (SeriesWindow) :
    def __init__(self, parent, id_: int) :
        super().__init__(parent)
        self.id_ = id_
        self.cat_dict = get_categories()
        self.book_cat_choice.SetItems([""]+ list(self.cat_dict.keys()))
        self.timer_tick = 0

        self.auth_choices = []
        self.auth_sizer = self.scroll_auth.GetSizer()
        self.auth_dict = get_auths()
        self.add_auth_ch()

        self.edit_choices = []
        self.edit_sizer = self.scroll_edit.GetSizer()
        self.edit_dict = get_edits()
        self.add_edit_ch()

        self.sub_frames = []
    
    def add_auth_ch(self) :
        new_choice = wx.Choice(
            self.scroll_auth, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            [""] + list(self.auth_dict.keys()), wx.CB_SORT )
        new_choice.Select(0)
        new_choice.SetId(1100+len(self.auth_choices))
        self.auth_sizer.Add( new_choice, 0, wx.ALL|wx.EXPAND, 5 )
        self.auth_choices.append(new_choice)
        new_choice.Bind(wx.EVT_CHOICE, self.auth_selected)
    
    def auth_selected(self, event: wx.Event) :
        choice_i = event.GetEventObject().GetId() - 1100
        if self.auth_choices[choice_i].GetSelection() == 0 \
            and choice_i != len(self.auth_choices) - 1 :
            for i in range(choice_i, len(self.auth_choices) - 1) :
                self.auth_choices[i].SetSelection(
                    self.auth_choices[i+1].GetSelection()
                )
            
            if len(self.auth_choices) > 1 :
                if self.auth_choices[-1].GetStringSelection() == "" :
                    last_choice = self.auth_choices.pop()
                    self.auth_sizer.Remove(last_choice.GetId() - 1100)
                    last_choice.Destroy()
                else :
                    self.auth_choices[-1].SetSelection(0)
        
        elif self.auth_choices[choice_i].GetSelection() != 0 \
            and choice_i == len(self.auth_choices) - 1 \
            and len(self.auth_choices) < len(self.auth_dict.keys()) :
            self.add_auth_ch()

        self.Layout()
    
    def add_edit_ch(self) :
        new_choice = wx.Choice(
            self.scroll_edit, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            [""] + list(self.edit_dict.keys()), wx.CB_SORT )
        new_choice.Select(0)
        new_choice.SetId(1200+len(self.edit_choices))
        self.edit_sizer.Add( new_choice, 0, wx.ALL|wx.EXPAND, 5 )
        self.edit_choices.append(new_choice)
        new_choice.Bind(wx.EVT_CHOICE, self.edit_selected)
    
    def edit_selected(self, event: wx.Event) :
        choice_i = event.GetEventObject().GetId() - 1200
        if self.edit_choices[choice_i].GetSelection() == 0  and choice_i != len(self.edit_choices) - 1 :
            for i in range(choice_i, len(self.edit_choices) - 1) :
                self.edit_choices[i].SetSelection(self.edit_choices[i+1].GetSelection())
            
            if len(self.edit_choices) > 1 :
                if self.edit_choices[-1].GetStringSelection() == "" :
                    last_choice = self.edit_choices.pop()
                    self.edit_sizer.Remove(last_choice.GetId() - 1100)
                    last_choice.Destroy()
                else :
                    self.edit_choices[-1].SetSelection(0)
        
        elif self.edit_choices[choice_i].GetSelection() != 0 and choice_i == len(self.edit_choices) - 1 :
            self.add_edit_ch()
        
        self.Layout()
    
    def add_series(self, event) :
        if self.book_cat_choice.GetSelection() == 0 :
            self.display("Sélectionnez une catégorie littéraire.")
            return
        
        if self.book_type_choice.GetSelection() == 0 :
            self.display("Sélectionnez un type de livres.")
            return
        
        series_id = self.series_id_txt.GetValue().strip(' ')
        if not series_id.isalnum() :
            self.display("Le code de la série doit être alpha-numérique.")
            return
        if len(series_id) != 5 :
            self.display("Le code de la série doit être composé de 5 charactères")
            return
    
        series_name = self.series_name_txt.GetValue().strip(' ')
        if series_name == "" :
            self.display("Le nom de la série ne peut pas être vide.")
        
        auth_ids = {self.auth_dict[choice.GetStringSelection()] for choice in self.auth_choices[:-1]}
        edit_ids = {self.edit_dict[choice.GetStringSelection()] for choice in self.edit_choices[:-1]}

        err_code = add(
            series_id,
            series_name,
            self.book_type_choice.GetStringSelection(),
            self.cat_dict[self.book_cat_choice.GetStringSelection()],
            auth_ids, edit_ids
        )

        if err_code == 0 :
            self.display(f"La série '{series_name}' a été ajoutée à la liste")
            
            p = self.Parent
            if p.id_ == -1 :
                if p.notebook.GetSelection() == 1 :
                    p.search_table(None)
            else :
                p.update_series()

        
        elif err_code == 1 :
            self.display(f"Le code de série '{series_id}' est déjà utilisé")
        elif err_code == 2 :
            self.display(f"La série '{series_name}' existe déjà")
        else :
            self.display("Erreur inconnue")
    
    def add_auth(self, event) :
        sub_frame = Author(self, id_=len(self.sub_frames))
        self.sub_frames.append(sub_frame)
        sub_frame.Show()
    
    def add_edit(self, event) :
        sub_frame = Editor(self, id_=len(self.sub_frames))
        self.sub_frames.append(sub_frame)
        sub_frame.Show()

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
    
    def clean_sub_frames(self) :
        while len(self.sub_frames) > 0 and self.sub_frames[-1] is None :
            self.sub_frames.pop()
    
    def on_activate(self, event):
        for sub_frame in self.sub_frames :
            if sub_frame is not None :
                sub_frame.Show()
        
    def on_iconize(self, event):
        for sub_frame in self.sub_frames :
            if sub_frame is not None :
                sub_frame.Hide()