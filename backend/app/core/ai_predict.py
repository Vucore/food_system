# backend/app/core/ai_predict.py
from datetime import datetime
from typing import Dict, Any, Optional, List
import os

from app.utils.food_db import FoodDatabase
from app.models.load_model_eff import FoodModelPredictorEff  # Cho EfficientNet
from app.models.load_model import FoodModelPredictorTF       # Cho EfficientNet_vinh
from app.models.load_model_30_sum import FoodModelPredictorSwin  # Cho Swin Transformer
from app.utils.vietnamese import format_food_name_with_accent

from pathlib import Path

# Thêm vào đầu file ai_predict.py, sau import
BASE_DIR = Path(__file__).resolve().parent.parent  # Thư mục backend/app/

MODEL_CONFIGS = [
    {
        "name": "efficientnet_vu",
        "model_type": "pytorch_eff", 
        "model_path": str(BASE_DIR / "models" / "best_model_eff.pth"),
        "food_db_path": str(BASE_DIR / "data" / "food_db_eff_vu.json"),
        "num_classes": 30
    },
    {
        "name": "efficientnet_vinh",
        "model_type": "tensorflow",  
        "model_path": str(BASE_DIR / "models" / "model_pro.h5"),  
        "food_db_path": str(BASE_DIR / "data" / "food_db_eff_vinh.json"),
        "num_classes": 20
    },

    {
        "name": "swin small",
        "model_type": "pytorch_swin",
        "model_path": str(BASE_DIR / "models" / "best_swinS_food.pth"),
        "food_db_path": str(BASE_DIR / "data" / "food_db_eff_vu.json"),
        "num_classes": 30
    }
]

CONFIDENCE_THRESHOLD = 85.0  # Ngưỡng confidence để chuyển model


