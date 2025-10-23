# File: main.py (Ở thư mục gốc)
# Điểm bắt đầu chạy ứng dụng.

import tkinter as tk
import sys
from tkinter import messagebox
import os

# --- Cấu hình đường dẫn ---
# Thêm thư mục gốc của project vào sys.path để Python tìm thấy các module con
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# ---------------------------

# --- Import Lớp Ứng dụng Chính ---
try:
    # Import lớp PoseApp từ module app.logic.app_logic
    from app.logic.app_logic import PoseApp
    print(">>> Đã import PoseApp thành công.")
except ImportError as e:
    messagebox.showerror("Lỗi Import Chính", f"Không thể import PoseApp:\n{e}\n\nVui lòng kiểm tra cấu trúc thư mục, các file __init__.py và đường dẫn import.")
    exit()
except Exception as e:
     messagebox.showerror("Lỗi Khởi tạo", f"Lỗi không xác định khi import:\n{e}")
     exit()
# --------------------------------

# === ĐIỂM BẮT ĐẦU CHẠY ===
if __name__ == "__main__":
    print("--- Bắt đầu chạy main.py ---")
    try:
        # Kiểm tra thư viện Pillow trước khi tạo UI
        try:
            from PIL import Image, ImageTk
        except ImportError:
            messagebox.showerror("Lỗi Thiếu Thư Viện", "Thư viện Pillow chưa cài.\nVui lòng chạy trong terminal:\npip install Pillow")
            exit()

        # Tạo cửa sổ gốc Tkinter
        root = tk.Tk()
        # Khởi tạo đối tượng ứng dụng (lớp PoseApp)
        app = PoseApp(root)
        # Bắt đầu vòng lặp sự kiện chính của Tkinter (để cửa sổ hiển thị và tương tác)
        print("--- Bắt đầu vòng lặp chính Tkinter ---")
        root.mainloop()
        print("--- Vòng lặp chính Tkinter đã kết thúc ---") # Dòng này chỉ chạy khi cửa sổ đóng

    except Exception as e:
         messagebox.showerror("Lỗi Chạy Ứng Dụng", f"Đã xảy ra lỗi không mong muốn:\n{e}")
         print(f"[LỖI CHUNG] {e}")