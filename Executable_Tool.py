import tkinter as tk
from tkinter import ttk
import sys
from multiprocessing import Process
import os

from tool.Compile_Pytoso import CompileWindow
from tool.Restart_Services import FunctionAWindow


class main():
    def __init__(self):
        self.all_windows = []

    def run_gui(self):
        # 创建主窗口
        root = tk.Tk()
        root.title("主程序")
        root.geometry("400x300")

        # 全局变量存储所有窗口
        self.all_windows = [root]


        # 清理所有窗口并退出程序
        def cleanup():
            for window in self.all_windows[:]:
                try:
                    window.destroy()
                except:
                    pass
            print("程序已关闭")

        def button_click():
            selected_option = dropdown.get()
            if selected_option == "将py文件编译成so":
                # 创建并添加按钮
                new_window = tk.Toplevel(root)
                self.all_windows.append(new_window)
                new_window.title("单独文件so编译工具")
                new_window.geometry("500x150")
                CompileWindow(new_window)
                # 新窗口关闭时从列表中移除
                def remove_window():
                    if new_window in self.all_windows:
                        self.all_windows.remove(new_window)
                    new_window.destroy()
                new_window.protocol("WM_DELETE_WINDOW", remove_window)
            elif selected_option == "重启wisdom服务":
                new_window = tk.Toplevel(root)
                self.all_windows.append(new_window)
                new_window.title("服务重启")
                new_window.geometry("500x300")
                FunctionAWindow(new_window)
                # 新窗口关闭时从列表中移除
                def remove_window():
                    if new_window in self.all_windows:
                        self.all_windows.remove(new_window)
                    new_window.destroy()
                new_window.protocol("WM_DELETE_WINDOW", remove_window)
            elif selected_option == "选项3":
                ...
            elif selected_option == "选项4":
                ...
        # 绑定主窗口关闭事件
        root.protocol("WM_DELETE_WINDOW", cleanup)

        # 创建并添加文本框
        label_textbox = tk.Label(root, text="选择使用功能")
        label_textbox.pack(pady=5)
        
        # 创建并添加下拉框
        options = ["将py文件编译成so", "重启wisdom服务", "选项3", "选项4"]
        dropdown = ttk.Combobox(root, values=options, state="readonly")
        dropdown.set("重启wisdom服务")
        dropdown.pack(pady=5)

        # 创建按钮事件
        button = tk.Button(root, text="使用", command=button_click)
        button.pack(pady=5)

        # 启动事件循环
        root.mainloop()

if __name__ == "__main__":
    # 启动 GUI 进程
    zhu_pro = main()
    p = Process(target=zhu_pro.run_gui, daemon=True)  # 设置为守护进程
    p.start()
    print("脚本执行完成，窗口在独立进程中运行")
    os._exit(0)  # 强制退出主进程，终端立即返回