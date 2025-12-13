from datetime import datetime
import json
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from app.utils.camera import generate, get_capture
from fastapi.responses import JSONResponse, StreamingResponse
import logging
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

from app.models.load_model import FoodModelPredictor
from ...bot.init import ChatbotBase
from fastapi import Form
from app.utils.db import get_db, serialize_mongo_document
from PIL import Image
from app.utils.food_db import FoodDatabase
import os
import io
from fastapi import WebSocket
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
active_websockets: List[WebSocket] = []
bot = ChatbotBase()
# predictor = FoodModelPredictor(model_path="/mnt/d/Công Nghệ IoT/CK/backend/app/models/my_food_model.keras")
predictor = FoodModelPredictor(model_path="D:\\Công Nghệ IoT\\CK\\backend\\app\\models\\modelFood.keras")
food_db = FoodDatabase(json_path="D:\\Công Nghệ IoT\\CK\\backend\\app\\data\\food_database.json")

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
    print(f"Ảnh đã được lưu tại: {save_path}")
    # Xử lý ảnh 
    # image = Image.open(io.BytesIO(image_data))
    result_predict = predictor.predict(image_path=save_path)
    predicted_name = result_predict['predicted_class']
    confidence = result_predict['confidence']
    print(f"Dự đoán: {result_predict['predicted_class']}")
    print(f"Độ tin cậy: {result_predict['confidence']}%")
    # # Lấy thông tin từ JSON - random chọn 1 nhà hàng
    food_info = food_db.get_food_by_name(predicted_name)
        
    if not food_info:
        # Fallback nếu không tìm thấy
        food_info = {
            "food_name": predicted_name,
            "restaurant_name": "Unknown",
            "address": "Unknown",
            "google_maps": ""
        }
    all_restaurants = food_db.get_all_restaurants_for_food(predicted_name)
    ai_result = {
            "user_id": user_id,
            "name": food_info["food_name"],
            "restaurant": food_info["restaurant_name"],
            "address": food_info["address"],
            "google_maps": food_info["google_maps"],
            "all_restaurants": all_restaurants,  # Lưu tất cả nhà hàng
            "image_path": save_path,
            "confidence": confidence,
            "predicted_class": predicted_name,
            "created_at": datetime.now().isoformat()
        }    
    try:
        db = get_db()
        # Lưu dữ liệu vào collection 'foods'
        inserted_id = db["foods"].insert_one(ai_result).inserted_id

        # Truy vấn chỉ lấy món ăn của user hiện tại
        foods_cursor = db["foods"].find({"user_id": user_id}).sort([("_id", -1)])
        foods = [serialize_mongo_document(doc) for doc in foods_cursor]
        return {
            "success": True,
            "detected_foods": foods,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi truy vấn MongoDB: {e}")

@router.get('/video_feed')
def video_feed():
    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

@router.get("/proxy_capture")
def proxy_capture():
    content = get_capture()
    return Response(content=content, media_type="image/jpeg")


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

class ButtonEvent(BaseModel):
    user_id : str = "anonymous"

@router.post("/capture/button")
async def capture_event(event: ButtonEvent):
    logger.info(f"ESP32 button pressed! {event.dict()}")
    
    try:
        user_id = event.user_id
        logger.info(f"[1] User ID: {user_id}")
        
        # Backend tự capture ảnh từ camera
        image_content = get_capture()
        logger.info(f"[2] Image captured, size: {len(image_content)} bytes")
        
        # Lưu ảnh
        os.makedirs(save_dir, exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_esp32_capture.jpg"
        save_path = os.path.join(save_dir, filename)
        
        with open(save_path, "wb") as f:
            f.write(image_content)
        logger.info(f"[3] Image saved to: {save_path}")
        
        # Xử lý AI
        result_predict = predictor.predict(image_path=save_path)
        predicted_name = result_predict['predicted_class']
        confidence = result_predict['confidence']
        logger.info(f"[4] Predicted: {predicted_name}, Confidence: {confidence}")
        
        food_info = food_db.get_food_by_name(predicted_name)
        logger.info(f"[5] Food info found: {food_info is not None}")
        
        if not food_info:
            food_info = {
                "food_name": predicted_name,
                "restaurant_name": "Unknown",
                "address": "Unknown",
                "google_maps": ""
            }
        
        all_restaurants = food_db.get_all_restaurants_for_food(predicted_name)
        logger.info(f"[6] Restaurants found: {len(all_restaurants)}")
        
        ai_result = {
            "user_id": user_id,
            "name": food_info["food_name"],
            "restaurant": food_info["restaurant_name"],
            "address": food_info["address"],
            "google_maps": food_info["google_maps"],
            "all_restaurants": all_restaurants,
            "image_path": save_path,
            "confidence": float(confidence),
            "predicted_class": predicted_name,
            "created_at": datetime.now().isoformat()
        }
        logger.info(f"[7] AI result created: {ai_result['name']}")
        
        try:
            db = get_db()
            logger.info("[8] Connected to MongoDB")
            
            # Lưu dữ liệu vào collection 'foods'
            insert_result = db["foods"].insert_one(ai_result)
            logger.info(f"[9] Inserted to DB with ID: {insert_result.inserted_id}")
            
            # Truy vấn chỉ lấy món ăn của user hiện tại
            foods_cursor = db["foods"].find({"user_id": user_id}).sort([("_id", -1)])
            foods = [serialize_mongo_document(doc) for doc in foods_cursor]
            logger.info(f"[10] Retrieved {len(foods)} foods from DB")
            
            response = {
                "success": True,
                "detected_foods": foods,
            }
            logger.info(f"[11] Sending response with {len(foods)} foods")
            
            # **GỬI QUA WEBSOCKET CHO FRONTEND**
            websocket_message = {
                "type": "capture_result",
                "data": response
            }
            
            for ws in active_websockets:
                try:
                    await ws.send_text(json.dumps(websocket_message))
                    logger.info(f"[12] Sent WebSocket message to frontend")
                except Exception as ws_error:
                    logger.error(f"Error sending WebSocket: {ws_error}")
            
            return response
            
        except Exception as ex:
            logger.error(f"[ERROR at DB] Error saving to DB: {ex}", exc_info=True)
            return {"status": "error", "message": f"Database error: {ex}"}
            
    except Exception as e:
        logger.error(f"[ERROR at capture] Error processing capture: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
    
@router.websocket("/ws/button")
async def websocket_button(websocket: WebSocket):
    try:
        await websocket.accept()
        logger.info("WebSocket client connected")
        active_websockets.append(websocket)
        
        while True:
            # Giữ kết nối mở, chỉ lắng nghe ping/pong
            try:
                data = await websocket.receive_text()
                logger.info(f"WebSocket message: {data}")
            except:
                break
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if websocket in active_websockets:
            active_websockets.remove(websocket)
        logger.info("WebSocket client disconnected")