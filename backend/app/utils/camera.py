# import cv2
# import requests
# import time
# cap = cv2.VideoCapture("http://192.168.1.53:81/stream")

# # def generate():
# #     while True:
# #         ret, frame = cap.read()
# #         if not ret:
# #             continue
# #         try:
# #             _, buffer = cv2.imencode('.jpg', frame)
# #             frame_bytes = buffer.tobytes()
# #             yield (
# #                 b'--frame\r\n'
# #                 b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
# #             )
# #         except Exception as e:
# #             print("Lỗi khi encode frame:", e)
# #             time.sleep(0.1)
# #             continue
# def generate():
    
#     retry_count = 0
#     max_retries = 5
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             retry_count += 1
#             if retry_count > max_retries:
#                 print("Mất kết nối camera, thử lại sau 2 giây...")
#                 time.sleep(2)
#                 cap.open("http://192.168.1.53:81/stream")
#                 retry_count = 0
#             else:
#                 time.sleep(0.2)
#             continue
#         retry_count = 0
#         try:
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (
#                 b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
#             )
#         except Exception as e:
#             print("Lỗi khi encode frame:", e)
#             time.sleep(0.1)
#             continue

# # def get_capture():
# #     cam_url = "http://192.168.1.53:81/capture"
# #     r = requests.get(cam_url)
# #     return r.content



# import cv2
# import requests
# import time
# import threading
# from PIL import Image
# import io

# # Global variables
# cap = None
# frame_lock = threading.Lock()
# latest_frame = None
# is_stream_active = False

# def initialize_camera():
#     """Khởi tạo camera một lần duy nhất"""
#     global cap, is_stream_active
#     try:
#         if cap is not None:
#             cap.release()
#         cap = cv2.VideoCapture("http://192.168.1.53:81/stream")
#         cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Giảm buffer để tránh lag
#         is_stream_active = True
#         print("Camera initialized successfully")
#         return True
#     except Exception as e:
#         print(f"Error initializing camera: {e}")
#         return False

# def update_frame():
#     """Thread riêng để cập nhật frame liên tục"""
#     global cap, latest_frame, is_stream_active
    
#     while is_stream_active:
#         if cap is not None:
#             ret, frame = cap.read()
#             if ret:
#                 with frame_lock:
#                     latest_frame = frame.copy()
#             else:
#                 # Thử kết nối lại nếu mất kết nối
#                 print("Lost connection, trying to reconnect...")
#                 initialize_camera()
#                 time.sleep(1)
#         time.sleep(0.03)  # ~30 FPS

# def generate():
#     """Generator cho video stream"""
#     global latest_frame
    
#     # Khởi tạo camera nếu chưa có
#     if cap is None:
#         initialize_camera()
#         # Start frame update thread
#         update_thread = threading.Thread(target=update_frame, daemon=True)
#         update_thread.start()
    
#     while True:
#         with frame_lock:
#             if latest_frame is not None:
#                 current_frame = latest_frame.copy()
#             else:
#                 # Frame mặc định nếu không có
#                 current_frame = None
        
#         if current_frame is not None:
#             try:
#                 _, buffer = cv2.imencode('.jpg', current_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
#                 frame_bytes = buffer.tobytes()
#                 yield (
#                     b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
#                 )
#             except Exception as e:
#                 print("Error encoding frame:", e)
        
#         time.sleep(0.03)

# def get_capture():
#     """Capture frame hiện tại từ stream"""
#     global latest_frame
    
#     try:
#         # Đợi frame mới nhất
#         max_wait = 50  # 50 * 0.1 = 5 giây
#         wait_count = 0
        
#         while latest_frame is None and wait_count < max_wait:
#             time.sleep(0.1)
#             wait_count += 1
        
#         if latest_frame is None:
#             raise Exception("Không thể lấy frame từ camera")
        
#         # Copy frame để tránh conflict
#         with frame_lock:
#             captured_frame = latest_frame.copy()
        
#         # Encode thành JPEG với quality cao hơn cho AI
#         _, buffer = cv2.imencode('.jpg', captured_frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
#         return buffer.tobytes()
        
#     except Exception as e:
#         print(f"Error in get_capture: {e}")
#         # Fallback: dùng URL capture (sẽ tạm ngắt stream)
#         try:
#             print("Using fallback capture method...")
#             cam_url = "http://192.168.1.53:81/capture"
#             response = requests.get(cam_url, timeout=10)
#             if response.status_code == 200:
#                 return response.content
#             else:
#                 raise Exception(f"Capture failed with status {response.status_code}")
#         except Exception as fallback_error:
#             print(f"Fallback capture also failed: {fallback_error}")
#             raise Exception("Không thể capture ảnh từ camera")

# def cleanup_camera():
#     """Dọn dẹp khi tắt ứng dụng"""
#     global cap, is_stream_active
#     is_stream_active = False
#     if cap is not None:
#         cap.release()
#         cap = None
import cv2
import requests
import time
import threading
    

cap = cv2.VideoCapture("http://10.150.38.30:81/stream")    
# cap = cv2.VideoCapture("http://192.168.1.53:81/stream")
# cap = cv2.VideoCapture("http://172.20.10.13:81/stream")   10.150.38.30
# Shared frame buffer
current_frame = None
frame_lock = threading.Lock()

def generate():
    global current_frame
    retry_count = 0
    max_retries = 5
    
    while True:
        ret, frame = cap.read()
        if not ret:
            retry_count += 1
            if retry_count > max_retries:
                print("Mất kết nối camera, thử lại sau 2 giây...")
                time.sleep(2)
                cap.release()
                cap.open("http://10.150.38.30:81/stream")
                retry_count = 0
            else:
                time.sleep(0.2)
            continue
            
        retry_count = 0
        
        # Lưu frame hiện tại để get_capture có thể sử dụng
        with frame_lock:
            current_frame = frame.copy()
        
        try:
            # Encode với quality tối ưu cho streaming
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame_bytes = buffer.tobytes()
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
            )
        except Exception as e:
            print("Lỗi khi encode frame:", e)
            time.sleep(0.1)
            continue

def get_capture():
    """Capture frame hiện tại cho ESP32 button"""
    global current_frame
    
    try:
        # Đợi frame từ stream
        max_wait = 30  # 3 giây
        wait_count = 0
        
        while current_frame is None and wait_count < max_wait:
            time.sleep(0.1)
            wait_count += 1
        
        if current_frame is None:
            raise Exception("Không thể lấy frame từ stream")
        
        # Copy frame hiện tại
        with frame_lock:
            captured_frame = current_frame.copy()
        
        # Encode với quality cao cho AI
        _, buffer = cv2.imencode('.jpg', captured_frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print("Successfully captured frame for ESP32")
        return buffer.tobytes()
        
    except Exception as e:
        print(f"Error in get_capture: {e}")
        raise Exception("Không thể capture ảnh từ camera")