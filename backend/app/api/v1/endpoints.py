# endpoints.py
import json
from fastapi import APIRouter, Response, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from app.utils.camera import generate, get_capture
from fastapi.responses import JSONResponse, StreamingResponse
import logging
from fastapi import WebSocket
from typing import List, Dict

from ...bot.init import ChatbotBase
from fastapi import Form
from app.utils.db import get_db, serialize_mongo_document
import os
from fastapi import WebSocket

# Import AI Predict Service
from app.core.ai_predict import get_ai_service, predict_food_cascade
from app.models.load_model_nutrition import create_nutrition_predictor
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Lưu thông tin WebSocket clients với mode của họ
class WebSocketClient:
    def __init__(self, websocket: WebSocket, mode: str = "restaurant"):
        self.websocket = websocket
        self.mode = mode  # "restaurant" hoặc "nutrition"

active_websockets: List[WebSocketClient] = []
bot = ChatbotBase()

# Khởi tạo AI service khi startup
ai_service = get_ai_service(save_dir="./images")

# Khởi tạo Nutrition service
BASE_DIR = Path(__file__).resolve().parent.parent.parent
nutrition_predictor = None
try:
    nutrition_predictor = create_nutrition_predictor(
        model_path=str(BASE_DIR / "models" / "best_swinS_food_Nutri.pth"),  # Thay đổi tên model của bạn
        nutrition_csv_path=str(BASE_DIR / "data" / "Get_Nutrition.csv")
    )
    logger.info("✅ Nutrition predictor loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load nutrition predictor: {e}")


@router.post("/capture")
async def capture(
    file: UploadFile = File(...), 
    user_id: str = Form("anonymous"),
    mode: str = Form("restaurant")  # Thêm mode parameter
):
    """Endpoint để capture ảnh từ frontend"""
    try:
        # Nhận file ảnh từ frontend
        image_data = await file.read()
        
        if mode == "nutrition":
            # Xử lý nutrition mode
            if nutrition_predictor is None:
                raise HTTPException(status_code=500, detail="Nutrition predictor not available")
            
            # Lưu ảnh tạm
            from datetime import datetime
            timestamp_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + file.filename
            image_path = os.path.join("./images", timestamp_filename)
            os.makedirs("./images", exist_ok=True)
            
            with open(image_path, "wb") as f:
                f.write(image_data)
            
            # Dự đoán nutrition
            result = nutrition_predictor.predict(image_path)
            
            nutrition_result = {
                "success": True,
                "user_id": user_id,
                "mode": "nutrition",
                "predicted_class": result["predicted_class"],
                "confidence": result["confidence"],
                "nutrition_info": result["nutrition_info"],
                "image_path": image_path,
                "created_at": datetime.now().isoformat()
            }
            
            # Lưu vào database
            db = get_db()
            inserted_id = db["nutrition_detections"].insert_one(nutrition_result).inserted_id
            
            return {
                "success": True,
                "mode": "nutrition",
                "nutrition_data": result["nutrition_info"],
                "predicted_class": result["predicted_class"],
                "confidence": result["confidence"]
            }
        else:
            # Xử lý restaurant mode (code cũ)
            ai_result = predict_food_cascade(
                image_data=image_data,
                filename=file.filename,
                user_id=user_id,
                for_esp32=False
            )
            
            # Lưu vào database
            db = get_db()
            inserted_id = db["foods"].insert_one(ai_result).inserted_id
            
            # Truy vấn lấy món ăn của user hiện tại
            foods_cursor = db["foods"].find({"user_id": user_id}).sort([("_id", -1)])
            foods = [serialize_mongo_document(doc) for doc in foods_cursor]
            
            return {
                "success": ai_result["success"],
                "mode": "restaurant",
                "detected_foods": foods,
            }
            
    except Exception as e:
        logger.error(f"Error in capture: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {e}")


@router.get('/video_feed')
def video_feed():
    """Stream video feed"""
    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')


@router.get("/proxy_capture")
def proxy_capture():
    """Proxy để capture ảnh từ camera"""
    content = get_capture()
    return Response(content=content, media_type="image/jpeg")


@router.get("/chatbot/recipe")
async def chatbot_recipe(
    query: str = Query(None, description="Tên hoặc câu hỏi về món ăn"),
    url: str = Query(None, description="URL của món ăn trên monngonmoingay.com"),
    isbot: bool = Query(True, description="True: sử dụng bot mode, False: sử dụng user mode")
):
    """Endpoint chatbot để hỏi về công thức nấu ăn"""
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
    user_id: str = "anonymous"


