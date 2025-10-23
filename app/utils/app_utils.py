# Chứa hàm tiện ích hiển thị ảnh OpenCV lên Tkinter Label.

import cv2
from PIL import Image, ImageTk # Cần cài: pip install Pillow
import numpy as np # Import numpy để tạo ảnh trống

def update_image_on_label(label_widget, frame, display_size=(640, 480)):
    """Chuyển frame OpenCV (BGR) thành PhotoImage, resize, và cập nhật tk.Label."""
    if frame is None:
        # Tạo ảnh nền xám nhạt nếu frame là None
        blank_frame = np.full((display_size[1], display_size[0], 3), 200, dtype=np.uint8) # Xám nhạt
        pil_image = Image.fromarray(blank_frame) # Chuyển sang PIL
        tk_image = ImageTk.PhotoImage(image=pil_image)
        label_widget.config(image=tk_image)
        label_widget.image = tk_image # Giữ tham chiếu
        print("[Cảnh báo] update_image_on_label: frame là None, hiển thị ảnh trống.")
        return

    try:
        # Resize ảnh
        resized_frame = cv2.resize(frame, display_size, interpolation=cv2.INTER_AREA)
        # Chuyển BGR sang RGB
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        # Tạo ảnh Pillow
        pil_image = Image.fromarray(rgb_frame)
        # Tạo ảnh Tkinter
        tk_image = ImageTk.PhotoImage(image=pil_image)
        # Cập nhật Label
        label_widget.config(image=tk_image)
        # QUAN TRỌNG: Giữ tham chiếu để ảnh không bị mất!
        label_widget.image = tk_image
    except Exception as e:
        print(f"[Lỗi] trong update_image_on_label: {e}")
        # Nếu lỗi, thử hiển thị ảnh trống để tránh crash
        try:
            blank_frame = np.full((display_size[1], display_size[0], 3), 128, dtype=np.uint8) # Xám đậm hơn
            pil_image = Image.fromarray(blank_frame)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            label_widget.config(image=tk_image)
            label_widget.image = tk_image
        except:
             pass # Bỏ qua nếu cả việc hiển thị ảnh trống cũng lỗi