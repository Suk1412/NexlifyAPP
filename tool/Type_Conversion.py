import tkinter as tk
from tkinter import ttk
import base64
import binascii
import ast

class TextConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Converter")
        self.root.geometry("600x400")

        # 主框架
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 输入文本框
        self.input_label = tk.Label(self.main_frame, text="Input Text:")
        self.input_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input_text = tk.Text(self.main_frame, height=4, width=50)
        self.input_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # 输入类型下拉列表
        self.input_type_label = tk.Label(self.main_frame, text="Input Type:")
        self.input_type_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.input_type = ttk.Combobox(self.main_frame, values=["Hex", "Bytes"], state="readonly")
        self.input_type.set("Hex")
        self.input_type.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # 输出类型下拉列表
        self.output_type_label = tk.Label(self.main_frame, text="Output Type:")
        self.output_type_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.output_type = ttk.Combobox(self.main_frame, values=["Hex","Bytes"], state="readonly")
        self.output_type.set("Hex")
        self.output_type.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # 转换按钮
        self.convert_button = tk.Button(self.main_frame, text="Convert", command=self.convert_text)
        self.convert_button.grid(row=4, column=0, columnspan=2, pady=10)

        # 输出文本框
        self.output_label = tk.Label(self.main_frame, text="Output Text:")
        self.output_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.output_text = tk.Text(self.main_frame, height=4, width=50, state="disabled")
        self.output_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # 确保网格布局调整
        self.main_frame.columnconfigure(1, weight=1)

    def convert_text(self):
        # 清空输出文本框
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)

        # 获取输入
        input_text = self.input_text.get("1.0", tk.END).strip()
        input_type = self.input_type.get()
        output_type = self.output_type.get()

        try:
            if input_type == "Hex":
                cleaned_input = input_text[2:] if input_text.lower().startswith('0x') else input_text
                if len(cleaned_input) % 2 != 0:
                    cleaned_input = '0' + cleaned_input
                if not all(c in '0123456789abcdefABCDEF' for c in cleaned_input.replace(' ', '')):
                    raise ValueError("Input is not a valid hexadecimal string")
                try:
                    intermediate = bytes.fromhex(cleaned_input)
                    print(type(intermediate),intermediate)
                except ValueError as e:
                    raise ValueError("Invalid hexadecimal string: " + str(e))
            elif input_type == "Bytes":
                # 安全解析 bytes 字面量
                try:
                    # 使用 ast.literal_eval 解析输入为 bytes 对象
                    bytes_obj = ast.literal_eval(input_text)
                    if not isinstance(bytes_obj, bytes):
                        raise ValueError("Input is not a valid Bytes")
                    intermediate = bytes_obj
                except (ValueError, SyntaxError) as e:
                    raise ValueError("Invalid bytes literal: " + str(e))
            
            # 从中间表示转换为输出类型
            if output_type == "Hex":
                result = intermediate.hex()
            elif output_type == "Bytes":
                result = repr(intermediate)
                print(type(result), result,intermediate)

            
            self.output_text.insert(tk.END, result)
            self.output_text.config(state="disabled")

        except (binascii.Error, UnicodeDecodeError, base64.binascii.Error) as e:
            self.output_text.insert(tk.END, f"Error: Invalid input format for {input_type}")
            self.output_text.config(state="disabled")
        except Exception as e:
            self.output_text.insert(tk.END, f"Unexpected error: {str(e)}")
            self.output_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextConverter(root)
    root.mainloop()