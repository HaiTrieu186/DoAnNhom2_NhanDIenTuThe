# Chứa hàm nhận dạng tư thế (công việc của Người 3).

import cv2
import numpy as np
import os

# Lấy đường dẫn thư mục chứa file pose_logic.py
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "graph_opt.pb")


inWidth = 368
inHeight = 368
thr = 0.2


try:
    net = cv2.dnn.readNetFromTensorflow(model_path)
    print(f">>> [Pose Logic] Đã load model thành công từ: {model_path}")

except Exception as e:
    print(f"!!! [Lỗi] Không tìm thấy file graph_opt.pb tại: {model_path}")
    print(f"    Chi tiết lỗi: {e}")
    net = None



BODY_PARTS = {
    "Nose": 0, "Neck": 1,
    "RShoulder": 2, "RElbow": 3, "RWrist": 4,
    "LShoulder": 5, "LElbow": 6, "LWrist": 7,
    "RHip": 8, "RKnee": 9, "RAnkle": 10,
    "LHip": 11, "LKnee": 12, "LAnkle": 13,
    "REye": 14, "LEye": 15,
    "REar": 16, "LEar": 17,
    "Background": 18
}
POSE_PAIRS = [
    ["Neck", "RShoulder"], ["Neck", "LShoulder"],
    ["RShoulder", "RElbow"], ["RElbow", "RWrist"],
    ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
    ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"],
    ["Neck", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"],
    ["Neck", "Nose"],
    ["Nose", "REye"], ["REye", "REar"],
    ["Nose", "LEye"], ["LEye", "LEar"]
]


def pose_detect(frame):
    """
    Hàm phát hiện pose và vẽ khung xương lên ảnh.
    Trả về: (ảnh đã vẽ, dict chứa tên body part và tọa độ)
    """
    if net is None:
        return frame, {}

    frameHeight, frameWidth = frame.shape[:2]

    net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight),
                                       (127.5, 127.5, 127.5), True, False))
    # Chạy mô hình
    out = net.forward()
    out = out[:, :19, :, :]

    # Dictionary chứa tên body part và tọa độ
    points = {}

    for body_part_name, body_part_id in BODY_PARTS.items():
        heatMap = out[0, body_part_id, :, :]
        _, conf, _, point = cv2.minMaxLoc(heatMap)

        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]

        # Lưu tọa độ kèm tên body part, None nếu confidence thấp
        points[body_part_name] = (int(x), int(y)) if conf > thr else None

    # Vẽ khung xương
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]

        if points.get(partFrom) and points.get(partTo):
            cv2.line(frame, points[partFrom], points[partTo], (0, 255, 255), 3)
            cv2.ellipse(frame, points[partFrom], (5, 5), 0, 0, 360, (255, 255, 0), cv2.FILLED)
            cv2.ellipse(frame, points[partTo], (5, 5), 0, 0, 360, (255, 0, 0), cv2.FILLED)

    # Hiển thị thời gian xử lý
    t, _ = net.getPerfProfile()
    freq = cv2.getTickFrequency() / 1000
    cv2.putText(frame, '%.2fms' % (t / freq), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    print("Pose detect processed")
    return frame, points


def ham_nhan_dang(frame_da_xu_ly):
    """
     Code nhận dạng tư thế và vẽ kết quả ở đây

    Hàm này nhận ảnh đã xử lý (từ Người 2).
    Bạn cần dùng thư viện (ví dụ: MediaPipe) để tìm các điểm khớp (landmarks),
    viết logic để suy luận ra tư thế từ tọa độ các điểm đó,
    vẽ các điểm khớp và đường nối lên ảnh (tạo `anh_ve_lai`),
    và xác định text kết quả (`ket_qua_text`).

    Cuối cùng, hàm phải trả về một tuple gồm 2 phần tử: (ảnh_đã_vẽ, text_kết_quả).
    """
    print(">>> [Pose Logic] Hàm nhận dạng đang chạy (chưa có code)...")

    anh_ve_lai = frame_da_xu_ly.copy() # Tạo bản sao để tránh thay đổi ảnh gốc
    ket_qua_text = "Chưa nhận dạng" # Kết quả mặc định

    # ----- BẮT ĐẦU CODE CỦA NGƯỜI 3 -----

    # Ví dụ: Tạm thời chỉ thêm text lên ảnh
    cv2.putText(anh_ve_lai, "Pose Logic Placeholder", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2) # Màu Cyan

    # ----- KẾT THÚC CODE CỦA NGƯỜI 3 -----

    # Đảm bảo trả về đúng định dạng tuple (ảnh NumPy, string)
    if not isinstance(anh_ve_lai, np.ndarray) or not isinstance(ket_qua_text, str):
        print("!!! [Lỗi Pose Logic] Hàm không trả về đúng định dạng (ảnh, text)!")
        # Trả về giá trị mặc định an toàn nếu lỗi
        return frame_da_xu_ly, "Lỗi định dạng trả về"

    return anh_ve_lai, ket_qua_text

# --- Các hàm phụ trợ khác (nếu cần) có thể viết ở dưới đây ---