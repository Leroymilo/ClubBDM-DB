from linked_classes.main_app import Main
from db_init import *
import wx

app = wx.App()
frame = Main(None)
app.MainLoop()

db.close()