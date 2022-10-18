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
## Class BookWindow
###########################################################################

class BookWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Ajouter un livre", pos = wx.DefaultPosition, size = wx.Size( 367,296 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_TOOL_WINDOW|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		v_sizer = wx.BoxSizer( wx.VERTICAL )

		h_sizer_1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Nom du volume :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		h_sizer_1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.vol_name_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_1.Add( self.vol_name_txt, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		v_sizer.Add( h_sizer_1, 0, wx.EXPAND, 5 )

		h_sizer_2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Série :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		h_sizer_2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		series_choiceChoices = []
		self.series_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, series_choiceChoices, wx.CB_SORT )
		self.series_choice.SetSelection( 0 )
		h_sizer_2.Add( self.series_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.add_series_button = wx.Button( self, wx.ID_ANY, u"Nouvelle série", wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_2.Add( self.add_series_button, 0, wx.ALL, 5 )


		v_sizer.Add( h_sizer_2, 0, wx.EXPAND, 5 )

		h_sizer_3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Numéro de volume :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		h_sizer_3.Add( self.m_staticText3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.vol_nb_spin = wx.SpinCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.SP_WRAP, 1, 999, 1 )
		h_sizer_3.Add( self.vol_nb_spin, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		v_sizer.Add( h_sizer_3, 0, wx.EXPAND, 5 )

		h_sizer_4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Etat :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		h_sizer_4.Add( self.m_staticText4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.condition_spin = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.SP_WRAP, 1, 10, 10 )
		h_sizer_4.Add( self.condition_spin, 0, wx.ALL, 5 )


		v_sizer.Add( h_sizer_4, 0, wx.EXPAND, 5 )

		h_sizer_5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Commentaire :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		h_sizer_5.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.com_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_5.Add( self.com_txt, 1, wx.ALL, 5 )


		v_sizer.Add( h_sizer_5, 0, wx.EXPAND, 5 )

		self.help_text = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.help_text.Wrap( -1 )

		v_sizer.Add( self.help_text, 0, wx.ALL|wx.EXPAND, 5 )

		self.add_book_button = wx.Button( self, wx.ID_ANY, u"Ajouter livre", wx.DefaultPosition, wx.DefaultSize, 0 )
		v_sizer.Add( self.add_book_button, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		self.SetSizer( v_sizer )
		self.Layout()
		self.help_timer = wx.Timer()
		self.help_timer.SetOwner( self, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_ACTIVATE, self.on_activate )
		self.Bind( wx.EVT_CLOSE, self.end_process )
		self.Bind( wx.EVT_ICONIZE, self.on_iconize )
		self.add_series_button.Bind( wx.EVT_BUTTON, self.add_series )
		self.add_book_button.Bind( wx.EVT_BUTTON, self.add_book )
		self.Bind( wx.EVT_TIMER, self.test_timer, id=wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_activate( self, event ):
		event.Skip()

	def end_process( self, event ):
		event.Skip()

	def on_iconize( self, event ):
		event.Skip()

	def add_series( self, event ):
		event.Skip()

	def add_book( self, event ):
		event.Skip()

	def test_timer( self, event ):
		event.Skip()


