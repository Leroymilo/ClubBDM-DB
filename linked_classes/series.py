from __future__ import annotations

import wx

from gen_classes.series import SeriesWindow

from functions.series import get_categories, get_auths, get_edits, get_item_data, add, edit

getters = {
    "cat": get_categories,
    "auth": get_auths,
    "edit": get_edits
}

#================================================================================================================================================================================

# Slightly modified class 

# Sub class containing averything usefull to implement
# the scrolled windows for authors and editors
class ScrolledChoices :
    def __init__(self, scroll: wx.ScrolledWindow, type_: str, frame: Series) :
        self.frame: Series = frame
        self.scroll = scroll
        self.sizer: wx.Sizer = scroll.GetSizer()
        self.choices: list[wx.Choice] = []
        self.type = type_
        self.dict = getters[type_]()
        self.to_update = []
        self.add_choice()
    
    def add_choice(self) :
        # Creating the new choice
        new_choice = wx.Choice(
            self.scroll, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            [""], wx.CB_SORT
        )
        self.to_update.append(True)
        new_choice.Select(0)

        # Setting some way to recognize it as an event's object
        new_choice.SetId(len(self.choices))
        new_choice.SetName(self.type)
        # Adding it to the sizer and the list of choices
        self.sizer.Add( new_choice, 0, wx.ALL|wx.EXPAND, 5 )
        self.choices.append(new_choice)
        
        self.update_choice(choice = new_choice)

        # Binding methods
        new_choice.Bind(wx.EVT_CHOICE, self.choice_selected)
        new_choice.Bind(wx.EVT_SET_FOCUS, self.test_focus)
    
    def set_choices(self, strings: list[str]) :
        for i in range(len(strings)) :
            self.add_choice()
            self.choices[i].SetStringSelection(strings[i])
    
    def choice_selected(self, event: wx.Event=None) :
        choice: wx.Choice = event.GetEventObject()
        max_id = len(self.choices) - 1
        self.to_update = [choice.GetId() != i for i in range(len(self.to_update))]

        # If any choice (except the last) is reset to 0 :
        if choice.GetSelection() == 0 and \
            choice.GetId() < max_id :
            
            # Push choices up :
            for i in range(choice.GetId(), max_id - 1) :
                new_string = self.choices[i+1].GetStringSelection()
                self.choices[i].Append(new_string)
                self.choices[i].SetStringSelection(new_string)
            
            # If the last choice is on 0 :
            if self.choices[-1].GetSelection() == 0 :
                self.choices[-2].SetSelection(0)
                # Remove the last choice :
                last_choice = self.choices.pop()
                self.sizer.Remove(last_choice.GetId())
                last_choice.Destroy()   # Just in case
                self.to_update.pop()
            
            # Else (only happens if every auth/edit is selected) :
            else :
                new_string = self.choices[-1].GetStringSelection()
                self.choices[-2].Append(new_string)
                self.choices[-2].SetStringSelection(new_string)
                self.choices[-1].SetSelection(0)

        # If a choice gets a non-0 selection :
        elif choice.GetSelection() != 0 :
            # If it's the last one and all the auth/edit are not selected :
            if choice.GetId() == max_id and len(self.choices) < len(self.dict.keys()) :
                self.add_choice()
        
        self.frame.Layout()
    
    def update_choice(self, event: wx.Event=None, choice: wx.Choice=None) :
        if choice is None :
            choice: wx.Choice = event.GetEventObject()
        
        if self.to_update[choice.GetId()] :
            self.to_update[choice.GetId()] = False

            selection = choice.GetStringSelection()
            selected = {choice.GetStringSelection() for choice in self.choices}
            choice.Clear()
            strings = set(self.dict.keys()).difference(selected)
            strings = {"", selection} | strings
            choice.SetItems(list(strings))
            choice.SetStringSelection(selection)
            print("choice", choice.GetId(), "updated")
    
    def test_focus(self, event: wx.Event=None) :
        choice: wx.Choice = event.GetEventObject()
        print("choice", choice.GetId(), "focused")
        self.update_choice(choice=choice)
        event.Skip()
    
    def get_selection_ids(self) :
        return [self.dict[choice.GetStringSelection()] for choice in self.choices if choice.GetStringSelection() != ""]

#================================================================================================================================================================================

