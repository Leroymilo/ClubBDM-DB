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
## Class SeriesWindow
###########################################################################

class SeriesWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Ajouter une série", pos = wx.DefaultPosition, size = wx.Size( 425,420 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_TOOL_WINDOW|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		v_sizer = wx.BoxSizer( wx.VERTICAL )

		h_sizer_1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Nom de la série :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		h_sizer_1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.series_name_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_1.Add( self.series_name_txt, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		v_sizer.Add( h_sizer_1, 0, wx.EXPAND, 5 )

		h_sizer_2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Code de la série (5 lettres en majuscules) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		h_sizer_2.Add( self.m_staticText2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.series_id_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		h_sizer_2.Add( self.series_id_txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		v_sizer.Add( h_sizer_2, 0, wx.EXPAND, 5 )

		h_sizer_3 = wx.BoxSizer( wx.HORIZONTAL )

		h_sizer_31 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText30 = wx.StaticText( self, wx.ID_ANY, u"Type de livres :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )

		h_sizer_31.Add( self.m_staticText30, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		book_type_choiceChoices = [ wx.EmptyString, u"bd", u"comics", u"manga", u"roman" ]
		self.book_type_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, book_type_choiceChoices, 0 )
		self.book_type_choice.SetSelection( 0 )
		h_sizer_31.Add( self.book_type_choice, 0, wx.ALL, 5 )


		h_sizer_3.Add( h_sizer_31, 1, 0, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		h_sizer_3.Add( self.m_staticline1, 0, wx.ALL|wx.EXPAND, 5 )

		h_sizer_32 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"Catégorie :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		h_sizer_32.Add( self.m_staticText31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		book_cat_choiceChoices = []
		self.book_cat_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, book_cat_choiceChoices, wx.CB_SORT )
		self.book_cat_choice.SetSelection( 0 )
		h_sizer_32.Add( self.book_cat_choice, 0, wx.ALL, 5 )


		h_sizer_3.Add( h_sizer_32, 1, 0, 5 )


		v_sizer.Add( h_sizer_3, 0, wx.EXPAND, 5 )

		h_sizer_4 = wx.BoxSizer( wx.HORIZONTAL )

		v_sizer_41 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"Auteurs :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )

		v_sizer_41.Add( self.m_staticText41, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.scroll_auth = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.scroll_auth.SetScrollRate( 5, 5 )
		v_sizer_auth_choices = wx.BoxSizer( wx.VERTICAL )


		self.scroll_auth.SetSizer( v_sizer_auth_choices )
		self.scroll_auth.Layout()
		v_sizer_auth_choices.Fit( self.scroll_auth )
		v_sizer_41.Add( self.scroll_auth, 1, wx.ALL|wx.EXPAND, 5 )

		self.add_auth_button = wx.Button( self, wx.ID_ANY, u"Nouvel auteur", wx.DefaultPosition, wx.DefaultSize, 0 )
		v_sizer_41.Add( self.add_auth_button, 0, wx.ALL|wx.EXPAND, 5 )


		h_sizer_4.Add( v_sizer_41, 1, wx.EXPAND, 5 )

		v_sizer_42 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText42 = wx.StaticText( self, wx.ID_ANY, u"Éditeurs :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )

		v_sizer_42.Add( self.m_staticText42, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.scroll_edit = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.scroll_edit.SetScrollRate( 5, 5 )
		v_sizer_edit_choices = wx.BoxSizer( wx.VERTICAL )


		self.scroll_edit.SetSizer( v_sizer_edit_choices )
		self.scroll_edit.Layout()
		v_sizer_edit_choices.Fit( self.scroll_edit )
		v_sizer_42.Add( self.scroll_edit, 1, wx.EXPAND |wx.ALL, 5 )

		self.add_edit_button = wx.Button( self, wx.ID_ANY, u"Nouvel éditeur", wx.DefaultPosition, wx.DefaultSize, 0 )
		v_sizer_42.Add( self.add_edit_button, 0, wx.ALL|wx.EXPAND, 5 )


		h_sizer_4.Add( v_sizer_42, 1, wx.EXPAND, 5 )


		v_sizer.Add( h_sizer_4, 1, wx.EXPAND, 5 )

		self.help_text = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.help_text.Wrap( -1 )

		v_sizer.Add( self.help_text, 0, wx.ALL, 5 )

		self.add_series_button = wx.Button( self, wx.ID_ANY, u"Créer la série", wx.DefaultPosition, wx.DefaultSize, 0 )
		v_sizer.Add( self.add_series_button, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		self.SetSizer( v_sizer )
		self.Layout()
		self.help_timer = wx.Timer()
		self.help_timer.SetOwner( self, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.end_process )
		self.add_auth_button.Bind( wx.EVT_BUTTON, self.add_auth )
		self.add_edit_button.Bind( wx.EVT_BUTTON, self.add_edit )
		self.add_series_button.Bind( wx.EVT_BUTTON, self.add_series )
		self.Bind( wx.EVT_TIMER, self.test_timer, id=wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def end_process( self, event ):
		event.Skip()

	def add_auth( self, event ):
		event.Skip()

	def add_edit( self, event ):
		event.Skip()

	def add_series( self, event ):
		event.Skip()

	def test_timer( self, event ):
		event.Skip()


