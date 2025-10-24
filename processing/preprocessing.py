# Chứa hàm tiền xử lý ảnh (công việc của Người 2).

import cv2
import numpy as np


def ham_tien_xu_ly(frame_goc):
    """
    Hàm tiền xử lý ảnh để cải thiện chất lượng cho nhận dạng tư thế.
    Tự động phát hiện và xử lý ảnh thiếu sáng.

    Tham số:
        frame_goc: Ảnh đầu vào từ camera/file (BGR format)

    Trả về:
        processed_frame: Ảnh đã được xử lý (BGR format)
    """
    print(">>> [Preprocessing] Bắt đầu tiền xử lý ảnh...")

    try:
        if frame_goc is None or frame_goc.size == 0:
            print("!!! [Lỗi] Ảnh đầu vào không hợp lệ!")
            return frame_goc

        gray_check = cv2.cvtColor(frame_goc, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray_check)
        is_dark = brightness < 80  # Ngưỡng phát hiện ảnh tối

        if is_dark:
            print(f"   [0] Phát hiện ảnh tối (độ sáng: {brightness:.1f}) - Áp dụng xử lý đặc biệt")

        working_frame = frame_goc.copy()

        if is_dark:
            hsv = cv2.cvtColor(working_frame, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)

            brightness_boost = int((80 - brightness) * 0.8)  # Tính toán mức tăng
            v = cv2.add(v, brightness_boost)

            clahe_v = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            v = clahe_v.apply(v)

            hsv_enhanced = cv2.merge([h, s, v])
            working_frame = cv2.cvtColor(hsv_enhanced, cv2.COLOR_HSV2BGR)
            print(f"   [1] Đã tăng độ sáng +{brightness_boost}")

        gray_frame = cv2.cvtColor(working_frame, cv2.COLOR_BGR2GRAY)
        print("   [2] Đã chuyển sang ảnh xám")

        kernel_size = (5, 5) if is_dark else (3, 3) #(5, 5) cho ảnh sáng , (3, 3) cho ảnh tối
        denoised_frame = cv2.GaussianBlur(gray_frame, kernel_size, 0)
        print(f"   [3] Đã giảm nhiễu với kernel {kernel_size}")

        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # Cân bằng Histogram Thích ứng Giới hạn Độ tương phản
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_frame = clahe.apply(denoised_frame)
        print("   [4] Đã tăng cường tương phản với CLAHE")

        sharpening_kernel = np.array([[-1, -1, -1],
                                      [-1, 9, -1],
                                      [-1, -1, -1]])
        sharpened_frame = cv2.filter2D(enhanced_frame, -1, sharpening_kernel)
        print("   [5] Đã làm sắc nét ảnh")

        processed_gray = cv2.cvtColor(sharpened_frame, cv2.COLOR_GRAY2BGR)

        # Xử lý màu từ ảnh gốc đã cải thiện ánh sáng
        lab = cv2.cvtColor(working_frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        l_clahe = clahe.apply(l)
        lab_enhanced = cv2.merge([l_clahe, a, b])
        color_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

        weight_gray = 0.4 if is_dark else 0.5
        weight_color = 0.6 if is_dark else 0.5
        final_frame = cv2.addWeighted(processed_gray, weight_gray, color_enhanced, weight_color, 0)
        print(f"   [6] Đã cân bằng màu (Gray:{weight_gray} Color:{weight_color})")

        print(">>> [Preprocessing] Hoàn tất tiền xử lý!")
        return final_frame

    except Exception as e:
        print(f"!!! [Lỗi Preprocessing] Lỗi trong quá trình xử lý: {e}")
        return frame_goc



# === HÀM PHỤ TRỢ ===

def resize_frame(frame, max_width=1280, max_height=720):

    h, w = frame.shape[:2]

    if w > max_width or h > max_height:
        scale = min(max_width / w, max_height / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        print(f"   [Resize] {w}x{h} -> {new_w}x{new_h}")
        return resized

    return frame