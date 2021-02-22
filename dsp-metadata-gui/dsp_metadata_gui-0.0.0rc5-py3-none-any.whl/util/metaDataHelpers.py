import sys
import wx
import wx.adv


class CalendarDlg(wx.Dialog):
    # def __init__(self, parent):
    def __init__(self, parent, title, date_str):

        # wx.Dialog.__init__(self, parent, title=parent.title)
        wx.Dialog.__init__(self, parent, title=title)
        panel = wx.Panel(self, -1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

        date = wx.DateTime()
        date.ParseDate(date_str)
        cal = wx.adv.GenericCalendarCtrl(panel, date=date)
        # cal = wx.adv.GenericCalendarCtrl(panel, date=parent.date)

        if sys.platform != 'win32':
            # gtk truncates the year - this fixes it
            w, h = cal.Size
            cal.Size = (w + 15, h + 85)
            cal.MinSize = cal.Size

        sizer.Add(cal, 0)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add((0, 0), 1)
        btn_ok = wx.Button(panel, wx.ID_OK)
        btn_ok.SetDefault()
        button_sizer.Add(btn_ok, 0, wx.ALL, 2)
        button_sizer.Add((0, 0), 1)
        btn_can = wx.Button(panel, wx.ID_CANCEL)
        button_sizer.Add(btn_can, 0, wx.ALL, 2)
        button_sizer.Add((0, 0), 1)
        sizer.Add(button_sizer, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Fit(panel)
        self.ClientSize = panel.Size

        cal.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        cal.SetFocus()
        self.cal = cal

    def on_key_down(self, evt):
        code = evt.KeyCode
        if code == wx.WXK_TAB:
            self.cal.Navigate()
        elif code in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.EndModal(wx.ID_OK)
        elif code == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        else:
            evt.Skip()
