import wx

from gen_classes.author_add import AuthorWindow

from functions.authors import add

class Author (AuthorWindow) :
    def __init__(self, parent, id_):
        self.id_ = id_
        super().__init__(parent)
    
    def add(self, event) :
        name = self.name_txt.GetValue().strip(' ').lstrip(' ')
        if name == "" :
            self.display("Le nom ne peut pas être vide")
            return
        
        err_code = add(name)

        if err_code == 1:
            self.display(f"L'auteur {name} existe déjà")
        elif err_code == 0 :
            self.display(f"L'auteur {name} a été ajouté à la liste")
            self.Parent.update_data("Authors")
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