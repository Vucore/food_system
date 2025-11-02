from datetime import datetime
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from app.utils.camera import generate, get_capture
from fastapi.responses import JSONResponse, StreamingResponse
from ...bot.init import ChatbotBase
from fastapi import Form
from app.utils.db import get_db, serialize_mongo_document
from PIL import Image
import logging
import os
import io

logging.basicConfig(level=logging.INFO)

router = APIRouter()

bot = ChatbotBase()

import random

FOOD_SAMPLES = [
    {
        "name": "Phở Gà",
        "restaurant": "Phở Hòa Nhai",
        "address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
        "google_maps": "https://maps.google.com/?q=Phở+Hòa+Nhai,+123+Nguyễn+Huệ,+Quận+1",
    },
    {
        "name": "Cơm Tấm",
        "restaurant": "Cơm Tấm Cây Xanh",
        "address": "456 Pasteur, Quận 3, TP.HCM",
        "google_maps": "https://maps.google.com/?q=Cơm+Tấm+Cây+Xanh,+456+Pasteur,+Quận+3",
    },
    {
        "name": "Bánh Mì",
        "restaurant": "Bánh Mì Tràng Tiền",
        "address": "789 Tràng Tiền, Quận 1, TP.HCM",
        "google_maps": "https://maps.google.com/?q=Bánh+Mì+Tràng+Tiền,+789+Tràng+Tiền,+Quận+1",
    },
    {
        "name": "Chả Giò",
        "restaurant": "Chả Giò Hà Nội",
        "address": "321 Nguyễn Thái Học, Quận 1, TP.HCM",
        "google_maps": "https://maps.google.com/?q=Chả+Giò+Hà+Nội,+321+Nguyễn+Thái+Học,+Quận+1",
    },
    {
        "name": "Bún Chả",
        "restaurant": "Bún Chả Hương Vị",
        "address": "654 Đinh Tiên Hoàng, Quận 1, TP.HCM",
        "google_maps": "https://maps.google.com/?q=Bún+Chả+Hương+Vị,+654+Đinh+Tiên+Hoàng,+Quận+1",
    },
    {
        "name": "Gỏi Cuốn",
        "restaurant": "Gỏi Cuốn Mễ Trì",
        "address": "987 Hai Bà Trưng, Quận 1, TP.HCM",
        "google_maps": "https://maps.google.com/?q=Gỏi+Cuốn+Mễ+Trì,+987+Hai+Bà+Trưng,+Quận+1",
    },
]



save_dir = "./images"

@router.post("/capture")
async def capture(file: UploadFile = File(...),  user_id: str = Form("anonymous")):
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
     # TODO: Thêm logic AI/ML để phân tích ảnh
    food = random.choice(FOOD_SAMPLES)
    fake_ai_result = {
        "user_id": user_id,
        "name": food["name"],
        "restaurant": food["restaurant"],
        "address": food["address"],
        "google_maps": food["google_maps"],
        "image_path": save_path
    }
    # Truy vấn dữ liệu thực từ MongoDB
    try:
        db = get_db()
        # Lưu dữ liệu vào collection 'foods'
        inserted_id = db["foods"].insert_one(fake_ai_result).inserted_id

        # Truy vấn chỉ lấy món ăn của user hiện tại
        foods_cursor = db["foods"].find({"user_id": user_id}).sort([("_id", -1)])
        foods = [serialize_mongo_document(doc) for doc in foods_cursor]
        return {
            "success": True,
            "detected_foods": foods,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi truy vấn MongoDB: {e}")

# @router.get('/video_feed')
# def video_feed():
#     return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

# @router.get("/proxy_capture")
# def proxy_capture():
#     content = get_capture()
#     return Response(content=content, media_type="image/jpeg")


@router.get("/chatbot/recipe")
async def chatbot_recipe(
    query: str = Query(None, description="Tên hoặc câu hỏi về món ăn"),
    url: str = Query(None, description="URL của món ăn trên monngonmoingay.com"),
    isbot: bool = Query(True, description="True: sử dụng bot mode, False: sử dụng user mode")
):
    try:
        result = bot.generate_response(query=query, url=url, isBot=isbot)
        if isinstance(result, dict):
            return result
        return {"message": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/config/maps-api-key")
async def get_maps_api_key():
    """Lấy Google Maps API Key từ backend"""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return JSONResponse(
            status_code=400,
            content={"error": "Google Maps API Key không được cấu hình"}
        )
    return {"apiKey": api_key}
# class ChatRequest(BaseModel):
#     message: str

# @router.post("/chat")
# async def chat_endpoint(request: ChatRequest):
#     try:
#         user_message = request.message

#         if not user_message:
#             return "Please provide a message."
#         else:
#             # response = bot.generate_response(user_message)
#             response = "This is a placeholder response."
#             return response
   
#     except Exception as e:
#         logging.error(f"Server error: {e}")
#         return "An error occurred on the server."
