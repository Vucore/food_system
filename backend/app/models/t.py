import os
import sys
import warnings
# ✅ PHẢI ĐẶT TRƯỚC KHI IMPORT TENSORFLOW
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['AUTOGRAPH_VERBOSITY'] = '0'
warnings.filterwarnings('ignore')

import tensorflow as tf
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any, Optional, List
from tensorflow.keras.preprocessing import image

import logging
logging.getLogger('tensorflow').setLevel(logging.CRITICAL)
logging.getLogger('absl').setLevel(logging.CRITICAL)

# --- DANH SÁCH NHÃN CỦA BẠN (20 MÓN) ---
DEFAULT_CLASS_NAMES = [
    'banh_mi_ap_chao',
    'banh_xeo_hai_san',
    'bun_gio_heo',
    'ca_bong_trung_kho_tieu',
    'canh_chua_ca',
    'canh_kho_qua_ham_thit',
    'chan_ga_xa_ot',
    'chao_ca_nau_bap_nep',
    'com_chien',
    'dau_hu_xot_cay',
    'ech_xao_lan',
    'ga_hap_hanh',
    'ga_nuong',
    'luon_xao_xa_ot',
    'ngheu_hap_thai',
    'pizza_hai_san',
    'sup_ga_bi_do',
    'thit_kho',
    'trung_chien_rau_cu_xot_mayonnaise',
    'vit_kho_rieng'
]

class FoodModelPredictorTF:
    """Class để tải model TensorFlow/Keras và dự đoán hình ảnh thức ăn"""

    def __init__(self, model_path: str, class_names: Optional[List[str]] = None):
        """
        Khởi tạo FoodModelPredictorTF
        
        Args:
            model_path: Đường dẫn đến file model (.keras hoặc .h5)
            class_names: Danh sách tên các lớp (nếu None sẽ dùng DEFAULT_CLASS_NAMES)
        """
        self.model_path = model_path
        # Nếu không truyền class_names thì dùng list mặc định 20 món của bạn
        self.class_names = class_names if class_names is not None else DEFAULT_CLASS_NAMES
        self.model = None
        self.target_size = (224, 224) # Kích thước chuẩn EfficientNetB0
        
        self._load_model()
    
    def _load_model(self) -> None:
        """Tải model Keras từ file"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file không tìm thấy: {self.model_path}")
            
            print(f"⏳ Đang tải model từ: {self.model_path}...")
            # Tải model TensorFlow/Keras với compile=False
            import sys
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                self.model = tf.keras.models.load_model(self.model_path, compile=False)
            finally:
                sys.stdout = old_stdout
            
            print(f"✅ Model TensorFlow đã được tải thành công!")
            # Kiểm tra khớp số lượng nhãn
            # Lưu ý: output_shape thường là (None, num_classes)
            output_shape = self.model.output_shape
            if output_shape[-1] != len(self.class_names):
                print(f"⚠️ Cảnh báo: Model có {output_shape[-1]} đầu ra, nhưng danh sách nhãn có {len(self.class_names)} tên.")
            
        except Exception as e:
            print(f"❌ Lỗi khi tải model: {e}")
            raise
    
    def _preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Tải và chuẩn bị ảnh cho Keras model
        Args:
            image_path: Đường dẫn ảnh
        Returns:
            Numpy array (1, 224, 224, 3)
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Ảnh không tìm thấy: {image_path}")
            
            # 1. Load ảnh và resize
            img = image.load_img(image_path, target_size=self.target_size)
            
            # 2. Chuyển thành mảng Numpy
            img_array = image.img_to_array(img)
            
            # 3. Thêm chiều Batch
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            print(f"Lỗi khi xử lý ảnh: {e}")
            raise
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        """
        Dự đoán lớp của một bức ảnh
        
        Returns:
            Dict chứa kết quả dự đoán
        """
        try:
            if self.model is None:
                raise RuntimeError("Model chưa được tải")
            
            # Xử lý ảnh
            img_array = self._preprocess_image(image_path)
            
            # Dự đoán
            predictions = self.model.predict(img_array, verbose=0)
            probs = predictions[0] # Lấy kết quả của ảnh đầu tiên
            
            # Tìm class có xác suất cao nhất
            predicted_idx = np.argmax(probs)
            predicted_class = self.class_names[predicted_idx]
            confidence = float(probs[predicted_idx]) * 100
            
            # Tạo dict tất cả dự đoán
            all_predictions = {
                self.class_names[i]: float(probs[i]) * 100
                for i in range(len(self.class_names))
            }
            
            # Sắp xếp kết quả từ cao xuống thấp
            sorted_predictions = dict(sorted(all_predictions.items(), key=lambda item: item[1], reverse=True))

            return {
                "predicted_class": predicted_class,
                "confidence": round(confidence, 2),
                "predictions": probs, # Raw probabilities array
                "all_predictions": sorted_predictions,
                "image_path": image_path
            }
        
        except Exception as e:
            raise RuntimeError(f"LỖI predict(): {e}")


    def predict_batch(self, image_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Dự đoán danh sách nhiều ảnh cùng lúc
        """
        results = []
        for path in image_paths:
            try:
                result = self.predict(path)
                if result:
                    results.append(result)
            except Exception as e:
                results.append({"error": str(e), "image_path": path})
        return results

    def get_model_info(self) -> Dict[str, Any]:
        """Lấy thông tin model"""
        if self.model is None:
            return {"error": "Model chưa được tải"}
        
        return {
            "model_path": self.model_path,
            "model_type": "EfficientNet-B0 (Keras)",
            "num_classes": len(self.class_names),
            "target_size": self.target_size
        }

def create_predictor(model_path: str, class_names: Optional[List[str]] = None) -> FoodModelPredictorTF:
    """
    Hàm tạo nhanh predictor instance (Factory function)
    """
    return FoodModelPredictorTF(model_path, class_names)

# ==========================================
# PHẦN CHẠY THỬ (MAIN)
# ==========================================
if __name__ == "__main__":
    # 1. Cấu hình đường dẫn
   # ĐÚNG - thêm r
    MODEL_FILE = r"D:\CN_IOT\CK\backend\app\models\best_food_model_pro.keras"
    TEST_IMG = r"D:\CN_IOT\CK\backend\images\20251213_200112_esp32_capture.jpg" # Ảnh muốn test
    
    # 2. Khởi tạo (Tự động lấy DEFAULT_CLASS_NAMES ở trên)
    predictor = create_predictor(MODEL_FILE)
    
    # 3. Dự đoán
    print(f"\n🔍 Đang dự đoán ảnh: {TEST_IMG}")
    result = predictor.predict(TEST_IMG)
    
    if result:
        print("\n" + "="*40)
        print(f"🍖 KẾT QUẢ: {result['predicted_class'].upper()}")
        print(f"🎯 ĐỘ TIN CẬY: {result['confidence']}%")
        print("="*40)
        
        print("\nTop 3 khả năng:")
        count = 0
        for name, conf in result['all_predictions'].items():
            print(f" - {name}: {conf:.2f}%")
            count += 1
            if count == 3: break