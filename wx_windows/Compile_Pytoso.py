import wx
import os
import subprocess

class CompileFrame(wx.Frame):
    def __init__(self, parent=None, title="单独文件so编译工具", size=(500, 200)):
        super().__init__(parent, title=title, size=size)
        panel = wx.Panel(self)

        # 文件路径输入框
        self.file_path_ctrl = wx.TextCtrl(panel, style=wx.TE_READONLY)

        # 浏览按钮
        browse_btn = wx.Button(panel, label="浏览")
        browse_btn.Bind(wx.EVT_BUTTON, self.on_browse)

        # 编译按钮
        compile_btn = wx.Button(panel, label="编译")
        compile_btn.Bind(wx.EVT_BUTTON, self.on_compile)

        # 输出标签
        self.output_label = wx.StaticText(panel, label="", style=wx.ST_NO_AUTORESIZE)
        self.output_label.SetMinSize(wx.Size(-1, 60))

        # 布局
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.file_path_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        hbox1.Add(browse_btn, flag=wx.ALL, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, flag=wx.EXPAND)
        vbox.Add(compile_btn, flag=wx.ALL | wx.CENTER, border=10)
        vbox.Add(self.output_label, flag=wx.ALL | wx.EXPAND, border=5)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def on_browse(self, event):
        with wx.FileDialog(
            self,
            "选择 Python 文件",
            wildcard="Python files (*.py)|*.py|All files (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            self.file_path_ctrl.SetValue(path)

    def on_compile(self, event):
        file_path = self.file_path_ctrl.GetValue()
        if not file_path:
            self.output_label.SetLabel("请先选择一个文件!")
            self.output_label.SetForegroundColour(wx.Colour(255, 0, 0))
            return

        try:
            working_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            base_name = os.path.splitext(file_name)[0]

            original_dir = os.getcwd()
            os.chdir(working_dir)

            try:
                # cython
                cython_cmd = ["python3", "-m", "cython", file_name, "--embed"]
                subprocess.run(cython_cmd, check=True, capture_output=True, text=True)

                # gcc 编译 .o
                gcc1_cmd = [
                    "gcc", "-c", "-fPIC",
                    "-I", "/usr/include/python3.10/",
                    f"{base_name}.c",
                    "-o", f"{base_name}.o"
                ]
                subprocess.run(gcc1_cmd, check=True, capture_output=True, text=True)

                # gcc 链接成 .so
                gcc2_cmd = [
                    "gcc", "-shared",
                    f"{base_name}.o",
                    "-o", f"{base_name}.so"
                ]
                subprocess.run(gcc2_cmd, check=True, capture_output=True, text=True)

                # 删除中间文件
                try:
                    os.remove(f"{base_name}.c")
                    os.remove(f"{base_name}.o")
                    self.output_label.SetLabel("编译成功！过渡文件已删除.")
                    self.output_label.SetForegroundColour(wx.Colour(0, 150, 0))
                except OSError as e:
                    self.output_label.SetLabel(f"编译成功！过渡文件未删除: {str(e)}")
                    self.output_label.SetForegroundColour(wx.Colour(255, 165, 0))

            finally:
                os.chdir(original_dir)

        except subprocess.CalledProcessError as e:
            self.output_label.SetLabel(f"编译失败！错误信息: {e.stderr}")
            self.output_label.SetForegroundColour(wx.Colour(255, 0, 0))
        except Exception as e:
            self.output_label.SetLabel(f"意外错误: {str(e)}")
            self.output_label.SetForegroundColour(wx.Colour(255, 0, 0))

if __name__ == "__main__":
    app = wx.App(False)
    CompileFrame()
    app.MainLoop()
