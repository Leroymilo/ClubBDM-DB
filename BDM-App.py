from linked_classes.main_app import Main
from db_init import *
import wx

app = wx.App()
frame = Main(None)
# frame.Show()
frame.ShowFullScreen(True)
app.MainLoop()

db.close()