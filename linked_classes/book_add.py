import wx

from gen_classes.book_add import BookWindow

from functions.books import get_item_data, get_series, add

class Book(BookWindow) :
    def __init__(self, parent, id_, item_id=None) :
        super().__init__(parent)
        self.id_ = id_
        self.series_dict = get_series()
        self.series_choice.Set([""] + list(self.series_dict.keys()))
        self.timer_tick = 0

        self.is_editor = item_id is not None

        if self.is_editor :
            item_data = get_item_data(item_id)
            self.SetLabel("Modifier le livre")
            self.vol_name_txt.SetValue(item_data["book_name"])
            self.series_choice.SetStringSelection(item_data["series_name"])
            self.series_choice.Disable()
            self.add_series_button.Disable()
            self.vol_nb_spin.SetValue(item_data["vol_nb"])
            self.vol_nb_spin.Disable()
            self.condition_spin.SetValue(item_data["condition"])
            self.com_txt.SetValue(item_data["comment"])
            self.add_book_button.SetLabel("Appliquer la modification")
    
    def add_book(self, event) :
        if self.series_choice.GetSelection() == 0 :
            self.display("Choisissez une série ou créez-en une nouvelle.")
            return
        
        if self.is_editor :
            print("book modified")
            self.Close()

        else :
            book_id = add(
                self.series_dict[self.series_choice.GetStringSelection()],
                self.vol_nb_spin.GetValue(),
                self.condition_spin.GetValue(),
                self.vol_name_txt.GetValue().strip(' ').lstrip(' '),
                self.com_txt.GetValue().strip(' ').lstrip(' ')
            )
            
            if book_id is None :
                self.display("Erreur inconnue")
            else :
                self.display(f"Livre {book_id} ajouté à la collection")
                self.Parent.update_data("Books")
    
    def add_series(self, event) :
        self.Parent.add(tab="Series")
    
    def update_data(self, tab: str=None) :
        if not self.is_editor :
            self.series_dict = get_series()
            old_choice = self.series_choice.GetStringSelection()
            self.series_choice.Set([""] + list(self.series_dict.keys()))
            self.series_choice.SetStringSelection(old_choice)
    
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