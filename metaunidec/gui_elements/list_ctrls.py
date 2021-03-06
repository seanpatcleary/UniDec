import os
import sys
import wx
import wx.lib.mixins.listctrl as listmix
import numpy as np
import matplotlib.cm as cm

from pubsub import pub

import unidec_modules.unidectools as ud
from copy import deepcopy


class YValueListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):
    def __init__(self, parent, id_value, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, id_value, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)
        self.InsertColumn(0, "Index")
        self.InsertColumn(1, "Variable 1")
        self.InsertColumn(2, "Variable 2")
        self.InsertColumn(3, "Name")
        self.SetColumnWidth(0, width=75)
        self.SetColumnWidth(1, width=75)
        self.SetColumnWidth(2, width=75)
        self.SetColumnWidth(3, width=75)

    def populate(self, dataset, colors=None):
        self.DeleteAllItems()
        colormap = cm.get_cmap('rainbow', dataset.len)
        peakcolors = colormap(np.arange(dataset.len))
        if colors is None:
            colors = peakcolors
        for i in range(0, dataset.len):
            s = dataset.spectra[i]
            index = self.InsertItem(sys.maxint, str(s.index))
            try:
                self.SetItem(index, 1, str(s.var1))
            except:
                self.SetItem(index, 1, str(i))

            try:
                self.SetItem(index, 2, str(s.var2))
            except:
                self.SetItem(index, 2, str(0))
            try:
                self.SetItem(index, 3, s.name)
            except:
                self.SetItem(index, 3, "")
            self.SetItemData(index, i)
            if colors is not None:
                color = wx.Colour(int(round(colors[i][0] * 255)), int(round(colors[i][1] * 255)),
                                  int(round(colors[i][2] * 255)), alpha=255)
                self.SetItemBackgroundColour(index, col=color)
                s.color = colors[i]
        self.data = dataset
        self.colors = colors
        self.rename_column(1, dataset.v1name)
        self.rename_column(2, dataset.v2name)

    def clear_list(self):
        self.DeleteAllItems()

    def add_line(self, var1="count", var2=0):
        if var1 == "count":
            var1 = self.GetItemCount()
        index = self.InsertItem(sys.maxint, str(self.GetItemCount()))
        self.SetItem(index, 1, str(var1))
        self.SetItem(index, 2, str(var2))
        self.SetItem(index, 3, str(""))

    def get_list(self):
        count = self.GetItemCount()
        colormap = cm.get_cmap('rainbow', count)
        peakcolors = colormap(np.arange(count))
        list_output = []
        for i in range(0, count):
            sublist = [int(self.GetItem(i, col=0).GetText()), float(self.GetItem(i, col=1).GetText()),
                       float(self.GetItem(i, col=2).GetText()), self.GetItem(i, col=3).GetText(), peakcolors[i][0],
                       peakcolors[i][1], peakcolors[i][2]]
            list_output.append(sublist)
        return list_output

    def repopulate(self):
        self.populate(self.data, self.colors)
        pass

    def rename_column(self, num, text):
        col = self.GetColumn(num)
        col.SetText(text)
        self.SetColumn(num, col)


