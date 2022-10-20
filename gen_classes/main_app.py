# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview
import wx.adv

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"App Club BDManga", pos = wx.DefaultPosition, size = wx.Size( 901,675 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		top_sizer = wx.BoxSizer( wx.VERTICAL )

		self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.books = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		book_v_sizer = wx.BoxSizer( wx.VERTICAL )

		book_top_h_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.book_add = wx.Button( self.books, wx.ID_ANY, u"Ajouter un livre", wx.DefaultPosition, wx.DefaultSize, 0 )
		book_top_h_sizer.Add( self.book_add, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline0 = wx.StaticLine( self.books, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		book_top_h_sizer.Add( self.m_staticline0, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText10 = wx.StaticText( self.books, wx.ID_ANY, u"Rechercher :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		book_top_h_sizer.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.book_search_val = wx.TextCtrl( self.books, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		book_top_h_sizer.Add( self.book_search_val, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText20 = wx.StaticText( self.books, wx.ID_ANY, u"dans :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		book_top_h_sizer.Add( self.m_staticText20, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		book_search_colChoices = [ u"série", u"auteur", u"éditeur" ]
		self.book_search_col = wx.Choice( self.books, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, book_search_colChoices, 0 )
		self.book_search_col.SetSelection( 0 )
		book_top_h_sizer.Add( self.book_search_col, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		book_v_sizer.Add( book_top_h_sizer, 0, 0, 5 )

		self.book_display = wx.dataview.DataViewListCtrl( self.books, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		self.book_col_0 = self.book_display.AppendTextColumn( u"Cotation", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.book_col_1 = self.book_display.AppendTextColumn( u"Nom", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.book_col_2 = self.book_display.AppendTextColumn( u"Série", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.book_col_3 = self.book_display.AppendTextColumn( u"Num", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_RIGHT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.book_col_4 = self.book_display.AppendTextColumn( u"État", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_RIGHT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.book_col_5 = self.book_display.AppendTextColumn( u"Dispo", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_RIGHT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.book_col_6 = self.book_display.AppendTextColumn( u"Ajouté le", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_RIGHT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.book_col_7 = self.book_display.AppendTextColumn( u"Commentaires", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		book_v_sizer.Add( self.book_display, 1, wx.ALL|wx.EXPAND, 5 )


		self.books.SetSizer( book_v_sizer )
		self.books.Layout()
		book_v_sizer.Fit( self.books )
		self.notebook.AddPage( self.books, u"Livres", True )
		self.series = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		series_v_sizer = wx.BoxSizer( wx.VERTICAL )

		series_top_h_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.series_add = wx.Button( self.series, wx.ID_ANY, u"Ajouter une série", wx.DefaultPosition, wx.DefaultSize, 0 )
		series_top_h_sizer.Add( self.series_add, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline3 = wx.StaticLine( self.series, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		series_top_h_sizer.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText13 = wx.StaticText( self.series, wx.ID_ANY, u"Rechercher :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		series_top_h_sizer.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.series_search_val = wx.TextCtrl( self.series, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		series_top_h_sizer.Add( self.series_search_val, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText23 = wx.StaticText( self.series, wx.ID_ANY, u"dans :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )

		series_top_h_sizer.Add( self.m_staticText23, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		series_search_colChoices = [ u"nom", u"type", u"catégorie", u"auteur", u"éditeur" ]
		self.series_search_col = wx.Choice( self.series, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, series_search_colChoices, 0 )
		self.series_search_col.SetSelection( 0 )
		series_top_h_sizer.Add( self.series_search_col, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		series_v_sizer.Add( series_top_h_sizer, 0, 0, 5 )

		self.series_display = wx.dataview.DataViewListCtrl( self.series, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		self.series_col_1 = self.series_display.AppendTextColumn( u"Code", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.series_col_2 = self.series_display.AppendTextColumn( u"Nom", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.series_col_3 = self.series_display.AppendTextColumn( u"Type", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.series_col_4 = self.series_display.AppendTextColumn( u"Catégorie", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.series_col_5 = self.series_display.AppendTextColumn( u"Auteurs", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.series_col_6 = self.series_display.AppendTextColumn( u"Éditeurs", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		series_v_sizer.Add( self.series_display, 1, wx.ALL|wx.EXPAND, 5 )


		self.series.SetSizer( series_v_sizer )
		self.series.Layout()
		series_v_sizer.Fit( self.series )
		self.notebook.AddPage( self.series, u"Séries", False )
		self.members = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		member_v_sizer = wx.BoxSizer( wx.VERTICAL )

		member_top_h_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.member_add = wx.Button( self.members, wx.ID_ANY, u"Ajouter un membre", wx.DefaultPosition, wx.DefaultSize, 0 )
		member_top_h_sizer.Add( self.member_add, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self.members, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		member_top_h_sizer.Add( self.m_staticline1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText11 = wx.StaticText( self.members, wx.ID_ANY, u"Rechercher :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		member_top_h_sizer.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.member_search_val = wx.TextCtrl( self.members, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		member_top_h_sizer.Add( self.member_search_val, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText21 = wx.StaticText( self.members, wx.ID_ANY, u"dans :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		member_top_h_sizer.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		member_search_colChoices = [ u"nom", u"statut" ]
		self.member_search_col = wx.Choice( self.members, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, member_search_colChoices, 0 )
		self.member_search_col.SetSelection( 0 )
		member_top_h_sizer.Add( self.member_search_col, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticline7 = wx.StaticLine( self.members, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		member_top_h_sizer.Add( self.m_staticline7, 0, wx.EXPAND|wx.ALL, 5 )

		self.m_checkBox1 = wx.CheckBox( self.members, wx.ID_ANY, u"Afficher inactifs :", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		member_top_h_sizer.Add( self.m_checkBox1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		member_v_sizer.Add( member_top_h_sizer, 0, 0, 5 )

		self.member_display = wx.dataview.DataViewListCtrl( self.members, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		self.member_col_1 = self.member_display.AppendTextColumn( u"Nom", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_2 = self.member_display.AppendTextColumn( u"Mail", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_3 = self.member_display.AppendTextColumn( u"Téléphone", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_4 = self.member_display.AppendTextColumn( u"Emprunts", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_5 = self.member_display.AppendTextColumn( u"Durée emprunts", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_6 = self.member_display.AppendTextColumn( u"Caution", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_7 = self.member_display.AppendTextColumn( u"Statut BDM", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_8 = self.member_display.AppendTextColumn( u"Statut ALIR", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_HIDDEN|wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_9 = self.member_display.AppendTextColumn( u"Dernier emprunt", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_HIDDEN|wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_10 = self.member_display.AppendTextColumn( u"Archivé", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_HIDDEN|wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.member_col_11 = self.member_display.AppendTextColumn( u"Commentaires", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		member_v_sizer.Add( self.member_display, 1, wx.ALL|wx.EXPAND, 5 )


		self.members.SetSizer( member_v_sizer )
		self.members.Layout()
		member_v_sizer.Fit( self.members )
		self.notebook.AddPage( self.members, u"Membres", False )
		self.loans = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		loan_v_sizer = wx.BoxSizer( wx.VERTICAL )

		loan_top_h_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.loan_add = wx.Button( self.loans, wx.ID_ANY, u"Nouvel emprunt", wx.DefaultPosition, wx.DefaultSize, 0 )
		loan_top_h_sizer.Add( self.loan_add, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self.loans, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		loan_top_h_sizer.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		self.loan_end = wx.Button( self.loans, wx.ID_ANY, u"Fin emprunt", wx.DefaultPosition, wx.DefaultSize, 0 )
		loan_top_h_sizer.Add( self.loan_end, 0, wx.ALL, 5 )

		self.m_staticline5 = wx.StaticLine( self.loans, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		loan_top_h_sizer.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText12 = wx.StaticText( self.loans, wx.ID_ANY, u"Rechercher :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		loan_top_h_sizer.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.loan_search_val = wx.TextCtrl( self.loans, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		loan_top_h_sizer.Add( self.loan_search_val, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText22 = wx.StaticText( self.loans, wx.ID_ANY, u"dans :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		loan_top_h_sizer.Add( self.m_staticText22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		loan_search_colChoices = [ u"Utilisateur", u"Livre" ]
		self.loan_search_col = wx.Choice( self.loans, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, loan_search_colChoices, 0 )
		self.loan_search_col.SetSelection( 0 )
		loan_top_h_sizer.Add( self.loan_search_col, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticline8 = wx.StaticLine( self.loans, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		loan_top_h_sizer.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_checkBox2 = wx.CheckBox( self.loans, wx.ID_ANY, u"Afficher archivés :", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		loan_top_h_sizer.Add( self.m_checkBox2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		loan_v_sizer.Add( loan_top_h_sizer, 0, 0, 5 )

		self.loan_display = wx.dataview.DataViewListCtrl( self.loans, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		self.loan_col_1 = self.loan_display.AppendTextColumn( u"Utilisateur", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.loan_col_2 = self.loan_display.AppendTextColumn( u"Livre", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.loan_col_3 = self.loan_display.AppendTextColumn( u"Date d'emprunt", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.loan_col_4 = self.loan_display.AppendTextColumn( u"Retour au plus tard", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		self.loan_col_5 = self.loan_display.AppendTextColumn( u"Date de retour", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_HIDDEN|wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
		loan_v_sizer.Add( self.loan_display, 1, wx.ALL|wx.EXPAND, 5 )


		self.loans.SetSizer( loan_v_sizer )
		self.loans.Layout()
		loan_v_sizer.Fit( self.loans )
		self.notebook.AddPage( self.loans, u"Emprunts", False )
		self.queries = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		query_v_sizer = wx.BoxSizer( wx.VERTICAL )

		query_h_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.run_query_button = wx.Button( self.queries, wx.ID_ANY, u"Run query", wx.DefaultPosition, wx.DefaultSize, 0 )
		query_h_sizer.Add( self.run_query_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.query_tuto_link = wx.adv.HyperlinkCtrl( self.queries, wx.ID_ANY, u"Tutoriel utilisation panneau SQL", u"https://github.com/Leroymilo/ClubBDM-DB/blob/main/documentation/tuto%20SQL.md", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		query_h_sizer.Add( self.query_tuto_link, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.query_structure_link = wx.adv.HyperlinkCtrl( self.queries, wx.ID_ANY, u"Structure de la base", u"https://github.com/Leroymilo/ClubBDM-DB/blob/main/documentation/structure%20db.md", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		query_h_sizer.Add( self.query_structure_link, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		query_v_sizer.Add( query_h_sizer, 0, wx.EXPAND, 5 )

		self.query_text = wx.TextCtrl( self.queries, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_PROCESS_TAB )
		query_v_sizer.Add( self.query_text, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline9 = wx.StaticLine( self.queries, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		query_v_sizer.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )

		self.query_result = wx.dataview.DataViewListCtrl( self.queries, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		query_v_sizer.Add( self.query_result, 1, wx.ALL|wx.EXPAND, 5 )


		self.queries.SetSizer( query_v_sizer )
		self.queries.Layout()
		query_v_sizer.Fit( self.queries )
		self.notebook.AddPage( self.queries, u"Requêtes SQL", False )

		top_sizer.Add( self.notebook, 1, wx.ALL|wx.EXPAND, 5 )

		self.help_text = wx.StaticText( self, wx.ID_ANY, u"display help here", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.help_text.Wrap( -1 )

		top_sizer.Add( self.help_text, 0, wx.ALL, 5 )


		self.SetSizer( top_sizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_ACTIVATE, self.on_activate )
		self.Bind( wx.EVT_ICONIZE, self.on_iconize )
		self.notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.load_display )
		self.book_add.Bind( wx.EVT_BUTTON, self.add )
		self.book_search_val.Bind( wx.EVT_TEXT_ENTER, self.search_table )
		self.book_display.Bind( wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit, id = wx.ID_ANY )
		self.series_add.Bind( wx.EVT_BUTTON, self.add )
		self.series_search_val.Bind( wx.EVT_TEXT_ENTER, self.search_table )
		self.series_display.Bind( wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit, id = wx.ID_ANY )
		self.member_add.Bind( wx.EVT_BUTTON, self.add )
		self.member_search_val.Bind( wx.EVT_TEXT_ENTER, self.search_table )
		self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.toggle_archived )
		self.member_display.Bind( wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit, id = wx.ID_ANY )
		self.loan_add.Bind( wx.EVT_BUTTON, self.add )
		self.loan_end.Bind( wx.EVT_BUTTON, self.end_loan )
		self.loan_search_val.Bind( wx.EVT_TEXT_ENTER, self.search_table )
		self.m_checkBox2.Bind( wx.EVT_CHECKBOX, self.toggle_archived )
		self.loan_display.Bind( wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.edit, id = wx.ID_ANY )
		self.run_query_button.Bind( wx.EVT_BUTTON, self.run_query )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_activate( self, event ):
		event.Skip()

	def on_iconize( self, event ):
		event.Skip()

	def load_display( self, event ):
		event.Skip()

	def add( self, event ):
		event.Skip()

	def search_table( self, event ):
		event.Skip()

	def edit( self, event ):
		event.Skip()






	def toggle_archived( self, event ):
		event.Skip()



	def end_loan( self, event ):
		event.Skip()




	def run_query( self, event ):
		event.Skip()


