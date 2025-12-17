# load_model_nutrition.py
import torch
from timm import create_model
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
from PIL import Image
import torchvision.transforms as transforms
import os


DEFAULT_CLASS_NAMES = [
    'Bánh_mì', 'Bắp_cải', 'Bí_đao', 'Bí_đỏ', 'Bông_cải_xanh', 'Bún', 
    'Cà_chua', 'Cà_rốt', 'Cà_tím', 'Cá_Basa', 'Cá_Chép', 'Cá_Chim', 
    'Cá_Diêu_Hồng', 'Cá_Hồi_Phi_lê', 'Cá_Kèo', 'Cá_Lăng', 'Cá_Lóc', 
    'Cá_Ngừ', 'Cần_tây', 'Cải_ngọt', 'Dưa_chuột', 'Gạo', 'Gạo_lứt', 
    'Gừng', 'Hành_tây', 'Hạt_Chia', 'Hạt_Kê', 'Hạt_dẻ', 'Hạt_hạnh_nhân', 
    'Hạt_hướng_dương', 'Hạt_macca', 'Hạt_óc_chó', 'Hạt_điều', 'Khoai_Tây', 
    'Khoai_lang', 'Măng_tây', 'Mực', 'Nấm Linh Chi', 'Nấm Mèo', 'Nấm_Hương', 
    'Nấm_Kim_Châm', 'Nấm_Rơm', 'Nấm_Đùi_Gà', 'Ớt_chuông', 'Su_hào', 
    'Thịt_Heo_Ba_Chỉ', 'Thịt_bò', 'Thịt_gà', 'Tỏi', 'Trái_Bắp', 'Trứng_Gà', 
    'Xà_lách', 'Yến_Mạch', 'cá rô đồng', 'con cua', 'con tôm ', 'Đậu_nành', 
    'Đậu_phụ', 'Đậu_que', 'Đậu_xanh', 'Đậu_đen', 'Đậu_đỏ'
]


