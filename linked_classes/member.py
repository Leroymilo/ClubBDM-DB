import wx

from gen_classes.member import MemberWindow

from functions.members import get_item_data, add, edit

# from functions.members import 

class Member (MemberWindow) :
    def __init__(self, parent, id_, item_name=None):
        self.id_ = id_
        super().__init__(parent)

        self.is_editor = item_name is not None

        if self.is_editor :
            self.SetLabel("Modifier le membre")
            self.end_button.SetLabel("Appliquer les modifications")
            item_data = get_item_data(item_name)
            self.item_id = item_data["id"]
            self.name_txt.SetValue(item_name)
            self.mail_txt.SetValue(item_data["mail"])
            self.tel_txt.SetValue(item_data["tel"])
            self.bail_txt.SetValue(item_data["bail"])
            self.BDM_status_choice.SetStringSelection(item_data["BDM"])
            self.ALIR_status_choice.SetStringSelection(item_data["ALIR"])
            self.comment_txt.SetValue(item_data["comment"])
    
    def complete(self, event) :
        name: str = self.name_txt.GetValue().strip().lstrip()
        if name == "" :
            self.display("Le nom ne doit pas être vide.")
            return
        
        mail: str = self.mail_txt.GetValue().strip().lstrip()
        tel: str = self.tel_txt.GetValue().strip().lstrip()
        if mail == "" and tel == "" :
            self.display("Il faut au moins un moyen de contact.")

        bail: str = self.bail_txt.GetValue()
        try :
            bail = float(bail.strip().lstrip())
        except :
            self.display("La caution doit être numérique")
            return
        
        BDMstatus = self.BDM_status_choice.GetStringSelection()
        ALIRstatus = self.ALIR_status_choice.GetStringSelection()
        if BDMstatus in {"Membre +", "Membre actif +"} :
            max_loan = bail//8
        elif BDMstatus == "Bureau" :
            max_loan = 20
        else :
            max_loan = 0
        
        if self.is_editor :
            err_code = edit(
                self.item_id, name, mail, tel, max_loan, 30, bail,
                BDMstatus, ALIRstatus, self.comment_txt.GetValue()
            )
            
            if err_code == 0 :
                self.Parent.update_data("Members")
                self.Close()

            elif err_code == 1 :
                self.display(f"Le membre {name} existe déjà.")
            else :
                self.display("Erreur inconnue")

        else :
            err_code = add(
                name, mail, tel, max_loan, 30, bail,
                BDMstatus, ALIRstatus, self.comment_txt.GetValue()
            )

            if err_code == 0 :
                self.display(f"Le membre {name} a été ajouté à la liste.")
                self.Parent.update_data("Members")

            elif err_code == 1 :
                self.display(f"Le membre {name} existe déjà.")
            else :
                self.display("Erreur inconnue")

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