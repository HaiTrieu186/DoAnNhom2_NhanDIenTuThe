import tkinter as tk
from tkinter import ttk


def create_ui_widgets(root, app_commands):
    root.configure(bg="#F0F0F0")

    style = ttk.Style()
    style.theme_use('vista')
    style.configure('TButton', font=('Segoe UI', 9), padding=3)
    style.configure('TLabel', font=('Segoe UI', 9), background="#F0F0F0")
    style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), background="#F0F0F0")
    style.configure('Result.TLabel', font=('Segoe UI', 10, 'italic'), foreground="navy", background="#F0F0F0")
    style.configure('Path.TLabel', font=('Segoe UI', 8), background="#F0F0F0", foreground="dimgray")
    style.configure('Param.TLabel', font=('Segoe UI', 8), background="#F0F0F0")

    canvas = tk.Canvas(root, bg="#F0F0F0", highlightthickness=0)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)

    main_frame = ttk.Frame(canvas, padding="10")

    canvas_frame = canvas.create_window((0, 0), window=main_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_frame_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas_width = canvas.winfo_width()
        canvas.itemconfig(canvas_frame, width=canvas_width)

    main_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_frame_configure)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    header_label = ttk.Label(main_frame, text="ỨNG DỤNG NHẬN DẠNG TƯ THẾ NGƯỜI",
                             style='Header.TLabel', anchor=tk.CENTER)
    header_label.pack(pady=(0, 10), fill=tk.X)

    image_label = tk.Label(main_frame, bg="darkgrey", width=640, height=480)
    image_label.pack(pady=5)

    result_frame = ttk.Frame(main_frame)
    result_frame.pack(fill=tk.BOTH, pady=5)

    ttk.Label(result_frame, text="Kết quả:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)

    result_label = tk.Label(result_frame, text="...",
                            font=('Segoe UI', 9, 'italic'),
                            foreground="navy",
                            background="#F0F0F0",
                            justify=tk.LEFT,
                            wraplength=500,
                            anchor=tk.W)
    result_label.pack(fill=tk.BOTH, expand=True, pady=(3, 0))

    # Khung xử lý ảnh
    params_frame = ttk.LabelFrame(main_frame, text="Xử lý ảnh", padding="8")
    params_frame.pack(fill=tk.X, pady=(5, 8))

    adjustable_frame = ttk.Frame(params_frame)
    adjustable_frame.pack(fill=tk.X, pady=(0, 5))

    entries_container = ttk.Frame(adjustable_frame)
    entries_container.pack(fill=tk.X, pady=(0, 5))

    gamma_frame = ttk.Frame(entries_container)
    gamma_frame.pack(side=tk.LEFT, padx=(0, 10))
    ttk.Label(gamma_frame, text="Gamma:", style='Param.TLabel').pack(side=tk.LEFT, padx=(0, 3))
    gamma_entry = ttk.Entry(gamma_frame, width=7)
    gamma_entry.insert(0, "1.0")
    gamma_entry.pack(side=tk.LEFT)

    contrast_frame = ttk.Frame(entries_container)
    contrast_frame.pack(side=tk.LEFT, padx=(0, 10))
    ttk.Label(contrast_frame, text="Tương phản:", style='Param.TLabel').pack(side=tk.LEFT, padx=(0, 3))
    contrast_entry = ttk.Entry(contrast_frame, width=7)
    contrast_entry.insert(0, "1.0")
    contrast_entry.pack(side=tk.LEFT)

    brightness_frame = ttk.Frame(entries_container)
    brightness_frame.pack(side=tk.LEFT, padx=(0, 10))
    ttk.Label(brightness_frame, text="Độ sáng:", style='Param.TLabel').pack(side=tk.LEFT, padx=(0, 3))
    brightness_entry = ttk.Entry(brightness_frame, width=7)
    brightness_entry.insert(0, "0")
    brightness_entry.pack(side=tk.LEFT)

    adjustable_buttons = ttk.Frame(adjustable_frame)
    adjustable_buttons.pack(fill=tk.X)

    btn_apply_gamma = ttk.Button(adjustable_buttons, text="Áp dụng Gamma",
                                 command=lambda: app_commands.get('apply_gamma', lambda: None)())
    btn_apply_gamma.pack(side=tk.LEFT, padx=(0, 3))

    btn_apply_contrast = ttk.Button(adjustable_buttons, text="Áp dụng Tương phản",
                                    command=lambda: app_commands.get('apply_contrast', lambda: None)())
    btn_apply_contrast.pack(side=tk.LEFT, padx=(0, 3))

    btn_apply_brightness = ttk.Button(adjustable_buttons, text="Áp dụng Độ sáng",
                                      command=lambda: app_commands.get('apply_brightness', lambda: None)())
    btn_apply_brightness.pack(side=tk.LEFT, padx=(0, 3))

    # Nhận dạng tư thế
    pose_frame = ttk.Frame(params_frame)
    pose_frame.pack(fill=tk.X, pady=(5, 5))

    btn_apply_pose = ttk.Button(pose_frame, text="🔍 Nhận dạng tư thế",
                                command=lambda: app_commands.get('apply_pose_detect', lambda: None)())
    btn_apply_pose.pack(side=tk.LEFT, padx=(0, 3))

    reset_frame = ttk.Frame(params_frame)
    reset_frame.pack(fill=tk.X)

    btn_reset_params = ttk.Button(reset_frame, text="🔄 Đặt lại ảnh gốc",
                                  command=lambda: app_commands.get('reset_params', lambda: None)())
    btn_reset_params.pack(side=tk.LEFT, padx=(0, 3))

    # Khung điều khiển
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(fill=tk.X, pady=(8, 0))

    upload_frame = ttk.Frame(bottom_frame)
    upload_frame.pack(fill=tk.X, pady=3)
    upload_button = ttk.Button(upload_frame, text="Tải Ảnh Lên",
                               command=app_commands['upload'], style='TButton')
    filepath_label = ttk.Label(upload_frame, text="Chưa chọn file",
                               style='Path.TLabel', width=50, anchor=tk.W,
                               relief=tk.SUNKEN, padding=2)
    upload_button.pack(side=tk.LEFT, padx=(0, 5))
    filepath_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    camera_frame = ttk.Frame(bottom_frame)
    camera_frame.pack(fill=tk.X, pady=3)
    btn_cam_on = ttk.Button(camera_frame, text="Bật Camera",
                            command=app_commands['start_cam'], style='TButton')
    btn_cam_off = ttk.Button(camera_frame, text="Dừng Camera",
                             command=app_commands['stop_cam'], state=tk.DISABLED, style='TButton')
    btn_capture = ttk.Button(camera_frame, text="Chụp Ảnh",
                             command=app_commands['capture'], state=tk.DISABLED, style='TButton')
    btn_exit = ttk.Button(camera_frame, text="Thoát",
                          command=app_commands['quit'], style='TButton')

    btn_cam_on.pack(side=tk.LEFT, padx=3)
    btn_cam_off.pack(side=tk.LEFT, padx=3)
    btn_capture.pack(side=tk.LEFT, padx=3)
    ttk.Frame(camera_frame).pack(side=tk.LEFT, expand=True, fill=tk.X)
    btn_exit.pack(side=tk.RIGHT, padx=3)

    return {
        'image_label': image_label,
        'result_label': result_label,
        'filepath_label': filepath_label,
        'btn_cam_on': btn_cam_on,
        'btn_cam_off': btn_cam_off,
        'btn_capture': btn_capture,
        'gamma_entry': gamma_entry,
        'contrast_entry': contrast_entry,
        'brightness_entry': brightness_entry,
        'btn_apply_gamma': btn_apply_gamma,
        'btn_apply_contrast': btn_apply_contrast,
        'btn_apply_brightness': btn_apply_brightness,
        'btn_apply_pose': btn_apply_pose,
        'btn_reset_params': btn_reset_params,
        'canvas': canvas
    }