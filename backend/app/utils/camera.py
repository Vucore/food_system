import cv2
import requests
import time

cap = cv2.VideoCapture("http://192.168.1.53:81/stream")

# def generate():
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             continue
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
def generate():
    retry_count = 0
    max_retries = 5
    while True:
        ret, frame = cap.read()
        if not ret:
            retry_count += 1
            if retry_count > max_retries:
                print("Mất kết nối camera, thử lại sau 2 giây...")
                time.sleep(2)
                cap.open("http://192.168.1.53:81/stream")
                retry_count = 0
            else:
                time.sleep(0.2)
            continue
        retry_count = 0
        try:
            _, buffer = cv2.imencode('.jpg', frame)
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
    cam_url = "http://192.168.1.53:81/capture"
    r = requests.get(cam_url)
    return r.content