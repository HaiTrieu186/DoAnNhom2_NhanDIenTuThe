# Chức năng: Tạo và sắp xếp các thành phần giao diện (widgets) cho ứng dụng.
import tkinter as tk
from tkinter import ttk


def create_ui_widgets(root, app_commands):
    """
    Tạo tất cả các widget và đặt chúng vào cửa sổ root.
    Trả về dictionary chứa các widget quan trọng.
    """
    root.configure(bg="#F0F0F0")

    # --- Style ---
    style = ttk.Style()
    style.theme_use('vista')
    style.configure('TButton', font=('Segoe UI', 10), padding=5)
    style.configure('TLabel', font=('Segoe UI', 10), background="#F0F0F0")
    style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), background="#F0F0F0")
    style.configure('Path.TLabel', font=('Segoe UI', 9), background="#F0F0F0", foreground="dimgray")
    style.configure('Param.TLabel', font=('Segoe UI', 9), background="#F0F0F0")

    # --- Khung chính ---
    main_frame = ttk.Frame(root, padding="15")
    main_frame.pack(expand=True, fill=tk.BOTH)

    # --- Tiêu đề ---
    header_label = ttk.Label(main_frame, text="ỨNG DỤNG NHẬN DẠNG TƯ THẾ NGƯỜI",
                             style='Header.TLabel', anchor=tk.CENTER)
    header_label.pack(pady=(0, 15), fill=tk.X)

    # --- Khung hiển thị ảnh ---
    image_label = tk.Label(main_frame, bg="darkgrey")
    image_label.pack(pady=10)

    # --- Hiển thị kết quả ---
    result_frame = ttk.Frame(main_frame)
    result_frame.pack(fill=tk.BOTH, pady=10)

    ttk.Label(result_frame, text="Kết quả:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)

    result_label = tk.Label(result_frame, text="...",
                            font=('Segoe UI', 11, 'italic'),
                            foreground="navy",
                            background="#F0F0F0",
                            justify=tk.LEFT,
                            wraplength=600,
                            anchor=tk.W)
    result_label.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    # ==================== KHUNG ĐIỀU CHỈNH THAM SỐ ẢNH ====================
    # Vị trí: Giữa result_frame và bottom_frame
    params_frame = ttk.LabelFrame(main_frame, text="Điều chỉnh ảnh", padding="10")
    params_frame.pack(fill=tk.X, pady=(5, 10))

    # >>>>>> VỊ TRÍ THÊM CÁC Ô NHẬP LIỆU (ENTRIES) <<<<<<
    # Container cho các entries nằm ngang
    entries_container = ttk.Frame(params_frame)
    entries_container.pack(fill=tk.X, pady=(0, 8))

    # Gamma
    gamma_frame = ttk.Frame(entries_container)
    gamma_frame.pack(side=tk.LEFT, padx=(0, 15))
    ttk.Label(gamma_frame, text="Gamma:", style='Param.TLabel').pack(side=tk.LEFT, padx=(0, 5))
    gamma_entry = ttk.Entry(gamma_frame, width=8)
    gamma_entry.insert(0, "1.0")  # Giá trị mặc định
    gamma_entry.pack(side=tk.LEFT)

    # Tương phản (Contrast)
    contrast_frame = ttk.Frame(entries_container)
    contrast_frame.pack(side=tk.LEFT, padx=(0, 15))
    ttk.Label(contrast_frame, text="Tương phản:", style='Param.TLabel').pack(side=tk.LEFT, padx=(0, 5))
    contrast_entry = ttk.Entry(contrast_frame, width=8)
    contrast_entry.insert(0, "1.0")  # Giá trị mặc định
    contrast_entry.pack(side=tk.LEFT)

    # Độ sáng (Brightness)
    brightness_frame = ttk.Frame(entries_container)
    brightness_frame.pack(side=tk.LEFT, padx=(0, 15))
    ttk.Label(brightness_frame, text="Độ sáng:", style='Param.TLabel').pack(side=tk.LEFT, padx=(0, 5))
    brightness_entry = ttk.Entry(brightness_frame, width=8)
    brightness_entry.insert(0, "0")  # Giá trị mặc định
    brightness_entry.pack(side=tk.LEFT)

    # >>>>>> VỊ TRÍ THÊM CÁC NÚT ĐIỀU CHỈNH (BUTTONS) <<<<<<
    # Container cho các buttons nằm ngang
    buttons_container = ttk.Frame(params_frame)
    buttons_container.pack(fill=tk.X)

    btn_apply_gamma = ttk.Button(buttons_container, text="Áp dụng Gamma",
                                 command=lambda: app_commands.get('apply_gamma', lambda: None)())
    btn_apply_gamma.pack(side=tk.LEFT, padx=(0, 5))

    btn_apply_contrast = ttk.Button(buttons_container, text="Áp dụng Tương phản",
                                    command=lambda: app_commands.get('apply_contrast', lambda: None)())
    btn_apply_contrast.pack(side=tk.LEFT, padx=(0, 5))

    btn_apply_brightness = ttk.Button(buttons_container, text="Áp dụng Độ sáng",
                                      command=lambda: app_commands.get('apply_brightness', lambda: None)())
    btn_apply_brightness.pack(side=tk.LEFT, padx=(0, 5))

    btn_reset_params = ttk.Button(buttons_container, text="Đặt lại",
                                  command=lambda: app_commands.get('reset_params', lambda: None)())
    btn_reset_params.pack(side=tk.LEFT, padx=(0, 5))

    # ===================================================================

    # --- Khung điều khiển dưới cùng ---
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

    # -- Tải ảnh --
    upload_frame = ttk.Frame(bottom_frame)
    upload_frame.pack(fill=tk.X, pady=5)

    upload_button = ttk.Button(upload_frame, text="Tải Ảnh Lên",
                               command=app_commands['upload'])
    upload_button.pack(side=tk.LEFT, padx=(0, 10))

    filepath_label = ttk.Label(upload_frame, text="Chưa chọn file",
                               style='Path.TLabel', width=60,
                               anchor=tk.W, relief=tk.SUNKEN, padding=3)
    filepath_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # -- Điều khiển Camera & Thoát --
    camera_frame = ttk.Frame(bottom_frame)
    camera_frame.pack(fill=tk.X, pady=5)

    btn_cam_on = ttk.Button(camera_frame, text="Bật Camera",
                            command=app_commands['start_cam'])
    btn_cam_off = ttk.Button(camera_frame, text="Dừng Camera",
                             command=app_commands['stop_cam'], state=tk.DISABLED)
    btn_capture = ttk.Button(camera_frame, text="Chụp Ảnh",
                             command=app_commands['capture'], state=tk.DISABLED)
    btn_exit = ttk.Button(camera_frame, text="Thoát",
                          command=app_commands['quit'])

    btn_cam_on.pack(side=tk.LEFT, padx=5)
    btn_cam_off.pack(side=tk.LEFT, padx=5)
    btn_capture.pack(side=tk.LEFT, padx=5)
    ttk.Frame(camera_frame).pack(side=tk.LEFT, expand=True, fill=tk.X)
    btn_exit.pack(side=tk.RIGHT, padx=5)

    # Trả về dictionary chứa các widget cần truy cập từ bên ngoài
    return {
        'image_label': image_label,
        'result_label': result_label,
        'filepath_label': filepath_label,
        'btn_cam_on': btn_cam_on,
        'btn_cam_off': btn_cam_off,
        'btn_capture': btn_capture,

        # >>>>>> THÊM CÁC WIDGET MỚI VÀO ĐÂY <<<<<<
        'gamma_entry': gamma_entry,
        'contrast_entry': contrast_entry,
        'brightness_entry': brightness_entry,
        'btn_apply_gamma': btn_apply_gamma,
        'btn_apply_contrast': btn_apply_contrast,
        'btn_apply_brightness': btn_apply_brightness,
        'btn_reset_params': btn_reset_params
    }