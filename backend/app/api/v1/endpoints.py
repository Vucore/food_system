from datetime import datetime
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from app.utils.camera import generate, get_capture
from fastapi.responses import StreamingResponse
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
    {"name": "Chicken", "calories": 248, "protein": 46, "carbs": 1, "fat": 5},
    {"name": "Beef", "calories": 250, "protein": 26, "carbs": 0, "fat": 15},
    {"name": "Salmon", "calories": 206, "protein": 22, "carbs": 0, "fat": 13},
    {"name": "Tofu", "calories": 76, "protein": 8, "carbs": 2, "fat": 4},
    {"name": "Egg", "calories": 155, "protein": 13, "carbs": 1, "fat": 11},
    {"name": "Pork", "calories": 242, "protein": 27, "carbs": 0, "fat": 14},
    {"name": "Shrimp", "calories": 99, "protein": 24, "carbs": 0, "fat": 1},
    {"name": "Duck", "calories": 337, "protein": 27, "carbs": 0, "fat": 24},
    {"name": "Rice", "calories": 130, "protein": 2, "carbs": 28, "fat": 0},
    {"name": "Bread", "calories": 265, "protein": 9, "carbs": 49, "fat": 3},
    {"name": "Potato", "calories": 77, "protein": 2, "carbs": 17, "fat": 0},
    {"name": "Sweet Corn", "calories": 86, "protein": 3, "carbs": 19, "fat": 1},
    {"name": "Apple", "calories": 52, "protein": 0, "carbs": 14, "fat": 0},
    {"name": "Banana", "calories": 89, "protein": 1, "carbs": 23, "fat": 0},
    {"name": "Carrot", "calories": 41, "protein": 1, "carbs": 10, "fat": 0},
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
    food = random.choice(FOOD_SAMPLES)
    fake_ai_result = {
        "user_id": user_id,
        "name": food["name"],
        "calories": food["calories"],
        "protein": food["protein"],
        "carbs": food["carbs"],
        "fat": food["fat"],
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
        total_calories = sum(doc.get("calories", 0) for doc in foods)
        return {
            "success": True,
            "detected_foods": foods,
            "total_calories": total_calories
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
    url: str = Query(None, description="URL của món ăn trên monngonmoingay.com")
):
    try:
        if url:
            # Xử lý URL trực tiếp
            result = bot.generate_response_from_url(url=url)
            # print(f"Processing URL: {url}")
        elif query:
            # Xử lý query
            result = bot.generate_response_from_query(query=query)
            # print(f"Processing query: {query}")
        else:
            return {"error": "Bạn cần cung cấp query hoặc url."}

        # Trả về kết quả
        if isinstance(result, dict):
            return result
        return {"message": result}
    except Exception as e:
        return {"error": str(e)}


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
