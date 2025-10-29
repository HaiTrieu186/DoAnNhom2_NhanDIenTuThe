import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import numpy as np

# Import các hàm utils và ui
try:
    from app.utils.app_utils import update_image_on_label
    from app.ui.app_ui import create_ui_widgets
except ImportError as e:
    messagebox.showerror("Lỗi", f"Không tìm thấy app_utils hoặc app_ui:\n{e}")
    exit()

# Import hàm xử lý (nếu có)
try:
    from processing.preprocessing import ham_tien_xu_ly
except ImportError:
    # Hàm xử lý tạm thời nếu import lỗi
    def ham_tien_xu_ly(frame):
        cv2.putText(frame, "PREPROC MISSING", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        return frame

# Import hàm logic (nếu có)
try:
    from processing.pose_logic import pose_detect
except ImportError:
    # Hàm logic tạm thời nếu import lỗi
    def pose_detect(frame):
        cv2.putText(frame, "POSELOGIC MISSING", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return frame, "Lỗi Import Logic"


class PoseApp:
    def __init__(self, root_window):
        self.root = root_window
        self.cap = None  # Đối tượng camera
        self.recording = False  # Cờ báo camera
        self.image_display_size = (640, 480)
        self.after_id = None  # ID cho vòng lặp camera
        self.widgets = {}

        # Gán các hàm cho nút bấm
        commands = {
            'upload': self.upload_image,
            'start_cam': self.start_webcam,
            'stop_cam': self.stop_webcam,
            'capture': self.capture_image,
            'quit': self.quit_app
        }

        # Tạo giao diện
        self.widgets = create_ui_widgets(self.root, commands)

        # Tạo ảnh nền xám
        self.blank_frame = np.full((self.image_display_size[1], self.image_display_size[0], 3), 200, dtype=np.uint8)
        update_image_on_label(self.widgets['image_label'], self.blank_frame, self.image_display_size)

        # Xử lý nút X (đóng cửa sổ)
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    # Xử lý nút 'Tải Ảnh Lên'
    def upload_image(self):
        if self.recording:
            self.stop_webcam()

        file_path = filedialog.askopenfilename(
            title="Chọn file ảnh",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        if not file_path or not os.path.isfile(file_path):
            self.widgets['filepath_label'].config(text="Chưa chọn file")
            return

        self.widgets['filepath_label'].config(text=os.path.basename(file_path))
        try:
            # Sửa lỗi đọc file có tên tiếng Việt
            with open(file_path, "rb") as f:
                file_bytes = np.fromfile(f, dtype=np.uint8)
            anh_goc = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if anh_goc is None:
                raise ValueError("Không đọc được file ảnh")

            # Xử lý ảnh
            anh_sach = ham_tien_xu_ly(anh_goc)
            anh_ve_lai, ket_qua_text = pose_detect(anh_sach)

            # Cập nhật giao diện
            update_image_on_label(self.widgets['image_label'], anh_ve_lai, self.image_display_size)
            self.widgets['result_label'].config(text=ket_qua_text)

        except Exception as e:
            messagebox.showerror("Lỗi Xử Lý Ảnh", f"Lỗi:\n{e}")
            update_image_on_label(self.widgets['image_label'], self.blank_frame, self.image_display_size)
            self.widgets['result_label'].config(text="Lỗi xử lý ảnh.")

    # Xử lý nút 'Bật Camera'
    def start_webcam(self):
        if self.cap is not None:
            return

        # Thử mở camera index 0 hoặc 1
        for cam_index in [0, 1]:
            self.cap = cv2.VideoCapture(cam_index)
            if self.cap.isOpened():
                break
            self.cap.release()
            self.cap = None

        if self.cap is None or not self.cap.isOpened():
            messagebox.showerror("Lỗi Camera", "Không thể mở webcam!")
            return

        self.recording = True
        self._update_camera_buttons(camera_on=True)
        self.widgets['result_label'].config(text="CAMERA ĐANG BẬT...")
        self.update_frame()

    # Xử lý nút 'Dừng Camera'
    def stop_webcam(self, show_blank=True):
        was_recording = self.recording
        self.recording = False

        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        if self.cap is not None:
            self.cap.release()
            self.cap = None

        self._update_camera_buttons(camera_on=False)
        if was_recording:
            self.widgets['result_label'].config(text="CAMERA ĐÃ TẮT")
        if show_blank:
            update_image_on_label(self.widgets['image_label'], self.blank_frame, self.image_display_size)

    # Xử lý nút 'Chụp Ảnh'
    def capture_image(self):
        if not self.recording or self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Lỗi Camera", "Không thể đọc frame để chụp!")
            self.stop_webcam()
            return

        frame = cv2.flip(frame, 1)
        self.stop_webcam(show_blank=False)  # Dừng cam sau khi chụp

        try:
            # Xử lý frame đã chụp
            anh_sach = ham_tien_xu_ly(frame)
            anh_ve_lai, ket_qua_text = pose_detect(anh_sach)

            # Cập nhật giao diện
            update_image_on_label(self.widgets['image_label'], anh_ve_lai, self.image_display_size)
            self.widgets['result_label'].config(text=f"(Ảnh chụp) {ket_qua_text}")

        except Exception as e:
            messagebox.showerror("Lỗi Xử Lý Ảnh Chụp", f"Lỗi:\n{e}")
            update_image_on_label(self.widgets['image_label'], frame, self.image_display_size)
            self.widgets['result_label'].config(text="Lỗi xử lý ảnh chụp.")

    # Vòng lặp cập nhật frame camera
    def update_frame(self):
        if not self.recording or self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.stop_webcam()
            messagebox.showwarning("Lỗi Camera", "Mất kết nối với webcam!")
            return

        frame = cv2.flip(frame, 1)

        try:
            # Xử lý frame
            frame_sach = ham_tien_xu_ly(frame)
            frame_ve_lai, ket_qua_text = pose_detect(frame_sach)

            # Cập nhật UI
            update_image_on_label(self.widgets['image_label'], frame_ve_lai, self.image_display_size)
            self.widgets['result_label'].config(text=ket_qua_text)

        except Exception as e:
            print(f"[LỖI] Xử lý frame camera: {e}")
            update_image_on_label(self.widgets['image_label'], frame, self.image_display_size)
            self.widgets['result_label'].config(text="LỖI XỬ LÝ")

        # Lên lịch gọi lại
        self.after_id = self.root.after(15, self.update_frame)

    # Xử lý khi đóng app
    def quit_app(self):
        self.stop_webcam()
        self.root.destroy()

    # Cập nhật trạng thái các nút
    def _update_camera_buttons(self, camera_on):
        if camera_on:
            self.widgets['btn_cam_on'].config(state=tk.DISABLED)
            self.widgets['btn_cam_off'].config(state=tk.NORMAL)
            self.widgets['btn_capture'].config(state=tk.NORMAL)
        else:
            self.widgets['btn_cam_on'].config(state=tk.NORMAL)
            self.widgets['btn_cam_off'].config(state=tk.DISABLED)
            self.widgets['btn_capture'].config(state=tk.DISABLED)