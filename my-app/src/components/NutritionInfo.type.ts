// NutritionInfo.type.ts
export interface NutritionData {
    name?: string;
    vietnamese_name?: string;
    english_name?: string;
    water?: number;
    energy?: number;
    protein?: number;
    total_lipid_fat?: number;
    carbohydrate_by_difference?: number;
    calcium_ca?: number;
    iron_fe?: number;
    magnesium_mg?: number;
    potassium_k?: number;
    sodium_na?: number;
}

export interface NutritionInfoProps {
    nutritionData: NutritionData | null;
}