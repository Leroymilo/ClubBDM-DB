import wx

from gen_classes.loan_end import LoanEndWindow

class LoanEnd (LoanEndWindow) :
    def __init__(self, parent):
        super().__init__(parent)
    
    def Yes(self, event) :
        self.EndModal(1)

    def No(self, event) :
        self.EndModal(0)
    
    def Close(self, force=False) :
        self.EndModal(0)
        return super().Close(force)