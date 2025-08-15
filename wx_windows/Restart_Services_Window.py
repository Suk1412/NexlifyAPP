import wx
import subprocess

class FunctionAFrame(wx.Frame):
    def __init__(self, parent=None, title="新窗口", size=(500, 200)):
        super().__init__(parent, title=title, size=size)
        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 第一行: wisdom_engine.service
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label1 = wx.StaticText(panel, label="wisdom_engine.service")
        hbox1.Add(label1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        btn_restart1 = wx.Button(panel, label="重启")
        btn_restart1.Bind(wx.EVT_BUTTON, lambda evt: self.run_command("sudo systemctl restart wisdom_engine.service"))
        hbox1.Add(btn_restart1, 0, wx.ALL, 5)
        btn_status1 = wx.Button(panel, label="查看")
        btn_status1.Bind(wx.EVT_BUTTON, lambda evt: self.run_command("sudo systemctl status wisdom_engine.service"))
        hbox1.Add(btn_status1, 0, wx.ALL, 5)
        main_sizer.Add(hbox1, 0, wx.EXPAND)

        # 第二行: supervisorctl
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label2 = wx.StaticText(panel, label="supervisorctl")
        hbox2.Add(label2, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        btn_restart2 = wx.Button(panel, label="重启")
        btn_restart2.Bind(wx.EVT_BUTTON, lambda evt: self.run_command("sudo supervisorctl restart all"))
        hbox2.Add(btn_restart2, 0, wx.ALL, 5)
        btn_status2 = wx.Button(panel, label="查看")
        btn_status2.Bind(wx.EVT_BUTTON, lambda evt: self.run_command("sudo supervisorctl status all"))
        hbox2.Add(btn_status2, 0, wx.ALL, 5)
        main_sizer.Add(hbox2, 0, wx.EXPAND)

        # 输出文本框和滚动条
        self.output_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        main_sizer.Add(self.output_text, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_sizer)

        self.Centre()
        self.Show()      
        self.Raise()      # 提升到最前面
        self.SetFocus()   # 获取焦点

    def run_command(self, cmd=None):
        self.output_text.Clear()
        if not cmd:
            cmd = "echo Hello, world!"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            self.output_text.AppendText(f"命令: {cmd}\n")
            self.output_text.AppendText(f"返回码: {result.returncode}\n")
            self.output_text.AppendText(f"标准输出:\n{result.stdout}\n")
            if result.stderr:
                self.output_text.AppendText(f"错误输出:\n{result.stderr}\n")
        except Exception as e:
            self.output_text.AppendText(f"执行异常: {e}\n")


if __name__ == "__main__":
    app = wx.App(False)
    frame = FunctionAFrame()
    app.MainLoop()
