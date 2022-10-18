import wx

from gen_classes.author_add import AuthorWindow

class Author (AuthorWindow) :
    def __init__(self, parent, id_):
        self.id_ = id_
        super().__init__(parent)