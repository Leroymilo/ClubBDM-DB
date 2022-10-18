import wx

from gen_classes.editor_add import EditorWindow

class Editor (EditorWindow) :
    def __init__(self, parent, id_):
        self.id_ = id_
        super().__init__(parent)