@router.post("/capture/button")
async def capture_event(event: ButtonEvent):
    """Endpoint để xử lý sự kiện nhấn nút từ ESP32"""
    logger.info(f"ESP32 button pressed! {event.dict()}")
    
    try:
        user_id = event.user_id
        logger.info(f"[1] User ID: {user_id}")
        
        # Backend tự capture ảnh từ camera
        image_content = get_capture()
        logger.info(f"[2] Image captured, size: {len(image_content)} bytes")
        
        # Xử lý cho TỪNG client dựa trên mode của họ
        for client in active_websockets:
            try:
                mode = client.mode
                logger.info(f"[3] Processing for client in {mode} mode")
                
                if mode == "nutrition":
                    # Xử lý Nutrition Mode
                    if nutrition_predictor is None:
                        logger.error("Nutrition predictor not available")
                        continue
                    
                    # Lưu ảnh tạm
                    from datetime import datetime
                    timestamp_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_esp32_capture.jpg"
                    image_path = os.path.join("./images", timestamp_filename)
                    os.makedirs("./images", exist_ok=True)
                    
                    with open(image_path, "wb") as f:
                        f.write(image_content)
                    
                    # Dự đoán nutrition
                    result = nutrition_predictor.predict(image_path)
                    logger.info(f"[4] Nutrition prediction: {result['predicted_class']} ({result['confidence']}%)")
                    
                    nutrition_result = {
                        "success": True,
                        "user_id": user_id,
                        "mode": "nutrition",
                        "predicted_class": result["predicted_class"],
                        "confidence": result["confidence"],
                        "nutrition_info": result["nutrition_info"],
                        "image_path": image_path,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    # Lưu vào database
                    db = get_db()
                    insert_result = db["nutrition_detections"].insert_one(nutrition_result)
                    logger.info(f"[5] Saved to nutrition_detections DB")
                    
                    # Gửi qua WebSocket
                    websocket_message = {
                        "type": "nutrition_result",
                        "data": {
                            "success": True,
                            "mode": "nutrition",
                            "nutrition_data": result["nutrition_info"],
                            "predicted_class": result["predicted_class"],
                            "confidence": result["confidence"]
                        }
                    }
                    
                else:
                    # Xử lý Restaurant Mode (code cũ)
                    ai_result = predict_food_cascade(
                        image_data=image_content,
                        filename="esp32_capture.jpg",
                        user_id=user_id,
                        for_esp32=True
                    )
                    logger.info(f"[4] Restaurant prediction: {ai_result['name']} ({ai_result['confidence']}%)")
                    
                    # Lưu vào database
                    db = get_db()
                    insert_result = db["foods"].insert_one(ai_result)
                    logger.info(f"[5] Saved to foods DB")
                    
                    # Serialize món ăn mới
                    new_food = serialize_mongo_document(ai_result)
                    new_food['_id'] = str(insert_result.inserted_id)
                    
                    # Gửi qua WebSocket
                    websocket_message = {
                        "type": "capture_result",
                        "data": {
                            "success": ai_result["success"],
                            "mode": "restaurant",
                            "new_food": new_food
                        }
                    }
                
                # Gửi message cho client này
                await client.websocket.send_text(json.dumps(websocket_message))
                logger.info(f"[6] Sent WebSocket message to client ({mode} mode)")
                
            except Exception as client_error:
                logger.error(f"Error processing for client: {client_error}")
        
        return {"status": "success", "message": "Processed for all connected clients"}
            
    except Exception as e:
        logger.error(f"[ERROR at capture] Error processing capture: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@router.websocket("/ws/button")
async def websocket_button(websocket: WebSocket):
    """WebSocket endpoint để nhận real-time updates"""
    client = None
    try:
        await websocket.accept()
        logger.info("WebSocket client connected")
        
        # Tạo client với mode mặc định
        client = WebSocketClient(websocket, mode="restaurant")
        active_websockets.append(client)
        
        while True:
            try:
                # Nhận message từ frontend
                data = await websocket.receive_text()
                logger.info(f"WebSocket message received: {data}")
                
                # Parse message
                try:
                    message = json.loads(data)
                    
                    # Cập nhật mode nếu frontend gửi
                    if message.get("type") == "set_mode":
                        new_mode = message.get("mode", "restaurant")
                        client.mode = new_mode
                        logger.info(f"Client mode updated to: {new_mode}")
                        
                        # Gửi xác nhận
                        await websocket.send_text(json.dumps({
                            "type": "mode_updated",
                            "mode": new_mode
                        }))
                        
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received: {data}")
                    
            except Exception as e:
                logger.error(f"Error in WebSocket loop: {e}")
                break
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if client and client in active_websockets:
            active_websockets.remove(client)
        logger.info("WebSocket client disconnected")