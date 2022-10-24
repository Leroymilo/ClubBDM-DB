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
## Class LoanEndWindow
###########################################################################

class LoanEndWindow ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Fin d'emprunt", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.CAPTION )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Êtes-vous sûr(e) de vouloir mettre fin à cet emprunt?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.yes_butt = wx.Button( self, wx.ID_ANY, u"Oui", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.yes_butt, 0, wx.ALL, 5 )

		self.no_butt = wx.Button( self, wx.ID_ANY, u"Non", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.no_butt, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.yes_butt.Bind( wx.EVT_BUTTON, self.Yes )
		self.no_butt.Bind( wx.EVT_BUTTON, self.No )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def Yes( self, event ):
		event.Skip()

	def No( self, event ):
		event.Skip()


