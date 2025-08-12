import tkinter as tk
from tkinter import ttk
import sys
from multiprocessing import Process
import os

from tool.Compile_Pytoso import CompileWindow
from tool.Error_Windows import ErrorAWindow
from tool.Restart_Services import FunctionAWindow
from tool.Zigbee_Sniffer import FunctionBWindow


class main():
    def __init__(self):
        self.all_windows = []

    
    def run_gui(self):
        # 创建主窗口
        root = tk.Tk()
        root.title("主程序")
        root.geometry("400x300")
        

        main_frame = tk.Frame(root)
        main_frame.pack(side="top")  # 占满剩余空间
        main_frame.pack_propagate(False)  # 防止被控件撑开

        # 全局变量存储所有窗口
        self.all_windows = [root]
        self.functions = {"单独文件so编译工具":lambda : open_window("单独文件so编译工具","500x150", CompileWindow),
                          "重启wisdom服务":lambda : open_window("重启wisdom服务","500x150", FunctionAWindow),
                          "ZigBee Sniffer":lambda : open_window("ZigBee Sniffer","500x150", FunctionBWindow)}

        # 清理所有窗口并退出程序
        def cleanup():
            for window in self.all_windows[:]:
                try:
                    window.destroy()
                except:
                    pass
            print("程序已关闭")

        def open_window(title, size, content_class):
            new_window = tk.Toplevel(root)
            new_window.title(title)
            new_window.geometry(size)
            content_class(new_window)
            _register_window(new_window)


        def _register_window(window):
            # 新窗口关闭时从列表中移除
            self.all_windows.append(window)
            def remove_window():
                if window in self.all_windows:
                    self.all_windows.remove(window)
                window.destroy()
            window.protocol("WM_DELETE_WINDOW", remove_window)



        def button_click():
            selected_option = dropdown.get()
            if selected_option in list(self.functions.keys()):
                self.functions[selected_option]()  # 调用对应的函数
            else:
                open_window("Error","500x150", ErrorAWindow)

            
            

        
        def clear_and_create():
            # 清空所有子控件
            for widget in main_frame.winfo_children():
                widget.destroy()
            # 添加新控件
  
            tk.Label(main_frame, text="单独文件so编译工具").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            tk.Button(main_frame, text="启动",command=lambda: open_window("单独文件so编译工具","500x150", CompileWindow)).grid(row=0, column=1, padx=5, pady=5)

            tk.Label(main_frame, text="重启wisdom服务").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
            tk.Button(main_frame, text="启动", command=lambda: open_window("重启wisdom服务","500x150", FunctionAWindow)).grid(row=1, column=1, padx=5, pady=5)
  
            tk.Label(main_frame, text="ZigBee Sniffer").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
            tk.Button(main_frame, text="启动", command=lambda: open_window("ZigBee Sniffer","500x150", FunctionBWindow)).grid(row=2, column=1, padx=5, pady=5)




        # 绑定主窗口关闭事件
        root.protocol("WM_DELETE_WINDOW", cleanup)

        # 创建并添加文本框
        label_textbox = tk.Label(main_frame, text="选择使用功能")   

        # 创建并添加下拉框
        options = list(self.functions.keys())
        dropdown = ttk.Combobox(main_frame, values=options, state="readonly")
        dropdown.set("ZigBee Sniffer")
        button = tk.Button(main_frame, text="使用", command=button_click)
        button2 = tk.Button(main_frame, text="展开全部", command=clear_and_create)

        label_textbox.grid(row=0, column=0,columnspan=2, padx=5, pady=5)
        dropdown.grid(row=1, column=0,columnspan=2, padx=5, pady=5)
        button.grid(row=2, column=0, padx=5, pady=5)
        button2.grid(row=2, column=1, padx=5, pady=5)




        # 启动事件循环
        root.mainloop()

if __name__ == "__main__":
    # 启动 GUI 进程
    zhu_pro = main()
    p = Process(target=zhu_pro.run_gui, daemon=True)  # 设置为守护进程
    p.start()
    print("脚本执行完成，窗口在独立进程中运行")
    os._exit(0)  # 强制退出主进程，终端立即返回