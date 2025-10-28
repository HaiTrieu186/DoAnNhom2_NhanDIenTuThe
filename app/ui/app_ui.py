import tkinter as tk
from tkinter import ttk

def create_ui_widgets(root, app_commands):
    """
    Tạo và sắp xếp các widget giao diện.
    """
    root.configure(bg="#F0F0F0")

    # Định nghĩa style
    style = ttk.Style()
    style.theme_use('vista')
    style.configure('TButton', font=('Segoe UI', 10), padding=5)
    style.configure('TLabel', font=('Segoe UI', 10), background="#F0F0F0")
    style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), background="#F0F0F0")
    style.configure('Result.TLabel', font=('Segoe UI', 14, 'italic'), foreground="navy", background="#F0F0F0")
    style.configure('Path.TLabel', font=('Segoe UI', 9), background="#F0F0F0", foreground="dimgray")

    # Khung chính
    main_frame = ttk.Frame(root, padding="15")
    main_frame.pack(expand=True, fill=tk.BOTH)

    # Tiêu đề
    header_label = ttk.Label(main_frame, text="ỨNG DỤNG NHẬN DẠNG TƯ THẾ NGƯỜI", style='Header.TLabel', anchor=tk.CENTER)
    header_label.pack(pady=(0, 15), fill=tk.X)

    # Khung hiển thị ảnh
    image_label = tk.Label(main_frame, bg="darkgrey")
    image_label.pack(pady=10)

    # Hiển thị kết quả
    result_frame = ttk.Frame(main_frame)
    result_frame.pack(fill=tk.BOTH, pady=10)

    ttk.Label(result_frame, text="Kết quả:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)

    result_label = tk.Label(result_frame, text="...",
                            font=('Segoe UI', 11, 'italic'),
                            foreground="navy",
                            background="#F0F0F0",
                            justify=tk.LEFT,
                            wraplength=600,  # Tự động xuống dòng
                            anchor=tk.W)
    result_label.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    # Khung điều khiển
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

    # Nút tải ảnh
    upload_frame = ttk.Frame(bottom_frame)
    upload_frame.pack(fill=tk.X, pady=5)
    upload_button = ttk.Button(upload_frame, text="Tải Ảnh Lên", command=app_commands['upload'], style='TButton')
    filepath_label = ttk.Label(upload_frame, text="Chưa chọn file", style='Path.TLabel', width=60, anchor=tk.W, relief=tk.SUNKEN, padding=3)
    upload_button.pack(side=tk.LEFT, padx=(0, 10))
    filepath_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Nút camera và thoát
    camera_frame = ttk.Frame(bottom_frame)
    camera_frame.pack(fill=tk.X, pady=5)
    btn_cam_on = ttk.Button(camera_frame, text="Bật Camera", command=app_commands['start_cam'], style='TButton')
    btn_cam_off = ttk.Button(camera_frame, text="Dừng Camera", command=app_commands['stop_cam'], state=tk.DISABLED, style='TButton')
    btn_capture = ttk.Button(camera_frame, text="Chụp Ảnh", command=app_commands['capture'], state=tk.DISABLED, style='TButton')
    btn_exit = ttk.Button(camera_frame, text="Thoát", command=app_commands['quit'], style='TButton')

    btn_cam_on.pack(side=tk.LEFT, padx=5)
    btn_cam_off.pack(side=tk.LEFT, padx=5)
    btn_capture.pack(side=tk.LEFT, padx=5)
    ttk.Frame(camera_frame).pack(side=tk.LEFT, expand=True, fill=tk.X) # Đẩy nút Thoát sang phải
    btn_exit.pack(side=tk.RIGHT, padx=5)

    # Trả về các widget cần điều khiển
    return {
        'image_label': image_label,
        'result_label': result_label,
        'filepath_label': filepath_label,
        'btn_cam_on': btn_cam_on,
        'btn_cam_off': btn_cam_off,
        'btn_capture': btn_capture
    }