import wx
import wx.lib.mixins.listctrl as listmix
import numpy as np
from copy import deepcopy

from unidec_modules import unidectools as ud


class PeakListCtrlPanel(wx.Panel, listmix.ColumnSorterMixin):
    """
    Creates a list control panel for displaying and interacting with Peaks object
    """

    def __init__(self, parent, meta=False):
        """
        Initialize list_ctrl, bind events, and setup events to be broadcast back.
        :param parent: Parent of panel that will be created
        :return: None
        """
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        self.meta = meta
        self.index = 0
        self.list_ctrl = wx.ListCtrl(self, pos=wx.DefaultPosition, size=(300, 1100),
                                     style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, " ", width=25)
        self.list_ctrl.InsertColumn(1, "Mass (Da)", wx.LIST_FORMAT_RIGHT, width=70)
        self.list_ctrl.InsertColumn(2, "Intensity", width=65)
        if meta:
            self.list_ctrl.InsertColumn(3, "", width=45)
        else:
            self.list_ctrl.InsertColumn(3, "Area", width=45)
        self.list_ctrl.InsertColumn(4, "Name", width=80)

        listmix.ColumnSorterMixin.__init__(self, 5)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_click, self.list_ctrl)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_right_click, self.list_ctrl)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)

        self.EVT_DELETE_SELECTION_2 = wx.PyEventBinder(wx.NewEventType(), 1)
        self.EVT_CHARGE_STATE = wx.PyEventBinder(wx.NewEventType(), 1)
        self.EVT_DIFFERENCES = wx.PyEventBinder(wx.NewEventType(), 1)

        self.remove = []
        self.selection = []
        self.selection2 = []
        self.pks = None
        self.errorsdisplayed = False

        self.popupID1 = wx.NewId()
        self.popupID2 = wx.NewId()
        self.popupID3 = wx.NewId()
        self.popupID4 = wx.NewId()
        self.popupID5 = wx.NewId()
        self.popupID6 = wx.NewId()
        self.popupID7 = wx.NewId()
        self.popupID8 = wx.NewId()
        self.popupID9 = wx.NewId()

        self.Bind(wx.EVT_MENU, self.on_popup_one, id=self.popupID1)
        self.Bind(wx.EVT_MENU, self.on_popup_two, id=self.popupID2)
        self.Bind(wx.EVT_MENU, self.on_popup_three, id=self.popupID3)
        self.Bind(wx.EVT_MENU, self.on_popup_four, id=self.popupID4)
        self.Bind(wx.EVT_MENU, self.on_popup_five, id=self.popupID5)
        self.Bind(wx.EVT_MENU, self.on_popup_six, id=self.popupID6)
        self.Bind(wx.EVT_MENU, self.on_popup_seven, id=self.popupID7)
        self.Bind(wx.EVT_MENU, self.on_popup_eight, id=self.popupID8)
        self.Bind(wx.EVT_MENU, self.on_popup_nine, id=self.popupID9)

    def clear_list(self):
        """
        Remove all elements from list_ctrl
        :return: None
        """
        self.list_ctrl.DeleteAllItems()
        self.remove = []

    def add_data(self, pks, show="area", collab1="Mass (Da)"):
        """
        Add data from a Peaks object to the list_ctrl
        :param pks: Peaks object
        :param show: Keyword describing what to show in column 1

        area = p.area
        integral = p.integral
        diff = p.diff

        :param collab1: Column 1 label
        :return: None
        """
        self.list_ctrl.DeleteAllItems()
        self.pks = pks

        col = self.list_ctrl.GetColumn(3)
        if not self.meta:
            col.SetText("Area")
        self.list_ctrl.SetColumn(3, col)
        self.list_ctrl.SetColumnWidth(3, 50)

        try:
            col = self.list_ctrl.GetColumn(1)
            col.SetText(collab1)
            self.list_ctrl.SetColumn(1, col)
            self.list_ctrl.SetColumnWidth(1, -2)
        except Exception, e:
            pass

        for i in xrange(0, self.pks.plen):
            p = pks.peaks[i]
            self.list_ctrl.InsertItem(i, p.textmarker)
            self.list_ctrl.SetItem(i, 1, str(p.mass))
            # TODO: Proper decimal places on this
            '''
            if self.pks.massbins < 1:
                self.list_ctrl.SetItem(i, 1, str(p.mass))
            else:
                self.list_ctrl.SetItem(i, 1, "{:,}".format(p.mass))
            '''
            self.list_ctrl.SetItem(i, 2, "%.2f" % p.height)
            try:
                if show == "area":
                    self.list_ctrl.SetItem(i, 3, str(p.area))
                elif show == "integral":
                    self.list_ctrl.SetItem(i, 3, "%.2f" % p.integral)
                elif show == "diff":
                    self.list_ctrl.SetItem(i, 3, str(p.diff))
                else:
                    self.list_ctrl.SetItem(i, 3, "")
            except (ValueError, AttributeError, TypeError):
                self.list_ctrl.SetItem(i, 3, "")
            self.list_ctrl.SetItem(i, 4, str(p.label))
            self.list_ctrl.SetItemData(i, i)
            color = wx.Colour(int(round(p.color[0] * 255)), int(round(p.color[1] * 255)), int(round(p.color[2] * 255)),
                              alpha=255)
            self.list_ctrl.SetItemBackgroundColour(i, col=color)
        self.remove = []
        listmix.ColumnSorterMixin.__init__(self, 4)

    def GetListCtrl(self):
        # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
        return self.list_ctrl

    def on_column_click(self, event):
        # print "column clicked"
        event.Skip()

    def on_right_click(self, event=None):
        """
        Spawn right click menu
        :param event: Unused Event
        :return: None
        """
        if self.errorsdisplayed is False:
            if hasattr(self, "popupID1"):
                menu = wx.Menu()
                menu.Append(self.popupID1, "Ignore")
                menu.Append(self.popupID2, "Isolate")
                menu.Append(self.popupID3, "Repopulate")
                menu.AppendSeparator()
                menu.Append(self.popupID4, "Label Charge States")
                menu.Append(self.popupID6, "Display Differences")
                menu.Append(self.popupID7, "Display Errors")
                menu.AppendSeparator()
                menu.Append(self.popupID5, "Color Select")
                menu.Append(self.popupID9, "Marker Select")
                self.PopupMenu(menu)
                menu.Destroy()
        else:
            if hasattr(self, "popupID1"):
                menu = wx.Menu()
                menu.Append(self.popupID1, "Ignore")
                menu.Append(self.popupID2, "Isolate")
                menu.Append(self.popupID3, "Repopulate")
                menu.AppendSeparator()
                menu.Append(self.popupID4, "Label Charge States")
                menu.Append(self.popupID6, "Display Differences")
                menu.Append(self.popupID8, "Hide Errors")
                menu.AppendSeparator()
                menu.Append(self.popupID5, "Color Select")
                menu.Append(self.popupID9, "Marker Select")
                self.PopupMenu(menu)
                menu.Destroy()

    def on_popup_one(self, event=None):
        """
        The selected peaks are added to self.selection and deleted. For each delete peak, p.ignore is set to 1.
        Triggers EVT_DELETE_SELECTION_2.
        :param event: Unused Event
        :return: None
        """
        # Delete
        item = self.list_ctrl.GetFirstSelected()
        num = self.list_ctrl.GetSelectedItemCount()
        self.selection = []
        self.selection.append(item)
        self.remove.append(float(self.list_ctrl.GetItem(item, col=1).GetText()))
        for i in range(1, num):
            item = self.list_ctrl.GetNextSelected(item)
            self.remove.append(float(self.list_ctrl.GetItem(item, col=1).GetText()))
            self.selection.append(item)
        for i in range(0, num):
            self.list_ctrl.DeleteItem(self.selection[num - i - 1])
        for p in self.pks.peaks:
            if p.mass in self.remove:
                p.ignore = 1
        newevent = wx.PyCommandEvent(self.EVT_DELETE_SELECTION_2._getEvtType(), self.GetId())
        self.GetEventHandler().ProcessEvent(newevent)

    def on_popup_two(self, event=None):
        """
        The selected peaks are added to self.selection. All other peaks are deleted form list ctrl
        and p.ignore for each is set to 1.
        Triggers EVT_DELETE_SELECTION_2.
        :param event: Unused Event
        :return: None
        """
        # Isolate
        item = self.list_ctrl.GetFirstSelected()
        num = self.list_ctrl.GetSelectedItemCount()
        tot = self.list_ctrl.GetItemCount()
        self.selection = []
        self.selection.append(item)
        for i in range(1, num):
            item = self.list_ctrl.GetNextSelected(item)
            self.selection.append(item)
        self.selection = np.array(self.selection)
        for i in range(tot - 1, -1, -1):
            if not np.any(self.selection == i):
                self.remove.append(float(self.list_ctrl.GetItem(i, col=1).GetText()))
                self.list_ctrl.DeleteItem(i)
        for p in self.pks.peaks:
            if p.mass in self.remove:
                p.ignore = 1
        newevent = wx.PyCommandEvent(self.EVT_DELETE_SELECTION_2._getEvtType(), self.GetId())
        self.GetEventHandler().ProcessEvent(newevent)

    def on_popup_six(self, event=None):
        """
        Triggers EVT_DIFFERENCES. The first selected item becomes the reference mass. The difference between all
        masses and the reference mass is calculated and displayed in column 3.
        :param event: Unused Event
        :return: None
        """
        # Show Differences
        item = self.list_ctrl.GetFirstSelected()
        # num = self.list_ctrl.GetSelectedItemCount()
        self.selection2 = float(self.list_ctrl.GetItem(item, col=1).GetText())

        for p in self.pks.peaks:
            p.diff = p.mass - self.selection2
        self.list_ctrl.DeleteAllItems()

        self.add_data(self.pks, show="diff")

        col = self.list_ctrl.GetColumn(3)
        col.SetText("Diff.")
        self.list_ctrl.SetColumn(3, col)
        self.list_ctrl.SetColumnWidth(3, 65)
        if self.errorsdisplayed is True:
            col = self.list_ctrl.GetColumn(4)
            col.SetText("Name")
            self.list_ctrl.SetColumn(4, col)

        self.errorsdisplayed = False
        newevent = wx.PyCommandEvent(self.EVT_DIFFERENCES._getEvtType(), self.GetId())
        self.GetEventHandler().ProcessEvent(newevent)

    def on_popup_three(self, event=None):
        """
        Repopulates the list control with all elements in self.pks.peaks.
        :param event: Unused event
        :return: None
        """
        # Repopluate
        self.list_ctrl.DeleteAllItems()
        for p in self.pks.peaks:
            p.ignore = 0
        self.add_data(self.pks)
        self.remove = []
        listmix.ColumnSorterMixin.__init__(self, 4)

        newevent = wx.PyCommandEvent(self.EVT_DELETE_SELECTION_2._getEvtType(), self.GetId())
        self.GetEventHandler().ProcessEvent(newevent)

    def on_popup_four(self, event=None):
        """
        Gets the selected items and adds it self.selection2. Triggers EVT_CHARGE_STATE.
        :param event:
        :return:
        """
        # Label Charge State
        item = self.list_ctrl.GetFirstSelected()
        num = self.list_ctrl.GetSelectedItemCount()
        self.selection2 = []
        self.selection2.append(float(self.list_ctrl.GetItem(item, col=1).GetText()))
        for i in range(1, num):
            item = self.list_ctrl.GetNextSelected(item)
            self.selection2.append(float(self.list_ctrl.GetItem(item, col=1).GetText()))
        newevent = wx.PyCommandEvent(self.EVT_CHARGE_STATE._getEvtType(), self.GetId())
        self.GetEventHandler().ProcessEvent(newevent)

    def on_popup_five(self, event=None):
        """
        Spawns a dialog for the first selected item to select the color.
        Redraws the list control with the new colors and then triggers an EVT_DELETE_SELECTION_2.
        :param event: Unused Event
        :return: None
        """
        # Change Color
        item = self.list_ctrl.GetFirstSelected()
        col = self.list_ctrl.GetItemBackgroundColour(item)
        print "Color In:", col
        col = wx.Colour(int(col[0]), int(col[1]), int(col[2]), alpha=int(col.alpha))
        col2 = wx.ColourData()
        col2.SetColour(col)
        colout = col2
        dlg = wx.ColourDialog(None, data=col2)
        if dlg.ShowModal() == wx.ID_OK:
            coloutdlg = dlg.GetColourData()
            colout = deepcopy(coloutdlg.GetColour())
            print "Color Out", colout
            dlg.Destroy()
        else:
            dlg.Destroy()
            return

        self.list_ctrl.SetItemBackgroundColour(item, col=colout)
        peak = float(self.list_ctrl.GetItem(item, col=1).GetText())
        i = ud.nearest(self.pks.masses, peak)
        self.pks.peaks[i].color = ([colout[0] / 255., colout[1] / 255., colout[2] / 255.])
        newevent = wx.PyCommandEvent(self.EVT_DELETE_SELECTION_2._getEvtType(), self.GetId())
        self.GetEventHandler().ProcessEvent(newevent)

    def on_popup_seven(self, event=None):
        """
        Replaces the third and fourth columns with the FWHM and mean errors.
        :param event:
        :return:
        """
        col = self.list_ctrl.GetColumn(3)
        col.SetText("FWHM Error")
        self.list_ctrl.SetColumn(3, col)
        first = 1
        for i in xrange(0, self.pks.plen):
            p = self.pks.peaks[i]
            self.list_ctrl.SetItem(i, 3, str(p.errorFWHM))
            if p.errormean == -1:
                self.list_ctrl.SetItem(i, 4, str(p.errorreplicate))
                if first == 1:
                    col = self.list_ctrl.GetColumn(4)
                    col.SetText("Duplicate Error")
                    self.list_ctrl.SetColumn(4, col)
                    first = 0
            else:
                self.list_ctrl.SetItem(i, 4, str(p.errormean))
        if first == 1:
            col = self.list_ctrl.GetColumn(4)
            col.SetText("Mean Error")
            self.list_ctrl.SetColumn(4, col)
        self.errorsdisplayed = True

    def on_popup_eight(self, event=None):
        """
        Hides the error stuff brought up by on_popup_seven
        :param event:
        :return:
        """
        col = self.list_ctrl.GetColumn(3)
        if self.meta:
            col.SetText("")
        else:
            col.SetText("Area")
        self.list_ctrl.SetColumn(3, col)
        col = self.list_ctrl.GetColumn(4)
        col.SetText("Name")
        self.list_ctrl.SetColumn(4, col)
        for i in xrange(0, self.pks.plen):
            p = self.pks.peaks[i]
            self.list_ctrl.SetItem(i, 3, str(p.area))
            self.list_ctrl.SetItem(i, 4, str(p.label))
        self.errorsdisplayed = False

    def on_popup_nine(self, e=None):
        item = self.list_ctrl.GetFirstSelected()
        peak = float(self.list_ctrl.GetItem(item, col=1).GetText())
        i = ud.nearest(self.pks.masses, peak)
        dlg = SelectMarker(self)
        dlg.initialize_interface(self.pks, i)
        self.list_ctrl.SetItem(i, 0, self.pks.peaks[i].textmarker)
        newevent = wx.PyCommandEvent(self.EVT_DELETE_SELECTION_2._getEvtType(), self.GetId())
        self.GetEventHandler().ProcessEvent(newevent)


