import wx

from gen_classes.author_add import AuthorWindow

class Author (AuthorWindow) :
    def __init__(self, parent, id_):
        self.id_ = id_
        super().__init__(parent)

    def end_process(self, event) :
        self.help_timer.Stop()
        self.Parent.sub_frames.pop(self.id_)
        self.Destroy()