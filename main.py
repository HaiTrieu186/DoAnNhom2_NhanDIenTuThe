import tkinter as tk
from tkinter import messagebox
import sys
import os

# Thêm thư mục 'app' vào path để import
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import lớp App chính
try:
    from app.logic.app_logic import PoseApp
except ImportError:
    messagebox.showerror("Lỗi", "Không tìm thấy file app_logic.py")
    sys.exit()


def main():
    # Kiểm tra thư viện PIL
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("Lỗi", "Chưa cài thư viện Pillow!\nVui lòng chạy: pip install Pillow")
        sys.exit()

    # Chạy app
    try:
        root = tk.Tk()
        app = PoseApp(root)
        root.mainloop()
    except Exception as e:
         messagebox.showerror("Lỗi", f"Gặp lỗi khi chạy app:\n{e}")


# Chạy hàm main
if __name__ == "__main__":
    main()