# TODO: Add in a column label drop down or some other way to select which information of self.pks is displayed

class SelectMarker(wx.Dialog):
    def __init__(self, *args, **kwargs):
        """
        Create a dialog for setting some obscure additional parameters.
        :param args: Passed to wx.Dialog
        :param kwargs: Passed to wx.Dialog
        :return: None
        """
        wx.Dialog.__init__(self, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, *args, **kwargs)
        self.SetSize((285, 125))
        self.SetTitle("Pick the Peak Marker")

    def initialize_interface(self, pks, index):
        """
        :return: None
        """
        self.pks = pks
        self.index = index

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Marker Type')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)

        for i, m in enumerate(self.pks.textmarkers):
            button = wx.Button(pnl, i, m, size=(35, 35))
            hbox5.Add(button, 0)
            button.Bind(wx.EVT_BUTTON, self.on_close)

        sbs.Add(hbox5, 0)

        pnl.SetSizer(sbs)

        vbox.Add(pnl, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(vbox)
        self.ShowModal()

    def on_close(self, e):
        """
        Close the window.
        :param e:  Event
        :return: None
        """
        id = e.GetId()
        marker = self.pks.markers[id]
        textmarker = self.pks.textmarkers[id]
        self.pks.peaks[self.index].marker = marker
        self.pks.peaks[self.index].textmarker = textmarker
        self.Destroy()
        self.EndModal(0)
