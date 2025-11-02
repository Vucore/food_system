import { useState } from 'react';

interface RecipeData {
  nguyenlieu?: string[];
  soche?: string[];
  thuchien?: string[];
  howtouse?: string[];
  tips?: string[];
}

export function useRecipe() {
  const [recipeData, setRecipeData] = useState<RecipeData>({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRecipe = async (foodName: string) => {
    setIsLoading(true);
    setError(null);
    try {
      // Gọi API backend
      const response = await fetch(
        `http://localhost:8000/api/v1/chatbot/recipe?query=${encodeURIComponent(foodName)}&isbot=false`
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      const data = await response.json();
      if (data.data) {
        const mappedData: RecipeData = {
          nguyenlieu: data.data.ingredients || [],
          soche: data.data.preparation || [],
          thuchien: data.data.cookingSteps || [],
          howtouse: data.data.howToServe || [],
          tips: data.data.tips || [],
        };

        setRecipeData(mappedData);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Lỗi không xác định');
      // Fallback: fake data
      setRecipeData({
        nguyenlieu: ["Không tìm thấy thông tin"],
        soche: ["Không tìm thấy thông tin"],
        thuchien: ["Không tìm thấy thông tin"],
        howtouse: ["Không tìm thấy thông tin"],
        tips: ["Không tìm thấy thông tin"],
      });
    } finally {
      setIsLoading(false);
    }
  };

  return { recipeData, isLoading, error, fetchRecipe };
}