class AIPredictService:
    """Service dự đoán món ăn với cascade models"""
    
    def __init__(self, save_dir: str = "./images"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
        self.models: List[Dict[str, Any]] = []
        self._load_all_models()
    
    def _load_all_models(self):
        """Load tất cả models từ config"""
        for config in MODEL_CONFIGS:
            try:
                print(f"🔄 Loading model: {config['name']}...")
                print(f"   📁 Model path: {config['model_path']}")
                print(f"   🔍 File exists: {os.path.exists(config['model_path'])}")
                
                # Chọn predictor phù hợp với model type
                if config['model_type'] == 'pytorch_eff':
                    predictor = FoodModelPredictorEff(
                        model_path=config['model_path'],
                        num_classes=config.get('num_classes', 30)
                    )
                elif config['model_type'] == 'tensorflow':
                    print(f"   🔧 Đang khởi tạo TensorFlow predictor...")
                    predictor = FoodModelPredictorTF(
                        model_path=config['model_path'],
                        class_names=None 
                    )
                    print(f"   ✅ TensorFlow predictor đã khởi tạo")
                elif config['model_type'] == 'pytorch_swin':
                    predictor = FoodModelPredictorSwin(
                        model_path=config['model_path'],
                        num_classes=config.get('num_classes', 30)
                    )
                    print(f"   ✅ Swin Transformer predictor đã khởi tạo")
                else:
                    raise ValueError(f"Unknown model_type: {config['model_type']}")
                
                # Load food database
                print(f"   📊 Loading food database...")
                food_db = FoodDatabase(json_path=config['food_db_path'])
                
                self.models.append({
                    "name": config['name'],
                    "predictor": predictor,
                    "food_db": food_db,
                    "config": config
                })
                
                print(f"✅ Model {config['name']} loaded successfully\n")
                
            except Exception as e:
                print(f"\n❌ ======== ERROR LOADING MODEL {config['name']} ========")
                print(f"Error message: {e}")
                print(f"Error type: {type(e).__name__}")
                print(f"Full traceback:")
                import traceback
                traceback.print_exc()
                print(f"========================================\n")
                
        print(f"\n📊 Tổng số models đã load: {len(self.models)}")
        for idx, m in enumerate(self.models, 1):
            print(f"   {idx}. {m['name']}")
        print()
    def predict_with_cascade(
        self, 
        image_data: bytes,
        filename: str,
        user_id: str = "anonymous",
        for_esp32: bool = False 
    ) -> Dict[str, Any]:
        """
        Dự đoán với cascade models
        
        Args:
            image_data: Dữ liệu ảnh bytes
            filename: Tên file
            user_id: ID người dùng
            for_esp32: True nếu response cho ESP32 (không dấu)
            
        Returns:
            Dict kết quả dự đoán
        """
        # 1. Lưu ảnh trước
        timestamp_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + filename
        image_path = os.path.join(self.save_dir, timestamp_filename)
        with open(image_path, "wb") as f:
            f.write(image_data)
        print(f"📸 Ảnh đã lưu: {image_path}")
        
        # 2. Thử dự đoán với từng model
        prediction_results = []
        
        for model_info in self.models:
            try:
                model_name = model_info['name']
                predictor = model_info['predictor']
                food_db = model_info['food_db']
                
                print(f"🔍 Đang dự đoán với model: {model_name}")
                
                # Dự đoán
                result = predictor.predict(image_path)
                predicted_class = result['predicted_class']
                confidence = result['confidence']
                
                print(f"   → {predicted_class}: {confidence}%")
                
                # Lưu kết quả
                prediction_results.append({
                    "model_name": model_name,
                    "predicted_class": predicted_class,
                    "confidence": confidence
                })
                
                # Nếu confidence >= 80%, dùng kết quả này
                if confidence >= CONFIDENCE_THRESHOLD:
                    print(f"✅ Confidence đạt {confidence}% - Sử dụng model {model_name}")
                    
                    # Lấy thông tin nhà hàng
                    food_info = food_db.get_food_by_name(predicted_class)
                    
                    if not food_info:
                        food_info = {
                            "food_name": predicted_class,
                            "restaurant_name": "Unknown",
                            "address": "Unknown",
                            "google_maps": ""
                        }
                    
                    all_restaurants = food_db.get_all_restaurants_for_food(predicted_class)
                    
                     # Format tên món ăn
                    food_name_with_accent = format_food_name_with_accent(predicted_class)
                    food_name_no_accent = predicted_class.replace('_', ' ')
                    
                    # Tên hiển thị: có dấu cho web, không dấu cho ESP32
                    display_name = food_name_no_accent if for_esp32 else food_name_with_accent
                    
                    return {
                        "success": True,
                        "user_id": user_id,
                        "name": display_name,  # Tên hiển thị (có/không dấu tùy client)
                        "name_with_accent": food_name_with_accent,  # Luôn có dấu
                        "name_no_accent": food_name_no_accent,  # Luôn không dấu
                        "restaurant": food_info["restaurant_name"],
                        "address": food_info["address"],
                        "google_maps": food_info["google_maps"],
                        "all_restaurants": all_restaurants,
                        "image_path": image_path,
                        "confidence": float(confidence),
                        "predicted_class": predicted_class,
                        "model_used": model_name,
                        "all_model_results": prediction_results,
                        "created_at": datetime.now().isoformat()
                    }
                else:
                    print(f"⚠️ Confidence {confidence}% < {CONFIDENCE_THRESHOLD}% - Thử model tiếp theo")
                    
            except Exception as e:
                print(f"❌ Error với model {model_name}: {e}")
                prediction_results.append({
                    "model_name": model_name,
                    "error": str(e)
                })
        
        # 3. Không có model nào đạt >= 80%
        print(f"❌ Không có model nào đạt confidence >= {CONFIDENCE_THRESHOLD}%")
        
        return {
            "success": False,
            "user_id": user_id,
            "name": "Khong nhan dien duoc" if for_esp32 else "Không nhận diện được",
            "name_with_accent": "Không nhận diện được",
            "name_no_accent": "Khong nhan dien duoc",
            "restaurant": "N/A",
            "address": "N/A",
            "google_maps": "",
            "all_restaurants": [],
            "image_path": image_path,
            "confidence": 0.0,
            "predicted_class": "Unknown",
            "model_used": "None",
            "all_model_results": prediction_results,
            "message": f"Không có model nào đạt confidence >= {CONFIDENCE_THRESHOLD}%",
            "created_at": datetime.now().isoformat()
        }


# Singleton instance
_ai_service_instance: Optional[AIPredictService] = None


def get_ai_service(save_dir: str = "./images") -> AIPredictService:
    """
    Lấy singleton instance của AI Service
    
    Args:
        save_dir: Thư mục lưu ảnh
        
    Returns:
        AIPredictService instance
    """
    global _ai_service_instance
    
    if _ai_service_instance is None:
        _ai_service_instance = AIPredictService(save_dir=save_dir)
    
    return _ai_service_instance


def predict_food_cascade(
    image_data: bytes,
    filename: str,
    user_id: str = "anonymous",
    for_esp32: bool = False
) -> Dict[str, Any]:
    """
    Hàm dự đoán với cascade models
    
    Args:
        image_data: Dữ liệu ảnh bytes
        filename: Tên file
        user_id: ID người dùng
        for_esp32: True nếu response cho ESP32 (không dấu)
        
    Returns:
        Dict kết quả dự đoán
    """
    service = get_ai_service()
    return service.predict_with_cascade(image_data, filename, user_id, for_esp32)