export interface Food {
  id: number;
  name: string;
  restaurant: string;
  address: string;
  google_maps: string;
  icon: string;
  color: string;
}

export interface NutriVisionProps {
  onSelectFood?: (food: any) => void;
}