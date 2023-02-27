from linked_classes.main_app import Main
from linked_classes.pwd_ask import Pwd
from db_init import *
import wx

app = wx.App()

secu_lvl = Pwd(None).ShowModal()

if secu_lvl :

    frame = Main(None, secu_lvl)
    frame.Show()
    # frame.Maximize()
    app.MainLoop()

db.close()