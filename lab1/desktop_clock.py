import tkinter as tk
import time

class DesktopClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("桌面时钟")
        self.root.configure(bg="#1a1a1a")  # 深色背景
        self.root.attributes("-topmost", True)  # 窗口置顶
        self.root.resizable(False, False)  # 禁止调整窗口大小
        self.root.attributes("-alpha", 0.9)  # 窗口透明度
        
        # 创建日期标签
        self.date_label = tk.Label(
            self.root,
            font=("Courier", 16, "bold"),
            bg="#1a1a1a",
            fg="#00ff00"  # 荧光绿字体
        )
        self.date_label.pack(padx=20, pady=(10, 0))
        
        # 创建时间标签
        self.time_label = tk.Label(
            self.root,
            font=("Courier", 48, "bold"),
            bg="#1a1a1a",
            fg="#00ff00"  # 荧光绿字体
        )
        self.time_label.pack(padx=20, pady=10)
        
        # 更新时间和日期
        self.update_time()
        
        self.root.mainloop()
    
    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y-%m-%d %A")
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.root.after(1000, self.update_time)  # 每秒更新一次

if __name__ == "__main__":
    DesktopClock()
