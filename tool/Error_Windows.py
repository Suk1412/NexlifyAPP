# cython: language_level=3
import tkinter as tk
import subprocess

class ErrorAWindow:
    def __init__(self, root):
        self.root = root
        # 创建主框架
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True,side="top")
        self.main_frame.pack_propagate(False)  # 防止被控件撑开

        self.file_entry = tk.Label(self.main_frame, text="没有找到对应的功能")
        self.file_entry.pack()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ErrorAWindow(root)
    root.mainloop()


