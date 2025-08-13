import wx

# class ErrorWindow(wx.Frame):
#     def __init__(self, parent=None, title="错误警告", size=(400,300)):
#         super().__init__(parent, title=title, size=size)
#         pnl = wx.Panel(self)
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         wx.MessageBox("USB 按钮被点击了！", "提示", wx.OK | wx.ICON_INFORMATION)

#         pnl.SetSizer(sizer)
#         self.Show()

class ErrorDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="错误警告", size=(300,150))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(panel, label="功能不存在！")
        sizer.Add(label, 1, wx.ALL | wx.EXPAND, 20)
        panel.SetSizer(sizer)
        self.Centre()



if __name__ == "__main__":
    app = wx.App(False)
    ErrorDialog()
    app.MainLoop()
