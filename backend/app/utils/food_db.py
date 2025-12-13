import json
import random
from pathlib import Path
from typing import Dict, List, Optional

class FoodDatabase:
    """Class để quản lý dữ liệu thức ăn từ JSON"""
    
    def __init__(self, json_path: str):
        """
        Khởi tạo FoodDatabase
        
        Args:
            json_path: Đường dẫn đến file JSON
        """
        self.json_path = json_path
        self.data = None
        self._load_json()
    
    def _load_json(self) -> None:
        """Tải dữ liệu từ JSON"""
        try:
            if not Path(self.json_path).exists():
                raise FileNotFoundError(f"JSON file không tìm thấy: {self.json_path}")
            
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            total_foods = len(self.data)
            total_restaurants = sum(len(v) for v in self.data.values())
            print(f"✅ Đã tải {total_foods} món ăn với {total_restaurants} nhà hàng")
        except Exception as e:
            print(f"❌ Lỗi khi tải JSON: {e}")
            raise
    
    def get_food_by_name(self, food_name: str) -> Optional[Dict]:
        """
        Lấy thông tin một nhà hàng random cho món ăn
        
        Args:
            food_name: Tên món ăn (ví dụ: 'Gà Nướng')
            
        Returns:
            Dict chứa: name, address, google_maps
            Hoặc None nếu không tìm thấy
        """
        try:
            if self.data is None:
                return None
            
            # Tìm kiếm (case-insensitive)
            for key in self.data.keys():
                if key.lower() == food_name.lower():
                    restaurants = self.data[key]
                    # Random chọn 1 nhà hàng
                    selected = random.choice(restaurants)
                    return {
                        "food_name": key,
                        "restaurant_name": selected.get("name"),
                        "address": selected.get("address"),
                        "google_maps": selected.get("google_maps")
                    }
            
            print(f"⚠️  Không tìm thấy '{food_name}' trong database")
            return None
        except Exception as e:
            print(f"❌ Lỗi khi tìm kiếm: {e}")
            return None
    
    def get_all_restaurants_for_food(self, food_name: str) -> List[Dict]:
        """
        Lấy tất cả các nhà hàng cho một món ăn
        
        Args:
            food_name: Tên món ăn
            
        Returns:
            Danh sách tất cả các nhà hàng
        """
        try:
            if self.data is None:
                return []
            
            for key in self.data.keys():
                if key.lower() == food_name.lower():
                    return self.data[key]
            
            return []
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return []
    
    def search_foods(self, keyword: str) -> List[str]:
        """
        Tìm kiếm các món ăn chứa từ khóa
        
        Args:
            keyword: Từ khóa tìm kiếm
            
        Returns:
            Danh sách các tên món ăn phù hợp
        """
        try:
            if self.data is None:
                return []
            
            results = [
                food_name for food_name in self.data.keys()
                if keyword.lower() in food_name.lower()
            ]
            return results
        except Exception as e:
            print(f"❌ Lỗi khi tìm kiếm: {e}")
            return []
    
    def get_all_foods(self) -> Dict:
        """Lấy tất cả dữ liệu"""
        return self.data or {}
    
    def reload_json(self) -> None:
        """Tải lại dữ liệu từ JSON"""
        self._load_json()