class NutritionModelPredictor:
    """Class để tải model Swin Transformer và dự đoán thông tin dinh dưỡng"""

    def __init__(
        self, 
        model_path: str, 
        nutrition_csv_path: str,
        class_names: Optional[list] = None, 
        num_classes: int = 62
    ):
        """
        Khởi tạo NutritionModelPredictor
        
        Args:
            model_path: Đường dẫn đến file model (.pth)
            nutrition_csv_path: Đường dẫn đến file CSV chứa thông tin dinh dưỡng
            class_names: Danh sách tên các lớp (nếu không có sẽ tự động lấy từ config)
            num_classes: Số lượng classes của model
        """
        self.model_path = model_path
        self.nutrition_csv_path = nutrition_csv_path
        self.class_names = class_names or DEFAULT_CLASS_NAMES
        self.num_classes = num_classes
        self.model = None
        self.nutrition_df = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.target_size = (224, 224)
        
        # Define image transforms
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        self._load_model()
        self._load_nutrition_data()
    
    def _load_model(self) -> None:
        """Tải model từ file"""
        try:
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Model file không tìm thấy: {self.model_path}")
            
            # Create model
            self.model = create_model(
                "swin_small_patch4_window7_224",
                pretrained=False,
                num_classes=self.num_classes
            )
            
            # Load checkpoint
            state_dict = torch.load(self.model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            print(f"✅ Model Swin Transformer đã được tải thành công từ: {self.model_path}")
            print(f"📱 Device: {self.device}")
        except Exception as e:
            print(f"Lỗi khi tải model: {e}")
            raise
    
    def _load_nutrition_data(self) -> None:
        """Tải dữ liệu dinh dưỡng từ CSV"""
        try:
            if not Path(self.nutrition_csv_path).exists():
                raise FileNotFoundError(f"Nutrition CSV không tìm thấy: {self.nutrition_csv_path}")
            
            self.nutrition_df = pd.read_csv(self.nutrition_csv_path)
            print(f"✅ Dữ liệu dinh dưỡng đã được tải: {len(self.nutrition_df)} dòng")
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu dinh dưỡng: {e}")
            raise
    
    def _preprocess_image(self, image_path: str) -> torch.Tensor:
        """
        Tải và chuẩn bị ảnh
        
        Args:
            image_path: Đường dẫn đến file ảnh
            
        Returns:
            Tensor ảnh đã xử lý
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Ảnh không tìm thấy: {image_path}")
            
            # Tải ảnh
            img = Image.open(image_path).convert('RGB')
            
            # Apply transforms
            img_tensor = self.transform(img)
            
            # Add batch dimension
            img_tensor = img_tensor.unsqueeze(0)
            
            return img_tensor
        except Exception as e:
            print(f"Lỗi khi xử lý ảnh: {e}")
            raise
    
    def _get_nutrition_info(self, class_index: int) -> Dict[str, Any]:
        """
        Lấy thông tin dinh dưỡng từ CSV dựa vào class index
        
        Args:
            class_index: Index của class được dự đoán
            
        Returns:
            Dictionary chứa thông tin dinh dưỡng
        """
        if self.nutrition_df is None:
            return {}
        
        try:
            # Lấy dòng tương ứng với class index
            nutrient_row = self.nutrition_df.iloc[class_index]
            
            # Lấy các cột từ cột thứ 5 (index 4) đến hết
            nutrient_data = nutrient_row.iloc[4:]
            
            # Chuyển sang dictionary
            nutrition_dict = {}
            for col, value in nutrient_data.items():
                # Xử lý giá trị NaN hoặc rỗng
                if pd.isna(value) or value == '' or value is None:
                    nutrition_dict[col] = None
                    continue
                    
                # Chuyển đổi giá trị có dấu phẩy thành số
                if isinstance(value, str):
                    try:
                        # Thay dấu phẩy thành dấu chấm và convert sang float
                        cleaned_value = value.replace(',', '.').strip()
                        if cleaned_value:
                            value = float(cleaned_value)
                        else:
                            value = None
                    except (ValueError, AttributeError):
                        # Nếu không convert được, giữ nguyên giá trị string
                        pass
                
                nutrition_dict[col] = value
            
            # Thêm thông tin bổ sung
            nutrition_dict['Vietnamese_Name'] = nutrient_row.get('Vietnamese Name', '')
            nutrition_dict['English_Name'] = nutrient_row.get('English Name', '')
            
            # Frontend expect lowercase với underscore
            mapped_dict = {
                'name': nutrition_dict.get('Name', ''),
                'vietnamese_name': nutrition_dict.get('Vietnamese_Name', ''),
                'english_name': nutrition_dict.get('English_Name', ''),
                'water': nutrition_dict.get('Water'),
                'energy': nutrition_dict.get('Energy'),
                'protein': nutrition_dict.get('Protein'),
                'total_lipid_fat': nutrition_dict.get('Total_lipid_fat'),
                'carbohydrate_by_difference': nutrition_dict.get('Carbohydrate_by_difference'),
                'calcium_ca': nutrition_dict.get('Calcium_Ca'),
                'iron_fe': nutrition_dict.get('Iron_Fe'),
                'magnesium_mg': nutrition_dict.get('Magnesium_Mg'),
                'potassium_k': nutrition_dict.get('Potassium_K'),
                'sodium_na': nutrition_dict.get('Sodium_Na'),
            }
            
            return mapped_dict
        except Exception as e:
            print(f"Lỗi khi lấy thông tin dinh dưỡng: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        """
        Dự đoán lớp của ảnh và trả về thông tin dinh dưỡng
        
        Args:
            image_path: Đường dẫn đến file ảnh
            
        Returns:
            Dict chứa:
                - predicted_class: Tên lớp dự đoán
                - predicted_index: Index của lớp dự đoán
                - confidence: Độ tin cậy (%)
                - nutrition_info: Thông tin dinh dưỡng
                - all_predictions: Dict tất cả các lớp với xác suất
        """
        try:
            if self.model is None:
                raise RuntimeError("Model chưa được tải")
            
            if self.class_names is None:
                raise ValueError("class_names chưa được cấu hình")
            
            # Xử lý ảnh
            img_tensor = self._preprocess_image(image_path)
            img_tensor = img_tensor.to(self.device)
            
            # Dự đoán
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                
            # Lấy kết quả
            probs = probabilities.cpu().numpy()[0]
            predicted_idx = np.argmax(probs)
            predicted_class = self.class_names[predicted_idx]
            confidence = 100 * float(probs[predicted_idx])
            
            # Lấy thông tin dinh dưỡng
            nutrition_info = self._get_nutrition_info(predicted_idx)
            
            # Tạo dict tất cả dự đoán
            all_predictions = {
                self.class_names[i]: float(probs[i]) * 100
                for i in range(len(self.class_names))
            }
            
            return {
                "predicted_class": predicted_class,
                "predicted_index": predicted_idx,
                "confidence": round(confidence, 2),
                "nutrition_info": nutrition_info,
                "all_predictions": all_predictions,
                "image_path": image_path
            }
        
        except Exception as e:
            print(f"Lỗi khi dự đoán: {e}")
            raise
    
    def predict_and_print_nutrition(self, image_path: str) -> None:
        """
        Dự đoán và in ra thông tin dinh dưỡng
        
        Args:
            image_path: Đường dẫn đến file ảnh
        """
        result = self.predict(image_path)
        
        print(f"\n{'='*50}")
        print(f"📸 Ảnh: {result['image_path']}")
        print(f"🍽️  Dự đoán: {result['predicted_class']}")
        print(f"📊 Độ tin cậy: {result['confidence']:.2f}%")
        print(f"{'='*50}")
        
        nutrition_info = result['nutrition_info']
        if nutrition_info:
            print("\n=== Thông tin chất dinh dưỡng ===")
            print(f"Tên Tiếng Việt: {nutrition_info.get('Vietnamese_Name', 'N/A')}")
            print(f"Tên Tiếng Anh: {nutrition_info.get('English_Name', 'N/A')}")
            print(f"\nThành phần dinh dưỡng (trên 100g):")
            
            # Danh sách các chất dinh dưỡng cần hiển thị
            nutrient_fields = [
                ('Name', 'Tên'),
                ('Water', 'Nước (g)'),
                ('Energy', 'Năng lượng (kcal)'),
                ('Protein', 'Protein (g)'),
                ('Total_lipid_fat', 'Chất béo (g)'),
                ('Carbohydrate_by_difference', 'Carbohydrate (g)'),
                ('Calcium_Ca', 'Canxi (mg)'),
                ('Iron_Fe', 'Sắt (mg)'),
                ('Magnesium_Mg', 'Magie (mg)'),
                ('Potassium_K', 'Kali (mg)'),
                ('Sodium_Na', 'Natri (mg)')
            ]
            
            for key, label in nutrient_fields:
                value = nutrition_info.get(key, 'N/A')
                print(f"  {label}: {value}")
        else:
            print("\n⚠️ Không tìm thấy thông tin dinh dưỡng")
    
    def get_nutrition_by_class_name(self, class_name: str) -> Dict[str, Any]:
        """
        Lấy thông tin dinh dưỡng theo tên class
        
        Args:
            class_name: Tên class (ví dụ: 'Cà_chua')
            
        Returns:
            Dictionary chứa thông tin dinh dưỡng
        """
        try:
            if class_name not in self.class_names:
                raise ValueError(f"Class '{class_name}' không tồn tại trong danh sách")
            
            class_index = self.class_names.index(class_name)
            return self._get_nutrition_info(class_index)
        except Exception as e:
            print(f"Lỗi khi lấy thông tin dinh dưỡng: {e}")
            return {}
    
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
        print(f"Danh sách lớp đã được cập nhật: {len(class_names)} classes")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Lấy thông tin model"""
        if self.model is None:
            return {"error": "Model chưa được tải"}
        
        return {
            "model_path": self.model_path,
            "model_type": "Swin Transformer Small",
            "nutrition_csv_path": self.nutrition_csv_path,
            "device": str(self.device),
            "num_classes": self.num_classes,
            "class_names_count": len(self.class_names),
            "target_size": self.target_size
        }


def create_nutrition_predictor(
    model_path: str, 
    nutrition_csv_path: str,
    class_names: Optional[list] = None
) -> NutritionModelPredictor:
    """
    Tạo nutrition predictor instance
    
    Args:
        model_path: Đường dẫn đến file model
        nutrition_csv_path: Đường dẫn đến file CSV chứa thông tin dinh dưỡng
        class_names: Danh sách tên lớp (optional)
        
    Returns:
        NutritionModelPredictor instance
    """
    return NutritionModelPredictor(model_path, nutrition_csv_path, class_names)


# ==================== EXAMPLE USAGE ====================
# if __name__ == "__main__":
#     # Cấu hình
#     MODEL_PATH = "path/to/your/model.pth"
#     NUTRITION_CSV_PATH = "D:/CN_IOT/CK/backend/app/data/Get_Nutrition.csv"
#     IMAGE_PATH = "path/to/test/image.jpg"
    
#     # Tạo predictor
#     predictor = create_nutrition_predictor(
#         model_path=MODEL_PATH,
#         nutrition_csv_path=NUTRITION_CSV_PATH
#     )
    
#     # Dự đoán và hiển thị thông tin dinh dưỡng
#     predictor.predict_and_print_nutrition(IMAGE_PATH)
    
#     # Hoặc lấy kết quả dạng dict
#     result = predictor.predict(IMAGE_PATH)
#     print(result)
    
#     # Lấy thông tin dinh dưỡng theo tên class
#     nutrition = predictor.get_nutrition_by_class_name("Cà_chua")
#     print(nutrition)