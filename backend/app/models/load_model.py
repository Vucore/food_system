import tensorflow as tf
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any, Optional


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

CLASS_NAMES_VIETNAMESE = {
    'banh_mi_ap_chao': 'Banh Mi Ap Chao',
    'banh_xeo_hai_san': 'Banh Xeo Hai San',
    'bun_gio_heo': 'Bun Gio Heo',
    'ca_bong_trung_kho_tieu': 'Ca Bong Trung Kho Tieu',
    'canh_chua_ca': 'Canh Chua Ca',
    'canh_kho_qua_ham_thit': 'Canh Kho Qua Ham Thit',
    'chan_ga_xa_ot': 'Chan Ga Xa Ot',
    'chao_ca_nau_bap_nep': 'Chao Ca Nau Bap Nep',
    'com_chien': 'Com Chien',
    'dau_hu_xot_cay': 'Dau Hu Xot Cay',
    'ech_xao_lan': 'Ech Xao Lan',
    'ga_hap_hanh': 'Ga Hap Hanh',
    'ga_nuong': 'Ga Nuong',
    'luon_xao_xa_ot': 'Luon Xao Xa Ot',
    'ngheu_hap_thai': 'Ngheu Hap Thai',
    'pizza_hai_san': 'Pizza Hai San',
    'sup_ga_bi_do': 'Sup Ga Bi Do',
    'thit_kho': 'Thit Kho',
    'trung_chien_rau_cu_xot_mayonnaise': 'Trung Chien Rau Cu Xot Mayonnaise',
    'vit_kho_rieng': 'Vit Kho Rieng'
}


def convert_to_vietnamese(english_name: str) -> str:
    """
    Chuyển đổi tên lớp từ snake_case sang tiếng Việt chuẩn
    
    Args:
        english_name: Tên lớp (ví dụ: 'ga_nuong')
        
    Returns:
        Tên tiếng Việt (ví dụ: 'Gà Nướng')
    """
    return CLASS_NAMES_VIETNAMESE.get(english_name, english_name)


def convert_predictions_to_vietnamese(predictions_dict: Dict[str, float]) -> Dict[str, float]:
    """
    Chuyển đổi toàn bộ dict dự đoán sang tiếng Việt
    
    Args:
        predictions_dict: Dict gốc với key là tên lớp English
        
    Returns:
        Dict mới với key là tên tiếng Việt
    """
    return {
        convert_to_vietnamese(key): value
        for key, value in predictions_dict.items()
    }


class FoodModelPredictor:
    """Class để tải model và dự đoán hình ảnh thức ăn"""

    def __init__(self, model_path: str, class_names: Optional[list] = None):
        """
        Khởi tạo FoodModelPredictor
        
        Args:
            model_path: Đường dẫn đến file model (.keras)
            class_names: Danh sách tên các lớp (nếu không có sẽ tự động lấy từ config)
        """
        self.model_path = model_path
        self.class_names = class_names or DEFAULT_CLASS_NAMES
        self.model = None
        self.target_size = (224, 224)
        
        self._load_model()
    
    def _load_model(self) -> None:
        """Tải model từ file"""
        try:
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Model file không tìm thấy: {self.model_path}")
            
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"✅ Model đã được tải thành công từ: {self.model_path}")
        except Exception as e:
            print(f"Lỗi khi tải model: {e}")
            raise
    
    def _preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Tải và chuẩn bị ảnh
        
        Args:
            image_path: Đường dẫn đến file ảnh
            
        Returns:
            Array ảnh đã xử lý
        """
        try:
            if not Path(image_path).exists():
                raise FileNotFoundError(f"Ảnh không tìm thấy: {image_path}")
            
            # Tải ảnh với kích thước target
            img = tf.keras.utils.load_img(
                image_path, 
                target_size=self.target_size
            )
            
            # Convert sang array
            img_array = tf.keras.utils.img_to_array(img)
            
            # Normalize nếu cần (0-1)
            img_array = img_array / 255.0
            
            # Tạo batch
            img_array = tf.expand_dims(img_array, 0)
            
            return img_array
        except Exception as e:
            print(f"Lỗi khi xử lý ảnh: {e}")
            raise
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        """
        Dự đoán lớp của ảnh
        
        Args:
            image_path: Đường dẫn đến file ảnh
            
        Returns:
            Dict chứa:
                - predicted_class: Tên lớp dự đoán
                - confidence: Độ tin cậy (%)
                - predictions: Array tất cả xác suất
                - all_predictions: Dict tất cả các lớp với xác suất
        """
        try:
            if self.model is None:
                raise RuntimeError("Model chưa được tải")
            
            if self.class_names is None:
                raise ValueError("class_names chưa được cấu hình")
            
            # Xử lý ảnh
            img_array = self._preprocess_image(image_path)
            
            # Dự đoán
            predictions = self.model.predict(img_array, verbose=0)
            score = tf.nn.softmax(predictions[0]).numpy()
            
            # Lấy kết quả
            predicted_idx = np.argmax(score)
            predicted_class = self.class_names[predicted_idx]
            confidence = 100 * float(score[predicted_idx])
            
            # Tạo dict tất cả dự đoán
            all_predictions = {
                self.class_names[i]: float(score[i]) * 100
                for i in range(len(self.class_names))
            }
            predicted_class = convert_to_vietnamese(predicted_class)
            all_predictions = convert_predictions_to_vietnamese(all_predictions)
            return {
                "predicted_class": predicted_class,
                "confidence": round(confidence, 2),
                "predictions": score,
                "all_predictions": all_predictions,
                "image_path": image_path
            }
        
        except Exception as e:
            print(f"Lỗi khi dự đoán: {e}")
            raise
    
    def predict_batch(self, image_paths: list) -> list:
        """
        Dự đoán nhiều ảnh cùng lúc
        
        Args:
            image_paths: Danh sách đường dẫn ảnh
            
        Returns:
            Danh sách kết quả dự đoán
        """
        results = []
        for image_path in image_paths:
            try:
                result = self.predict(image_path)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e), "image_path": image_path})
        
        return results
    
    def set_class_names(self, class_names: list) -> None:
        """Cập nhật danh sách tên các lớp"""
        self.class_names = class_names
        print(f"Danh sách lớp đã được cập nhật: {class_names}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Lấy thông tin model"""
        if self.model is None:
            return {"error": "Model chưa được tải"}
        
        return {
            "model_path": self.model_path,
            "input_shape": self.model.input_shape,
            "output_shape": self.model.output_shape,
            "total_params": self.model.count_params(),
            "class_names": self.class_names,
            "num_classes": len(self.class_names) if self.class_names else 0
        }