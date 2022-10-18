from __future__ import annotations

import wx

from gen_classes.series_add import SeriesWindow

from functions.series import get_categories, get_auths, get_edits, add

#================================================================================================================================================================================

# Sub class containing averything usefull to implement the scrolled windows
# for authors and editors
class ScrolledChoices :
    def __init__(self, scroll: wx.ScrolledWindow, d: dict) :
        self.choices: list[wx.Choice] = []
        self.scroll = scroll
        self.sizer: wx.Sizer = scroll.GetSizer()
        self.dict = d
        self.to_update = []
    
    def add_choice(self, type_: str, frame: Series) :
        # Creating the new choice
        new_choice = wx.Choice(
            self.scroll, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            [""], wx.CB_SORT
        )
        self.to_update.append(True)
        new_choice.Select(0)

        # Setting some way to recognize it as an event's object
        new_choice.SetId(len(self.choices))
        new_choice.SetName(type_)
        # Adding it to the sizer and the list of choices
        self.sizer.Add( new_choice, 0, wx.ALL|wx.EXPAND, 5 )
        self.choices.append(new_choice)

        # Binding methods
        new_choice.Bind(wx.EVT_CHOICE, frame.choice_selected)
        new_choice.Bind(wx.EVT_ENTER_WINDOW, frame.update_choice)
    
    def manage_select(self, type_: str, choice: wx.Choice, frame: Series) :
        max_id = len(self.choices) - 1
        self.to_update = [choice.GetId() != i for i in range(len(self.to_update))]

        # If any choice (except the last) is reset to 0 :
        if choice.GetSelection() == 0 and \
            choice.GetId() < max_id :
            
            # Push choices up :
            for i in range(choice.GetId(), max_id) :
                new_string = self.choices[i+1].GetStringSelection()
                self.choices[i].Set(self.choices[i].GetStrings() + [new_string])
                self.choices[i].SetStringSelection(new_string)
            
            # If the last choice is on 0 :
            if self.choices[-1].GetSelection() == 0 :
                # Remove the last choice :
                last_choice = self.choices.pop()
                self.sizer.Remove(last_choice.GetId())
                last_choice.Destroy()   # Just in case
                self.to_update.pop()
            
            # Else (only happens if every auth/edit is selected) :
            else :
                self.choices[-1].SetSelection(0)

        # If a choice gets a non-0 selection :
        elif choice.GetSelection() != 0 :
            # If it's the last one and all the auth/edit are not selected :
            if choice.GetId() == max_id and len(self.choices) < len(self.dict.keys()) :
                self.add_choice(type_, frame)
    
    def update_choice(self, choice: wx.Choice) :
        if self.to_update[choice.GetId()] :
            self.to_update[choice.GetId()] = False

            selection = choice.GetStringSelection()
            selected = {choice.GetStringSelection() for choice in self.choices}
            strings = set(self.dict.keys()).difference(selected)
            strings = {"", selection} | strings
            choice.SetItems(list(strings))
            choice.SetStringSelection(selection)
            # print("choice", choice.GetId(), "updated")
    
    def get_selection_ids(self) :
        return [self.dict[choice.GetStringSelection()] for choice in self.choices if choice.GetSelection() != 0]

#================================================================================================================================================================================

# Main frame class
class Series (SeriesWindow) :
    def __init__(self, parent, id_: int) :
        super().__init__(parent)
        self.id_ = id_
        self.cat_dict = get_categories()
        self.book_cat_choice.SetItems([""]+ list(self.cat_dict.keys()))
        self.timer_tick = 0

        self.auth_edit = {
            "auth" : ScrolledChoices(self.scroll_auth, get_auths()),
            "edit" : ScrolledChoices(self.scroll_edit, get_edits())
        }
        self.auth_edit["auth"].add_choice("auth", self)
        self.auth_edit["edit"].add_choice("edit", self)

        self.sub_frames = []
    
    def choice_selected(self, event: wx.Event) :
        choice: wx.Choice = event.GetEventObject()
        type_: str = choice.GetName()

        self.auth_edit[type_].manage_select(type_, choice, self)

        self.Layout()
    
    def update_choice(self, event: wx.Event) :
        choice: wx.Choice = event.GetEventObject()
        type_: str = choice.GetName()

        self.auth_edit[type_].update_choice(choice)

    
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
        
        auth_ids = self.auth_edit["auth"].get_selection_ids()
        edit_ids = self.auth_edit["edit"].get_selection_ids()

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
        self.Parent.add(tab="Authors")
    
    def add_edit(self, event) :
        self.Parent.add(tab="Editors")

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
        self.Parent.sub_frames.pop(self.id_)
        self.Destroy()