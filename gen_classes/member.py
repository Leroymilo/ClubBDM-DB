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
## Class MemberWindow
###########################################################################

class MemberWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Ajouter un membre", pos = wx.DefaultPosition, size = wx.Size( -1,262 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_TOOL_WINDOW|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		v_sizer = wx.BoxSizer( wx.VERTICAL )

		h_sizer_1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Nom/Prénom :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		h_sizer_1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.name_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_1.Add( self.name_txt, 1, wx.ALL, 5 )


		v_sizer.Add( h_sizer_1, 0, wx.EXPAND, 5 )

		h_sizer_2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Mail :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		h_sizer_2.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.mail_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_2.Add( self.mail_txt, 1, wx.ALL, 5 )

		self.m_staticline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		h_sizer_2.Add( self.m_staticline, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, u"Tel :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		h_sizer_2.Add( self.m_staticText22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.tel_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_2.Add( self.tel_txt, 1, wx.ALL, 5 )


		v_sizer.Add( h_sizer_2, 0, wx.EXPAND, 5 )

		h_sizer_3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"Statut BDM :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		h_sizer_3.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		BDM_status_choiceChoices = [ u"Non-membre", u"Membre", u"Membre +", u"Membre actif", u"Membre actif +", u"Bureau" ]
		self.BDM_status_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, BDM_status_choiceChoices, 0 )
		self.BDM_status_choice.SetSelection( 0 )
		h_sizer_3.Add( self.BDM_status_choice, 1, wx.ALL, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		h_sizer_3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText32 = wx.StaticText( self, wx.ID_ANY, u"Statut ALIR :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )

		h_sizer_3.Add( self.m_staticText32, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		ALIR_status_choiceChoices = [ u"Non-membre", u"Membre" ]
		self.ALIR_status_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ALIR_status_choiceChoices, 0 )
		self.ALIR_status_choice.SetSelection( 0 )
		h_sizer_3.Add( self.ALIR_status_choice, 1, wx.ALL, 5 )


		v_sizer.Add( h_sizer_3, 0, wx.EXPAND, 5 )

		h_sizer_4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"Caution :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )

		h_sizer_4.Add( self.m_staticText41, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.bail_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_4.Add( self.bail_txt, 0, wx.ALL, 5 )

		self.m_staticText42 = wx.StaticText( self, wx.ID_ANY, u"€", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )

		h_sizer_4.Add( self.m_staticText42, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		v_sizer.Add( h_sizer_4, 0, wx.EXPAND, 5 )

		h_sizer_5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Commentaires :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		h_sizer_5.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.comment_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_5.Add( self.comment_txt, 1, wx.ALL, 5 )


		v_sizer.Add( h_sizer_5, 0, wx.EXPAND, 5 )

		self.help_text = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.help_text.Wrap( -1 )

		v_sizer.Add( self.help_text, 0, wx.ALL|wx.EXPAND, 5 )

		self.end_button = wx.Button( self, wx.ID_ANY, u"Ajouter le membre", wx.DefaultPosition, wx.DefaultSize, 0 )
		v_sizer.Add( self.end_button, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		self.SetSizer( v_sizer )
		self.Layout()
		self.help_timer = wx.Timer()
		self.help_timer.SetOwner( self, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.end_process )
		self.end_button.Bind( wx.EVT_BUTTON, self.complete )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def end_process( self, event ):
		event.Skip()

	def complete( self, event ):
		event.Skip()


