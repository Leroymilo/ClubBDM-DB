# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class AuthorWindow
###########################################################################

class AuthorWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Ajouter un auteur", pos = wx.DefaultPosition, size = wx.Size( 312,134 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_TOOL_WINDOW|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.help_timer = wx.Timer()
		self.help_timer.SetOwner( self, wx.ID_ANY )
		global_sizer = wx.BoxSizer( wx.VERTICAL )

		self.global_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		v_sizer = wx.BoxSizer( wx.VERTICAL )

		h_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self.global_panel, wx.ID_ANY, u"Nom :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		h_sizer.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.name_txt = wx.TextCtrl( self.global_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer.Add( self.name_txt, 1, wx.ALL, 5 )


		v_sizer.Add( h_sizer, 0, wx.EXPAND, 5 )

		self.help_text = wx.StaticText( self.global_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.help_text.Wrap( -1 )

		v_sizer.Add( self.help_text, 0, wx.ALL, 5 )

		self.add_button = wx.Button( self.global_panel, wx.ID_ANY, u"Ajouter l'auteur", wx.DefaultPosition, wx.DefaultSize, 0 )
		v_sizer.Add( self.add_button, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		self.global_panel.SetSizer( v_sizer )
		self.global_panel.Layout()
		v_sizer.Fit( self.global_panel )
		global_sizer.Add( self.global_panel, 1, wx.EXPAND, 5 )


		self.SetSizer( global_sizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_ACTIVATE, self.on_activate )
		self.Bind( wx.EVT_CLOSE, self.end_process )
		self.Bind( wx.EVT_ICONIZE, self.on_iconize )
		self.add_button.Bind( wx.EVT_BUTTON, self.add )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_activate( self, event ):
		event.Skip()

	def end_process( self, event ):
		event.Skip()

	def on_iconize( self, event ):
		event.Skip()

	def add( self, event ):
		event.Skip()


