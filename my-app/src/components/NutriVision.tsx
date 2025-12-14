"use client";
import React, { useState, useEffect } from "react";
import { Header } from "./Header";
import { CameraFeed } from "./CameraFeed";
import { DetectedFoods } from "./DetectedFoods";
import { MapDirections } from "./MapDirections";
import { NutritionInfo } from "./NutritionInfo";
import { useCamera } from '../hooks/useCamera';
import type { NutriVisionProps } from "./NutriVision.type";

export const NutriVision: React.FC<NutriVisionProps> = ({ onSelectFood }) => {
  const {
    isAnalyzing,
    handleCapture,
    handleReset,
    detectedFoods,
    nutritionData,
    nutritionMode,
    setNutritionMode
  } = useCamera();

  const [selectedFoodForMap, setSelectedFoodForMap] = useState<any>(null);
  const [isLiveFeedActive] = useState(true);

  useEffect(() => {
    handleReset();
  }, []);

  const handleSelectFood = (food: any) => {
    if (nutritionMode) {
      // In nutrition mode, nutrition data comes from WebSocket/capture
      // No need to fetch separately
      console.log("Nutrition mode - data already loaded");
    } else {
      if (onSelectFood) {
        onSelectFood(food);
      }
    }
  };

  // Toggle nutrition mode
  const toggleNutritionMode = () => {
    const newMode = !nutritionMode;
    setNutritionMode(newMode);

    if (!newMode) {
      setSelectedFoodForMap(null);
    }
  };

  // Chỉ hiển thị map
  const handleShowMap = (food: any) => {
    if (!nutritionMode) {
      setSelectedFoodForMap(food);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header
        isLiveFeedActive={isLiveFeedActive}
        nutritionMode={nutritionMode}
        onToggleNutritionMode={toggleNutritionMode}
      />
      <main className="flex gap-6 justify-center items-start p-6 w-full max-md:flex-col max-md:items-center">
        {/* Cột trái: Camera */}
        <div className="flex flex-col items-center max-w-full w-[480px] h-[480px]">
          <CameraFeed
            isAnalyzing={isAnalyzing}
            onCapture={handleCapture}
            onReset={handleReset}
          />
        </div>

        {/* Cột phải: Detected Foods hoặc Nutrition Info */}
        <div className="flex flex-col gap-6 max-w-full w-[700px]">
          {nutritionMode ? (
            <NutritionInfo nutritionData={nutritionData?.nutrition_info || null} />
          ) : (
            <>
              <DetectedFoods
                detectedFoods={detectedFoods}
                onSelectFood={handleSelectFood}
                onShowMap={handleShowMap}
              />
              <MapDirections
                selectedFood={selectedFoodForMap}
                onClose={() => setSelectedFoodForMap(null)}
              />
            </>
          )}
        </div>
      </main>
    </div>
  );
};

export default NutriVision;