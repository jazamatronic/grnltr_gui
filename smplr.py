#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.1.0pre on Sat Mar 25 20:57:52 2023
#

# begin wxGlade: dependencies
import wx
import wx.lib.mixins.inspection as wit

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import (
    FigureCanvasWxAgg as FigureCanvas,
    NavigationToolbar2WxAgg as NavigationToolbar)

from smpl import smpl
import math
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure(figsize=(2, 2))
        self.axes = self.figure.add_subplot()
        self.axes.get_yaxis().set_visible(False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.canvas.mpl_connect("scroll_event", self.mouse_scroll_event)
        self.canvas.mpl_connect("button_press_event", self.click_event)
        self.canvas.Bind(wx.EVT_ENTER_WINDOW, self.change_cursor)
        self.xlim = None
        #these should be per sample really
        #then startfill/endfill should be taken from the waveform itself
        self.start = None
        self.end = None
        self.startfill = None
        self.endfill = None

    def clear(self):
        self.xlim = None
        self.start = None
        self.end = None
        self.startfill = None
        self.endfill = None
        self.axes.clear()
        self.canvas.draw()
        self.canvas.Refresh()

    def draw(self, wf):
        self.axes.clear()
        self.axes.plot(wf)
        self.axes.autoscale(False)
        self.xlim = self.axes.get_xlim()
        self.canvas.draw()
        self.canvas.Refresh()

    def change_cursor(self, evt):
        self.canvas.SetCursor(wx.Cursor(wx.CURSOR_CROSS))

    # https://matplotlib.org/stable/users/explain/event_handling.html
    def mouse_scroll_event(self, evt):
        #print("xdata: {}, ydata: {}, button: {}".format(evt.xdata, evt.ydata, evt.button))
        if ((self.xlim == None) | (evt.xdata == None) | (evt.ydata == None)):
            return
        xdata = evt.xdata
        xlim = self.axes.get_xlim()
        xldist = xdata - xlim[0]
        xrdist = xlim[-1] - xdata
        if evt.button == "up":
            newxl = max(self.xlim[0],  xdata - xldist / 2)
            newxr = min(self.xlim[-1], xdata + xrdist / 2)
            self.axes.set_xlim((newxl, newxr))
        if evt.button == "down":
            newxl = max(self.xlim[0],  xdata - xldist * 2)
            newxr = min(self.xlim[-1], xdata + xrdist * 2)
            self.axes.set_xlim((newxl, newxr))
        self.canvas.draw()
        self.canvas.Refresh()

    def click_event(self, evt):
        #print("xdata: {}, ydata: {}, button: {}".format(evt.xdata, evt.ydata, evt.button))
        if ((self.xlim == None) | (evt.xdata == None) | (evt.ydata == None)):
            return
        xdata = evt.xdata
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        xrange = xlim[-1] - xlim[0]
        xrange10pct = xrange * 0.1
        if evt.button == 1:
            if self.startfill != None:
                for f in self.startfill:
                    f.remove()
            self.startfill = self.axes.fill((self.xlim[0], xdata, xdata, self.xlim[0]), (ylim[0], ylim[0], ylim[-1], ylim[-1]), "b", alpha=0.3)
            self.start = xdata
            newxl = max(self.xlim[0],  xdata - xrange10pct)
            self.axes.set_xlim((newxl, xlim[-1]))
        if evt.button == 3:
            if self.endfill != None:
                for f in self.endfill:
                    f.remove()
            self.endfill = self.axes.fill((self.xlim[-1], xdata, xdata, self.xlim[-1]), (ylim[0], ylim[0], ylim[-1], ylim[-1]), "b", alpha=0.3)
            self.end = xdata
            newxr = min(self.xlim[-1], xdata + xrange10pct)
            self.axes.set_xlim((xlim[0], newxr))
        if evt.button == 2:
            if ((self.start != None) and (xdata < self.start)):
                for f in self.startfill:
                    f.remove()
                self.start = None
                self.startfill = None
                newxl = self.xlim[0]
                self.axes.set_xlim((newxl, xlim[-1]))
            if ((self.end != None) and (xdata > self.end)):
                for f in self.endfill:
                    f.remove()
                self.end = None
                self.endfill = None
                newxr = self.xlim[-1]
                self.axes.set_xlim((xlim[0], newxr))
        self.canvas.draw()
        self.canvas.Refresh()


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((944, 352))
        self.SetTitle("smplr")

        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end

        self.panel_1 = wx.Panel(self, wx.ID_ANY, name="main")

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        self.gauge_1 = wx.Gauge(self.panel_1, wx.ID_ANY, 64, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        sizer_2.Add(self.gauge_1, 0, wx.EXPAND, 0)

        grid_sizer_1 = wx.GridSizer(4, 4, 0, 0)
        sizer_2.Add(grid_sizer_1, 1, wx.EXPAND, 0)

        self.sample_list = []
        self.active_slotnum = 0 
        for slot_number in range(1, 17, 1): 
            self.sample_list.append(smpl())
            label = "slot_{:02d}".format(slot_number)
            btn = wx.Button(self.panel_1, wx.ID_ANY, label)
            grid_sizer_1.Add(btn, 0, wx.EXPAND | wx.FIXED_MINSIZE, 0)
            btn.Bind(wx.EVT_BUTTON, lambda evt, temp=label: self.slot_button(evt, temp))

        self.panel_2 = wx.Panel(self.panel_1, wx.ID_ANY, name="right")
        sizer_1.Add(self.panel_2, 1, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)

        grid_sizer_2 = wx.FlexGridSizer(6, 2, 0, 0)
        sizer_3.Add(grid_sizer_2, 1, wx.EXPAND, 0)

        label_1 = wx.StaticText(self.panel_2, wx.ID_ANY, "input_file")
        grid_sizer_2.Add(label_1, 0, 0, 0)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_2.Add(self.text_ctrl_1, 0, 0, 0)

        label_2 = wx.StaticText(self.panel_2, wx.ID_ANY, "input_rate")
        grid_sizer_2.Add(label_2, 0, 0, 0)

        self.text_ctrl_2 = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_2.Add(self.text_ctrl_2, 0, 0, 0)

        label_3 = wx.StaticText(self.panel_2, wx.ID_ANY, "input_channels")
        grid_sizer_2.Add(label_3, 0, 0, 0)

        self.text_ctrl_3 = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_2.Add(self.text_ctrl_3, 0, 0, 0)

        label_4 = wx.StaticText(self.panel_2, wx.ID_ANY, "input_bitdepth")
        grid_sizer_2.Add(label_4, 0, 0, 0)

        self.text_ctrl_4 = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_2.Add(self.text_ctrl_4, 0, 0, 0)

        label_5 = wx.StaticText(self.panel_2, wx.ID_ANY, "input_duration")
        grid_sizer_2.Add(label_5, 0, 0, 0)

        self.text_ctrl_5 = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_2.Add(self.text_ctrl_5, 0, 0, 0)
        
        self.load_sample = wx.Button(self.panel_2, wx.ID_ANY, "reload")
        grid_sizer_2.Add(self.load_sample, 0, 0, 0)

        self.play_sample = wx.Button(self.panel_2, wx.ID_ANY, "play")
        grid_sizer_2.Add(self.play_sample, 0, 0, 0)

        #grid_sizer_2.Add((0, 0), 0, 0, 0)

        self.wf_panel = CanvasPanel(self.panel_2)
        sizer_3.Add(self.wf_panel, 1, wx.EXPAND, 0)

        sizer_3.Add((0, 0), 0, 0, 0)

        self.panel_2.SetSizer(sizer_3)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.load_sample.Bind(wx.EVT_BUTTON, self.load_sample_button)
        self.play_sample.Bind(wx.EVT_BUTTON, self.play_sample_button)

        self.lastdir = ""

        # end wxGlade

        # switchable panels?
        # https://oren-sifri.medium.com/switching-between-panels-in-wxpython-9b1cd479eab3
    def open_wav(self):
        with wx.FileDialog(self, "Open WAV file", wildcard="WAV files (*.wav;*.WAV)|*.wav;*.WAV",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if self.lastdir != "":
                fileDialog.SetDirectory(self.lastdir)
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.lastdir = fileDialog.GetDirectory()
            return pathname

    def display_sample_info(self):
        slotnum = self.active_slotnum
        self.text_ctrl_1.SetValue(self.sample_list[slotnum].input_filename)
        self.text_ctrl_2.SetValue(str(self.sample_list[slotnum].input_rate))
        self.text_ctrl_3.SetValue(str(self.sample_list[slotnum].input_channels))
        self.text_ctrl_4.SetValue(str(self.sample_list[slotnum].input_bitdepth))
        self.text_ctrl_5.SetValue(str(self.sample_list[slotnum].input_duration))
        self.wf_panel.draw(self.sample_list[slotnum].get_waveform())

    def clear_sample_info(self):
        slotnum = self.active_slotnum
        self.text_ctrl_1.SetValue('')
        self.text_ctrl_2.SetValue('')
        self.text_ctrl_3.SetValue('')
        self.text_ctrl_4.SetValue('')
        self.text_ctrl_5.SetValue('')
        self.wf_panel.clear()

    def slot_button(self, event, button_label):  # wxGlade: MyFrame.<event_handler>
        slot, slotnumstr = button_label.split('_')
        slotnum = int(slotnumstr) - 1
        self.active_slotnum = slotnum
        #print("{} {}".format(button_label, slotnum))
        if (self.sample_list[slotnum].input_file_is_set() == False):
            pathname = self.open_wav()
            if pathname is None:
                self.clear_sample_info()
                return
            else:
                self.sample_list[slotnum].set_input_file(pathname)
        self.display_sample_info()
        event.Skip()

    def load_sample_button(self, event):
        pathname = self.open_wav()
        if pathname is None:
            return
        self.sample_list[self.active_slotnum].set_input_file(pathname)
        self.display_sample_info()
        event.Skip()

    def play_sample_button(self, event): 
        self.sample_list[self.active_slotnum].preview()

# end of class MyFrame

#class MyApp(wx.App):
#    def OnInit(self):
#        self.frame = MyFrame(None, wx.ID_ANY, "")
#        self.SetTopWindow(self.frame)
#        self.frame.Show()
#        return True

class MyApp(wit.InspectableApp):
    def OnInit(self):
        self.Init()
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()