# Main frame class
class Series (SeriesWindow) :
    def __init__(self, parent, id_: int, item_id=None) :
        super().__init__(parent)
        self.default_text = ""
        self.id_ = id_
        self.item_id = item_id
        self.cat_dict = get_categories()
        self.book_cat_choice.SetItems([""]+ list(self.cat_dict.keys()))
        self.timer_tick = 0

        self.auth_edit = {
            "auth" : ScrolledChoices(self.scroll_auth, "auth", self),
            "edit" : ScrolledChoices(self.scroll_edit, "edit", self)
        }

        self.is_editor = item_id is not None

        if self.is_editor :
            self.SetLabel("Modifier la série")
            item_data = get_item_data(item_id)
            self.series_name_txt.SetValue(item_data["series_name"])
            self.series_id_txt.SetValue(item_id)
            self.series_id_txt.Disable()
            self.book_type_choice.SetStringSelection(item_data["book_type"])
            self.book_cat_choice.SetStringSelection(item_data["book_cat"])
            
            if item_data["has_books"] :
                self.default_text = "La catégorie ne peut pas être changée car cette série contient des livres."
                self.help_text.SetLabel(self.default_text)
                self.book_cat_choice.Disable()

            self.auth_edit["auth"].set_choices(item_data["authors"])
            self.auth_edit["edit"].set_choices(item_data["editors"])

            self.end_button.SetLabel("Appliquer la modification")
    
    def complete(self, event) :
        if self.book_cat_choice.GetSelection() == 0 :
            self.display("Sélectionnez une catégorie littéraire.")
            return
        
        if self.book_type_choice.GetSelection() == 0 :
            self.display("Sélectionnez un type de livres.")
            return
        
        series_id = self.series_id_txt.GetValue().strip(' ').lstrip(' ')
        if not series_id.isalnum() :
            self.display("Le code de la série doit être alpha-numérique.")
            return
        if len(series_id) != 5 :
            self.display("Le code de la série doit être composé de 5 charactères.")
            return
    
        series_name = self.series_name_txt.GetValue().strip(' ').lstrip(' ')
        if series_name == "" :
            self.display("Le nom de la série ne peut pas être vide.")
        
        auth_ids = self.auth_edit["auth"].get_selection_ids()
        edit_ids = self.auth_edit["edit"].get_selection_ids()

        if self.is_editor :
            err_code = edit(
                series_id,
                series_name,
                self.book_type_choice.GetStringSelection(),
                self.cat_dict[self.book_cat_choice.GetStringSelection()],
                auth_ids, edit_ids
            )

            if err_code == 0 :
                self.Parent.update_data("Series")
                self.Close()
            
            elif err_code == 1 :
                self.display(f"Le nom de série {series_name} est déjà utilisé.")
            else :
                self.display("Erreur inconnue.")

        else :
            err_code = add(
                series_id,
                series_name,
                self.book_type_choice.GetStringSelection(),
                self.cat_dict[self.book_cat_choice.GetStringSelection()],
                auth_ids, edit_ids
            )

            if err_code == 0 :
                self.display(f"La série {series_name} a été ajoutée à la liste.")
                self.Parent.update_data("Series")
            
            elif err_code == 1 :
                self.display(f"Le code de série '{series_id}' est déjà utilisé.")
            elif err_code == 2 :
                self.display(f"La série {series_name} existe déjà.")
            else :
                self.display("Erreur inconnue.")
    
    def add_auth(self, event) :
        self.Parent.add(tab="Authors")
    
    def add_edit(self, event) :
        self.Parent.add(tab="Editors")
    
    def update_data(self, tab: str) :
        type_ = {"Authors": "auth", "Editors": "edit"}[tab]
        self.auth_edit[type_].dict = getters[type_]()
        self.auth_edit[type_].to_update = [True for _ in self.auth_edit[type_].choices]

    def display(self, text: str) :
        self.help_text.SetLabel(text)
        self.help_timer.Start()
        self.timer_tick = 0
    
    def test_timer(self, event) :
        if self.timer_tick == 500 :
            self.help_text.SetLabel(self.default_text)
            self.help_timer.Stop()
        else :
            self.timer_tick += 1

    def end_process(self, event) :
        self.help_timer.Stop()
        self.Parent.sub_frames.pop(self.id_)
        self.Destroy()