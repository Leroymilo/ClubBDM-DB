from linked_classes.main_app import Main
from linked_classes.pwd_ask import Pwd
from db_init import *
import wx

app = wx.App()

if Pwd(None).ShowModal() :

    frame = Main(None)
    frame.Show()
    # frame.Maximize()
    app.MainLoop()

db.close()