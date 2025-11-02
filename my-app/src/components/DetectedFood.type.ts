export interface Food {
  id: number;
  name: string;
  restaurant?: string;
  address?: string;
  google_maps?: string;
  icon?: string;
  color?: string;
}
export interface DetectedFoodsProps {
  detectedFoods: Food[];
  // onNavigate?: (address: string, googleMaps?: string) => void;
}

export interface DetectedFoodsPropsWithClick extends DetectedFoodsProps {
  onSelectFood?: (food: Food) => void;  // Mở recipe modal
  onShowMap?: (food: Food) => void;     // Chỉ hiển thị map
}