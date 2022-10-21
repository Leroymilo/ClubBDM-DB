import wx

from gen_classes.loan import LoanWindow

from functions.loans import get_members, get_books, get_item_data, add, edit

class Loan (LoanWindow) :
    def __init__(self, parent, id_, item_id=None) :
        self.id_ = id_
        super().__init__(parent)
        self.update_data("Members")
        self.update_data("Books")

        self.is_editor = item_id is not None

        if self.is_editor :
            pass

    def update_data(self, type_: str) :
        if type_ == "Members" :
            self.member_dict = get_members()
            selection = self.member_choice.GetStringSelection()
            self.member_choice.SetItems([""] + list(self.member_dict.keys()))
            self.member_choice.SetStringSelection(selection)
        
        elif type_ == "Books" :
            selection = self.book_choice.GetStringSelection()
            self.book_choice.SetItems([""] + get_books())
            self.book_choice.SetStringSelection(selection)
        
        elif type_ == "Loans" :
            self.member_dict = get_members()
            selection = self.member_choice.GetStringSelection()
            self.member_choice.SetItems([""] + list(self.member_dict.keys()))
            self.member_choice.SetStringSelection(selection)
            
            selection = self.book_choice.GetStringSelection()
            self.book_choice.SetItems([""] + get_books())
            self.book_choice.SetStringSelection(selection)
    
    def complete(self, event):
        if self.member_choice.GetSelection() == 0 :
            self.display("Choisissez un emprunteur.")
            return
        member_name = self.member_choice.GetStringSelection()
        member_id = self.member_dict[member_name]
        
        if self.book_choice.GetSelection() == 0 :
            self.display("Choisissez un livre.")
            return
        book_id = self.book_choice.GetStringSelection()

        if self.is_editor :
            pass

        else :
            err_code = add(member_id, book_id)

            if err_code == 0 :
                self.display(f"L'emprunt de {book_id} par {member_name} a bien été enregistré.")
                self.Parent.update_data("Loans")
            
            else :
                self.display("Erreur inconnue.")

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