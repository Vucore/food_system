from datetime import datetime
import os
from fastapi import APIRouter, Response, UploadFile, File
from app.utils.camera import generate, get_capture
from fastapi.responses import StreamingResponse
import io
from PIL import Image

router = APIRouter()

save_dir = "./images"


@router.post("/capture")
async def capture(file: UploadFile = File(...)):
    # Nhận file ảnh từ frontend
    image_data = await file.read()
    os.makedirs(save_dir, exist_ok=True)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + file.filename
    save_path = os.path.join(save_dir, filename)
    with open(save_path, "wb") as f:
        f.write(image_data)

    # Xử lý ảnh (nhận diện món ăn, tính calo, etc.)
    # Ví dụ: mở ảnh bằng PIL
    image = Image.open(io.BytesIO(image_data))
    
    # TODO: Thêm logic AI/ML để phân tích ảnh
    # result = analyze_food(image)
    
    # Trả về kết quả giả lập
    return {
        "success": True,
        "detected_foods": [
            {
                "name": "Chicken", 
                "calories": 248,
                "protein": 46,
                "carbs": 0,
                "fat": 5
            }
        ],
        "total_calories": 248
    }


@router.get('/video_feed')
def video_feed():
    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

@router.get("/proxy_capture")
def proxy_capture():
    content = get_capture()
    return Response(content=content, media_type="image/jpeg")