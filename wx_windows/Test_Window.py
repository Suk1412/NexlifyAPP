import wx

class NonogramFrame(wx.Frame):
    def __init__(self, parent=None, title="新窗口", size=(500, 200)):
        super().__init__(parent, title=title, size=size)
        # 创建菜单栏
        menubar = wx.MenuBar()

        # 文件菜单
        file_menu = wx.Menu()
        new_item = file_menu.Append(wx.ID_NEW, "新建(&N)\tCtrl+N", "新建文件")
        open_item = file_menu.Append(wx.ID_OPEN, "打开(&O)\tCtrl+O", "打开文件")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "退出(&Q)\tCtrl+Q", "退出程序")
        menubar.Append(file_menu, "文件(&F)")

        # 帮助菜单
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, "关于(&A)", "关于本程序")
        menubar.Append(help_menu, "帮助(&H)")

        # 绑定菜单事件
        self.Bind(wx.EVT_MENU, self.on_new, new_item)
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

        # 设置菜单栏
        self.SetMenuBar(menubar)

        # 中间面板
        panel = wx.Panel(self)
        wx.StaticText(panel, label="这是一个带菜单栏的窗口", pos=(20, 20))

        self.Centre()
        self.Show()

    def on_new(self, event):
        self.main_pnl = wx.Panel(self)


    def on_open(self, event):
        wx.MessageBox("打开文件功能", "提示")

    def on_exit(self, event):
        self.Close()

    def on_about(self, event):
        wx.MessageBox("这是一个 wxPython 菜单栏示例", "关于", wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = wx.App(False)
    NonogramFrame()
    app.MainLoop()