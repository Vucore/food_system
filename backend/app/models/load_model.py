import os
import sys
import warnings
import logging

# --- 1. CẤU HÌNH MÔI TRƯỜNG ---
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore') # Cần import warnings trước khi dùng

import tensorflow as tf
import numpy as np
from typing import Tuple, Dict, Any, Optional, List
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input

logging.getLogger('tensorflow').setLevel(logging.CRITICAL)

# --- DANH SÁCH NHÃN (Giữ nguyên) ---
DEFAULT_CLASS_NAMES = [
    'banh_mi_ap_chao', 'banh_xeo_hai_san', 'bun_gio_heo', 'ca_bong_trung_kho_tieu',
    'canh_chua_ca', 'canh_kho_qua_ham_thit', 'chan_ga_xa_ot', 'chao_ca_nau_bap_nep',
    'com_chien', 'dau_hu_xot_cay', 'ech_xao_lan', 'ga_hap_hanh', 'ga_nuong',
    'luon_xao_xa_ot', 'ngheu_hap_thai', 'pizza_hai_san', 'sup_ga_bi_do', 'thit_kho',
    'trung_chien_rau_cu_xot_mayonnaise', 'vit_kho_rieng'
]

# --- CLASS DỰ ĐOÁN ---
class FoodModelPredictorTF:
    def __init__(self, model_path: str, class_names: Optional[List[str]] = None):
        self.model_path = model_path
        self.class_names = class_names if class_names is not None else DEFAULT_CLASS_NAMES
        self.model = None
        self.target_size = (224, 224)
        self._load_model()

    def _load_model(self) -> None:
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Không tìm thấy file model tại: {self.model_path}")

            print(f"⏳ Đang tải model...", end="")

            # Tắt log rác khi load model
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                self.model = tf.keras.models.load_model(self.model_path, compile=False)
            finally:
                sys.stdout = old_stdout

            print(f" -> ✅ Xong!")

            if self.model.output_shape[-1] != len(self.class_names):
                print(f"⚠️ Cảnh báo: Model output {self.model.output_shape[-1]} != {len(self.class_names)} nhãn.")

        except Exception as e:
            print(f"\n❌ Lỗi tải model: {e}")
            raise

    def _preprocess_image(self, image_path: str) -> np.ndarray:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Không tìm thấy ảnh: {image_path}")

        # 1. Load ảnh
        img = image.load_img(image_path, target_size=self.target_size)

        # 2. Chuyển thành mảng
        img_array = image.img_to_array(img)

        # 3. Thêm chiều batch (Sample dimension)
        img_array = np.expand_dims(img_array, axis=0)

        img_array = preprocess_input(img_array)

        return img_array

    def predict(self, image_path: str) -> Dict[str, Any]:
        if self.model is None: raise RuntimeError("Model chưa tải")
        try:
            img_array = self._preprocess_image(image_path)
            predictions = self.model.predict(img_array, verbose=0)
            probs = predictions[0]
            predicted_idx = np.argmax(probs)

            all_predictions = {
                self.class_names[i]: float(probs[i]) * 100
                for i in range(len(self.class_names))
            }
            # Sắp xếp từ cao xuống thấp
            sorted_predictions = dict(sorted(all_predictions.items(), key=lambda item: item[1], reverse=True))

            return {
                "predicted_class": self.class_names[predicted_idx],
                "confidence": round(float(probs[predicted_idx]) * 100, 2),
                "all_predictions": sorted_predictions,
                "image_path": image_path
            }
        except Exception as e:
            raise RuntimeError(f"Lỗi predict: {e}")

def create_predictor(model_path):
    return FoodModelPredictorTF(model_path)
