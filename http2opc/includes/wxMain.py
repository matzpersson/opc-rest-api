import wx
import os
import sys

TBFLAGS = ( wx.TB_HORIZONTAL
            | wx.NO_BORDER
            | wx.TB_FLAT
            #| wx.TB_TEXT
            #| wx.TB_HORZ_LAYOUT
            )

class MainPanel(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title='Moogle HTTP to OPC Server', size=(800,600) )

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_colours = { 'rest': 'blue', 'opc': 'purple'}

        ## -- Configure Top Tool bar 
        tb = wx.ToolBar(self, style=TBFLAGS)
        sizer.Add(tb, 0, wx.EXPAND)
        tsize = (24,24)
        tb.SetToolBitmapSize(tsize)
        tb.Realize()

        self.list =  wx.ListCtrl(self, -1,
            style=wx.LC_REPORT 
            #| wx.BORDER_SUNKEN
            #| wx.BORDER_NONE
            | wx.LC_EDIT_LABELS
            | wx.LC_SORT_ASCENDING
            | wx.LC_NO_HEADER
            | wx.LC_VRULES
            | wx.LC_HRULES
            #| wx.LC_SINGLE_SEL
            ) 
        self.loadListviewHeader()

        sizer.Add(self.list, 1, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Layout()

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def loadListviewHeader(self):
        self.list.InsertColumn(0, 'Created')
        self.list.InsertColumn(1, 'Type')
        self.list.InsertColumn(1, 'Comment')

        self.list.SetColumnWidth(0, 180)
        self.list.SetColumnWidth(1, 50)
        self.list.SetColumnWidth(2, 600)


    def writeRow(self, row):

        index = self.list.InsertStringItem(sys.maxint, row['created'] ) 
        self.list.SetStringItem(index, 1, row['type'] )
        self.list.SetStringItem(index, 2, row['comment'] )
        self.list.SetItemTextColour(index, self.row_colours[row['type'].lower()])


    def loadListviewRow2(self):

        index = self.list.InsertStringItem(sys.maxint, '20016-01-21 12:21' ) 
        self.list.SetStringItem(index, 1, 'Rest' )
        self.list.SetStringItem(index, 2, '1.0.0.127.in-addr.arpa - - [13/Mar/2016 11:22:37] "GET /api HTTP/1.1" 200 -' )

        self.list.SetItemTextColour(index, 'blue')

        index = self.list.InsertStringItem(sys.maxint, '20016-01-21 12:21' ) 
        self.list.SetStringItem(index, 1, 'OPC')
        self.list.SetStringItem(index, 2, 'Connect to 128.100.1.21' )

        self.list.SetItemTextColour(index, 'purple')

    def onClose(self, event):

        self.Destroy()