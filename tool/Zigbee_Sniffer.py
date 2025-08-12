# cython: language_level=3
import tkinter as tk
import subprocess

class FunctionBWindow:
    def __init__(self, root):
        self.root = root
        # 创建主框架
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)


        self.file_entry = tk.Label(self.main_frame, text="Channle")
        self.file_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        

        # 文件路径输入框
        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(self.main_frame, textvariable=self.file_path_var, width=40)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")


        # 编译按钮
        self.compile_button = tk.Button(self.main_frame, text="查看", command=self.start_sniff)
        self.compile_button.grid(row=1, column=1,columnspan=2, padx=5, pady=5)

    def start_sniff(self):
        # 开始抓包
        channel = self.file_path_var.get()
        if not channel:
            channel = "11"
        print(f"开始抓包: {channel}")
        try:
            # 这里写你想执行的命令，比如：
            cmd = f"sudo whsniff -c {channel} | wireshark -k -i -"
            print(cmd)
            subprocess.Popen(cmd, shell=True)
        except Exception as e:
            print(f"执行异常: {e}")
        finally:
            print("执行结束")
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionBWindow(root)
    root.mainloop()


