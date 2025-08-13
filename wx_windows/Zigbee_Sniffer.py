import wx
import subprocess

class FunctionBFrame(wx.Frame):
    def __init__(self, parent=None, title="Zigbee Sniffer", size=(500, 200)):
        super().__init__(parent, title=title, size=size)
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 水平布局：标签 + 输入框
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, label="Channel")
        hbox.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.channel_txt = wx.TextCtrl(panel)
        hbox.Add(self.channel_txt, 1, wx.ALL | wx.EXPAND, 5)

        # 嗅探按钮
        main_sizer.Add(hbox, 0, wx.EXPAND)
        self.btn_start = wx.Button(panel, label="嗅探")
        self.btn_start.Bind(wx.EVT_BUTTON, self.start_sniff)
        main_sizer.Add(self.btn_start, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        panel.SetSizer(main_sizer)
        self.Centre()
        self.Show()

    def start_sniff(self, event):
        channel = self.channel_txt.GetValue()
        if not channel:
            channel = "11"
        print(f"开始抓包: {channel}")
        try:
            cmd = f"sudo whsniff -c {channel} | wireshark -k -i -"
            print(cmd)
            subprocess.Popen(cmd, shell=True)
        except Exception as e:
            print(f"执行异常: {e}")
        finally:
            print("执行结束")
            self.Close()  # 关闭窗口，相当于 tk 的 root.destroy()


if __name__ == "__main__":
    app = wx.App(False)
    frame = FunctionBFrame()
    app.MainLoop()
