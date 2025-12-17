import torch
import timm
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
from PIL import Image
import torchvision.transforms as transforms


DEFAULT_CLASS_NAMES = [
    'Banh beo', 'Banh bot loc', 'Banh can', 'Banh canh', 'Banh chung', 
    'Banh cuon', 'Banh duc', 'Banh gio', 'Banh khot', 'Banh mi', 
    'Banh pia', 'Banh tet', 'Banh trang nuong', 'Banh xeo', 'Bun bo Hue', 
    'Bun dau mam tom', 'Bun mam', 'Bun rieu', 'Bun thit nuong', 'Ca kho to', 
    'Canh chua', 'Cao lau', 'Chao long', 'Com tam', 'Goi cuon', 
    'Hu tieu', 'Mi quang', 'Nem chua', 'Pho', 'Xoi xeo'
]


class FoodModelPredictorEff:
    """Class để tải model EfficientNet và dự đoán hình ảnh thức ăn"""

    def __init__(self, model_path: str, class_names: Optional[list] = None, num_classes: int = 30):
        """
        Khởi tạo FoodModelPredictorEff
        
        Args:
            model_path: Đường dẫn đến file model (.pth)
            class_names: Danh sách tên các lớp (nếu không có sẽ tự động lấy từ config)
            num_classes: Số lượng classes của model
        """
        self.model_path = model_path
        self.class_names = class_names or DEFAULT_CLASS_NAMES
        self.num_classes = num_classes
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.target_size = (224, 224)
        
        # Define image transforms
        self.transform = transforms.Compose([
            transforms.Resize(self.target_size),
            transforms.ToTensor()
        ])
        
        self._load_model()
    
    def _load_model(self) -> None:
        """Tải model từ file"""
        try:
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Model file không tìm thấy: {self.model_path}")
            
            # Create model
            self.model = timm.create_model(
                "efficientnet_b0",
                pretrained=False,
                num_classes=self.num_classes
            )
            
            # Load checkpoint
            state_dict = torch.load(self.model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            print(f"✅ Model EfficientNet đã được tải thành công từ: {self.model_path}")
            print(f"📱 Device: {self.device}")
        except Exception as e:
            print(f"Lỗi khi tải model: {e}")
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
            if not Path(image_path).exists():
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
            
            # Tạo dict tất cả dự đoán
            all_predictions = {
                self.class_names[i]: float(probs[i]) * 100
                for i in range(len(self.class_names))
            }
            
            return {
                "predicted_class": predicted_class,
                "confidence": round(confidence, 2),
                "predictions": probs,
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
            "model_type": "EfficientNet-B0",
            "device": str(self.device),
            "num_classes": self.num_classes,
            "class_names": self.class_names,
            "target_size": self.target_size
        }


def create_predictor(model_path: str, class_names: Optional[list] = None) -> FoodModelPredictorEff:
    """
    Tạo predictor instance
    
    Args:
        model_path: Đường dẫn đến file model
        class_names: Danh sách tên lớp (optional)
        
    Returns:
        FoodModelPredictorEff instance
    """
    return FoodModelPredictorEff(model_path, class_names)