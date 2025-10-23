# File: app_logic.py (Trong app/logic/)
# Chứa lớp PoseApp điều khiển logic ứng dụng.

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import numpy as np

# --- Import từ các module khác trong project ---
try:
    # Hàm cập nhật ảnh từ thư mục utils
    from app.utils.app_utils import update_image_on_label
    # Hàm tạo UI từ thư mục ui
    from app.ui.app_ui import create_ui_widgets
except ImportError as e:
    messagebox.showerror("Lỗi Import Nội bộ", f"Không tìm thấy app_utils hoặc app_ui:\n{e}")
    exit()

try:
    # Hàm tiền xử lý từ thư mục processing (cần file preprocessing.py)
    from processing.preprocessing import ham_tien_xu_ly
    print(">>> Logic: Đã import 'ham_tien_xu_ly'.")
except ImportError:
    messagebox.showwarning("Import Warning", "Không tìm thấy 'preprocessing.py' hoặc hàm 'ham_tien_xu_ly'.\nSẽ dùng hàm xử lý tạm thời.")
    # Hàm tạm thời nếu import lỗi
    def ham_tien_xu_ly(frame):
        print("[LOGIC] Đang dùng hàm tiền xử lý TẠM THỜI!")
        cv2.putText(frame, "PREPROC MISSING", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,165,255), 2) # Màu cam
        return frame

try:
    # Hàm nhận dạng từ thư mục processing (cần file pose_logic.py)
    from processing.pose_logic import ham_nhan_dang
    print(">>> Logic: Đã import 'ham_nhan_dang'.")
except ImportError:
    messagebox.showwarning("Import Warning", "Không tìm thấy 'pose_logic.py' hoặc hàm 'ham_nhan_dang'.\nSẽ dùng hàm nhận dạng tạm thời.")
    # Hàm tạm thời nếu import lỗi
    def ham_nhan_dang(frame):
        print("[LOGIC] Đang dùng hàm nhận dạng TẠM THỜI!")
        cv2.putText(frame, "POSELOGIC MISSING", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2) # Màu đỏ
        return frame, "Lỗi Import Logic"
# ------------------------------------------------

