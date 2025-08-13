import wx
class ChildFrame(wx.Frame):
    """子窗口"""
    def __init__(self, parent):
        super().__init__(parent, title="子窗口", size=(250, 150))
        panel = wx.Panel(self)
        wx.StaticText(panel, label="这是一个子窗口", pos=(50, 50))
        self.Show()