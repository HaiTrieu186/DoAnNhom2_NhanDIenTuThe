# Chứa hàm tiền xử lý ảnh (công việc của Người 2).

import cv2
import numpy as np
# (Người 2: Thêm các import cần thiết khác ở đây)

def ham_tien_xu_ly(frame_goc):

    print(">>> [Preprocessing] Hàm tiền xử lý đang chạy (chưa có code)...")

    # ----- BẮT ĐẦU CODE CỦA NGƯỜI 2 -----

    # Ví dụ: Tạm thời trả về ảnh gốc
    processed_frame = frame_goc.copy()

    # ----- KẾT THÚC CODE CỦA NGƯỜI 2 -----

    # Đảm bảo trả về một NumPy array là ảnh
    if not isinstance(processed_frame, np.ndarray):
        print("!!! [Lỗi Preprocessing] Hàm không trả về ảnh NumPy hợp lệ!")
        return frame_goc # Trả về gốc nếu lỗi

    return processed_frame

# --- Các hàm phụ trợ khác (nếu cần) có thể viết ở dưới đây ---

"""
    >>> GỢI Ý: Thực hiện các bước tiền xử lý ảnh dưới đây <<<

    Mục tiêu: Cải thiện chất lượng ảnh đầu vào (frame_goc) trước khi
              đưa cho Người 3 (hàm nhận dạng AI).

    Input: frame_goc (Ảnh màu BGR đọc từ camera/file).
    Output: processed_frame_final (Ảnh đã xử lý, định dạng BGR hoặc Grayscale
            - cần thống nhất với Người 3).

    Các bước gợi ý (dựa trên tài liệu đã học):

    Bước 1: Chuyển đổi sang ảnh xám (Grayscale Conversion).
        - Mục đích: Đơn giản hóa ảnh, loại bỏ màu sắc, nhiều thuật toán
          hoạt động tốt hơn trên ảnh xám.
        - Hàm OpenCV: cv2.cvtColor(frame_goc, cv2.COLOR_BGR2GRAY)
        - Tài liệu: Chương 1, 2.

    Bước 2: Giảm nhiễu (Noise Reduction).
        - Mục đích: Làm mượt ảnh, loại bỏ nhiễu (từ camera, ánh sáng yếu)
          để AI nhận dạng ổn định hơn.
        - Thuật toán gợi ý (Chương 2 - Lọc không gian):
            - cv2.GaussianBlur(): Làm mờ mượt, hiệu quả với nhiễu chung.
              (Nên dùng kernel 3x3 hoặc 5x5).
            - cv2.medianBlur(): Hiệu quả với nhiễu "muối tiêu".
              (Nên dùng kernel 3 hoặc 5).
        - Thực hiện: Áp dụng một (hoặc cả hai) bộ lọc lên ảnh xám từ Bước 1.

    Bước 3: Tăng cường tương phản (Contrast Enhancement).
        - Mục đích: Làm rõ sự khác biệt giữa đối tượng (người) và nền,
          đặc biệt khi ánh sáng không tốt.
        - Thuật toán gợi ý (Chương 2 - Biến đổi mức xám):
            - cv2.equalizeHist(): Tự động cân bằng histogram, làm rõ chi tiết
              trong vùng tối/sáng. Rất hiệu quả và dễ dùng.
        - Thực hiện: Áp dụng lên ảnh đã giảm nhiễu từ Bước 2.

    Bước 4: Chuẩn bị ảnh Output.
        - Thống nhất với Người 3: Hàm nhận dạng cần ảnh xám (1 kênh) hay
          ảnh màu (BGR - 3 kênh)?
        - Nếu cần ảnh BGR: Chuyển ảnh xám đã xử lý ở Bước 3 về BGR bằng
          cv2.cvtColor(anh_xam_da_xu_ly, cv2.COLOR_GRAY2BGR).
        - Nếu cần ảnh xám: Giữ nguyên kết quả từ Bước 3.
        - Gán kết quả cuối cùng cho biến `processed_frame_final`.

    Lưu ý:
        - KHÔNG dùng các thuật toán phát hiện biên (Canny, Sobel - Chương 5)
          hoặc biến đổi hình thái (Erosion, Dilation - Chương 3) ở bước này,
          vì chúng có thể làm mất thông tin AI cần.
        - Thử nghiệm các tham số (kích thước kernel) để có kết quả tốt nhất.
    """