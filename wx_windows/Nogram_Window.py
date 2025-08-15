import wx
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from weave.nogram import solve_nonogram


class MultiNumberInput(wx.Frame):
    def __init__(self, parent=None, title="新窗口", size=(600, 600), table=[10,10]):
        super().__init__(parent, title=title, size=size)
        self.panel = wx.Panel(self)

        self.x_count = table[0]  # 横向个数
        self.y_count = table[1]  # 纵向个数

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 横向输入框（列标题）
        hbox_top = wx.BoxSizer(wx.HORIZONTAL)
        hbox_top.Add(wx.StaticText(self.panel, label="", size=(100, 100)), 0, wx.ALL, 5)  # 左上角空白

        self.x_inputs = []
        for col in range(self.x_count):
            txt = wx.TextCtrl(self.panel, size=(24, 100),style=wx.TE_MULTILINE | wx.BORDER_SIMPLE)
            font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            txt.SetFont(font)
            txt.SetMargins(0, 0)
            hbox_top.Add(txt, 0, wx.ALL, 5)
            self.x_inputs.append(txt)
        main_sizer.Add(hbox_top, 0, wx.CENTER)
        self.squares = []
        self.y_inputs = []
        for col in range(self.y_count):
            hbox_row = wx.BoxSizer(wx.HORIZONTAL)
            txt = wx.TextCtrl(self.panel, size=(100, 24),style=wx.TE_MULTILINE | wx.BORDER_SIMPLE)
            font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            txt.SetFont(font)
            txt.SetMargins(0, 0)
            hbox_row.Add(txt, 0, wx.ALL, 5)
            self.y_inputs.append(txt)
            row_squares = []
            for _ in range(self.x_count):
                square = wx.Panel(self.panel, size=(24, 24), style=wx.BORDER_SIMPLE)
                square.SetBackgroundColour(wx.Colour(255, 255, 255))
                square.SetMinSize((24, 24))  # 保证固定大小
                hbox_row.Add(square, 0, wx.ALL, 5)
                row_squares.append(square)
            self.squares.append(row_squares)
            main_sizer.Add(hbox_row, 0, wx.CENTER)

        # 按钮

        hbtn_row = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self.panel, label="计算结果")
        btn.Bind(wx.EVT_BUTTON, self.on_print)
        btn2 = wx.Button(self.panel, label="返回")
        btn2.Bind(wx.EVT_BUTTON, self.on_back)
        hbtn_row.Add(btn, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        hbtn_row.Add(btn2, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        main_sizer.Add(hbtn_row, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizer(main_sizer)
        self.Centre()
        self.Show()

    def on_print(self, event):
        # 初始化棋盘
        x_values = [txt.GetValue() for txt in self.x_inputs]
        y_values = [txt.GetValue() for txt in self.y_inputs]
        row_clues = [[int(x) for x in s.split() if x.strip()] for s in y_values]
        col_clues = [[int(x) for x in s.split() if x.strip()] for s in x_values]
        # 初始化棋盘
        height = len(row_clues)
        width = len(col_clues)
        board_default = [[-1]*width for _ in range(height)]   
        solution = solve_nonogram(board_default, row_clues, col_clues)
        if solution:
            for r in range(self.y_count):
                for c in range(self.x_count):
                    if solution[r][c]==1:
                        self.squares[r][c].SetBackgroundColour(wx.Colour(0, 0, 0))
                    else:
                        self.squares[r][c].SetBackgroundColour(wx.Colour(255, 255, 255))
                    self.squares[r][c].Refresh()  # 刷新UI
        else:
            wx.MessageBox("数据无法生成结果", "报错", wx.OK | wx.ICON_INFORMATION)
    
    def on_back(self, event):
        # 创建新窗口
        try:
            new_frame = NogramFrame()
            new_frame.Show()
            self.Close()
        except:
            wx.MessageBox(f"没有输入有效数字！", "提示")

class NogramFrame(wx.Frame):
    def __init__(self, parent=None, title="", size=(175, 200)):
        super().__init__(parent, title=title, size=size)
        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 第一行: wisdom_engine.service
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label1 = wx.StaticText(panel, label="Row", style=wx.ALIGN_RIGHT)
        self.text_input1 = wx.TextCtrl(panel, value="", size=(75, -1))
        hbox1.Add(label1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        hbox1.Add(self.text_input1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label2 = wx.StaticText(panel, label="Col", style=wx.ALIGN_RIGHT)
        self.text_input2 = wx.TextCtrl(panel, value="", size=(75, -1))
        hbox2.Add(label2, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        hbox2.Add(self.text_input2, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        main_sizer.Add(hbox1, 0, wx.EXPAND)
        main_sizer.Add(hbox2, 0, wx.EXPAND)
        self.btn_start = wx.Button(panel, label="确认")
        self.btn_start.Bind(wx.EVT_BUTTON, self.on_confirm)
        main_sizer.Add(self.btn_start, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        panel.SetSizer(main_sizer)
        self.Centre()
        self.Show()      
        self.Raise()      # 提升到最前面
        self.SetFocus()   # 获取焦点

    def on_confirm(self, event):
        # 读取输入值
        row = self.text_input1.GetValue()
        col = self.text_input2.GetValue()

        # 创建新窗口
        try:
            new_frame = MultiNumberInput(None, title="",table=[int(row),int(col)])
            new_frame.Show()
            self.Close()
        except:
            wx.MessageBox(f"没有输入有效数字！", "提示")

if __name__ == "__main__":
    app = wx.App(False)
    # frame = RowColFrame()
    frame = MultiNumberInput()
    app.MainLoop()
