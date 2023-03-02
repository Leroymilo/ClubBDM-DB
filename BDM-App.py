import wx

from linked_classes.main_app import Main
from linked_classes.pwd_ask import Pwd

from db_init import *

app = wx.App()

data = {}
secu_lvl = Pwd(None, data).ShowModal()

db.__init__(data["user"], data["pwd"])

if secu_lvl :

    frame = Main(None, secu_lvl)
    frame.Show()
    # frame.Maximize()
    print("start main loop")
    app.MainLoop()
    print("end main loop")

db.close()