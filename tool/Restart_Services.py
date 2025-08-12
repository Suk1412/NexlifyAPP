# cython: language_level=3
import tkinter as tk
import subprocess

class FunctionAWindow:
    def __init__(self, root):
        self.root = root
        # 创建主框架
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)


        self.file_entry = tk.Label(self.main_frame, text="wisdom_engine.service")
        self.file_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # 重启按钮
        self.browse_button = tk.Button(self.main_frame, text="重启", command=lambda: self.run_command("sudo systemctl restart wisdom_engine.service"))
        self.browse_button.grid(row=0, column=1, padx=5, pady=5)
        
        # 编译按钮
        self.compile_button = tk.Button(self.main_frame, text="查看", command=lambda: self.run_command("sudo systemctl status wisdom_engine.service"))
        self.compile_button.grid(row=0, column=2, padx=5, pady=5)


        self.file_entry = tk.Label(self.main_frame, text="supervisorctl")
        self.file_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # 重启按钮
        self.browse_button = tk.Button(self.main_frame, text="重启", command=lambda: self.run_command("sudo supervisorctl restart all"))
        self.browse_button.grid(row=1, column=1, padx=5, pady=5)
        
        # 编译按钮
        self.compile_button = tk.Button(self.main_frame, text="查看", command=lambda: self.run_command("sudo supervisorctl status all"))
        self.compile_button.grid(row=1, column=2, padx=5, pady=5)


        # 文本区域，用于显示输出
        self.output_text = tk.Text(self.main_frame, height=10, width=50, wrap="none")
        self.output_text.grid(row=2, column=0, columnspan=3)
        xscroll = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.output_text.xview)
        xscroll.grid(row=3, column=0,columnspan=3, sticky="ew")
        yscroll = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        yscroll.grid(row=2, column=3, sticky="ns")
        self.output_text.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)


    def run_command(self,cmd = None):
        # 清空之前内容
        self.output_text.delete(1.0, tk.END)
        try:
            # 这里写你想执行的命令，比如：
            if not cmd:
                cmd = "echo Hello, world!"  # 示例命令，替换为你的命令
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            self.output_text.insert(tk.END, f"命令: {cmd}\n")
            self.output_text.insert(tk.END, f"返回码: {result.returncode}\n")
            self.output_text.insert(tk.END, f"标准输出:\n{result.stdout}\n")
            if result.stderr:
                self.output_text.insert(tk.END, f"错误输出:\n{result.stderr}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"执行异常: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionAWindow(root)
    root.mainloop()


