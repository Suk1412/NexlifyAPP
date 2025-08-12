# cython: language_level=3
import tkinter as tk
from tkinter import filedialog
import os
import subprocess

class CompileWindow:
    def __init__(self, root):
        self.root = root
        # self.root.title("单独文件so编译工具")
        # self.root.geometry("500x150")
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 文件路径输入框
        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(self.main_frame, textvariable=self.file_path_var, width=40)
        self.file_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # 浏览按钮
        self.browse_button = tk.Button(self.main_frame, text="浏览", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, padx=5, pady=5)
        
        # 编译按钮
        self.compile_button = tk.Button(self.main_frame, text="编译", command=self.compile_file)
        self.compile_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # 输出标签
        self.output_label = tk.Label(self.main_frame, text="", wraplength=450)
        self.output_label.grid(row=2, column=0, columnspan=2, pady=5)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def compile_file(self):
        file_path = self.file_path_var.get()
        if not file_path:
            self.output_label.config(text="请先选择一个文件!", fg="red")
            return
            
        try:
            # 获取文件所在目录
            working_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            base_name = os.path.splitext(file_name)[0]
            
            # 切换到文件所在目录
            original_dir = os.getcwd()
            os.chdir(working_dir)
            
            try:
                # 执行 cython 命令
                cython_cmd = ["python3", "-m", "cython", file_name, "--embed"]
                subprocess.run(cython_cmd, check=True, capture_output=True, text=True)
                
                # 执行第一个 gcc 命令
                gcc1_cmd = [
                    "gcc", "-c", "-fPIC",
                    "-I", "/usr/include/python3.10/",
                    f"{base_name}.c",
                    "-o", f"{base_name}.o"
                ]
                subprocess.run(gcc1_cmd, check=True, capture_output=True, text=True)
                
                # 执行第二个 gcc 命令
                gcc2_cmd = [
                    "gcc", "-shared",
                    f"{base_name}.o",
                    "-o", f"{base_name}.so"
                ]
                subprocess.run(gcc2_cmd, check=True, capture_output=True, text=True)
                
                # 删除中间生成的 .c 和 .o 文件
                try:
                    os.remove(f"{base_name}.c")
                    os.remove(f"{base_name}.o")
                except OSError as e:
                    self.output_label.config(
                        text=f"编译成功！过渡文件未删除: {str(e)}",
                        fg="orange"
                    )
                    return
                
                self.output_label.config(
                    text="编译成功！过渡文件已删除.",
                    fg="green"
                )
                
            finally:
                # 恢复原始工作目录
                os.chdir(original_dir)
                
        except subprocess.CalledProcessError as e:
            self.output_label.config(
                text=f"编译失败！错误信息: {e.stderr}",
                fg="red"
            )
        except Exception as e:
            self.output_label.config(
                text=f"意外错误: {str(e)}",
                fg="red"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = CompileWindow(root)
    root.mainloop()


