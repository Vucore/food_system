export type Nutrients = {
  protein: number; // grams
  carbs: number; // grams
  fat: number; // grams
};

export type DetectedFood = {
  id: string;
  name: string;
  thumbnail?: string; // data URL or path
  calories: number;
  nutrients: Nutrients;
  confidence?: number; // 0-1
};

export const sampleDetected: DetectedFood[] = [
  {
    id: "1",
    name: "Cơm trắng",
    thumbnail: "",
    calories: 200,
    nutrients: { protein: 4, carbs: 45, fat: 1 },
    confidence: 0.93,
  },
  {
    id: "2",
    name: "Gà rán",
    thumbnail: "",
    calories: 320,
    nutrients: { protein: 25, carbs: 10, fat: 20 },
    confidence: 0.88,
  },
];