class PoseApp:
    """Lớp chính điều khiển logic và trạng thái của ứng dụng."""
    def __init__(self, root_window):
        self.root = root_window
        self.cap = None                 # Đối tượng camera OpenCV
        self.recording = False          # Cờ báo camera đang chạy
        self.image_display_size = (640, 480) # Kích thước hiển thị ảnh/video
        self.after_id = None            # ID để quản lý vòng lặp camera của Tkinter
        self.widgets = {}               # Dictionary lưu trữ các widget giao diện

        # Dictionary chứa các hàm xử lý sự kiện cho các nút
        commands = {
            'upload': self.upload_image,
            'start_cam': self.start_webcam,
            'stop_cam': self.stop_webcam,
            'capture': self.capture_image,
            'quit': self.quit_app
        }

        # Gọi hàm từ app_ui để tạo giao diện và lấy về các widget
        self.widgets = create_ui_widgets(self.root, commands)

        # Tạo ảnh nền xám nhạt ban đầu
        self.blank_frame = np.full((self.image_display_size[1], self.image_display_size[0], 3), 200, dtype=np.uint8)
        # Hiển thị ảnh trống lên label ảnh
        update_image_on_label(self.widgets['image_label'], self.blank_frame, self.image_display_size)

        # Gán hàm xử lý khi người dùng nhấn nút X đỏ để đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        print("--- Logic App: Khởi tạo hoàn tất ---")

    # --- Các hàm xử lý sự kiện ---

    def upload_image(self):
        """Xử lý khi nhấn nút 'Tải Ảnh Lên'."""
        print("Logic: upload_image...")
        if self.recording: self.stop_webcam() # Dừng camera nếu đang chạy

        file_path = filedialog.askopenfilename(
            title="Chọn file ảnh",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )

        # Nếu người dùng chọn file và file đó tồn tại
        if file_path and os.path.isfile(file_path):
            self.widgets['filepath_label'].config(text=os.path.basename(file_path)) # Hiển thị tên file
            try:
                anh_goc = cv2.imread(file_path)
                if anh_goc is not None:
                    # Gọi hàm xử lý ảnh
                    anh_sach = ham_tien_xu_ly(anh_goc)
                    anh_ve_lai, ket_qua_text = ham_nhan_dang(anh_sach)
                    # Cập nhật giao diện
                    update_image_on_label(self.widgets['image_label'], anh_ve_lai, self.image_display_size)
                    self.widgets['result_label'].config(text=ket_qua_text)
                else:
                    messagebox.showerror("Lỗi Đọc Ảnh", f"Không đọc được file:\n{file_path}")
                    # Hiển thị lại ảnh trống và thông báo lỗi
                    update_image_on_label(self.widgets['image_label'], self.blank_frame, self.image_display_size)
                    self.widgets['result_label'].config(text="Lỗi tải ảnh.")
            except Exception as e:
                messagebox.showerror("Lỗi Xử Lý Ảnh", f"Lỗi xử lý ảnh tĩnh:\n{e}")
                update_image_on_label(self.widgets['image_label'], self.blank_frame, self.image_display_size)
                self.widgets['result_label'].config(text="Lỗi xử lý ảnh.")
        else:
            # Nếu người dùng hủy chọn file
             self.widgets['filepath_label'].config(text="Chưa chọn file")

    def start_webcam(self):
        """Xử lý khi nhấn nút 'Bật Camera'."""
        print("Logic: start_webcam...")
        if self.cap is None: # Chỉ bật nếu chưa bật
            self.cap = cv2.VideoCapture(0) # Thử cam index 0
            if not self.cap.isOpened():
                print("   -> Thử camera index 1...")
                self.cap = cv2.VideoCapture(1) # Thử cam index 1

            if self.cap and self.cap.isOpened():
                self.recording = True
                # Cập nhật trạng thái các nút
                self.widgets['btn_cam_on'].config(state=tk.DISABLED)
                self.widgets['btn_cam_off'].config(state=tk.NORMAL)
                self.widgets['btn_capture'].config(state=tk.NORMAL)
                self.widgets['result_label'].config(text="CAMERA ĐANG BẬT...")
                print("   -> Camera đã bật. Bắt đầu vòng lặp frame.")
                self.update_frame() # Bắt đầu vòng lặp cập nhật frame
            else:
                messagebox.showerror("Lỗi Camera", "Không thể mở webcam!")
                self.cap = None # Reset về None nếu không mở được

    def stop_webcam(self, show_blank=True):
        """Xử lý khi nhấn nút 'Dừng Camera' hoặc khi cần dừng camera."""
        print(f"Logic: stop_webcam (show_blank={show_blank})...")
        was_recording = self.recording
        self.recording = False # Tắt cờ camera
        # Hủy lịch trình gọi lại hàm update_frame (nếu có)
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        # Giải phóng camera nếu đang được sử dụng
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            if was_recording: print("   -> Camera đã dừng và giải phóng.")
        # Cập nhật trạng thái các nút
        self.widgets['btn_cam_on'].config(state=tk.NORMAL)
        self.widgets['btn_cam_off'].config(state=tk.DISABLED)
        self.widgets['btn_capture'].config(state=tk.DISABLED)
        # Cập nhật text trạng thái
        if was_recording: self.widgets['result_label'].config(text="CAMERA ĐÃ TẮT")
        # Hiển thị ảnh trống nếu được yêu cầu
        if show_blank:
            update_image_on_label(self.widgets['image_label'], self.blank_frame, self.image_display_size)

    def capture_image(self):
        """Xử lý khi nhấn nút 'Chụp Ảnh'."""
        print("Logic: capture_image...")
        if self.recording and self.cap is not None:
            ret, frame = self.cap.read() # Đọc frame hiện tại từ camera
            if ret:
                frame = cv2.flip(frame, 1) # Lật ảnh
                print("   -> Đã chụp frame. Dừng camera tạm thời và xử lý...")
                # Dừng camera nhưng không hiện ảnh trống ngay lập tức
                self.stop_webcam(show_blank=False)
                try:
                    # Gọi xử lý cho frame tĩnh vừa chụp
                    anh_sach = ham_tien_xu_ly(frame)
                    anh_ve_lai, ket_qua_text = ham_nhan_dang(anh_sach)
                    # Cập nhật giao diện với kết quả xử lý ảnh tĩnh
                    update_image_on_label(self.widgets['image_label'], anh_ve_lai, self.image_display_size)
                    self.widgets['result_label'].config(text=f"(Ảnh chụp) {ket_qua_text}")
                    print(f"   -> Xử lý ảnh chụp xong.")
                except Exception as e:
                    messagebox.showerror("Lỗi Xử Lý Ảnh Chụp", f"Lỗi:\n{e}")
                    update_image_on_label(self.widgets['image_label'], frame, self.image_display_size) # Hiện ảnh gốc nếu lỗi
                    self.widgets['result_label'].config(text="Lỗi xử lý ảnh chụp.")
            else:
                messagebox.showerror("Lỗi Camera", "Không thể đọc frame để chụp!")
                self.stop_webcam() # Dừng hẳn nếu đọc lỗi
        else:
             print("   -> Camera chưa bật để chụp.") # Thông báo nếu camera chưa bật


    def update_frame(self):
        """Vòng lặp chính để đọc frame từ camera, xử lý và hiển thị."""
        # Kiểm tra nếu cần dừng (do nhấn nút Dừng hoặc lỗi)
        if not self.recording or self.cap is None:
            print("Logic: update_frame dừng.")
            return

        ret, frame = self.cap.read() # Đọc frame
        if ret:
            frame = cv2.flip(frame, 1) # Lật frame
            try:
                # Gọi xử lý
                frame_sach = ham_tien_xu_ly(frame)
                frame_ve_lai, ket_qua_text = ham_nhan_dang(frame_sach)
                # Cập nhật UI
                update_image_on_label(self.widgets['image_label'], frame_ve_lai, self.image_display_size)
                self.widgets['result_label'].config(text=ket_qua_text)
            except Exception as e:
                print(f"[LỖI] Xử lý frame camera: {e}")
                update_image_on_label(self.widgets['image_label'], frame, self.image_display_size) # Hiện gốc nếu lỗi
                self.widgets['result_label'].config(text=f"LỖI XỬ LÝ")

            # Lên lịch để gọi lại hàm này sau 15ms
            # Giá trị 15ms tương đương khoảng 66 FPS (1000/15), có thể tăng lên nếu cần (vd: 30ms ~ 33 FPS)
            self.after_id = self.root.after(15, self.update_frame)
        else:
            print("[Lỗi] Không đọc được frame từ webcam trong vòng lặp!")
            self.stop_webcam() # Tự động dừng nếu đọc lỗi
            messagebox.showwarning("Lỗi Camera", "Mất kết nối với webcam!")

    def quit_app(self):
        """Dọn dẹp và đóng ứng dụng."""
        print("Logic: quit_app...")
        self.stop_webcam() # Đảm bảo dừng camera
        print("   -> Đang đóng cửa sổ...")
        self.root.destroy() # Đóng cửa sổ Tkinter
        print("--- ỨNG DỤNG ĐÃ ĐÓNG ---")