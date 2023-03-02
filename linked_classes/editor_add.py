import wx

from gen_classes.editor_add import EditorWindow

from functions.editors import add

class Editor (EditorWindow) :
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
            self.display(f"L'éditeur {name} existe déjà")
        elif err_code == 0 :
            self.display(f"L'éditeur {name} a été ajouté à la liste")
            self.Parent.update_data("Editors")
        else :
            self.display("Erreur inconnue")

    def display(self, text: str) :
        self.Parent.display_status(text)

    def end_process(self, event) :
        self.Parent.sub_frames.pop(self.id_)
        self.Destroy()