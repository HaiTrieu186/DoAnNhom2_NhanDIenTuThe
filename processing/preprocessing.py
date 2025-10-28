import cv2
import numpy as np

def ham_tien_xu_ly(frame_goc):
    """
    Thực hiện tiền xử lý ảnh:
    1. Chuyển sang ảnh xám để xử lý.
    2. Áp dụng: Lọc Gaussian -> Cân bằng Histogram -> Làm sắc nét Laplace.
    3. Chuyển ảnh xám đã xử lý về định dạng RGB (vì mediapipe cần ảnh 3 kênh).
    """
    try:
    # ----------------- [Start] Kiểm tra ảnh đầu vào -----------
        if frame_goc is None or frame_goc.size == 0:
            print("[Lỗi Preprocessing] Ảnh đầu vào không hợp lệ!")
            return frame_goc
    #------------------------ [End] Kiểm tra ảnh đầu vào ------




    # ------------------------ [Start] Xử lý ảnh -------------------
        # --- a) Chuyển sang ảnh xám
        gray_frame = cv2.cvtColor(frame_goc, cv2.COLOR_BGR2GRAY)

        # --- b) Lọc Gaussian (Giảm nhiễu) trên ảnh xám
        blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

        # --- c) Cân bằng Histogram (Tăng cường tương phản) trên ảnh đã lọc nhiễu
        equalized_frame = cv2.equalizeHist(blurred_frame)


        # --- d) phát hiện biên bằng Laplace (Tăng sắc nét cho biên) ---
        laplacian = cv2.Laplacian(equalized_frame, cv2.CV_64F, ksize=2)
        lap_abs = cv2.convertScaleAbs(laplacian)
        sharpened_gray_frame = cv2.subtract(equalized_frame, lap_abs) # ảnh gốc - ảnh biên
# ------------------------ [End] Xử lý ảnh ------------------------






# -------------- [Start]  Chuyển ảnh xám đã xử lý về BGR -----------------
        final_bgr_frame = cv2.cvtColor(sharpened_gray_frame, cv2.COLOR_GRAY2BGR)

        # --- Kết quả trả về ---
        return final_bgr_frame
# -------------- -[End]  Chuyển ảnh xám đã xử lý về BGR -------------------

    except Exception as e:
        print(f"[LỖI] Trong hàm ham_tien_xu_ly: {e}")
        return frame_goc # Trả về ảnh gốc nếu có lỗi




# --- Hàm resize_frame giữ nguyên ---
def resize_frame(frame, max_width=1280, max_height=720):
    h, w = frame.shape[:2]
    if w > max_width or h > max_height:
        scale = min(max_width / w, max_height / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return resized
    return frame

