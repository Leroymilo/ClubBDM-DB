import wx

from gen_classes.loan import LoanWindow

from functions.loans import get_members, get_books, get_item_data, add, edit

class Loan (LoanWindow) :
    def __init__(self, parent, id_, item_id=None) :
        self.id_ = id_
        super().__init__(parent)
        
        self.is_editor = item_id is not None

        self.update_data("Members")
        self.update_data("Books")

        if self.is_editor :
            self.SetLabel("Modifier l'emprunt")
            item_data = get_item_data(item_id)
            self.loan_id = item_data["loan_id"]
            self.member_dict[item_id[0]] = item_data["member_id"]
            if item_id[0] not in self.member_choice.GetStrings() :
                self.member_choice.Append(item_id[0])
            self.book_choice.Append(item_id[1])
            self.member_choice.SetStringSelection(item_id[0])
            self.book_choice.SetStringSelection(item_id[1])
            self.end_button.SetLabel("Appliquer les modifications")
            
    def update_data(self, type_: str) :
        if type_ == "Members" :
            self.member_dict = get_members()
            selection = self.member_choice.GetStringSelection()
            self.member_choice.SetItems(
                list(set(self.member_dict.keys()) | {"", selection})
            )
            self.member_choice.SetStringSelection(selection)
        
        elif type_ == "Books" :
            selection = self.book_choice.GetStringSelection()
            self.book_choice.SetItems(
                list(get_books() | {"", selection})
            )
            self.book_choice.SetStringSelection(selection)
        
        elif type_ == "Loans" :
            self.member_dict = get_members()
            selection = self.member_choice.GetStringSelection()
            self.member_choice.SetItems(
                list(set(self.member_dict.keys()) | {"", selection})
            )
            self.member_choice.SetStringSelection(selection)
            
            selection = self.book_choice.GetStringSelection()
            self.book_choice.SetItems(
                list(get_books() | {"", selection})
            )
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
            err_code = edit(self.loan_id, member_id, book_id)

            if err_code == 0 :
                self.Parent.update_data("Loans")
                self.Close()
            
            else :
                self.display("Erreur inconnue")

        else :
            err_code = add(member_id, book_id)

            if err_code == 0 :
                self.display(f"L'emprunt de {book_id} par {member_name} a bien été enregistré.")
                self.Parent.update_data("Loans")
            
            else :
                self.display("Erreur inconnue.")

    def display(self, text: str) :
        self.Parent.display_status(text)

    def end_process(self, event) :
        self.Parent.sub_frames.pop(self.id_)
        self.Destroy()
    
    def resize(self, event: wx.Event) :
        print(self.Size)
        event.Skip()