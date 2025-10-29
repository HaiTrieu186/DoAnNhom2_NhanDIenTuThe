import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import numpy as np

# Import các hàm utils và ui
from app.utils.app_utils import update_image_on_label
from app.ui.app_ui import create_ui_widgets

# Import hàm xử lý
from processing.preprocessing import ham_tien_xu_ly
from processing.basic_process import gamma_process, adjust_contrast, adjust_brightness
from processing.pose_logic import pose_detect


class PoseApp:
    def __init__(self, root_window):
        self.root = root_window
        self.cap = None  # Đối tượng camera
        self.recording = False  # Cờ báo camera
        self.image_display_size = (640, 480)
        self.after_id = None  # ID cho vòng lặp camera
        self.widgets = {}

        # Lưu ảnh gốc để xử lý
        self.current_original_image = None
        self.current_processed_image = None
        self.pose_detected = False  # Cờ đánh dấu đã nhận dạng tư thế
        self.before_pose_image = None  # Lưu ảnh trước khi nhận dạng (đã xử lý gamma/contrast/brightness)

        # Gán các hàm cho nút bấm
        commands = {
            'apply_gamma': self.apply_gamma,
            'apply_contrast': self.apply_contrast,
            'apply_brightness': self.apply_brightness,
            'apply_pose_detect': self.apply_pose_detect,
            'reset_params': self.reset_params,
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

    # ==================== CÁC HÀM XỬ LÝ ẢNH CƠ BẢN ====================

    def apply_gamma(self):
        """Áp dụng biến đổi Gamma lên ảnh hiện tại"""
        if self.current_processed_image is None:
            messagebox.showwarning("Cảnh báo", "Chưa có ảnh để xử lý!")
            return

        try:
            gamma_value = float(self.widgets['gamma_entry'].get())
            if gamma_value <= 0:
                raise ValueError("Gamma phải > 0")

            # Xử lý ảnh hiện tại (đè lên)
            processed = gamma_process(self.current_processed_image, gamma_value)
            self.current_processed_image = processed

            # Cập nhật hiển thị
            update_image_on_label(self.widgets['image_label'], processed, self.image_display_size)
            self.widgets['result_label'].config(text=f"Đã áp dụng Gamma: {gamma_value}")

        except ValueError as e:
            messagebox.showerror("Lỗi", f"Giá trị Gamma không hợp lệ!\n{e}")

    def apply_contrast(self):
        """Áp dụng điều chỉnh tương phản lên ảnh hiện tại"""
        if self.current_processed_image is None:
            messagebox.showwarning("Cảnh báo", "Chưa có ảnh để xử lý!")
            return

        try:
            contrast_value = float(self.widgets['contrast_entry'].get())
            if contrast_value < 0:
                raise ValueError("Tương phản phải >= 0")

            # Xử lý ảnh hiện tại (đè lên)
            processed = adjust_contrast(self.current_processed_image, contrast_value)
            self.current_processed_image = processed

            # Cập nhật hiển thị
            update_image_on_label(self.widgets['image_label'], processed, self.image_display_size)
            self.widgets['result_label'].config(text=f"Đã áp dụng Tương phản: {contrast_value}")

        except ValueError as e:
            messagebox.showerror("Lỗi", f"Giá trị Tương phản không hợp lệ!\n{e}")

    def apply_brightness(self):
        """Áp dụng điều chỉnh độ sáng lên ảnh hiện tại"""
        if self.current_processed_image is None:
            messagebox.showwarning("Cảnh báo", "Chưa có ảnh để xử lý!")
            return

        try:
            brightness_value = int(self.widgets['brightness_entry'].get())

            # Xử lý ảnh hiện tại (đè lên)
            processed = adjust_brightness(self.current_processed_image, brightness_value)
            self.current_processed_image = processed

            # Cập nhật hiển thị
            update_image_on_label(self.widgets['image_label'], processed, self.image_display_size)
            self.widgets['result_label'].config(text=f"Đã áp dụng Độ sáng: {brightness_value:+d}")

        except ValueError as e:
            messagebox.showerror("Lỗi", f"Giá trị Độ sáng không hợp lệ!\n{e}")

    def apply_pose_detect(self):
        """Áp dụng nhận dạng tư thế lên ảnh hiện tại"""
        if self.current_processed_image is None:
            messagebox.showwarning("Cảnh báo", "Chưa có ảnh để xử lý!")
            return

        # Nếu đã nhận dạng rồi, quay về ảnh gốc trước khi nhận dạng lại
        if self.pose_detected:
            self.current_processed_image = self.current_original_image.copy()
            self.pose_detected = False

        try:
            # Tiền xử lý ảnh hiện tại
            anh_sach = ham_tien_xu_ly(self.current_processed_image)
            # Nhận dạng tư thế
            anh_ve_lai, ket_qua_text = pose_detect(anh_sach)

            self.current_processed_image = anh_ve_lai
            self.pose_detected = True  # Đánh dấu đã nhận dạng

            # Cập nhật hiển thị
            update_image_on_label(self.widgets['image_label'], anh_ve_lai, self.image_display_size)
            self.widgets['result_label'].config(text=f"Nhận dạng: {ket_qua_text}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi nhận dạng tư thế:\n{e}")
            self.widgets['result_label'].config(text="Lỗi nhận dạng tư thế")

    def reset_params(self):
        """Đặt lại về ảnh gốc và reset các tham số"""
        if self.current_original_image is None:
            messagebox.showwarning("Cảnh báo", "Chưa có ảnh để reset!")
            return

        # Reset các giá trị về mặc định
        self.widgets['gamma_entry'].delete(0, tk.END)
        self.widgets['gamma_entry'].insert(0, "1.0")

        self.widgets['contrast_entry'].delete(0, tk.END)
        self.widgets['contrast_entry'].insert(0, "1.0")

        self.widgets['brightness_entry'].delete(0, tk.END)
        self.widgets['brightness_entry'].insert(0, "0")

        # Hiển thị lại ảnh gốc (xóa hình nhận dạng nếu có)
        self.current_processed_image = self.current_original_image.copy()
        self.pose_detected = False  # Reset cờ nhận dạng

        update_image_on_label(self.widgets['image_label'], self.current_original_image, self.image_display_size)
        self.widgets['result_label'].config(text="Đã đặt lại về ảnh gốc")

    # ==================== CÁC HÀM XỬ LÝ CHÍNH ====================

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

            # Lưu ảnh gốc để xử lý
            self.current_original_image = anh_goc.copy()
            self.current_processed_image = anh_goc.copy()
            self.pose_detected = False  # Reset cờ khi tải ảnh mới

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
            self.current_original_image = None
            self.current_processed_image = None

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
            # Lưu ảnh gốc để xử lý
            self.current_original_image = frame.copy()
            self.current_processed_image = frame.copy()
            self.pose_detected = False  # Reset cờ khi chụp ảnh mới

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
            self.current_original_image = None
            self.current_processed_image = None

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