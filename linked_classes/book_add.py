import wx

from gen_classes.book_add import BookWindow

class Book(BookWindow) :
    def __init__(self, parent):
        super().__init__(parent)
        self.Show()