class ListCtrlPanel(wx.Panel):
    def __init__(self, parent, pres, size=(200, 400)):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        id_value = wx.NewId()
        self.selection = []
        self.pres = pres
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.list = YValueListCtrl(self, id_value, size=size, style=wx.LC_REPORT | wx.BORDER_NONE)

        sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_right_click, self.list)

        self.popupID1 = wx.NewId()
        self.popupID2 = wx.NewId()
        self.popupID3 = wx.NewId()
        self.popupID4 = wx.NewId()
        self.popupID5 = wx.NewId()
        self.popupID6 = wx.NewId()
        self.popupID7 = wx.NewId()
        self.popupID10 = wx.NewId()
        self.popupID11 = wx.NewId()

        self.Bind(wx.EVT_MENU, self.on_popup_one, id=self.popupID1)
        self.Bind(wx.EVT_MENU, self.on_popup_two, id=self.popupID2)
        self.Bind(wx.EVT_MENU, self.on_popup_three, id=self.popupID3)
        self.Bind(wx.EVT_MENU, self.on_popup_four, id=self.popupID4)
        self.Bind(wx.EVT_MENU, self.on_popup_five, id=self.popupID5)
        self.Bind(wx.EVT_MENU, self.on_popup_six, id=self.popupID6)
        self.Bind(wx.EVT_MENU, self.on_popup_seven, id=self.popupID7)
        self.Bind(wx.EVT_MENU, self.on_popup_ten, id=self.popupID10)
        self.Bind(wx.EVT_MENU, self.on_popup_eleven, id=self.popupID11)

    def on_right_click(self, event):
        if hasattr(self, "popupID1"):
            menu = wx.Menu()
            menu.Append(self.popupID4, "Ignore")
            menu.Append(self.popupID5, "Isolate")
            menu.Append(self.popupID6, "Repopulate")
            menu.AppendSeparator()
            menu2 = wx.Menu()

            menu2.Append(self.popupID10, "Autocorrelation")
            menu2.Append(self.popupID11, "FFT Window")
            menu.Append(wx.ID_ANY, "Analysis Tools", menu2)
            menu.AppendSeparator()
            menu.Append(self.popupID7, "Change Color")
            menu.Append(self.popupID2, "Make Top")
            menu.Append(self.popupID3, "Fill Down Variable 2")
            menu.AppendSeparator()
            menu.Append(self.popupID1, "Delete")

            self.PopupMenu(menu)
            menu.Destroy()

    def on_popup_one(self, event):
        # Delete
        item = self.list.GetFirstSelected()
        num = self.list.GetSelectedItemCount()
        self.selection = []
        self.selection.append(item)
        for i in range(1, num):
            item = self.list.GetNextSelected(item)
            self.selection.append(item)
        for i in range(0, num):
            self.list.DeleteItem(self.selection[num - i - 1])
        self.pres.on_delete_spectrum(indexes=self.selection)

    def on_popup_two(self, event):
        item = self.list.GetFirstSelected()
        self.pres.make_top(item)

    def on_popup_three(self, event):
        item = self.list.GetFirstSelected()
        val = self.list.GetItem(item, col=2).GetText()
        count = self.list.GetItemCount()
        for i in range(0, count):
            self.list.SetItem(i, 2, val)

    def on_popup_four(self, event):
        item = self.list.GetFirstSelected()
        num = self.list.GetSelectedItemCount()
        self.selection = []
        self.selection.append(item)
        for i in range(1, num):
            item = self.list.GetNextSelected(item)
            self.selection.append(item)
        for i in range(0, num):
            self.list.DeleteItem(self.selection[num - i - 1])
        self.pres.on_ignore(self.selection)

    def on_popup_five(self, event):
        item = self.list.GetFirstSelected()
        num = self.list.GetSelectedItemCount()
        tot = self.list.GetItemCount()
        self.selection = []
        self.selection.append(item)
        for i in range(1, num):
            item = self.list.GetNextSelected(item)
            self.selection.append(item)
        for i in range(tot - 1, -1, -1):
            if not np.any(np.array(self.selection) == i):
                self.list.DeleteItem(i)
        self.pres.on_isolate(self.selection)

    def on_popup_six(self, event):
        self.list.repopulate()
        self.pres.on_repopulate()

    def on_popup_seven(self, event=None):
        """
        Spawns a dialog for the first selected item to select the color.
        Redraws the list control with the new colors and then triggers an EVT_DELETE_SELECTION_2.
        :param event: Unused Event
        :return: None
        """
        # Change Color
        item = self.list.GetFirstSelected()
        col = self.list.GetItemBackgroundColour(item)
        print "Color In:", col
        col = wx.Colour(int(col[0]), int(col[1]), int(col[2]), alpha=int(col.alpha))
        col2 = wx.ColourData()
        col2.SetColour(col)
        colout = col2
        dlg = wx.ColourDialog(None, data=col2)
        if dlg.ShowModal() == wx.ID_OK:
            colout = dlg.GetColourData()
            colout = deepcopy(colout.GetColour())
            print "Color Out", colout
        dlg.Destroy()
        self.list.SetItemBackgroundColour(item, col=colout)
        colout = colout.Get(includeAlpha=True)
        colout = ([colout[0] / 255., colout[1] / 255., colout[2] / 255., colout[3] / 255.])
        self.pres.on_color_change(item, colout)

    def on_popup_ten(self, event=None):
        item = self.list.GetFirstSelected()
        self.pres.on_autocorr2(item)

    def on_popup_eleven(self, event=None):
        item = self.list.GetFirstSelected()
        self.pres.on_fft_window2(item)
