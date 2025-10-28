import cv2
from PIL import Image, ImageTk
import numpy as np


def update_image_on_label(label_widget, frame, display_size=(640, 480)):
    """
    Chuyển frame OpenCV (BGR) thành ảnh Tkinter và hiển thị lên Label.
    """
    if frame is None:
        # Tạo ảnh xám nếu frame rỗng
        blank_frame = np.full((display_size[1], display_size[0], 3), 200, dtype=np.uint8)
        pil_image = Image.fromarray(blank_frame)
        tk_image = ImageTk.PhotoImage(image=pil_image)
        label_widget.config(image=tk_image)
        label_widget.image = tk_image
        return

    try:
        # Resize, chuyển BGR -> RGB, và tạo ảnh TK
        resized_frame = cv2.resize(frame, display_size, interpolation=cv2.INTER_AREA)
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        tk_image = ImageTk.PhotoImage(image=pil_image)

        # Cập nhật label
        label_widget.config(image=tk_image)
        label_widget.image = tk_image  # Giữ tham chiếu

    except Exception as e:
        print(f"[Lỗi] update_image_on_label: {e}")
        # Thử hiển thị ảnh trống nếu có lỗi
        try:
            blank_frame = np.full((display_size[1], display_size[0], 3), 128, dtype=np.uint8)
            pil_image = Image.fromarray(blank_frame)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            label_widget.config(image=tk_image)
            label_widget.image = tk_image
        except:
            pass