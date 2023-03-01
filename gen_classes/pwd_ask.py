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
## Class PwdDlg
###########################################################################

class PwdDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.image = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.image, 0, wx.ALL, 5 )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Veuillez vous connecter avec un des niveaux d'accès.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer4.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Si vous voulez accéder à la liste des livres disponibles, contactez le bureau du club BD-Mangas", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer4.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Si un mot de passe a été perdu, contactez Lecorché Adriaan.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer4.Add( self.m_staticText3, 0, wx.ALL, 5 )


		bSizer11.Add( bSizer4, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer11, 1, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"Nom d'utilisateur :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )

		bSizer21.Add( self.m_staticText41, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.unm_ctrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.unm_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( bSizer21, 1, wx.EXPAND, 5 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText42 = wx.StaticText( self, wx.ID_ANY, u"Mot de passe :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )

		bSizer22.Add( self.m_staticText42, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.pwd_ctrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD|wx.TE_PROCESS_ENTER )
		bSizer22.Add( self.pwd_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( bSizer22, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		self.help_txt = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.help_txt.Wrap( -1 )

		bSizer1.Add( self.help_txt, 0, wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.pwd_ctrl.Bind( wx.EVT_TEXT_ENTER, self.send_pwd )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def send_pwd( self, event ):
		event.Skip()


