import wx
from wx_windows.Compile_Pytoso import CompileFrame
from wx_windows.Restart_Services import FunctionAFrame
from wx_windows.Zigbee_Sniffer import FunctionBFrame


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.functions = {"单独文件so编译工具":lambda:self.open_window(self.main_pnl, "单独文件so编译工具", (400, 300), CompileFrame),
                          "重启wisdom服务":lambda:self.open_window(self.main_pnl, "单独文件so编译工具", (400, 300), FunctionAFrame),
                          "ZigBee Sniffer":lambda:self.open_window(self.main_pnl, "单独文件so编译工具", (400, 300), FunctionBFrame)}
        self.selected_option = list(self.functions.keys())
        self.InitUI()

    def InitUI(self):
        self.main_pnl = wx.Panel(self)
        self.label = wx.StaticText(self.main_pnl, label="请选择一个工具")
        self.cb = wx.ComboBox(self.main_pnl, pos=(50, 30), choices=self.selected_option, style=wx.CB_READONLY, value=self.selected_option[2])
        self.button_usb = wx.Button(self.main_pnl, label="使用")
        self.button_usb.Bind(wx.EVT_BUTTON, self.button_click)
        self.button_expand = wx.Button(self.main_pnl, label="使用")
        self.button_expand.Bind(wx.EVT_BUTTON, self.button_click)

        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        hbox_buttons.Add(self.button_usb, 0, wx.ALL, 5)
        hbox_buttons.Add(self.button_expand, 0, wx.ALL, 5)
        # 创建水平盒子布局管理器
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(self.label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        hbox.Add(self.cb, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        hbox.Add(hbox_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.main_pnl.SetSizer(hbox)

        self.SetSize((400, 300))
        self.SetTitle("主程序")
        self.Show(True)
        
    def open_window(self, parent, title, size, content_class):
        content_class(parent,title=title, size=size)
        

    def button_click(self, event):
        """使用按钮点击事件"""
        value = self.cb.GetValue()
        if value in list(self.functions.keys()):
            self.functions[value]()  # 调用对应的函数
        else:
            wx.MessageBox("功能不存在！", "提示", wx.OK | wx.ICON_INFORMATION)


def main():
    ex = wx.App()
    MyFrame(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main() 