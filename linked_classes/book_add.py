import wx

from gen_classes.book_add import BookWindow
from linked_classes.series_add import Series

from functions.books import get_series, add

class Book(BookWindow) :
    def __init__(self, parent, id_) :
        super().__init__(parent)
        self.id_ = id_
        self.series_dict = get_series()
        self.series_choice.Set([""] + list(self.series_dict.keys()))
        self.timer_tick = 0

        self.sub_frames = []
        sizer_h = self.GetSizer().GetSize()[1]
        self.SetSize(-1, -1, -1, sizer_h+10)
    
    def add_book(self, event) :
        if self.series_choice.GetSelection() == -1 :
            self.display("Choisissez une série ou créez-en une nouvelle.")
            return
        book_id = add(
            self.series_dict[self.series_choice.GetStringSelection()],
            self.vol_nb_spin.GetValue(),
            self.condition_spin.GetValue(),
            self.vol_name_txt.GetValue(),
            self.com_txt.GetValue()
        )
        self.display(f"Livre {book_id} ajouté à la collection")

        p = self.Parent
        if p.id_ == -1 :
            if p.notebook.GetSelection() == 0 :
                p.search_table(None)
    
    def add_series(self, event) :
        sub_frame = Series(self, id_=len(self.sub_frames))
        self.sub_frames.append(sub_frame)
        sub_frame.Show()
    
    def update_series(self) :
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